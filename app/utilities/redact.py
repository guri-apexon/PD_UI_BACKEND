import logging
import re
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
            genre_grouped = self.redact_df.loc[self.redact_df[redaction_profile] == True , ['genre', 'subCategory']].groupby('genre')
            redact_dict = genre_grouped['subCategory'].apply(lambda sub_cat: sub_cat.tolist()).to_dict()
            redact_dict = {**empty_profile_dict, **redact_dict}
            all_redaction_dict[redaction_profile] = redact_dict
        
        return all_redaction_dict

    def get_profiles(self):
        return self.redact_dict

    def get_current_redact_profile(self, current_db, user_id=None, protocol=None, profile_name=None, genre=config.GENRE_ENTITY_NAME) -> Tuple[str, dict, list]:
        """
        Input: profile_name or user_id+protocol
        Ouput: Valid profile name, current profile's details AND its particular genre details
        """
        if not profile_name and (user_id and protocol):
            user_protocol_obj = crud.pd_user_protocols.get_by_userid_protocol(current_db, userid=user_id, protocol=protocol)
            logger.debug(f"user_protocol_obj: {user_protocol_obj}")
            if user_protocol_obj:
                profile_name = user_protocol_obj.redactProfile

        valid_profile_name = profile_name if profile_name in config.USERROLE_REDACTPROFILE_MAP.values() else config.USERROLE_REDACTPROFILE_MAP['default']
        profile = self.redact_dict.get(valid_profile_name) 
        profile_genre = profile.get(genre, [])
        return valid_profile_name, profile, profile_genre

    def check_allow_download(self, current_db, user_id=None, protocol=None, redact_profile_name=None, action_type=None) -> Tuple[bool, str]:
        """
        Verifies whether action_type is allowed or not
        Input: UserId/protocol OR profile name
        Output: Yes/No AND profile_name
        """
        profile_name, _, profile_genre = self.get_current_redact_profile(current_db=current_db, user_id=user_id, protocol=protocol, 
                                                                            profile_name=redact_profile_name, genre='action')
        if action_type not in profile_genre:
            return True, profile_name

        logger.debug(f"{user_id}/{protocol} has {profile_name}; Requested action [{action_type}] exists in deny list {profile_genre}")
        return False, profile_name


redactor = Redactor()
