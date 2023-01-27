import logging
from app.utilities.config import settings
import pandas as pd

logger = logging.getLogger(settings.LOGGER_NAME)


def update_section_data_with_enriched_data(section_data: dict,
                                           enriched_data: list) -> dict:
    """
    To modify the section data with enriched text and terms.
    :param section_data: Response of section data API
    :param enriched_data: Response of enriched API with clinical terms
    :returns: Updated section data with clinical terms
    """

    enriched_df = pd.DataFrame(enriched_data)
    if enriched_df.empty:
        logger.info("There is no clinical terms present for the sections")
        return section_data

    for sub_section in section_data:
        font_info = sub_section.get("font_info")
        content = sub_section.get("content")
        if content:
            roi_id = font_info.get("roi_id")
            para_id = roi_id.get("para")
            childbox = roi_id.get("childbox")
            subtext = roi_id.get("subtext")

            rows = enriched_df[
                enriched_df['parent_id'].isin([para_id, childbox, subtext])]
            # remove the duplicates records from the rows df
            rows.drop_duplicates(subset=['text'], inplace=True)
            # Deleted df columns which is not needed any more
            rows.drop(['doc_id', 'link_id', 'parent_id'], axis=1, inplace=True)
            terms_values = rows.set_index('text').to_dict(orient='index')
            sub_section.update({'clinical_terms': terms_values})

    return section_data
