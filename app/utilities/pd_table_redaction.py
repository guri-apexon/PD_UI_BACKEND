import logging
from app.utilities.config import settings
from app import config
from app.utilities.redaction.footnotes_redaction import RedactFootNotes

import json
import pandas as pd

logger = logging.getLogger(settings.PROJECT_NAME)



class TableRedaction():
    """
     user		redact_flag		hide_table_json_flag		return_refreshed_table_html
        (if true, redact)   (if true, donot return json)    (if true, return reconstruct html from content in properties)
    primary = 	  false				true						     false
    secondary =   true				true						     true
    QC = 		  false			    false						     true
    """
    def __init__(self,
                 redact_flag: bool = False,
                 hide_table_json_flag: bool = True,
                 return_refreshed_table_html: bool = False,
                 redact_text: str = '~REDACTED~'
                 ):
        self.redact_flag = redact_flag
        self.hide_table_json_flag = hide_table_json_flag
        self.return_refreshed_table_html = return_refreshed_table_html
        self.redact_text = redact_text

    redact_text_fn = lambda self, text, start_idx, end_idx: ' '.join([text[0:start_idx],
                                                                      '<span class="redact">',
                                                                      self.redact_text,
                                                                      '</span>',
                                                                      text[end_idx + 1:]])

    def redact_entity(self, table_property):
        try:
            tmp = 1
            table_property['entities'].sort(key = lambda x:(x['start_idx'], x['end_idx']), reverse = True)
            tmp = 1
            for entity in table_property['entities']:
                table_property['content'] = self.redact_text_fn(table_property['content'],
                                                                entity[config.FOOTNOTES_START_INDEX],
                                                                entity[config.FOOTNOTES_END_INDEX])

            return table_property
        except Exception as ex:
            print(ex)

    def refresh_html_table(self, properties_df_cols, properties_df):
        table_df = pd.DataFrame()
        for col_idx in properties_df_cols:
            table_df[col_idx] = [x['content'] if x and x['content'] else x for x in
                                 properties_df[col_idx]]

        return table_df

    def refresh_footnotes(self, table_dictonary, footnote_json):

        footnote_pattern = ''.join((config.FOOTNOTE_STR, '_'))
        table_dictonary_keys = list(table_dictonary.keys())
        for key in table_dictonary_keys:
            if key.startswith(footnote_pattern):
                del table_dictonary[key]
        table_dictonary.update(footnote_json)

        return table_dictonary


    def redact_table(self,
                     table_dictonary: dict
                     ):
        try:
            if table_dictonary:
                properties = table_dictonary.get('TableProperties')
                if properties:
                    properties = json.loads(properties)
                    properties_df = pd.DataFrame(properties)
                    properties_df_cols = properties_df.columns

                    """
                        Block that redacts the table HTML and footnotes with the redacted text
                    """
                    if self.redact_flag:
                        # Table redaction
                        for col_idx in properties_df_cols:
                            properties_df[col_idx] = [self.redact_entity(x) if x and x['entities'] else x for x in
                                                      properties_df[col_idx]]

                            table_df = self.refresh_html_table(properties_df_cols, properties_df)

                        table_dictonary['Table'] = table_df.to_html(escape=False)

                        # Footnote redaction
                        attachment_list_properties = table_dictonary.get('AttachmentListProperties', list())

                        redactFootNotes = RedactFootNotes(attachments=attachment_list_properties,
                                                          redacted_placeholder=self.redact_text,
                                                          redact_flag=self.redact_flag)
                        redacted_json = redactFootNotes.redact_footnotes_pipeline()

                        if redacted_json:
                            table_dictonary = self.refresh_footnotes(table_dictonary, redacted_json)

                    """
                        redact_flag == False checking this because if it True, already updated the table HTML 
                        and footnotes in the above block
                    """
                    if self.return_refreshed_table_html and self.redact_flag == False:
                        # Table refresh
                        table_df = self.refresh_html_table(properties_df_cols, properties_df)
                        table_dictonary['Table'] = table_df.to_html(escape=False)

                        # Footnote refresh
                        footnote_json = dict()
                        footnote_pattern = ''.join((config.FOOTNOTE_STR, '_'))
                        idx = 0
                        attachment_list_properties = table_dictonary.get('AttachmentListProperties', list())
                        for attachment in attachment_list_properties:
                            footnote_json[''.join((footnote_pattern, str(idx)))] = attachment['Text']
                            idx += 1
                        if footnote_json:
                            table_dictonary = self.refresh_footnotes(table_dictonary, footnote_json)

                    """
                        Block to delete the ROI ID's and the unredacted text from the return json
                    """
                    if self.hide_table_json_flag:
                        if 'TableProperties' in table_dictonary:
                            del table_dictonary['TableProperties']
                        if 'AttachmentListProperties' in table_dictonary:
                            del table_dictonary['AttachmentListProperties']

        except Exception as ex:
            logger.error(f"Exception raised in - Table Redaction: {str(ex)}")

        return table_dictonary

