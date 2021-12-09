import logging
import re
from copy import deepcopy
from itertools import zip_longest
from typing import Tuple

import numpy as np
import pandas as pd
from app import config, crud
from app.crud import pd_redact_profile
from app.db.session import SessionLocal
from app.utilities.config import settings
from fastapi import HTTPException
from starlette import status

logger = logging.getLogger(settings.LOGGER_NAME)

db = SessionLocal()


class Redactor:
    def __init__(self):
        db = SessionLocal()
        self.profile_entries = pd_redact_profile.get_all_active(db)
        if self.profile_entries is None or len(self.profile_entries) == 0:
            logger.exception(f'Active profile extraction failed')
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No active profile details extracted")

        self.redact_df = self.get_all_profiles_df()
        self.redact_dict = self.get_all_profiles_dict()
        self.legacy_protocol_upload_date = pd.to_datetime(settings.LEGACY_PROTOCOL_UPLOAD_DATE).date()
        
    def get_all_profiles_df(self) -> pd.DataFrame:
        """
        Convert profile entries to dataframe
        """
        all_profile = []
        _ = [all_profile.append(tuple(row.as_dict().values())) for row in self.profile_entries]

        col_names = tuple(self.profile_entries[0].as_dict().keys())
        redact_df = pd.DataFrame(data=all_profile, columns=col_names)
        return redact_df

    def get_all_profiles_dict(self) -> dict:
        empty_profile_dict = {key: [] for key in np.unique(self.redact_df.loc[:, ['genre']])}

        all_redaction_dict = dict()
        all_redaction_profiles = set(config.USERROLE_REDACTPROFILE_MAP.values())
        for redaction_profile in all_redaction_profiles:
            genre_grouped = self.redact_df.loc[self.redact_df[redaction_profile] == True, ['genre', 'subCategory']].groupby('genre')
            redact_dict = genre_grouped['subCategory'].apply(lambda sub_cat: sub_cat.tolist()).to_dict()
            redact_dict = {**empty_profile_dict, **redact_dict}
            all_redaction_dict[redaction_profile] = redact_dict
        
        return all_redaction_dict

    def get_profiles(self):
        return self.redact_dict

    def get_current_redact_profile(self, current_db, user_id=None, protocol=None, profile_name=None,
                                   genre=config.GENRE_ENTITY_NAME) -> Tuple[str, dict, list]:
        """
        Input: profile_name or user_id+protocol
        Output: Valid profile name, current profile's details AND its particular genre details
        """
        if not profile_name and (user_id and protocol):
            user_protocol_obj = crud.pd_user_protocols.get_by_userid_protocol(current_db, userid=user_id,
                                                                              protocol=protocol)
            if user_protocol_obj:
                profile_name = user_protocol_obj.redactProfile

        valid_profile_name = profile_name if profile_name in config.USERROLE_REDACTPROFILE_MAP.values() \
            else config.USERROLE_REDACTPROFILE_MAP['default']
        profile = self.redact_dict.get(valid_profile_name) 
        profile_genre = profile.get(genre, [])
        return valid_profile_name, profile, profile_genre

    def check_allow_download(self, current_db, user_id=None, protocol=None, redact_profile_name=None,
                             action_type=None) -> Tuple[bool, str]:
        """
        Verifies whether action_type is allowed or not
        Input: UserId/protocol OR profile name
        Output: Yes/No AND profile_name
        """
        profile_name, _, profile_genre = self.get_current_redact_profile(current_db=current_db,
                                                                         user_id=user_id,
                                                                         protocol=protocol,
                                                                         profile_name=redact_profile_name,
                                                                         genre='action')
        if action_type not in profile_genre:
            return True, profile_name

        logger.debug(f"{user_id}/{protocol} has {profile_name}; Requested action [{action_type}] "
                     f"exists in deny list {profile_genre}")
        return False, profile_name

    def on_attributes(self, current_db, multiple_doc_attributes: list = [], single_doc_attributes: dict = {}) -> Tuple[list, dict]:
        """
        Each dict need to have key 'redactProfile' which represent the profile which is to be applied on the attributes.

        Input: multiple_doc_attributes as list[dict]. single_doc_attributes as dict. If both inputs are present, single_doc_attributes takes priority
        Output: Redacted multiple_doc_attributes and single_doc_attributes
        """
        redacted_multiple_doc_attributes = []
        if single_doc_attributes:
            multiple_doc_attributes = list(single_doc_attributes)

        if multiple_doc_attributes:
            default_redact_attr = dict(zip_longest(multiple_doc_attributes[0].keys(), '', fillvalue=config.REDACT_ATTR_STR))
        else:
            logger.warning(f"Redaction on attributes did not received valid inputs. multiple_doc_attributes: "
                           f"{multiple_doc_attributes}; single_doc_attributes: {single_doc_attributes}")
            return multiple_doc_attributes, single_doc_attributes

        for doc_attributes in multiple_doc_attributes:
            profile_name, profile, profile_attributes = self.get_current_redact_profile(current_db=current_db,
                                                                                        profile_name=doc_attributes.get('redactProfile'),
                                                                                        genre=config.GENRE_ATTRIBUTE_NAME)
            # logger.debug(f"profile_name: {profile_name}; profile_attributes: {profile_attributes}")

            redacted_entities = profile.get(config.GENRE_ENTITY_NAME, [])
            aidoc_id = doc_attributes.get("id", None) or doc_attributes.get("AiDocId", None)
            summary_entities = crud.pd_protocol_summary_entities.get_protocol_summary_entities(db=current_db,
                                                                                                    aidocId=aidoc_id)
            for attribute in profile.get(config.GENRE_ATTRIBUTE_ENTITY, []):
                doc_attributes = self.redact_attribute_entity(attribute=attribute,
                                                              doc_attributes=doc_attributes,
                                                              redacted_entities=redacted_entities,
                                                              summary_entities=summary_entities,
                                                              redact_flg=config.REDACTION_FLAG[profile_name])

            nonredact_attr = {name: value for name, value in doc_attributes.items() if name not in profile_attributes}
            redact_attr = {**default_redact_attr, **nonredact_attr}
            redacted_multiple_doc_attributes.append(redact_attr)
        
        return redacted_multiple_doc_attributes, redacted_multiple_doc_attributes[0]

    def redact_attribute_entity(self, attribute, doc_attributes, redacted_entities, summary_entities, redact_flg=True):
        upload_date_obj = doc_attributes.get("uploadDate", None)
        if upload_date_obj and type(upload_date_obj) == str:
            upload_date_obj = pd.to_datetime(upload_date_obj)

        attr_lm_entity_dict = {
            'primary_objectives': 'objectives_section',
            'inclusion_criteria': 'inclusion_section',
            'exclusion_criteria': 'exclusion_section',
            'protocol_title': 'ProtocolTitle',
            'protocolTitle': 'ProtocolTitle'}

        if redact_flg:
            if upload_date_obj and upload_date_obj.date() <= self.legacy_protocol_upload_date:
                doc_attributes[attribute] = config.REDACT_PARAGRAPH_STR
                return doc_attributes

            if summary_entities:
                content = doc_attributes.get(attribute, "")
                if content:
                    for entity in summary_entities.get(attr_lm_entity_dict.get(attribute, attribute), []):
                        if entity["subcategory"] in redacted_entities:
                            entity_adjusted_text = config.REGEX_SPECIAL_CHAR_REPLACE.sub(r".{1}", entity.get('text', ''))
                            content = re.sub(entity_adjusted_text, config.REDACT_PARAGRAPH_STR, content)
                    doc_attributes[attribute] = content
        return doc_attributes

    def on_paragraph(self, text, font_info, redact_profile_entities=[], redact_flg=True, exclude_redact_property_flg=True) -> Tuple[str, dict]:
        """
        Redact paragraph based on redaction entity text

        Inputs
            text: Paragraph
            font_info: List of redaction entities associated with the text
            redact_entities: List of entity genre subcategory to be redacted
            redact_flg: Apply redaction on text OR not
            exclude_redact_property_flg: Exclude entity property OR not
        Outputs
            processed_text: Redacted paragraph (if redact_flg is set) OR actual paragraph
            processed_property: Excluded redact property(if exclude_redact_propery is set) OR actual property
        """
        redacted_text = text
        redacted_property = deepcopy(font_info)
        text_redaction_entity = font_info.get('entity', [])

        if redact_flg and text and text_redaction_entity:
            for idx, entity in enumerate(text_redaction_entity):
                try:
                    if entity.get('subcategory', '') in redact_profile_entities:
                        logger.debug(f"Processing for idx[{idx}] with entity:{entity}")
                        entity_adjusted_text = config.REGEX_SPECIAL_CHAR_REPLACE.sub(r".{1}", entity['text'])
                        redacted_text = re.sub(entity_adjusted_text, config.REDACT_PARAGRAPH_STR, redacted_text)
                except Exception as exc:
                    logger.warning(f"[entity# {idx}] subtext: {text}; font_info: {font_info}; Exception message: {str(exc)}")
            
        if exclude_redact_property_flg:
            _ = redacted_property.pop('entity', "entity is not present")
            
        return redacted_text, redacted_property


redactor = Redactor()
