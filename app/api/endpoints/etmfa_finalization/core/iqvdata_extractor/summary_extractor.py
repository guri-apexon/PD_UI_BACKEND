import logging
from collections import Counter

import numpy as np
import pandas as pd
from etmfa_core.aidoc.io import IQVDocument
from etmfa_finalization import Constants
from etmfa_finalization.core.iqvdata_extractor.extractor_config import \
    ModuleConfig
from iqv_finalization_error import ErrorCodes, FinalizationException
from etmfa_finalization.core.iqvdata_extractor.table_extractor import SOAResponse as soa
logger = logging.getLogger(Constants.MICROSERVICE_NAME)


class SummaryResponse:
    def __init__(self, iqv_document: IQVDocument, response_type:str = "split", table_response_type:str = "html"):
        if iqv_document is None:
            raise FinalizationException(ErrorCodes.IQVDATA_FAILURE, f'During SummaryResponse init, iqv_document object is {iqv_document}')

        self.iqv_document = iqv_document
        self.response_type = response_type
        self.table_response_type = table_response_type

    def read_summary_tags(self) -> list:
        """
        Reads summary tags from IQVDocument object and returns it

        Input: IQVDocument object
        Output: List of summary details
        """

        std_summary_element_tag = ModuleConfig.GENERAL.std_tags_dict['KEY_IsSummaryElement']
        table_index_tag = ModuleConfig.GENERAL.std_tags_dict[ModuleConfig.GENERAL.TABLE_INDEX_KEY]
        footnote_tag = ModuleConfig.GENERAL.std_tags_dict[ModuleConfig.GENERAL.FOOTNOTE_KEY]
        subsection_tags = ModuleConfig.SUMMARY.subsection_tags

        all_summary_list = []

        for master_roi in self.iqv_document.DocumentParagraphs:
            master_roi_dict = dict()
            for kv_obj in master_roi.Properties:
                master_roi_dict[kv_obj.key] = kv_obj.value

            all_roi_tags = master_roi_dict.keys()

            # Footnotes are now part of table json
            if std_summary_element_tag not in all_roi_tags or footnote_tag in all_roi_tags:
                continue

            master_dict = dict()
            master_font_style = master_roi_dict.get('font_style', '')
            master_dict['para_master_roi_id'] = master_roi.id

            master_dict['table_index'] = master_roi_dict.get(table_index_tag, '')
            master_dict['subsection'] = [name for name in master_roi_dict.keys() if name in subsection_tags]

            all_child_list = []
            for level_roi in master_roi.ChildBoxes:
                master_dict['para_child_roi_id'] = level_roi.id
                master_dict['para_child_roi_text'] = ' '.join(level_roi.strTexts)
                master_dict['para_child_font_details'] = {'IsBold': level_roi.fontInfo.Bold, 'font_size': level_roi.fontInfo.Size}

                for iqv_subtext in level_roi.IQVSubTextList:
                    iqv_subtext_dict=dict()
                    iqv_subtext_dict['para_subtext_roi_id'] = iqv_subtext.id
                    iqv_subtext_dict['para_subtext_text'] = iqv_subtext.strText
                    iqv_subtext_dict['para_subtext_font_details'] = {'IsBold': iqv_subtext.fontInfo.Bold, 'font_size': iqv_subtext.fontInfo.Size,
                                                                     'font_style': master_font_style}

                    iqv_subtext_dict.update(master_dict)
                    all_child_list.append(iqv_subtext_dict)

            if master_font_style and all_child_list:
                combined_text = ''
                for detail in all_child_list:
                    combined_text += ' ' + detail['para_subtext_text']
                combined_dict = all_child_list[0]
                combined_dict['para_subtext_text'] = combined_text
                all_summary_list.append(combined_dict)
            else:
                all_summary_list.extend(all_child_list)

        return all_summary_list


    def get_iqvdata_summary(self) -> (dict, pd.DataFrame):
        """
        Input arguments:
        id: Unique ID of the document

        Returns:
        In DICT format for the summary section, contains three main sections:
            * Content: Actual text (or) table json
            * type: text or table
            * font_info: dictionary of font details
        """
        try:
            if self.iqv_document is None:
                return None, None

            summary_details = self.read_summary_tags()
            raw_summary_df = pd.DataFrame(summary_details)

            len_summary_details = len(summary_details)
            if len_summary_details == 0:
                logger.warning(f"No summary section tags are present: {len_summary_details}")
                return None, None

            raw_summary_df.fillna(value='', inplace=True)
            raw_summary_df['table_index'] = raw_summary_df['table_index'].apply(lambda x: int(float(x)) if len(x)> 0 else -1)

            # Keep single table
            raw_summary_df = raw_summary_df.loc[(raw_summary_df['table_index'] <= 0) | (~raw_summary_df.duplicated(subset=['table_index'], keep='first')) , :]
            raw_summary_df.reset_index(drop=True, inplace=True)

            unique_table_index = [table_index for table_index in set(raw_summary_df['table_index']) if table_index > 0]

            # Populate table contents
            table_list = soa.getTOIfromProprties(soa(self.iqv_document, self.profile_details, self.entity_profile_genre), table_indexes=unique_table_index, returntype=self.table_response_type)
            table_index_dict = {int(float(item['TableIndex'])):item for item in table_list}
            del table_list

            raw_summary_df['table_content'] = raw_summary_df['table_index'].apply(lambda col: table_index_dict.get(col, ''))
            raw_summary_df['type'] = np.where(raw_summary_df['table_index'] > 0, 'table', 'text')

            summary_df = pd.DataFrame()
            summary_df['content'] = np.where(raw_summary_df['type'] == 'text', raw_summary_df['para_subtext_text'], raw_summary_df['table_content'])
            summary_df['type'] = raw_summary_df['type']
            summary_df['subsection'] = raw_summary_df['subsection']
            summary_df['font_info'] = raw_summary_df['para_subtext_font_details']

            # Remove merged table references
            summary_display_eligibile = summary_df['content'].apply(lambda x: x != '{}')
            summary_df = summary_df.loc[summary_display_eligibile, :]

            # Build in requested format
            summary_dict = summary_df.to_dict(orient=self.response_type)
            logger.info(f"Summary section stats: \n Total # of rows: {summary_df.shape[0]} \
                            \n unique subsection count: {summary_df['subsection'].apply(lambda x: str(x)).nunique()} \
                            \n subsection stats : {Counter(summary_df['subsection'].apply(lambda x: str(x)))} \
                            \n type stats: {Counter(summary_df['type'])} ")
        except Exception as exc:
            logger.exception(f"Exception received in summary section iqvdata:{exc}")
            return None, None

        return summary_dict, summary_df
