import logging
from app import config
from app.utilities.config import settings

logger = logging.getLogger(settings.PROJECT_NAME)


class RedactFootNotes:
    def __init__(self, attachments: list, redacted_placeholder: str, redact_flag: bool):
        self.attachments = attachments
        self.redacted_placeholder = redacted_placeholder
        self.redact_flag = redact_flag

    def redact_footnotes(self, content: str, entities: dict) -> str:
        if content:
            for entity in sorted(entities, key=lambda x: (x[config.FOOTNOTES_START_INDEX],
                                                          x[config.FOOTNOTES_END_INDEX]), reverse=True):
                content = content[0:entity[config.FOOTNOTES_START_INDEX]] + \
                          self.redacted_placeholder + \
                          content[entity[config.FOOTNOTES_END_INDEX]+1:]
        return content

    def redact_footnotes_pipeline(self):
        redacted_json = {}
        try:
            if self.attachments:
                for idx, attachment in enumerate(self.attachments):
                    text = attachment[config.FOOTNOTES_TEXT]
                    entities = attachment[config.FOOTNOTES_ENTITIES]
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
