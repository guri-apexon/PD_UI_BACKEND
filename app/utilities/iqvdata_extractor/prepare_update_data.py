import json
import logging
import pandas as pd

import sys
sys.path.append(r'app/api/endpoints/')

# import etmfa_finalization.core.iqvdata_extractor.Elastic_ingest as ei
# from etmfa_core.aidoc.io.load_xml import readXML
# from etmfa_core.aidoc.IQVDocumentFunctions import IQVDocument, IQVKeyValueSet
# from etmfa_finalization import Constantsapp.utilities.iqvdata_extractor.
# from etmfa_finalization.core.iqvdata_extractor import cpt_extractor, jsonb_datastructure
# from etmfa_finalization.core.iqvdata_extractor import summary_extractor as se
# from etmfa_finalization.core.iqvdata_extractor import table_extractor
# from etmfa_finalization.core.iqvdata_extractor.extractor_config import ModuleConfig

import app.utilities.iqvdata_extractor.Elastic_ingest as ei
from etmfa_core.aidoc.io.load_xml import readXML
from app.utilities.iqvdata_extractor import Constants
from etmfa_core.aidoc.IQVDocumentFunctions import IQVDocument, IQVKeyValueSet
from app.utilities.iqvdata_extractor import cpt_extractor, jsonb_datastructure
from app.utilities.iqvdata_extractor import summary_extractor as se
from app.utilities.iqvdata_extractor import table_extractor
from app.utilities.iqvdata_extractor.extractor_config import ModuleConfig

logger = logging.getLogger(Constants.MICROSERVICE_NAME)


class PrepareUpdateData:
    def __init__(self, iqv_document: IQVDocument, FeedbackRunId: int, profile_details: dict, entity_profile_genre: list):
        self.iqv_document = iqv_document
        self.dict_orient_type = ModuleConfig.GENERAL.dict_orient_type
        self.empty_json = ModuleConfig.GENERAL.empty_json
        self.FeedbackRunId = FeedbackRunId

        self.profile_details = profile_details
        self.entity_profile_genre = entity_profile_genre

    def prepare_msg(self) -> (dict, IQVDocument):
        db_data = self._prepare_db_data()
        return db_data, self.iqv_document

    def _prepare_db_data(self):
        iqv_document = self.iqv_document
        db_data = dict()
        db_data['iqvdoc_tagid'] = iqv_document.id
        db_data['toc'] = self.empty_json
        db_data['soa'] = self.empty_json
        db_data['summary'] = self.empty_json
        db_data['normalized_soa'] = self.empty_json

        # Elastic search ingestion
        try:
            cpt_iqvdata = cpt_extractor.CPTExtractor(iqv_document, self.profile_details, self.entity_profile_genre)
            display_df, search_df, _, _, _ = cpt_iqvdata.get_cpt_iqvdata()

            db_data, summary_entities = ei.ingest_doc_elastic(iqv_document, search_df, self.FeedbackRunId)
            logger.info("Elastic search ingestion step completed")

            db_data["summary_entities"] = json.dumps(summary_entities)
            db_data['ProtocolName'] = db_data.get("protocol_name", "")
            db_data['Activity_Status'] = ''
            db_data['Completeness_of_digitization'] = ''
            db_data['Digitized_Confidence_interval'] = ''

        except Exception as exc:
            logger.exception(f"Exception received in Elastic search ingestion step: {exc}")

        # Collect additional metadata fields (for downstream applications)
        try:
            metadata_fields = dict()

            for key in ModuleConfig.GENERAL.es_metadata_mapping:
                metadata_fields[ModuleConfig.GENERAL.es_metadata_mapping[key]] = db_data.get(key, '')

            metadata_fields['accuracy'] = ''
            logger.info(f"metadata: {metadata_fields}")
        except Exception as exc:
            logger.exception(f"Exception received in building metadata_fields step: {exc}")

        # Entire file content extraction
        try:
            if display_df is not None:
                display_df['aidocid'] = iqv_document.id
                display_df['synonyms_extracted_terms'] = ''
                display_df['semantic_extraction'] = ''

                display_df["section_locked"] = False

                display_dict = display_df.to_dict(orient=self.dict_orient_type)
                display_dict['metadata'] = metadata_fields
                db_data['toc'] = json.dumps(display_dict)
                logger.info("CPT extraction step completed")

            else:
                logger.error("No data received at CPT extraction step. display_df is empty")

        except Exception as exc:
            logger.exception(f"Exception received in CPT extraction step: {exc}")


        try:
            normalized_soa = self.normalized_soa_extraction(iqv_document)
            db_data['normalized_soa'] = json.dumps(normalized_soa)
            logger.info("Normalized SOA json extraction step completed")
        except Exception as exc:
            logger.exception(f"Exception received in normalized soa extraction: {exc}")

        try:
            soa = table_extractor.SOAResponse(iqv_document, self.profile_details, self.entity_profile_genre)
            db_data['soa'] = json.dumps(soa.getTOIfromProprties(returntype='html', roi=None, toi='SOA')[0])
            logger.info("SOA extraction step completed")
        except Exception as exc:
            logger.exception(f"Exception received in SOA: {exc}")

        # Summary data
        try:
            summary_dict = list()
            for key, val in ModuleConfig.SUMMARY.summary_key_list.items():
                if key == "primary_objectives":
                    summary_dict.append((key, metadata_fields.get("objectives_section", ""), val))
                else:
                    summary_dict.append((key, metadata_fields.get(key, ""), val))

            summary_dict = pd.DataFrame(summary_dict)

            summary_dict.columns = ["field_name", "field_value", "field_header"]
            summary_dict = summary_dict.to_dict(orient=self.dict_orient_type)
            summary_dict['metadata'] = {"accuracy": ""}

            db_data['summary'] = json.dumps(summary_dict)
            logger.info("Summary extraction step completed")
        except Exception as exc:
            logger.exception(f"Exception received in Summary extraction step: {exc}")

        return display_df.to_dict(orient = 'records') if display_df is not None else dict()
        # return (db_data)

    def _add_tag(self, db_data):
        try:
            iqv_document = self.iqv_document
            roi_obj = iqv_document

            for key_data in db_data.keys():
                kv_obj = IQVKeyValueSet()
                kv_obj.key = key_data
                kv_obj.value = str(db_data[key_data])
                roi_obj.Properties.append(kv_obj)
            return (iqv_document)

        except Exception as e:
            logger.warning(
                "warning Finalization: Adding Tag to XML failed  with error : {} , The values are Key:{} value:{} id:{} ".format(
                    e, key_data, db_data[key_data]))

    def normalized_soa_extraction(self, iqv_document):
        try:
            iqv_document = self.iqv_document
            for kv in iqv_document.Properties:
                if kv.key == 'NormalizedSOA_JSONFilename':
                    normalized_soa_path = kv.value
                    with open(normalized_soa_path) as f:
                        soa_json_data = json.load(f)
                        return soa_json_data
        except Exception as e:
            logger.error("No Normalized SOA Json path")


