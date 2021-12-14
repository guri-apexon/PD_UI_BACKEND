import logging
from app import config
from app.utilities.config import settings
import re

logger = logging.getLogger(settings.PROJECT_NAME)


class RedactFootNotes:
    def __init__(self, attachments: list, redacted_placeholder: str, redact_flag: bool, redact_profile_entities = list()):
        self.attachments = attachments
        self.redacted_placeholder = redacted_placeholder
        self.redact_flag = redact_flag
        self.redact_profile_entities = redact_profile_entities

    def redact_footnotes(self, content: str, entities: dict) -> str:
        if content:
            for entity in sorted(entities, key=lambda x: (x[config.FOOTNOTES_START_INDEX],
                                                          x[config.FOOTNOTES_END_INDEX]), reverse=True):
                if entity.get('subcategory', '') in self.redact_profile_entities and len(config.REGEX_SPECIAL_CHAR_REPLACE.sub(r"", entity['text'])) != 0:
                    entity_adjusted_text = config.REGEX_SPECIAL_CHAR_REPLACE.sub(r".{1}", entity.get('text', ''))
                    content = re.sub(entity_adjusted_text, self.redacted_placeholder, content)

        return content

    def redact_footnotes_pipeline(self):
        redacted_json = {}
        try:
            if self.attachments:
                for idx, attachment in enumerate(self.attachments):
                    text = attachment.get(config.FOOTNOTES_TEXT, '')
                    entities = attachment.get(config.FOOTNOTES_ENTITIES, list())
                    if self.redact_flag:
                        redacted_text = self.redact_footnotes(text, entities)
                    else:
                        redacted_text = text
                    foot_note_key = f"{config.FOOTNOTE_STR}_{idx}"
                    redacted_json[foot_note_key] = " ".join([attachment[config.FOOTNOTES_KEY], redacted_text]).strip()
        except KeyError as exc:
            logger.error(f"Missing Key : {str(exc)}")
        except Exception as exc:
            logger.error(f"Exception raised : {str(exc)}")
        return redacted_json
