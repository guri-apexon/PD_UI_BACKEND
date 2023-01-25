from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class ConfigDb(SchemaBase):
   __tablename__ = "config_db"
   id = Column(VARCHAR(128),primary_key=True,nullable=False)
   IQVDocumentMappingFilename = Column(TEXT)
   GroundTruthMasterFilename = Column(TEXT)
   GroundTruthOutputDirectory = Column(TEXT)
   TMFRawDataSourceDirectory = Column(TEXT)
   bNoiseGenGreyscale = Column(BOOLEAN,nullable=False)
   bNoiseGenLegibility = Column(BOOLEAN,nullable=False)
   bNoiseGenPageSequence = Column(BOOLEAN,nullable=False)
   bNoiseGenPageBlanks = Column(BOOLEAN,nullable=False)
   bNoiseGenPageOrientation = Column(BOOLEAN,nullable=False)
   NoiseGenStartIndex = Column(INTEGER,nullable=False)
   NoiseGenMaxRecords = Column(INTEGER,nullable=False)
   LocalTopLevelDataDir = Column(TEXT)
   DropBox1Dir = Column(TEXT)
   DropBoxWebUI = Column(TEXT)
   MasterIQVDocumentListFilename = Column(TEXT)
   WatchLogFilename = Column(TEXT)
   WatchLogCheckIntervalSeconds = Column(DOUBLE_PRECISION,nullable=False)
   sofficeLocation = Column(TEXT)
   PythonEXEFilename = Column(TEXT)
   PythonEnvironment = Column(TEXT)
   Dig1CodePathFilename = Column(TEXT)
   bRunPyIPOCRProcesses = Column(INTEGER,nullable=False)
   bRunInternalOCRProcesses = Column(INTEGER,nullable=False)
   bOCRRaiseErrorIfScan = Column(INTEGER,nullable=False)
   ProcessSource = Column(INTEGER,nullable=False)
   XLIFFMarkupVersion = Column(TEXT)
   bDeleteInputSourceFile = Column(BOOLEAN,nullable=False)
   bDeleteAllFilesExceptFinalizerOutputFile = Column(BOOLEAN,nullable=False)
   bTMFGTOutputConstrained = Column(BOOLEAN,nullable=False)
   TMFGTOutputConstrained_MinSamples = Column(INTEGER,nullable=False)
   TMFGTOutputConstrained_AvgPages = Column(INTEGER,nullable=False)
   NoiseType = Column(INTEGER,nullable=False)
   GenerateNoise = Column(INTEGER,nullable=False)
   CorpusLevel = Column(INTEGER,nullable=False)
   DataSplit_TrainingPercent = Column(INTEGER,nullable=False)
   DataSplit_TestPercent = Column(INTEGER,nullable=False)
   MinPixelWidthForValidImage = Column(INTEGER,nullable=False)
   MinPixelHeightForValidImage = Column(INTEGER,nullable=False)
   MinPixelWidthForOCR = Column(INTEGER,nullable=False)
   MinPixelHeightForOCR = Column(INTEGER,nullable=False)
   ETMFDocumentSource = Column(TEXT)
   ETMFOutputDir = Column(TEXT)
   DictionaryIncludeAdditionalFeatures = Column(INTEGER,nullable=False)
   DictionaryIncludeBigrams = Column(INTEGER,nullable=False)
   DictionaryIncludeTrigrams = Column(INTEGER,nullable=False)
   DictionaryIncludeLines = Column(INTEGER,nullable=False)
   DictionaryIncludeStopWords = Column(INTEGER,nullable=False)
   bDictionaryBernoulliSingleCounts = Column(INTEGER,nullable=False)
   DictionarybRemoveSparseTerms = Column(INTEGER,nullable=False)
   DictionaryRemoveSparseTerms_MinDocCount = Column(INTEGER,nullable=False)
   DictionarybRemoveCommonTerms = Column(INTEGER,nullable=False)
   DictionaryRemoveCommonTerms_MaxDocCount = Column(INTEGER,nullable=False)
   bDeleteWorkingTempDirOnSuccessComplete = Column(INTEGER,nullable=False)
   bUseDBConnection = Column(INTEGER,nullable=False)
   DBConn_Server = Column(TEXT)
   DBConn_Database = Column(TEXT)
   DBConn_Login = Column(TEXT)
   DBConn_Password = Column(TEXT)
   IQVXML_DBConn_Server = Column(TEXT)
   IQVXML_DBConn_Database = Column(TEXT)
   IQVXML_DBConn_Port = Column(INTEGER,nullable=False)
   IQVXML_DBConn_Login = Column(TEXT)
   IQVXML_DBConn_Password = Column(TEXT)
   RemoteServer_MachineName = Column(TEXT)
   RemoteServer_Port = Column(TEXT)
   RemoteServer_ServerLocalDir = Column(TEXT)
   RemoteServer_SharedDir = Column(TEXT)
   bProvideRemoteService = Column(INTEGER,nullable=False)
   bCorrectRotation = Column(INTEGER,nullable=False)
   DefaultRotation = Column(DOUBLE_PRECISION,nullable=False)
   CorrectRotation_RotationRangeDegrees = Column(DOUBLE_PRECISION,nullable=False)
   CorrectRotation_RotationIncrementDegrees = Column(DOUBLE_PRECISION,nullable=False)
   ImageQC_GreyscaleThreshold = Column(DOUBLE_PRECISION,nullable=False)
   ImageQC_LegibilityThreshold = Column(DOUBLE_PRECISION,nullable=False)
   Recon_TemplateFilename = Column(TEXT)
   Recon_TemplateDirectory = Column(TEXT)
   Recon_bUseTemplateMatching = Column(INTEGER,nullable=False)
   ImageProc_BulletImagesDir = Column(TEXT)
   DebugType = Column(INTEGER,nullable=False)
   DebugMode = Column(INTEGER,nullable=False)
   SegmentationType = Column(INTEGER,nullable=False)
   CustomHostName = Column(TEXT)
   LanguageAnalysisLib = Column(TEXT)
   AIDocQueue_NumWorkers = Column(INTEGER,nullable=False)
   AIDocQueue_IsAdmin = Column(INTEGER,nullable=False)
   AIDocQueue_IsWorker = Column(INTEGER,nullable=False)
   bOutput_ToMetricsDir = Column(INTEGER,nullable=False)
   Output_ToMetricsDir = Column(TEXT)
   Output_ToCompareDir = Column(TEXT)
   bOutput_PrefixText = Column(INTEGER,nullable=False)
   Output_PrefixText = Column(TEXT)
   bOutput_OmopPrefixText = Column(INTEGER,nullable=False)
   Output_OmopPrefixText = Column(TEXT)
   IQVEnvironment = Column(TEXT)
   RedactionProfileListingFilename = Column(TEXT)
   RedactionReplacementMethod = Column(TEXT)
   RedactionTextMask = Column(TEXT)
   RedactionTextPrefix = Column(TEXT)
   RedactionTextSuffix = Column(TEXT)
   RedactionProfileID = Column(TEXT)
   StandardTemplateIQVXML = Column(TEXT)
   ExcelTemplate_SOA = Column(TEXT)
   NLP_DictionaryDirectory = Column(TEXT)
   NLP_CharMatrixDirectory = Column(TEXT)
   DOCANALYSIS_TrainedNaiveBayesLibFilename = Column(TEXT)
   OCR_UserWordsDirectory = Column(TEXT)
   OCR_SpellCheckDirectory = Column(TEXT)
   OCR_bUseSpellCheck = Column(INTEGER,nullable=False)
   tessdataDir = Column(TEXT)
   bWatchLog_EnableWebserverRequests = Column(INTEGER,nullable=False)
   bELK_EnableLogging = Column(INTEGER,nullable=False)
   ELK_HostName = Column(TEXT)
   ELK_Port = Column(INTEGER,nullable=False)
   MSG_ErrorLevelLowerBound = Column(INTEGER,nullable=False)
   bMSG_EnableMessaging = Column(INTEGER,nullable=False)
   bMSG_EnableMessaging_Digitizer2Processing = Column(INTEGER,nullable=False)
   bMSG_EnableMessaging_CompareProcessing = Column(INTEGER,nullable=False)
   bMSG_EnableMessaging_OMOPProcessing = Column(INTEGER,nullable=False)
   bMSG_EnableMessaging_QCFeedbackProcessing = Column(INTEGER,nullable=False)
   API_Endpoint = Column(TEXT)
   API_Key = Column(TEXT)
   MSG_MaxCPU = Column(INTEGER,nullable=False)
   MSG_MaxRAM = Column(INTEGER,nullable=False)
   MSG_HostName = Column(TEXT)
   MSG_Port = Column(INTEGER,nullable=False)
   MSG_User = Column(TEXT)
   MSG_Password = Column(TEXT)
   MSG_VirtualHost = Column(TEXT)
   MSG_ExchangeIsDurable = Column(INTEGER,nullable=False)
   MSG_QueueIsDurable = Column(INTEGER,nullable=False)
   TMSServer_MachineName = Column(TEXT)
   TMSServer_Port = Column(TEXT)
   TMSServer_Endpoint = Column(TEXT)
   TMSServer_Info = Column(TEXT)
   MTServer_Endpoint = Column(TEXT)
   MTServer_MachineName = Column(TEXT)
   MTServer_Port = Column(TEXT)
   MTServer_LocalPathMapping = Column(TEXT)
   MTServer_SharedDir = Column(TEXT)
   bUseMTServer = Column(INTEGER,nullable=False)
   MTServer_SecureHTTP = Column(INTEGER,nullable=False)
   MTServer_User = Column(TEXT)
   MTServer_Password = Column(TEXT)
   CountryMappingFilename = Column(TEXT)
   SegServer_Endpoint = Column(TEXT)
   SegServer_MachineName = Column(TEXT)
   SegServer_Port = Column(TEXT)
   SegServer_LocalPathMapping = Column(TEXT)
   SegServer_SharedDir = Column(TEXT)
   bUseSegServer = Column(INTEGER,nullable=False)
   SegServer_SecureHTTP = Column(INTEGER,nullable=False)
   FileDownloadStartIndex = Column(INTEGER,nullable=False)
   MaxPagesCoreProcessing_FrontSection = Column(INTEGER,nullable=False)
   MaxPagesCoreProcessing_BackSection = Column(INTEGER,nullable=False)
   MaxCellsPerPage = Column(INTEGER,nullable=False)
   MaxPagesToProcessIQVTM = Column(INTEGER,nullable=False)
   MaxPagesToProcess = Column(INTEGER,nullable=False)
   MaxNumDocsToProcess = Column(INTEGER,nullable=False)
   MaxTimeMinutesPerPage = Column(INTEGER,nullable=False)
   RunRemote = Column(BOOLEAN,nullable=False)
   ShowProgressForm = Column(INTEGER,nullable=False)
   bDocumentManagerEXE_CloseAfterProcessDocument = Column(INTEGER,nullable=False)
   DocumentManagerEXE = Column(TEXT)
   DocumentManagerVersion = Column(TEXT)
   GhostscriptEXEFilename = Column(TEXT)
   TesseractEXEFilename = Column(TEXT)
   InputImageFilename = Column(TEXT)
   InputRawFilename = Column(TEXT)
   InputSourceMasterFilename = Column(TEXT)
   UserID = Column(TEXT)
   UserEmail = Column(TEXT)
   Dig1DocID = Column(TEXT)
   DocID = Column(TEXT)
   DocID1 = Column(TEXT)
   DocID2 = Column(TEXT)
   InputWorkingMasterFilename = Column(TEXT)
   OutputFilename = Column(TEXT)
   OutputDirectory = Column(TEXT)
   LogFilename = Column(TEXT)
   LogDirectory = Column(TEXT)
   IQVXMLInputFilename = Column(TEXT)
   IQVXMLInputFilename2 = Column(TEXT)
   OMOPUpdateFilename = Column(TEXT)
   QCFeedbackJSONFilename = Column(TEXT)
   QCFeedbackRunId = Column(TEXT)
   bOutput_QCFeedbackPrefixText = Column(INTEGER,nullable=False)
   Output_QCFeedbackPrefixText = Column(TEXT)
   XLIFFInputFilename = Column(TEXT)
   WorkingDirectory = Column(TEXT)
   ImagesDirectory = Column(TEXT)
   bClearWorkingDirectory = Column(INTEGER,nullable=False)
   ConfigFilename = Column(TEXT)
   InputDataDirectory = Column(TEXT)
   MatrixFile = Column(TEXT)
   Priority = Column(INTEGER,nullable=False)
   OutputLevel = Column(INTEGER,nullable=False)
   TargetLanguage = Column(TEXT)
   SourceLanguage = Column(TEXT)
   DisplayLabel = Column(TEXT)
   PerformDocumentDeconstruction = Column(INTEGER,nullable=False)
   PerformXLIFFSourceCreation = Column(INTEGER,nullable=False)
   PerformXLIFFSend = Column(INTEGER,nullable=False)
   PerformXLIFFReceive = Column(INTEGER,nullable=False)
   PerformDocumentReconstruction = Column(INTEGER,nullable=False)
   PerformImageQC = Column(INTEGER,nullable=False)
   PerformDuplicateCheck = Column(INTEGER,nullable=False)
   PerformBatchDocClass = Column(INTEGER,nullable=False)
   PerformMetadata = Column(INTEGER,nullable=False)
   PerformRotations = Column(INTEGER,nullable=False)
   MasterFile = Column(INTEGER,nullable=False)
   PageIndex = Column(INTEGER,nullable=False)
   Rotation = Column(INTEGER,nullable=False)