# def add_compare_event(compare_req_msg, protocol_number, project_id, protocol_number2, project_id2, user_id):
#     compare = Documentcompare()
#     compare.compare_id = compare_req_msg['COMPARE_ID']
#     compare.doc_id = compare_req_msg['BASE_DOC_ID']
#     compare.protocol_number = protocol_number
#     compare.project_id = project_id
#     # compare.version_number = compare_req_msg['']#these will added if additional details are made mandatory
#     # compare.amendment_number = compare_req_msg['']#these will added if additional details are made mandatory
#     # compare.document_status = compare_req_msg['']#these will added if additional details are made mandatory
#     compare.doc_id2 = compare_req_msg['COMPARE_DOC_ID']
#     compare.protocol_number2 = protocol_number2
#     compare.project_id2 = project_id2
#     # compare.version_number2 = compare_req_msg['']#these will added if additional details are made mandatory
#     # compare.amendment_number2 = compare_req_msg['']#these will added if additional details are made mandatory
#     # compare.document_status2 = compare_req_msg['']#these will added if additional details are made mandatory
#     compare.user_id = user_id
#     compare.base_IQV_xml_path = compare_req_msg['BASE_IQVXML_PATH']
#     compare.compare_IQV_xml_path = compare_req_msg['COMPARE_IQVXML_PATH']
#     compare.request_type = compare_req_msg['REQUEST_TYPE']
#     try:
#         db_context.session.add(compare)
#         db_context.session.commit()
#         return compare.compare_id
#     except Exception as ex:
#         db_context.session.rollback()
#         exception = ManagementException(id, ErrorCodes.ERROR_DOCUMENT_ATTRIBUTES)
#         received_documentprocessing_error_event(exception.__dict__)
#         logger.error("Error while writing record to PD_document_compare file in DB for ID: {},{}".format(
#             compare['compare_id'], ex))
            