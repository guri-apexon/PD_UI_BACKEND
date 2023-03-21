import logging
from app.utilities.config import settings
import pandas as pd

logger = logging.getLogger(settings.LOGGER_NAME)


def update_section_data_with_enriched_data(section_data: dict,
                                           enriched_data: list,
                                           preffered_data: list) -> dict:
    """
    To modify the section data with enriched text and terms.
    :param section_data: Response of section data API
    :param enriched_data: Response of enriched API with clinical terms
    :param preffered_data: Response of enriched API with preffered terms
    :returns: Updated section data with clinical terms
    """
    enriched_df = pd.DataFrame(enriched_data)
    preffered_df = pd.DataFrame(preffered_data)

    if enriched_df.empty and preffered_df.empty:
        logger.info("There is no clinical and preffered terms present for the sections")
    else:
        for sub_section in section_data:
            font_info = sub_section.get("font_info")
            content = sub_section.get("content")
            link_id = font_info.get("link_id")
            link_id_level2 = font_info.get("link_id_level2")
            link_id_level3 = font_info.get("link_id_level3")
            link_id_level4 = font_info.get("link_id_level4")
            link_id_level5 = font_info.get("link_id_level5")
            link_id_level6 = font_info.get("link_id_level6")
            if content:
                roi_id = font_info.get("roi_id")
                para_id = roi_id.get("para")
                childbox = roi_id.get("childbox")
                subtext = roi_id.get("subtext")
                if not enriched_df.empty:
                    rows = enriched_df[
                        enriched_df['parent_id'].isin([para_id, childbox, subtext])]
                    # remove the duplicates records from the rows df
                    rows.drop_duplicates(subset=['text'], keep="last", inplace=True)
                    # Deleted df columns which is not needed any more
                    rows.drop(['doc_id', 'link_id', 'parent_id'], axis=1, inplace=True)
                    terms_values = rows.set_index('text').to_dict(orient='index')
                    sub_section.update({'clinical_terms': terms_values})

                if not preffered_df.empty:
                    rows = preffered_df[
                        preffered_df['id'].isin([link_id, link_id_level2, link_id_level3, link_id_level4, link_id_level5, link_id_level6])]
                    # Deleted df columns which is not needed any more
                    rows.drop(['parent_id'], axis=1, inplace=True)
                    terms_values = rows.set_index('text').to_dict(orient='index')
                    sub_section.update({'preffered_term': terms_values})

    return section_data
