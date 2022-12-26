import logging

import sys
sys.path.append(r'app/api/endpoints/')

from app.utilities.iqvdata_extractor.extractor_config import ModuleConfig, QcStatus
from app.utilities.iqvdata_extractor.utils import get_redaction_entities, align_redaction_with_subtext
from datetime import datetime
from app.utilities.config import settings

# Sets logger
logger = logging.getLogger(settings.LOGGER_NAME)

"""
Keys for Extraction from DocumentLinks
"""
es_toc_sec_pat = [
    'IsInclusionCriteria',
    'IsExclusionCriteria',
    'IsObjectives',
    'IsEndpoints',
    'IsAdverseEvents',
    'IsSeriousAdverseEvents'
]

summary_sec_pat = ['IsObjectiveAndEndpoint',
                   'IsInclusionCriteria',
                   'IsExclusionCriteria',
                   'IsNumberOfParticipants',
                   'IsTitle',
                   'IsShortTitle',
                   'IsPrimaryObjective',
                   'IsSecondaryObjective',
                   'IsExploratoryObjective',
                   'IsPrimaryEndpoint',
                   'IsSecondaryEndpoint',
                   'IsRationale',
                   'IsDesign',
                   'IsBriefSummary',
                   'IsInterventionGroups',
                   'IsDataMonitoringCommittee',
                   'IsSchema']


ling_es_mapping = {
    "ProtocolTitle": "ProtocolTitle",
    "short_title": "ShortTitle",
    "amendment_number": "AmendmentNumber",
    "phase": "phase",
    "sponsor": "SponsorName",
    "sponsor_address": "SponsorAddress",
    "drug": "Drug",
    "approval_date": "approval_date",
    "ProtocolVersion": "VersionNumber",
    "version_date": "VersionDate",
    "blinding": "Blinding",
    "compound": "Compound",
    "control": "Control",
    "investigator": "Investigator",
    "study_id": "StudyId",
    "number_of_subjects": "NumberOfSubjects",
    "participant_age": "ParticipantAge",
    "participant_sex": "ParticipantSex",
    "exclusion_section": "ExclusionSection",
    "inclusion_section": "InclusionSection",
    "indication": "Indication",
    "objectives_section": "ObjectivesSection",
    "population": "Population",
    "entities_in_assessments": "EntitiesInAssessments",
    "soa_epochs": "SoaEpochs",
    "soa_footnotes": "SoaFootnote"
}

# ["SponsorName", "AmendmentNumber", "Indication"] Old intake_field_list_priority
intake_field_list_priority = ["SponsorName", "Indication"]


