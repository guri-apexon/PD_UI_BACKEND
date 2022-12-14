import numpy as np
from dataclasses import asdict, dataclass, field, fields, is_dataclass, InitVar
from datetime import datetime, timedelta
from etmfa_finalization.config import Config
from etmfa_core.aidoc.models.IQVDocument import IQVKeyValueSet


@dataclass(frozen=True)
class ClassificationAttributes:
    doc_classification: list
    doc_classification_conf: list


@dataclass(frozen=True)
class DocumentWingspanMapping:
    mapped_classifications: ClassificationAttributes
    date_guidance: str
    additional_instructions_list: list

    def top_1_wingspan(self):
        return self.mapped_classifications.doc_classification[0]

    def top_1_wingspan_conf(self):
        return self.mapped_classifications.doc_classification_conf[0]

@dataclass(frozen=True)
class LanguageAttribute:
    language_codes: list
    language: list
    language_conf: list


@dataclass(frozen=True)
class NameAttributes:
    name: str
    name_conf: float
    name_role: str


@dataclass(frozen=True)
class Subject:
    subject: str
    subject_conf: float
    language_identifier: str
    language_identifier_conf: float
    version: str
    version_conf: float

    @classmethod
    def create_subject(cls, languageidentifier=None, languageidentifier_conf=None,
                       version=None, version_conf=None, individualname=None,
                       individualname_conf=None, **kwargs):
        confidence_scores = [version_conf, languageidentifier_conf, individualname_conf]
        filtered_confidence = [confidence for confidence in confidence_scores if confidence is not None]
        subject_conf = np.mean(filtered_confidence) if filtered_confidence else 1.0
        subject = ' '.join(filter(lambda x: x not in [None, 'None'], [version, languageidentifier, individualname]))
        return Subject(language_identifier=languageidentifier, subject=subject, subject_conf=round(subject_conf, 4),
                       language_identifier_conf=languageidentifier_conf, version=version,
                       version_conf=version_conf)


@dataclass
class DocumentDate:
    document_date: str
    date_guidance: str
    score: float
    selected: bool


@dataclass
class DocumentDateList:
    doc_date: list
    expiry_date: DocumentDate = None
    selected_date: DocumentDate = None
    date_guidance: InitVar[str] = None

    def __post_init__(self, date_guidance):
        self._initialize_dates_by_guidance(date_guidance)

    def _initialize_dates_by_guidance(self, date_guidance):
        """
        Identify the date from the list which matched with the date guidance.
        If exact match not found, then look for the fallback date.

        Reference - http://wiki.quintiles.net/display/EA/Date+guidance+implementation

        params
        ------
            date_guidance: Primary date guidance

        """
        date_dict = dict()
        alias_guidances = Config.FALL_BACK_DATE.get(date_guidance, {}).get(Config.ALIAS_GUIDANCE, [])
        alias_date = None
        for date in self.doc_date:
            date_dict[date.date_guidance] = date

            # Primary guidance match
            if date.date_guidance == date_guidance:
                date.selected = True
                self.selected_date = date

            # Expiration date match
            elif date.date_guidance == Config.EXPIRATION_DATE:
                date.selected = True
                self.expiry_date = date

            # if no primary guidance identified yet, but an alias found and
            # if is greater than the current alias date, then update
            elif not self.selected_date and date.date_guidance in alias_guidances and (alias_date is None or
                                                                                       date.document_date >
                                                                                       alias_date.document_date):
                alias_date = date

        # If no primary guidance found but alias guidance present then update selected date.
        if self.selected_date is None and alias_date is not None:
            alias_date.selected = True
            self.selected_date = alias_date

        # If no primary or alias guidance found, then find secondary date guidance
        if self.selected_date is None:
            self.selected_date = self._get_fall_back_date(date_dict, date_guidance)

    def _get_fall_back_date(self, date_dict, date_guidance):
        """
        Identify the nearest fallback date for the primary date guidance.

        params
        ------
            date_dict - Dictionary with key as date as date guidance and value DocumentDate
            model object

            date_guidance - Primary date guidance
        returns:
            DocumentDate model object.
        """
        while date_guidance != Config.LAST_ENTRY_DATE:
            date_guidance = Config.FALL_BACK_DATE.get(date_guidance, {}).get(Config.SECONDARY_GUIDANCE,
                                                                             Config.LAST_ENTRY_DATE)
            date = date_dict.get(date_guidance, None)
            if date is not None:
                date.selected = True
                return date

    def _to_management_service(self):
        return {"doc_date": [asdict(row) for row in self.doc_date]}

    def create_iqv_attributes(self):
        """

        Creates a list of IQVKeyValueSet
            key - Date guidance
            value - Date
            rawScore - Probability score

        Parameters
        ----------
            date_list: List of DocumentDate objects.
        Returns
        -------
            List of IQVKeyValueSet

        """
        date_attr_list = []

        for obj in self.doc_date:

            date_guidance = IQVKeyValueSet()
            date_guidance.key = obj.date_guidance
            date_guidance.value = obj.document_date
            date_guidance.rawScore = obj.score
            date_attr_list.append(date_guidance)

        return date_attr_list


