import sys
import logging
import pandas as pd
from app.utilities.config import settings

logger = logging.getLogger(settings.PROJECT_NAME)


class SummaryRedaction:
    """
    This class represents to perform the summary redaction based on attributes
    needs to be redacted, complete value will be redacted for an attribute
     params:
        summary_data: data contains list of summary contains name, value and header
        redacted_attributes: list of attributes needs to be redacted
        redact_flag: perform redaction or not
            True: secondary user_role
            False: primary & QC user_role
        redacted_placeholder: value will be redacted with redacted string provided as a placeholder
    """
    def __init__(self, summary_data: list, redacted_attributes: list, redact_flag: bool, redacted_placeholder: str):
        self.summary_data = summary_data
        self.redacted_attributes = redacted_attributes
        self.redact_flag = redact_flag
        self.redacted_placeholder = redacted_placeholder

    def redact_summary(self, summary: dict) -> str:
        try:
            attr_name = summary["attr_name"]
            attr_value = summary["attr_value"]

            if attr_name in self.redacted_attributes:
                attr_value = self.redacted_placeholder
            return attr_value
        except Exception:
            err_type, value, _ = sys.exc_info()
            logger.error(f"Exception raised in - Summary Redaction: {err_type}:{value}")
            return ""

    def redact_summary_pipeline(self):
        summary_df = pd.DataFrame(data=self.summary_data,
                                  columns=["attr_name", "attr_value", "attr_header"])

        summary_df["attr_value"] = summary_df.apply(self.redact_summary, axis=1)
        return summary_df.values.tolist()
