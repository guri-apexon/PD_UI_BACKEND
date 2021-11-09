import logging, json
import re
from copy import deepcopy
from typing import Tuple


from app import config, crud
from app.db.session import SessionLocal
from app.utilities.config import settings
from app.utilities.redact import redactor
from app.utilities.pd_table_redaction import TableRedaction
from app.utilities.redaction.summary_redaction import SummaryRedaction

logger = logging.getLogger(settings.LOGGER_NAME)

db = SessionLocal()


class ProtocolViewRedaction:
    def __init__(self, user_id: str, protocol: str):
        self.user_id = user_id
        self.protocol = protocol

        profile_name, profile_details, profile_genre = redactor.get_current_redact_profile(current_db=db,
                                                                                           user_id=self.user_id,
                                                                                           protocol=self.protocol)
        self.profile_name = profile_name
        self.profile_details = profile_details
        self.entity_profile_genre = profile_genre

        self.table_redaction = TableRedaction(redact_flag=config.REDACTION_FLAG[self.profile_name],
                                              hide_table_json_flag=config.HIDE_TABLE_JSON_FLAG[self.profile_name],
                                              return_refreshed_table_html=config.RETURN_REFRESHED_TABLE_HTML_FLAG[
                                                  self.profile_name],
                                              redact_text=config.REDACT_PARAGRAPH_STR,
                                              redact_profile_entities=self.entity_profile_genre)

    def get_section_to_be_redacted(self, profile_details):
        redact_toc_flag = False
        redact_soa_flag = False
        redact_summary_flag = False
        if profile_details['section']:
            if 'File contents' in profile_details['section']:
                redact_toc_flag = True
            if 'SOA Tables' in profile_details['section']:
                redact_soa_flag = True
            if 'Summary Attributes' in profile_details['section']:
                redact_summary_flag = True
        return redact_toc_flag, redact_soa_flag, redact_summary_flag

    def on_paragraph(self, text, font_info, redact_profile_entities=[], redact_flg=True,
                     exclude_redact_property_flg=True) -> Tuple[str, dict]:
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
                    logger.warning(
                        f"[entity# {idx}] subtext: {text}; font_info: {font_info}; Exception message: {str(exc)}")

        if exclude_redact_property_flg:
            _ = redacted_property.pop('entity', "entity is not present")

        return redacted_text, redacted_property

    def get_protocol_data(self, aidoc_id, user):
        """
        Get Protocol data for a given aidoc
        """
        resource = crud.pd_protocol_data.get(db, aidoc_id, user)
        if resource is None:
            logger.error("No resource found for aidoc {}".format(aidoc_id))

        return resource

    def update_toc_with_redacted_tag(self, paragraph_dict: dict):
        """
        Update the json with the redacted tag for texts, headers and tables.
        """
        records = paragraph_dict['data']
        if records:
            try:
                for record in records:
                    if record[2] == 'text' or record[2] == 'header':
                        redacted_text, redacted_property = self.on_paragraph(record[3], record[4],
                                                                             self.entity_profile_genre)
                        record[3] = redacted_text
                        record[4] = redacted_property
                    if record[2] == 'table':
                        redacted_toc_table = self.table_redaction.redact_table(table_dictonary=record[3])
                        record[3] = redacted_toc_table

                paragraph_dict['data'] = records
            except Exception as exc:
                logger.error(f"Exception raised while updating Redaction tag in TOC: {str(exc)}")
        return paragraph_dict['data']

    def update_toc_metadata_with_redacted_tag(self, aidoc_id: str, metadata_dict: dict):
        """
        Partially Redact on protocol title and protocol title short.
        """

        try:
            for attribute in self.profile_details.get(config.GENRE_ATTRIBUTE_ENTITY, []):
                protocol_title = metadata_dict.get(attribute, "")
                if protocol_title:
                    doc_attributes = {
                        "AiDocId": aidoc_id,
                        attribute: protocol_title
                    }
                    redacted_doc_attributes = redactor.redact_protocolTitle(current_db=db,
                                                                            attribute=attribute,
                                                                            profile=self.profile_details,
                                                                            doc_attributes=doc_attributes,
                                                                            redact_flg=config.REDACTION_FLAG[self.profile_name])

                    metadata_dict[attribute] = redacted_doc_attributes[attribute]
        except Exception as exc:
            logger.error(f"Exception raised while updating Redaction tag in TOC Metadata: {str(exc)}")
        return metadata_dict

    def update_soa_with_redacted_tag(self, table_list: list):
        """
        Update the json with redacted tag for tables.
        """
        if table_list:
            try:
                list_of_redacted_tables = []
                for table in table_list:
                    redacted_soa_table = self.table_redaction.redact_table(table_dictonary=table)
                    list_of_redacted_tables.append(redacted_soa_table)

                table_list = list_of_redacted_tables
            except Exception as exc:
                logger.error(f"Exception raised while updating Redaction tag in SOA: {str(exc)}")
        return table_list

    def update_summary_with_redacted_tag(self, aidoc_id: str, summary_dict: dict):
        """
        Update the json with redacted tag for summary data.
        """

        protocol_attributes = self.profile_details['attributes']
        records = summary_dict['data']
        if records:
            try:
                redacted_summary_list = SummaryRedaction(records, protocol_attributes, config.REDACTION_FLAG[self.profile_name],
                                                         config.REDACT_PARAGRAPH_STR, self.profile_details, aidoc_id).redact_summary_pipeline()
                summary_dict['data'] = redacted_summary_list
            except Exception as exc:
                logger.error(f"Exception raised while updating Redaction tag in Summary: {str(exc)}")
        return summary_dict

    def redact_toc(self, aidoc_id, iqv_data_toc):
        """
        Parse iqviadataTOC json, send parsed json for adding redaction tag and convert redacted data into original json structure
        """
        redacted_toc = iqv_data_toc
        if iqv_data_toc:
            toc_data = json.loads(json.loads(iqv_data_toc))
            toc_with_redacted_tag = self.update_toc_with_redacted_tag(toc_data)
            toc_data['data'] = toc_with_redacted_tag
            toc_metadata_redacted_tag = self.update_toc_metadata_with_redacted_tag(aidoc_id, toc_data.get("metadata", {}))
            toc_data['metadata'] = toc_metadata_redacted_tag
            redacted_toc = str(json.dumps(json.dumps(toc_data)))
        return redacted_toc

    def redact_soa(self, iqv_data_soa):
        """
        Parse iqviadataSOA json, send parsed json for adding redaction tag and convert redacted data into original json structure
        """
        redacted_soa = iqv_data_soa
        if iqv_data_soa:
            soa_data = json.loads(json.loads(iqv_data_soa))
            soa_with_redacted_tag = self.update_soa_with_redacted_tag(soa_data)
            redacted_soa = str(json.dumps(json.dumps(soa_with_redacted_tag)))
        return redacted_soa

    def redact_summary(self, aidoc_id, iqv_data_summary):
        """
        Parse iqviadataSummary json, send parsed json for adding redaction tag and convert redacted data into original json structure
        """
        redacted_summary = iqv_data_summary
        if iqv_data_summary:
            summary_data = json.loads(json.loads(iqv_data_summary))
            summary_with_redacted_tag = self.update_summary_with_redacted_tag(aidoc_id, summary_data)
            redacted_summary = str(json.dumps(json.dumps(summary_with_redacted_tag)))
        return redacted_summary

    def redact_protocol_data(self, aidoc_id, user):
        """
        Get protocol data and call individual function for each section i.e, soa, toc, summary
        """
        redacted_protocol_data = dict()
        protocol_data = self.get_protocol_data(aidoc_id, user)
        redact_toc_flag, redact_soa_flag, redact_summary_flag = self.get_section_to_be_redacted(self.profile_details)
        if protocol_data:
            iqvdata_toc = protocol_data.iqvdataToc
            iqvdata_soa = protocol_data.iqvdataSoa
            iqvdata_summary = protocol_data.iqvdataSummary

            if redact_toc_flag:
                iqvdata_toc = self.redact_toc(aidoc_id, iqvdata_toc)
            if redact_soa_flag:
                iqvdata_soa = self.redact_soa(iqvdata_soa)
            if redact_summary_flag:
                iqvdata_summary = self.redact_summary(aidoc_id, iqvdata_summary)

            redacted_protocol_data = {"documentFilePath": protocol_data.documentFilePath, "id": protocol_data.id,
                                      "userId": protocol_data.userId, "fileName": protocol_data.fileName,
                                      "iqvdata": protocol_data.iqvdata, "iqvdataSoa": iqvdata_soa,
                                      "iqvdataSoaStd": protocol_data.iqvdataSoaStd, "iqvdataSummary": iqvdata_summary,
                                      "iqvdataToc": iqvdata_toc, "isActive": protocol_data.isActive}

        return redacted_protocol_data