@dataclass(frozen=True)
class DocumentAttributes:

    def __post_init__(self):

        # No reason to have in place date guidance if no date has been extracted
        # Its cleaner to do it here than prior to object creation
        # since doc_date is extracted from IQVIA XML and
        # doc_date_type (date guidance) is loaded from IQVIA mapping XML
        # based on top_1 elvis classification.
        if not self.date.doc_date:
            # The following does not work when frozen=True
            # self.doc_date_type = None
            # Instead we override doc_date_type with the following:
            super().__setattr__('doc_date_type', None)

    id: str
    doc_comp_conf: float

    # Classification results
    classification: ClassificationAttributes

    date: DocumentDateList

    language: LanguageAttribute

    name: NameAttributes

    subject: Subject

    alcoac_check_comp_score: float
    alcoac_check_comp_score_conf: float
    alcoac_check_error: str

    doc_date_type: str
    doc_type: int
    doc_type_original: int
    doc_pages: int
    doc_segments: int

    # POST API params, we need to sent them to managment service
    # as these are yet not stored in the DB.
    # https://gitlabrnds.quintiles.com/etmf-group/etmfa-management-service/issues/7
    customer: str
    protocol: str
    country: str
    site: str
    doc_class: str
    blinded: str
    DateTimeCreated: str
    received_date: str
    priority: str
    site_personnel_list: dict
    tmf_ibr: str
    tmf_environment: str

    attribute_auxiliary_list: list = field(init=False, default=None)
    doc_subclassification: str = field(init=False, default=None)
    doc_subclassification_conf: float = field(init=False, default=None)

    def flatten_dict(self) -> dict:
        """Helper to flatten nested dataclass objects."""
        flatten_dict = {}

        for attr_field in fields(self):

            if attr_field.type == DocumentDateList:
                flatten_dict.update(getattr(self, attr_field.name)._to_management_service())

            elif is_dataclass(attr_field.type):
                flatten_dict.update(asdict(getattr(self, attr_field.name)))

            else:
                flatten_dict[attr_field.name] = getattr(self, attr_field.name)

        return flatten_dict


@dataclass(frozen=True)
class ProcessingAttributes:
    triage_start_time: datetime
    triage_end_time: datetime
    triage_proc_time: timedelta
    triage_version: str
    triage_machine_name: str

    classification_start_time: datetime
    classification_end_time: datetime
    classification_proc_time: timedelta
    classification_machine_name: str
    classification_version: str

    att_extraction_start_time: datetime
    att_extraction_end_time: datetime
    att_extraction_proc_time: timedelta
    att_extraction_machine_name: str
    att_extraction_version: str

    finalization_start_time: datetime
    finalization_end_time: datetime
    finalization_proc_time: timedelta
    finalization_machine_name: str
    finalization_version: str

    total_process_time: timedelta
    queue_wait_time: timedelta

    digitizer_start_time: datetime = None
    digitizer_end_time: datetime = None
    digitizer_proc_time: timedelta = None
    digitizer_machine_name: str = None
    digitizer_version: str = None