def ingest_doc_elastic(iqv_document, search_df, FeedbackRunId):
    current_timestamp = datetime.utcnow()
    current_utc_num_format = current_timestamp.strftime("%Y%m%d%H%M%S")
    es_sec_dict = dict()
    summary_entities = dict()
    search_rollup_column = ModuleConfig.GENERAL.SEARCH_ROLLUP_COLUMN

    try:
        if iqv_document.id:
            es_sec_dict['AiDocId'] = iqv_document.id
    except Exception as exc:
        logger.exception(f"Exception received in ingest_doc_elastic, AIDocId not present:{exc}")

    # CPT file content extraction
    try:
        if search_df is not None and len(search_df) > 0:
            rollup_df = search_df
            rollup_df = rollup_df.groupby(search_rollup_column)['content'].apply(list).reset_index()
            rollup_df['content'] = rollup_df['content'].apply(lambda x: ' '.join(x))
            toc_dict = {hdr[search_rollup_column]: hdr['content'] for hdr in rollup_df.to_dict(orient='records')}
            es_sec_dict.update(toc_dict)
        else:
            logger.warning("No data from digitized document inserted to elastic search. search_df is empty")

    except Exception as exc:
        logger.exception(f"Exception received in rollup stage : {exc}")

    # Populating intake fields
    try:
        intake_dict = dict()

        intake_fields_list = ['ProtocolNo', 'MoleculeDevice', 'SponsorName', 'SourceFileName', 'DocumentStatus',
                              'VersionNumber', 'UserId', 'UserModified', 'ProjectId', 'IsAmendment', 'Indication',
                              'uploadDate', 'TimeCreated', 'TimeUpdated', 'Environment', 'SourceSystem', 'StudyStatus',
                              'DraftVersion', 'documentPath', 'is_active']
        for field in intake_fields_list:
            intake_dict[field] = ''

        es_sec_dict['uploadDate'] = iqv_document.dateTimeUploaded
        es_sec_dict['SourceFileName'] = iqv_document.originalSourceFilename.split('\\')[-1]
        es_sec_dict['documentPath'] = iqv_document.DropBoxDir
        es_sec_dict['is_active'] = 1
        for IQVDocumentFeedbackResults in iqv_document.IQVDocumentFeedbackResultsList:
            if 'ProtocolNo' not in intake_dict or intake_dict['ProtocolNo'] == '':
                intake_dict['ProtocolNo'] = IQVDocumentFeedbackResults.protocol.strip()
            if 'MoleculeDevice' not in intake_dict or intake_dict['MoleculeDevice'] == '':
                intake_dict['MoleculeDevice'] = IQVDocumentFeedbackResults.molecule_device.strip()
            if 'SponsorName' not in intake_dict or intake_dict['SponsorName'] == '':
                intake_dict['SponsorName'] = IQVDocumentFeedbackResults.sponsor.strip()
            if 'SourceFileName' not in intake_dict or intake_dict['SourceFileName'] == '':
                intake_dict['SourceFileName'] = IQVDocumentFeedbackResults.source_filename.split("\\")[-1]
            if 'DocumentStatus' not in intake_dict or intake_dict['DocumentStatus'] == '':
                intake_dict['DocumentStatus'] = IQVDocumentFeedbackResults.document_status.strip()
            if 'VersionNumber' not in intake_dict or intake_dict['VersionNumber'] == '':
                intake_dict['VersionNumber'] = IQVDocumentFeedbackResults.version_number.strip()
            if 'UserId' not in intake_dict or intake_dict['UserId'] == '': # User created field
                intake_dict['UserId'] = IQVDocumentFeedbackResults.user_id.strip()
            if 'UserModified' not in intake_dict or intake_dict['UserModified'] == '':
                intake_dict['UserModified'] = "" # IQVDocumentFeedbackResults.user_id
            if 'ProjectId' not in intake_dict or intake_dict['ProjectId'] == '':
                intake_dict['ProjectId'] = IQVDocumentFeedbackResults.project_id.strip()
            if 'IsAmendment' not in intake_dict or intake_dict['IsAmendment'] == '':
                intake_dict['IsAmendment'] = IQVDocumentFeedbackResults.amendment_number.strip()  # This is Yes, No Flag from UI
            if 'Indication' not in intake_dict or intake_dict['Indication'] == '':
                intake_dict['Indication'] = IQVDocumentFeedbackResults.indication.strip()
            if 'uploadDate' not in intake_dict or intake_dict['uploadDate'] == '':
                intake_dict['uploadDate'] = IQVDocumentFeedbackResults.date_time_stamp.strip()  # YYYYMMDDHHMMSS
            if 'TimeCreated' not in intake_dict or intake_dict['TimeCreated'] == '':
                intake_dict['TimeCreated'] = "" # IQVDocumentFeedbackResults.date_time_stamp # YYYYMMDDHHMMSS
            if 'TimeUpdated' not in intake_dict or intake_dict['TimeUpdated'] == '':
                intake_dict['TimeUpdated'] = "" # IQVDocumentFeedbackResults.date_time_stamp # YYYYMMDDHHMMSS
            if 'Environment' not in intake_dict or intake_dict['Environment'] == '':
                intake_dict['Environment'] = IQVDocumentFeedbackResults.environment.strip()
            if 'SourceSystem' not in intake_dict or intake_dict['SourceSystem'] == '':
                intake_dict['SourceSystem'] = IQVDocumentFeedbackResults.source_system.strip()
            if 'StudyStatus' not in intake_dict or intake_dict['StudyStatus'] == '':
                intake_dict['StudyStatus'] = IQVDocumentFeedbackResults.study_status.strip()
            if 'DraftVersion' not in intake_dict or intake_dict['DraftVersion'] == '':
                intake_dict['DraftVersion'] = IQVDocumentFeedbackResults.draft_number.strip()

        for sec in intake_dict:
            if sec not in es_sec_dict or es_sec_dict[sec] == '':
                es_sec_dict[sec] = intake_dict[sec]

        es_sec_dict['qcStatus'] = QcStatus.NOT_STARTED.value if FeedbackRunId == 0 else QcStatus.COMPLETED.value  # Default digitized protocol qcStatus from R1.4
        es_sec_dict['QC_Flag'] = False if FeedbackRunId == 0 else True
        es_sec_dict['TimeCreated'] = current_utc_num_format
        es_sec_dict['TimeUpdated'] = current_utc_num_format

    except Exception as exc:
        logger.exception(f"Exception received in ingest_doc_elastic, intake field extraction:{exc}")

    # Populating Linguamatics fields
    try:
        linguamatics_op_dict = {
            "ProtocolTitle": "",  # yes
            "amendment_number": "",  # yes
            "compound": "",  # yes
            "control": "",  # yes
            "drug": "",  # yes, nothing but intervention name
            "investigator": "",  # yes
            "short_title": "",  # yes
            "sponsor_address": "",  # yes
            "study_id": "",  # yes
            "version_date": "",  # yes
            "ProtocolVersion": "",  # yes
            "phase": "",  # yes
            "sponsor": "",  # yes
            "approval_date": "",  # yes
            "blinding": "",  # yes
            "number_of_subjects": "",  # yes
            "participant_age": "",  # yes
            "participant_sex": "",  # yes
            "exclusion_section": "",
            "inclusion_section": "",
            "indication": "",
            "objectives_section": "",
            "population": "",
            "entities_in_assessments": "",
            "soa_epochs": "",
            "soa_footnotes": ""
        }

        for kv in iqv_document.Properties:
            if kv.key in linguamatics_op_dict and linguamatics_op_dict[kv.key] == '':
                linguamatics_op_dict[kv.key] = kv.value.strip()
                _, redaction_entities = get_redaction_entities(kv)
                _, subtext_redaction_entities = align_redaction_with_subtext(kv.value, redaction_entities)
                if subtext_redaction_entities:
                    summary_entities[kv.key] = subtext_redaction_entities

        for key in ling_es_mapping:
            if ling_es_mapping[key] not in intake_field_list_priority:
                if ling_es_mapping[key] in es_sec_dict and linguamatics_op_dict[key] != '':
                    es_sec_dict[ling_es_mapping[key]] = linguamatics_op_dict[key]
                elif ling_es_mapping[key] not in es_sec_dict:
                    es_sec_dict[ling_es_mapping[key]] = linguamatics_op_dict[key]

        if (es_sec_dict['approval_date'].isnumeric() and len(es_sec_dict['approval_date']) != 8) or (not es_sec_dict['approval_date'].isnumeric()):
            es_sec_dict['approval_date'] = ''

        feedback_run_additional_keys = {
            "molecule_device": "MoleculeDevice",
            "protocol_name": "protocol_name",
            "ProtocolNumber": "ProtocolNo",
            "is_amendment": "IsAmendment",
            "secondary_objectives": "secondary_objectives",
            "study_status": "StudyStatus",
            "endpoints": "endpoints",
            "trial_type_randomized": "trial_type_randomized",
            "indication":"Indication",
            "sponsor":"SponsorName"
        }

        if FeedbackRunId > 0:
            for kv in iqv_document.Properties:
                if kv.key in feedback_run_additional_keys:
                    es_sec_dict[feedback_run_additional_keys[kv.key]] = kv.value

    except Exception as exc:
        logger.exception(f"Exception received in ingest_doc_elastic, intake field extraction:{exc}")

    return es_sec_dict, summary_entities
