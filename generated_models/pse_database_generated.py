# coding: utf-8
from sqlalchemy import (
    DECIMAL,
    NCHAR,
    BigInteger,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    LargeBinary,
    String,
    Table,
    Unicode,
    text,
)
from sqlalchemy.dialects.mssql import (
    BIT,
    DATETIME2,
    IMAGE,
    MONEY,
    NTEXT,
    SMALLDATETIME,
    TINYINT,
    UNIQUEIDENTIFIER,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class ACCOUNTINGHISTORY(Base):
    __tablename__ = "ACCOUNTING_HISTORY"
    __table_args__ = (
        Index("IX_ACCOUNTING_HISTORY_P_ID_SO_NO", "P_ID", "SO_NUMBER"),
        {"schema": "dbo"},
    )

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ACO_ID = Column(Integer)
    P_ID = Column(Integer)
    SO_NUMBER = Column(Integer)
    ACO_POS = Column(Unicode(10))
    ACOT_ID = Column(Integer)
    ST_ID = Column(Integer)
    CC_ID = Column(Unicode(10))
    ACO_DATE = Column(DateTime)
    ZP_ID = Column(Unicode(3))
    ZO_ID = Column(Unicode(3))
    ZP_LOCATION = Column(NCHAR(2))
    ACO_UNITS = Column(DECIMAL(18, 2))
    ACO_RATE = Column(MONEY)
    ACO_SPENDS = Column(MONEY)
    ACO_TOTAL = Column(MONEY)
    ACO_DESCRIPTION = Column(Unicode(3500))
    CUR_ID = Column(NCHAR(3))
    ACO_REGBY = Column(Integer)
    ACO_REGDATE = Column(DateTime)
    ACO_UPDATEBY = Column(Integer)
    ACO_UPDATE = Column(DateTime)
    ACO_DISABLED = Column(BIT)
    ACO_POSTINGSTATUS = Column(Unicode(12))
    ZM_ID = Column(Unicode(18))
    ACO_MEASURE = Column(Unicode(3))
    ACO_RATE_BASECUR = Column(MONEY)
    ACO_SPENDS_BASECUR = Column(MONEY)
    ACO_TOTAL_BASECUR = Column(MONEY)
    ACO_IS_LEGACY = Column(BIT)
    ACTUAL_HOURS = Column(DECIMAL(5, 2))
    TRAVELS = Column(DECIMAL(8, 2))
    EXTERNALS = Column(DECIMAL(8, 2))
    INVOICE_LOCK = Column(BIT)
    SYSTEM_MESSAGE = Column(Unicode(512))
    ACO_IDOC_FILE = Column(Unicode(50))
    REJECT_MESSAGE = Column(Unicode(512))
    ACO_REGBY_TEAM = Column(Integer)
    ACO_UPDATEBY_TEAM = Column(Integer)
    ST_ID_TEAM = Column(Integer)
    AL_ID = Column(Integer)
    IDOC_ID = Column(Integer)
    ST_ID_SAPOK = Column(Integer)
    NONCLEARABLE = Column(BIT)
    INVOICE_TEXT = Column(Unicode(512))
    ZAPFI_ID = Column(Integer)
    INVOICING_TRAVEL_COST = Column(BIT)
    RFAE_ID = Column(Integer)
    ACO_DIVERGENT_RATE = Column(MONEY)
    LAST_SAP_TRANSFER = Column(DateTime)
    NEXT_SAP_TRANSFER = Column(DateTime)
    IS_COLLECTIVE_POSTING = Column(BIT)
    STATUS_POSTED_DATE = Column(DateTime)
    ACO_INZARA = Column(BIT)


class ACOPERIOD(Base):
    __tablename__ = "ACO_PERIOD"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    SAP_ID = Column(Integer, nullable=False)
    TIME_FROM = Column(DateTime, nullable=False)
    TIME_TO = Column(DateTime, nullable=False)
    POST_FROM = Column(DateTime, nullable=False)
    POST_TO = Column(DateTime, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime, nullable=False)


class ACTION(Base):
    __tablename__ = "ACTION"
    __table_args__ = (
        Index(
            "IX_ACTION_P_ID_ACT_DISABLED_REPORT_SENT",
            "P_ID",
            "ACT_DISABLED",
            "REPORT_SENT",
        ),
        Index(
            "IX_ACTION_ACT_READY_ACT_REMINDER_ACT_DISABLED_ACT_NEWDATE",
            "ACT_READY",
            "ACT_REMINDER",
            "ACT_DISABLED",
            "ACT_NEWDATE",
        ),
        Index(
            "IX_ACTION_SO_NUMBER_ACTT_ID_ACT_DISABLED",
            "SO_NUMBER",
            "ACTT_ID",
            "ACT_DISABLED",
            "P_ID",
        ),
        Index(
            "IX_ACTION_ACT_READY_ACT_DISABLED_ST_ID",
            "ACT_READY",
            "ACT_DISABLED",
            "ST_ID",
        ),
        {"schema": "dbo"},
    )

    P_ID = Column(Integer, primary_key=True, nullable=False)
    SO_NUMBER = Column(Integer)
    ACT_NUMBER = Column(Integer, primary_key=True, nullable=False)
    ACT_DATE = Column(DateTime)
    ACT_NEWDATE = Column(DateTime)
    ST_ID = Column(Integer, index=True)
    ACTT_ID = Column(Integer)
    ACT_INFO = Column(Unicode(512))
    ACT_FILE = Column(Unicode(255))
    ACT_READY = Column(SMALLDATETIME, index=True)
    ACT_INTERNAL = Column(BIT, nullable=False)
    ACT_PREDATE = Column(DateTime)
    ACT_REMINDER = Column(BIT, nullable=False)
    ACT_PREDATEINFO = Column(Unicode(255))
    ACT_REGBY = Column(Integer)
    ACT_REGDATE = Column(DateTime)
    ACT_UPDATEBY = Column(Integer)
    ACT_UPDATE = Column(DateTime)
    ACT_DISABLED = Column(BIT, nullable=False)
    REPORT_SENT = Column(BIT, nullable=False)
    ACT_FORECASTRELEVANT = Column(BIT, nullable=False)
    ACT_SO_DEADLINECONNECTION = Column(BIT, nullable=False)
    REMINDER_START_DATE = Column(DateTime)
    REMINDER_END_DATE = Column(DateTime)
    REMINDER_FREQUENCY = Column(Integer)
    REMINDER_LAST_SENT = Column(DateTime)
    ACT_ID = Column(Integer, nullable=False, index=True)
    REMINDER_CREATOR_IN_CC = Column(BIT, nullable=False)


class ACTIONHISTORY(Base):
    __tablename__ = "ACTION_HISTORY"
    __table_args__ = (
        Index("IX_ACTION_HISTORY_P_ID_SO_NO", "P_ID", "SO_NUMBER"),
        {"schema": "dbo"},
    )

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    P_ID = Column(Integer)
    SO_NUMBER = Column(Integer)
    ACT_NUMBER = Column(Integer)
    ACT_DATE = Column(DateTime)
    ACT_NEWDATE = Column(DateTime)
    ST_ID = Column(Integer)
    ACTT_ID = Column(Integer)
    ACT_INFO = Column(Unicode(512))
    ACT_FILE = Column(Unicode(255))
    ACT_READY = Column(SMALLDATETIME)
    ACT_INTERNAL = Column(BIT)
    ACT_PREDATE = Column(DateTime)
    ACT_REMINDER = Column(BIT)
    ACT_PREDATEINFO = Column(Unicode(255))
    ACT_REGBY = Column(Integer)
    ACT_REGDATE = Column(DateTime)
    ACT_UPDATEBY = Column(Integer)
    ACT_UPDATE = Column(DateTime)
    ACT_DISABLED = Column(BIT)
    REPORT_SENT = Column(BIT)
    ACT_FORECASTRELEVANT = Column(BIT)
    ACT_SO_DEADLINECONNECTION = Column(BIT)
    REMINDER_START_DATE = Column(DateTime)
    REMINDER_END_DATE = Column(DateTime)
    REMINDER_FREQUENCY = Column(Integer)
    REMINDER_LAST_SENT = Column(DateTime)
    ACT_ID = Column(Integer)
    REMINDER_CREATOR_IN_CC = Column(BIT)


class ACTIONTYPEHISTORY(Base):
    __tablename__ = "ACTION_TYPE_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ACTT_ID = Column(Integer, index=True)
    ACTT_NAME_DE = Column(Unicode(256))
    ACTT_NAME_EN = Column(Unicode(256))
    ACTT_NAME_FR = Column(Unicode(256))
    CREATED = Column(DateTime)
    CREATED_BY = Column(Integer)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)
    ACTT_LEVEL = Column(Integer)


class ANONYMIZATIONLOG(Base):
    __tablename__ = "ANONYMIZATION_LOG"
    __table_args__ = {"schema": "dbo"}

    AL_ID = Column(Integer, primary_key=True)
    AL_DATE = Column(DateTime, nullable=False)
    AL_COUNT_ACCOUNTING = Column(Integer, nullable=False)
    AL_COUNT_CHANCES = Column(Integer, nullable=False)
    AL_COUNT_PROCESS = Column(Integer, nullable=False)
    AL_COUNT_PROCESSFOLDER = Column(Integer, nullable=False)
    AL_COUNT_PROJECT = Column(Integer, nullable=False)
    AL_COUNT_PROKALKMODUL = Column(Integer, nullable=False)
    AL_COUNT_SUBORDERS = Column(Integer, nullable=False)
    AL_COUNT_TESTSAMPLE = Column(Integer, nullable=False)
    AL_ERROR_ACCOUNTING = Column(Integer, nullable=False)
    AL_ERROR_CHANCES = Column(Integer, nullable=False)
    AL_ERROR_PROCESS = Column(Integer, nullable=False)
    AL_ERROR_PROCESSFOLDER = Column(Integer, nullable=False)
    AL_ERROR_PROJECT = Column(Integer, nullable=False)
    AL_ERROR_PROKALKMODUL = Column(Integer, nullable=False)
    AL_ERROR_SUBORDERS = Column(Integer, nullable=False)
    AL_ERROR_TESTSAMPLE = Column(Integer, nullable=False)


class ARCHIVINGLOG(Base):
    __tablename__ = "ARCHIVING_LOG"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    TYPE = Column(Unicode(32), nullable=False)
    TIMESTAMP = Column(DateTime, nullable=False)
    MESSAGE = Column(Unicode, nullable=False)


class ARCHIVINGRUN(Base):
    __tablename__ = "ARCHIVING_RUN"
    __table_args__ = (
        Index("IX_ARCHIVING_RUN_PC_ID", "PC_ID", "STATUS"),
        Index("IX_ARCHIVING_RUN_P_ID_STATUS", "P_ID", "STATUS"),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    P_ID = Column(Integer)
    PC_ID = Column(Integer)
    SOURCE_FILE = Column(Unicode(1024), nullable=False)
    TARGET_FILE = Column(Unicode(1024), nullable=False)
    STATUS = Column(Unicode(32), nullable=False)
    TIMESTAMP = Column(DateTime, nullable=False)


class CALENDARENTRYHISTORY(Base):
    __tablename__ = "CALENDAR_ENTRY_HISTORY"
    __table_args__ = (
        Index("IX_CALENDAR_ENTRY_HISTORY_P_ID_SO_NO", "P_ID", "SO_NUMBER"),
        {"schema": "dbo"},
    )

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ID = Column(Integer)
    P_ID = Column(Integer)
    SO_NUMBER = Column(Integer)
    ST_ID = Column(Integer)
    SUBJECT = Column(Unicode(255))
    DESCRIPTION = Column(Unicode(4000))
    START_TIME = Column(DateTime)
    END_TIME = Column(DateTime)
    ALL_DAY_EVENT = Column(BIT)
    DISABLED = Column(BIT)
    CREATED = Column(DateTime)
    CREATED_BY = Column(Integer)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)
    TRANSFER_STATUS = Column(Integer)


class CERTIFICATECLIENTHISTORY(Base):
    __tablename__ = "CERTIFICATE_CLIENT_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ID = Column(Integer, index=True)
    CERTIFICATE_ID = Column(Integer)
    TYPE = Column(Integer)
    CU_ID = Column(Integer)
    CBW_NUMBER = Column(Integer)
    NAME1 = Column(Unicode(40))
    NAME2 = Column(Unicode(40))
    NAME3 = Column(Unicode(40))
    NAME4 = Column(Unicode(40))
    STREET = Column(Unicode(60))
    STREET_NUMBER = Column(Unicode(10))
    STREET_ADDITION = Column(Unicode(10))
    ADDITIONAL_STREET1 = Column(Unicode(40))
    ADDITIONAL_STREET2 = Column(Unicode(40))
    ADDITIONAL_STREET3 = Column(Unicode(40))
    ADDITIONAL_STREET4 = Column(Unicode(40))
    DISTRICT = Column(Unicode(40))
    ZIP_CITY = Column(Unicode(10))
    CITY = Column(Unicode(40))
    COUNTRY_CODE = Column(Unicode(3))
    ZIP_COMPANY = Column(Unicode(10))
    SAP_NUMBER = Column(Unicode(10))
    DEPARTMENT_NOTIFY = Column(Unicode(8))
    DEPARTMENT_RESPONSIBLE = Column(Unicode(8))
    KEY_ACCOUNT_MANAGER = Column(Unicode(94))
    NUMBER_OF_EMPLOYEES = Column(Integer)
    PHONE = Column(Unicode(48))
    FAX = Column(Unicode(48))
    SALES_TAX_NUMBER = Column(Unicode(64))
    EMAIL = Column(Unicode(60))
    INFORMATION = Column(Unicode(2000))
    COMPLETE_ADDRESS = Column(Unicode(2000))
    CREATED = Column(DateTime)
    CREATED_BY = Column(Integer)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)
    SORT = Column(Integer)


class CERTIFICATEHISTORY(Base):
    __tablename__ = "CERTIFICATE_HISTORY"
    __table_args__ = (
        Index("IX_CERTIFICATE_HISTORY_P_ID_SO_NUMBER", "P_ID", "SO_NUMBER"),
        {"schema": "dbo"},
    )

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ID = Column(Integer)
    P_ID = Column(Integer)
    SO_NUMBER = Column(Integer)
    NUMBER = Column(Unicode(30))
    MAIN_CERTIFICATE = Column(BIT)
    TYPES = Column(Unicode(256))
    HOLDER_CONTACT = Column(Unicode(128))
    UNIT_FEES = Column(Integer)
    TECHNICAL_CERTIFIER = Column(Unicode(60))
    TESTING_BASE = Column(Unicode(2000))
    PRODUCT = Column(Unicode(4000))
    PRODUCT_ADDITIONAL = Column(Unicode(120))
    MODELS = Column(Unicode(4000))
    RESPONSIBLE_DEPARTMENT = Column(Unicode(20))
    ISSUING_DEPARTMENT = Column(Unicode(50))
    ISSUE_DATE = Column(DateTime)
    EXPIRATION_DATE = Column(DateTime)
    STATUS = Column(Unicode(30))
    LAST_IMPORT_FROM_CBW = Column(DateTime)
    CREATED = Column(DateTime)
    CREATED_BY = Column(Integer)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)


class CHANCESHISTORY(Base):
    __tablename__ = "CHANCES_HISTORY"
    __table_args__ = (
        Index("IX_CHANCES_HISTORY_CH_ID_P_ID", "CH_ID", "P_ID"),
        {"schema": "dbo"},
    )

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    CH_ID = Column(Integer)
    P_ID = Column(Integer)
    CHT_ID = Column(Integer)
    CH_INFO = Column(Unicode(255))
    CH_DATE = Column(DateTime)
    CH_CHECKDATE = Column(DateTime)
    CH_CHECKBY = Column(Integer)
    CH_CHECKCOMMENT = Column(Unicode(255))
    CH_DISABLED = Column(BIT)
    CH_CHECKBY_TEAM = Column(Integer)
    AL_ID = Column(Integer)


class CODESEGMENTTYPE(Base):
    __tablename__ = "CODESEGMENT_TYPE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_EN = Column(Unicode(256), nullable=False)
    DISABLED = Column(Date)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)


class COLOR(Base):
    __tablename__ = "COLOR"
    __table_args__ = {"schema": "dbo"}

    COL_ID = Column(Integer, primary_key=True)
    COL_R = Column(Integer, nullable=False)
    COL_G = Column(Integer, nullable=False)
    COL_B = Column(Integer, nullable=False)
    COL_NAME = Column(Unicode(20), nullable=False)
    COL_HEX = Column(Unicode(6))
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime, nullable=False)


class CONNECTION(Base):
    __tablename__ = "CONNECTION"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    CONNECTION_STRING = Column(Unicode(512), nullable=False)
    CONNECTION_STRING_ENCRYPTED = Column(Unicode(512), nullable=False)


class CRMLOGDATUM(Base):
    __tablename__ = "CRM_LOG_DATA"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    OPERATION = Column(Integer, nullable=False)
    P_ID = Column(Integer)
    CRM_ID = Column(Unicode(10))
    CUSTOMER_NUMBER = Column(Unicode(10))
    CUSTOMER_CPD_NAME = Column(Unicode(40))
    CUSTOMER_CPD_COUNTRY_CODE = Column(Unicode(3))
    CUSTOMER_CPD_CITY = Column(Unicode(40))
    CUSTOMER_CONTACT_NAME = Column(Unicode(255))
    CUSTOMER_CONTACT_NUMBER = Column(Unicode(10))
    OFFICER_IN_CHARGE = Column(Unicode(8))
    DESCRIPTION = Column(Unicode(2048))
    VALID_UNTIL = Column(DateTime)
    START_DATE = Column(DateTime)
    END_DATE = Column(DateTime)
    PROFIT_CENTER = Column(Unicode(9))
    CURRENCY = Column(Unicode(3))
    DOCUMENT_LIBRARY_URL = Column(Unicode(2048))
    CREATED = Column(DateTime, nullable=False)
    TRANSFERRED_BY = Column(Unicode(128))
    RETURN_VALUE = Column(Integer)
    ORDER_REFERENCE = Column(Unicode(60))
    COORDINATOR = Column(Unicode(8))
    SALES_REPRESENTATIVE = Column(Unicode(8))
    SIGNATURE_LEFT = Column(Unicode(8))
    SIGNATURE_RIGHT = Column(Unicode(8))
    GLOBAL_PARTNER_NUMBER = Column(Unicode(10))
    INVOICE_RECIPIENT_CONTACT_NUMBER = Column(Unicode(10))
    OBJECT_OF_ORDER = Column(Unicode(2048))
    ADDITIONAL_ORDER_TEXT = Column(Unicode(2048))
    PRODUCT = Column(Unicode(255))
    MODEL = Column(Unicode(255))
    INTERNAL_PROJECT_INFO = Column(Unicode(4000))
    PROJECT_MANAGER = Column(Unicode(8))
    INVOICE_RECIPIENT_NUMBER = Column(Unicode(10))
    REGULATOR_NUMBER = Column(Unicode(10))
    GOODS_RECIPIENT_NUMBER = Column(Unicode(10))
    OPPORTUNITY_ID = Column(Unicode(10))


class CUSTOMERNATION(Base):
    __tablename__ = "CUSTOMER_NATION"
    __table_args__ = {"schema": "dbo"}

    CN_ID = Column(Integer, primary_key=True)
    CN_NATION = Column(NCHAR(1), nullable=False)
    CN_DISPLAY_EN = Column(Unicode(120))
    CN_DISPLAY_DE = Column(Unicode(120))
    CN_DISPLAY_FR = Column(Unicode(120))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)


class DISPO(Base):
    __tablename__ = "DISPO"
    __table_args__ = (
        Index(
            "IX_DISPO_WOC_IAN_DISABLED_PROCESS",
            "PROCESS",
            "IAN",
            "DISABLED",
            "WOC",
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    PROCESS = Column(Integer)
    ORDERING_PARTY = Column(Integer, nullable=False)
    MANUFACTURER = Column(Integer)
    IAN = Column(Unicode(256))
    BATCH_NUMBER = Column(Unicode(16))
    WEEK = Column(Integer)
    YEAR = Column(Integer)
    SHOPDATE = Column(DateTime)
    PRODUCT = Column(Unicode(255))
    MODEL = Column(Unicode(255))
    KEY2 = Column(Unicode(16))
    KEY3 = Column(Unicode(16))
    CATEGORY = Column(Integer)
    LIDL_QA_MEMBER = Column(Integer)
    CUSTOMERCONTACT = Column(Integer)
    LOTSIZE = Column(Integer)
    DISABLED = Column(DateTime)
    FILE_NAME = Column(Unicode(256), nullable=False)
    FILE_CONTENT = Column(LargeBinary)
    READY_TO_SHOP = Column(Integer)
    PROCESSDESIGNATION = Column(Unicode(255))
    WOC = Column(UNIQUEIDENTIFIER, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)
    ORDERDATE = Column(DateTime)


class DISPOCUSTOMEREVALUATORRULE(Base):
    __tablename__ = "DISPO_CUSTOMEREVALUATOR_RULE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    TEST_TYPE = Column(Unicode(100), nullable=False)
    RULE = Column(Unicode(4000), nullable=False)
    OPTIONS = Column(Unicode(4000))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)
    DISABLED = Column(DateTime)


class DISPOHISTORY(Base):
    __tablename__ = "DISPO_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ID = Column(Integer)
    PROCESS = Column(Integer)
    ORDERING_PARTY = Column(Integer)
    MANUFACTURER = Column(Integer)
    IAN = Column(Unicode(256))
    BATCH_NUMBER = Column(Unicode(16))
    WEEK = Column(Integer)
    YEAR = Column(Integer)
    SHOPDATE = Column(DateTime)
    PRODUCT = Column(Unicode(255))
    MODEL = Column(Unicode(255))
    KEY2 = Column(Unicode(16))
    KEY3 = Column(Unicode(16))
    CATEGORY = Column(Integer)
    LIDL_QA_MEMBER = Column(Integer)
    CUSTOMERCONTACT = Column(Integer)
    LOTSIZE = Column(Integer)
    DISABLED = Column(DateTime)
    FILE_NAME = Column(Unicode(256))
    FILE_CONTENT = Column(LargeBinary)
    READY_TO_SHOP = Column(Integer)
    PROCESSDESIGNATION = Column(Unicode(255))
    WOC = Column(UNIQUEIDENTIFIER)
    CREATED = Column(DateTime)
    CREATED_BY = Column(Integer)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)
    ORDERDATE = Column(DateTime)


class DISPOKNOWNCUSTOMER(Base):
    __tablename__ = "DISPO_KNOWN_CUSTOMERS"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME = Column(Unicode(200), nullable=False)
    SAP_NUMBER = Column(Unicode(50), nullable=False)
    READY_DATE_OFFSET = Column(Integer, nullable=False)
    HAS_QM = Column(BIT, nullable=False)
    WOC = Column(UNIQUEIDENTIFIER, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)
    DISABLED = Column(DateTime)


class FAILUREMD(Base):
    __tablename__ = "FAILURE_MD"
    __table_args__ = {"schema": "dbo"}

    FAIL_ID = Column(Integer, primary_key=True)
    MD_ID = Column(Integer, nullable=False)
    FAIL_KEY = Column(Unicode(16), nullable=False)
    FAIL_TEXT_EN = Column(Unicode(150))
    FAIL_TEXT_DE = Column(Unicode(150))
    FAIL_TEXT_FR = Column(Unicode(150))
    FAIL_EXAMPLE_EN = Column(Unicode(500))
    FAIL_EXAMPLE_DE = Column(Unicode(500))
    FAIL_EXAMPLE_FR = Column(Unicode(500))
    Created = Column(DateTime, nullable=False)
    CreatedBy = Column(Integer)
    Updated = Column(DateTime)
    UpdatedBy = Column(Integer)


class FAZHISTORY(Base):
    __tablename__ = "FAZ_HISTORY"
    __table_args__ = (
        Index("IX_FAZ_HISTORY_FAZ_ID_P_ID", "FAZ_ID", "P_ID", "SO_NUMBER"),
        {"schema": "dbo"},
    )

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    FAZ_ID = Column(Integer)
    P_ID = Column(Integer)
    SO_NUMBER = Column(Integer)
    FAZ_CERTNUMBER = Column(Unicode(30))
    FAZ_REMARK = Column(Unicode(255))
    FAZ_CLEAR = Column(Unicode(255))
    FAZ_DATE = Column(DateTime)
    FAZ_BY = Column(Unicode(30))
    FAZ_DISABLED = Column(BIT)
    ZETY_TYP = Column(Unicode(100))
    FAZ_PSOBJECT_TERM = Column(Unicode(50))
    FAZ_CERT_OWNER = Column(Integer)
    TS_ID = Column(Integer)
    FAZ_POSTING_STATUS = Column(Unicode(50))
    RM_ID = Column(Integer)


class FOCUSDOCUMENTHISTORY(Base):
    __tablename__ = "FOCUSDOCUMENT_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ID = Column(Integer)
    PROJECT = Column(Integer)
    SUBORDER = Column(Integer)
    PATH = Column(Unicode(1024))
    NAME = Column(Unicode(1024))
    FOCUS = Column(BIT)
    CREATED = Column(DateTime)
    CREATED_BY = Column(Integer)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)
    DISABLED = Column(DateTime)


class FOLDERRIGHTSMANAGEMENTTASKDATUM(Base):
    __tablename__ = "FOLDERRIGHTSMANAGEMENT_TASK_DATA"
    __table_args__ = (
        Index(
            "IX_FOLDERRIGHTSMANAGEMENT_TASK_DATA_PROJECT_TASK",
            "RIGHTSMANAGEMENTTASK",
            "PROJECT",
        ),
        {"schema": "dbo"},
    )

    ID = Column(BigInteger, primary_key=True)
    RIGHTSMANAGEMENTTASK = Column(BigInteger, nullable=False)
    PROJECT = Column(Integer, nullable=False)
    ORIGINALFOLDER = Column(Unicode(255))


class GMAENTRYHISTORY(Base):
    __tablename__ = "GMA_ENTRY_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DATETIME2, nullable=False)
    ID = Column(Integer)
    P_ID = Column(Integer)
    SO_NUMBER = Column(Integer)
    COUNTRY_ID = Column(Integer)
    STATUS_ID = Column(Integer)
    RESULT_ID = Column(Integer)
    COMMENT = Column(Unicode(256))
    STATUS_DATE = Column(Date)
    DISABLED = Column(BIT)
    CREATED = Column(DATETIME2)
    CREATED_BY = Column(Integer)
    UPDATED = Column(DATETIME2)
    UPDATED_BY = Column(Integer)


class HIERARCHY(Base):
    __tablename__ = "HIERARCHY"
    __table_args__ = (
        Index(
            "IX_HIERARCHY_HR_ACTIVE_HR_PARENT",
            "HR_ACTIVE",
            "HR_PARENT",
            "HR_ID",
        ),
        Index(
            "IX_HIERARCHY_HR_TYPE",
            "HR_TYPE",
            "HR_ID",
            "HR_LOCATION",
            "HR_ACTIVE",
            "HR_PARENT",
            "HR_NEW_ID",
            "IS_PLACEHOLDER",
            "ST_ID",
            "CC_ID",
            "CREATED",
            "CREATED_BY",
            "HR_LAST_UPDATED",
            "UPDATED_BY",
        ),
        Index(
            "IX_HIERARCHY_HR_ACTIVE_HR_TYPE",
            "HR_ACTIVE",
            "HR_TYPE",
            "HR_ID",
            "HR_LOCATION",
            "HR_NEW_ID",
        ),
        {"schema": "dbo"},
    )

    HR_ID = Column(UNIQUEIDENTIFIER, primary_key=True)
    HR_LOCATION = Column(Unicode(40))
    HR_SHORT = Column(Unicode(20))
    HR_PREFIX = Column(Unicode(20))
    HR_ACTIVE = Column(BIT, nullable=False)
    HR_TYPE = Column(Unicode(50))
    HR_CURRENT = Column(BIT)
    HR_PARENT = Column(UNIQUEIDENTIFIER)
    HR_UPDATE_TYPE = Column(TINYINT)
    HR_NEW_ID = Column(Integer, nullable=False, unique=True)
    HR_LEVEL = Column(Integer, nullable=False)
    HR_EMAIL = Column(Unicode(80))
    ST_ID = Column(ForeignKey("dbo.STAFF.ST_ID"))
    CC_ID = Column(ForeignKey("dbo.KST.CC_ID"))
    POSTING_TARGET = Column(Unicode(4))
    COSTING_DATA_ORDER_SIZE = Column(DECIMAL(19, 4))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    HR_LAST_UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    IS_PLACEHOLDER = Column(BIT, nullable=False)

    KST = relationship("KST")
    STAFF = relationship(
        "STAFF", primaryjoin="HIERARCHY.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="HIERARCHY.ST_ID == STAFF.ST_ID"
    )
    STAFF2 = relationship(
        "STAFF", primaryjoin="HIERARCHY.UPDATED_BY == STAFF.ST_ID"
    )


t_ID_PACKETS = Table(
    "ID_PACKETS",
    metadata,
    Column("FIRST_ID", BigInteger, nullable=False),
    Column("LAST_ID", BigInteger, nullable=False),
    schema="dbo",
)


class INDUSTRY(Base):
    __tablename__ = "INDUSTRY"
    __table_args__ = {"schema": "dbo"}

    IN_ID = Column(Integer, primary_key=True)
    IN_KEY = Column(NCHAR(2), nullable=False)
    IN_DISPLAY_EN = Column(Unicode(120))
    IN_DISPLAY_DE = Column(Unicode(120))
    IN_DISPLAY_FR = Column(Unicode(120))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)


class KALKMODULBEARBEITER(Base):
    __tablename__ = "KALKMODULBEARBEITER"
    __table_args__ = {"schema": "dbo"}

    KALM_ID = Column(Integer, primary_key=True, nullable=False)
    WC_ID = Column(UNIQUEIDENTIFIER, primary_key=True, nullable=False)
    KAL_ID = Column(Integer)
    ST_ID = Column(Integer)


class KEYWORDTYPE(Base):
    __tablename__ = "KEYWORD_TYPE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME = Column(Unicode(100), nullable=False, unique=True)
    DESCRIPTION = Column(Unicode(1000), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)
    DISABLED = Column(BIT, nullable=False)


class KST(Base):
    __tablename__ = "KST"
    __table_args__ = {"schema": "dbo"}

    CC_ID = Column(Unicode(10), primary_key=True)
    CC_NAME = Column(Unicode(16))
    CC_BOOKINGAREA = Column(Unicode(4))
    CC_TYPE = Column(Integer)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    CC_GLOBAL_PARTNER_MANDATORY = Column(BIT, nullable=False)
    VALID_FROM = Column(DateTime)
    VALID_UNTIL = Column(DateTime)
    RUN_ID = Column(Integer)
    KTEXT = Column(Unicode(256))
    LTEXT = Column(Unicode(256))

    STAFF = relationship("STAFF", primaryjoin="KST.CREATED_BY == STAFF.ST_ID")
    STAFF1 = relationship("STAFF", primaryjoin="KST.UPDATED_BY == STAFF.ST_ID")


class LANGUAGETYPE(Base):
    __tablename__ = "LANGUAGE_TYPE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_EN = Column(Unicode(256), nullable=False, unique=True)
    DISABLED = Column(Date)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)
    TWODIGITISO = Column(NCHAR(2), nullable=False)


t_LIDL_CUSTOMERS = Table(
    "LIDL_CUSTOMERS",
    metadata,
    Column("ID", Integer, nullable=False),
    schema="dbo",
)


class LIMSTESTMETHOD(Base):
    __tablename__ = "LIMS_TEST_METHOD"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    TEST_METHOD_NAME = Column(Unicode(128), nullable=False)
    PARAMETER = Column(Unicode(128), nullable=False)
    UNIT = Column(Unicode(32))
    METHOD = Column(Unicode(256))
    REFERENCE_SUBSTANCE = Column(Unicode(64))
    STANDARD = Column(Unicode(64))
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)


class LOCATIONBASEPERMISSION(Base):
    __tablename__ = "LOCATION_BASE_PERMISSION"
    __table_args__ = (
        Index(
            "UK_LOCATION_BASE_PERMISSION",
            "SERVER_PATH",
            "PATH_TYPE",
            "SID",
            unique=True,
        ),
        {"schema": "dbo"},
    )

    ID = Column(BigInteger, primary_key=True)
    SERVER_PATH = Column(Unicode(255), nullable=False)
    PATH_TYPE = Column(Integer, nullable=False)
    SID = Column(Unicode(200), nullable=False)
    PERMISSIONS = Column(Integer, nullable=False)
    INHERITANCE = Column(Integer, nullable=False)
    PROPAGATION = Column(Integer, nullable=False)
    NAME = Column(Unicode(300), nullable=False)
    DESCRIPTION = Column(Unicode(3000))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)


class MANDATOR(Base):
    __tablename__ = "MANDATOR"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    Name = Column(Unicode(100), nullable=False)


class MHSPROJECTDATACODEHISTORY(Base):
    __tablename__ = "MHS_PROJECTDATA_CODE_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ID = Column(Integer, index=True)
    MHSPROJECTDATA = Column(Integer)
    CODE = Column(Integer)


class MHSPROJECTDATAHISTORY(Base):
    __tablename__ = "MHS_PROJECTDATA_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ID = Column(Integer)
    PROJECT = Column(Integer)
    JUSTIFICATION = Column(Unicode)
    DEVICE = Column(Integer)
    CREATED = Column(DateTime)
    CREATED_BY = Column(Integer)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)


class PORTALSOURCEFILE(Base):
    __tablename__ = "PORTAL_SOURCE_FILE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    PC_ID = Column(Integer)
    P_ID = Column(Integer)
    FULL_PATH = Column(Unicode(2056), nullable=False)


class PORTALUSERRESPONSE(Base):
    __tablename__ = "PORTAL_USER_RESPONSE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    ACCOUNT_NAME = Column(Unicode(256), nullable=False)
    TERMS_ACCEPTED = Column(DateTime)


class PRINTOPTIONTYPE(Base):
    __tablename__ = "PRINT_OPTION_TYPE"
    __table_args__ = {"schema": "dbo"}

    KEY = Column(Unicode(3), primary_key=True)
    NAME_DE = Column(Unicode(100), nullable=False)
    NAME_EN = Column(Unicode(100), nullable=False)
    DISABLED = Column(DATETIME2)
    CREATED = Column(DATETIME2, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DATETIME2, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)


class PROCESSFOLDERHISTORY(Base):
    __tablename__ = "PROCESSFOLDER_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    PCF_ID = Column(Integer, index=True)
    PZ_ID = Column(Integer)
    TPT_ID = Column(Integer)
    PCF_VERSION = Column(Integer)
    PCF_CURRENTVERSION = Column(BIT)
    PCF_FILENAME = Column(Unicode(255))
    PCF_COMMENT = Column(Unicode(255))
    PCF_REGDATE = Column(DateTime)
    PCF_REGBY = Column(Integer)
    PCF_UPDATE = Column(DateTime)
    PCF_UPDATEBY = Column(Integer)
    PCF_CHECKOUTBY = Column(Integer)
    PCF_CHECKOUT = Column(DateTime)
    PCF_WEBNAME = Column(Unicode(255))
    PCF_CHECKOUTBY_TEAM = Column(Integer)
    PCF_REGBY_TEAM = Column(Integer)
    PCF_UPDATEBY_TEAM = Column(Integer)
    AL_ID = Column(Integer)


class PROCESSPORTALFILE(Base):
    __tablename__ = "PROCESSPORTAL_FILES"
    __table_args__ = {"schema": "dbo"}

    PZPF = Column(Integer, primary_key=True)
    PZPI_ID = Column(Integer, nullable=False, index=True)
    PZ_ID = Column(Integer)
    P_ID = Column(Integer)
    PZPF_PATH = Column(Unicode(255))
    PZPF_EXIST = Column(BIT, nullable=False)
    PZPF_EXTERNAL_ID = Column(Integer)
    PZPF_FILE_SIZE = Column(Integer)


class PROCESSPORTALFILESHISTORY(Base):
    __tablename__ = "PROCESSPORTAL_FILES_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    PZPF = Column(Integer, index=True)
    PZPI_ID = Column(Integer)
    PZ_ID = Column(Integer)
    P_ID = Column(Integer)
    PZPF_PATH = Column(Unicode(255))
    PZPF_EXIST = Column(BIT)
    PZPF_EXTERNAL_ID = Column(Integer)
    PZPF_FILE_SIZE = Column(Integer)


class PROCESSPORTALIN(Base):
    __tablename__ = "PROCESSPORTAL_IN"
    __table_args__ = (
        Index("IX_PROCESSPORTAL_IN_PZ_ID_P_ID", "P_ID", "PZPI_PROCESSED_BY"),
        {"schema": "dbo"},
    )

    PZPI_ID = Column(Integer, primary_key=True)
    PZ_ID = Column(Integer)
    P_ID = Column(Integer)
    PZPI_NAME = Column(Unicode(60))
    PZPI_COMPANY = Column(Unicode(90))
    PZPI_CUST_TEXT = Column(Unicode(1000))
    PZPI_REGDATE = Column(DateTime, nullable=False)
    PZPI_COMMENT = Column(Unicode(255))
    PZPI_PROCESSED_BY = Column(Integer)
    PZPI_PROCESSED_DATE = Column(DateTime)
    SEND_NOTIFICATION = Column(BIT, nullable=False)
    NOTIFICATION_SENT = Column(DateTime)


class PROCESSPORTALINHISTORY(Base):
    __tablename__ = "PROCESSPORTAL_IN_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    PZPI_ID = Column(Integer, index=True)
    PZ_ID = Column(Integer)
    P_ID = Column(Integer)
    PZPI_NAME = Column(Unicode(60))
    PZPI_COMPANY = Column(Unicode(90))
    PZPI_CUST_TEXT = Column(Unicode(1000))
    PZPI_REGDATE = Column(DateTime)
    PZPI_COMMENT = Column(Unicode(255))
    PZPI_PROCESSED_BY = Column(Integer)
    PZPI_PROCESSED_DATE = Column(DateTime)
    SEND_NOTIFICATION = Column(BIT)
    NOTIFICATION_SENT = Column(DateTime)


class PROCESSFILE(Base):
    __tablename__ = "PROCESS_FILES"
    __table_args__ = {"schema": "dbo"}

    PCF_ID = Column(BigInteger, primary_key=True)
    PC_ID = Column(Integer)
    P_ID = Column(Integer)
    PCF_FOLDER = Column(Unicode(255))
    PCF_DATE = Column(DateTime)
    PRP_ID = Column(Integer)
    PCF_FILE = Column(Unicode(255))
    PCF_PATH = Column(Unicode(255))
    PCF_LAST_TRANSFER = Column(DateTime)
    PCF_SOURCE = Column(Unicode(2056))


class PROCESSFILESHISTORY(Base):
    __tablename__ = "PROCESS_FILES_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    PCF_ID = Column(BigInteger, index=True)
    PC_ID = Column(Integer)
    P_ID = Column(Integer)
    PCF_FOLDER = Column(Unicode(255))
    PCF_DATE = Column(DateTime)
    PRP_ID = Column(Integer)
    PCF_FILE = Column(Unicode(255))
    PCF_PATH = Column(Unicode(255))
    PCF_LAST_TRANSFER = Column(DateTime)
    PCF_SOURCE = Column(Unicode(2056))


class PROCESSHISTORY(Base):
    __tablename__ = "PROCESS_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    PC_ID = Column(Integer, index=True)
    PC_WC_ID = Column(UNIQUEIDENTIFIER)
    PC_CLIENT = Column(Integer)
    PC_PRODUCT = Column(Unicode(255))
    PC_MODEL = Column(Unicode(255))
    PC_NAME = Column(Unicode(255))
    PC_ORDERTEXT = Column(Unicode(255))
    PC_PROJECTMANAGER = Column(Integer)
    PC_LOTSIZE = Column(Integer)
    PC_STATUS = Column(Integer)
    PC_READY_TO_SHOP = Column(Integer)
    PC_SHOPDATE = Column(DateTime)
    PC_PATH = Column(Unicode(50))
    PC_FILE_MEASUREMENT = Column(Unicode(255))
    PC_FILE_DOCS = Column(Unicode(255))
    PC_REGDATE = Column(DateTime)
    PC_CREATEDBY = Column(Integer)
    PC_UPDATE = Column(DateTime)
    PC_UPDATEBY = Column(Integer)
    PC_DISABLED = Column(BIT)
    PC_VISIBLE_FOR = Column(Integer)
    PC_CREATEDBY_TEAM = Column(Integer)
    PC_UPDATEBY_TEAM = Column(Integer)
    AL_ID = Column(Integer)
    PC_REPEATER_OF = Column(Integer)
    PC_CERT_TYPE = Column(Unicode(255))
    PC_IAN = Column(Unicode(256))
    PC_LIDL_QA_MEMBER = Column(Unicode(256))
    PROTOCOL_PROJECT = Column(Integer)
    PC_KEY2 = Column(Unicode(16))
    PC_KEY3 = Column(Unicode(16))
    FILE_FORMAT = Column(Integer)
    ARCHIVING_STATUS = Column(Unicode(32))
    PC_PROJECTMANAGER_TEAM = Column(Integer)
    IS_FST_PROCESS = Column(BIT)
    FACILITY_NUMBER = Column(Integer)
    NACE_CODE = Column(Unicode(256))
    COLLECTIVE_INVOICE_SENT = Column(DateTime)
    BATCH_NUMBER = Column(Unicode(16))
    DISCOUNT_PERCENTAGE = Column(DECIMAL(19, 10))


class PROJECTADDONHISTORY(Base):
    __tablename__ = "PROJECT_ADDON_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    PA_ID = Column(Integer)
    P_ID = Column(Integer, index=True)
    PA_DISPATCHER = Column(Integer)
    OC_ID = Column(Integer)
    PA_PART_NUMBER = Column(Unicode(255))
    PA_RFN = Column(Unicode(255))
    PA_MANUFACTURER_NUMBER = Column(Unicode(255))
    PA_DRAFT_NUMBER = Column(Unicode(255))
    RRTB_ID = Column(Integer)
    PCAT_ID = Column(Integer)
    PMOD_ID = Column(Integer)
    PA_MAIN_DIMENSIONS = Column(Unicode(255))
    CERT_APPL_ID = Column(Integer)
    PA_OPERATORS_IDENTIFICATION = Column(Unicode(255))
    PA_BUILDING = Column(Unicode(255))


class PROJECTADDONROOMSPECIFICDATAHISTORY(Base):
    __tablename__ = "PROJECT_ADDON_ROOMSPECIFICDATA_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    PAR_ID = Column(Integer)
    P_ID = Column(Integer, index=True)
    PAR_COLUMN = Column(Integer)
    RD_ID = Column(Integer)
    PAR_PRESSURE = Column(Unicode(50))
    PU_ID = Column(Integer)
    PAR_TEMPERATURE = Column(Unicode(50))
    PAR_VOLUME = Column(Unicode(50))
    PAR_VOLUME_UNIT = Column(Unicode(50))
    PAR_MEDIUM = Column(Unicode(50))
    SOA_ID = Column(Integer)
    PAR_SUBSTANCE1 = Column(Unicode(50))
    PAR_SUBSTANCE2 = Column(Unicode(50))
    PAR_CATEGORY_ID = Column(Integer)
    PAR_FLUIDGROUP_ID = Column(Integer)


class PROJECTAPPLICATIONFORMHISTORY(Base):
    __tablename__ = "PROJECT_APPLICATION_FORM_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DATETIME2, nullable=False)
    ID = Column(Integer)
    P_ID = Column(Integer)
    APPLICATION_FORM = Column(Integer)
    DISABLED = Column(BIT)
    CREATED = Column(DATETIME2)
    CREATED_BY = Column(Integer)
    UPDATED = Column(DATETIME2)
    UPDATED_BY = Column(Integer)


class PROJECTCONTACT(Base):
    __tablename__ = "PROJECT_CONTACT"
    __table_args__ = (
        Index(
            "IX_PROJECT_CONTACT_PRC_P_ID_PRC_SO_NUMBER",
            "PRC_P_ID",
            "PRC_SO_NUMBER",
        ),
        {"schema": "dbo"},
    )

    PRC_ID = Column(Integer, primary_key=True)
    PRC_P_ID = Column(Integer, nullable=False, index=True)
    PRC_TYPE = Column(NCHAR(1), nullable=False)
    PRC_CU_ID = Column(Integer, nullable=False)
    PRC_CUC_ID = Column(Integer, nullable=False)
    PRC_ORDER_ID = Column(Integer, nullable=False)
    PRC_LAST_UPDATED = Column(DateTime)
    PRC_SO_NUMBER = Column(Integer)


class PROJECTCONTACTHISTORY(Base):
    __tablename__ = "PROJECT_CONTACT_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    PRC_ID = Column(Integer)
    PRC_P_ID = Column(Integer, index=True)
    PRC_TYPE = Column(NCHAR(1))
    PRC_CU_ID = Column(Integer)
    PRC_CUC_ID = Column(Integer)
    PRC_ORDER_ID = Column(Integer)
    PRC_LAST_UPDATED = Column(DateTime)
    PRC_SO_NUMBER = Column(Integer)


class PROJECTFAILURERELHISTORY(Base):
    __tablename__ = "PROJECT_FAILURE_REL_HISTORY"
    __table_args__ = (
        Index(
            "IX_PROJECT_FAILURE_REL_HISTORY_P_ID_SO_NO", "P_ID", "SO_NUMBER"
        ),
        {"schema": "dbo"},
    )

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ID = Column(Integer)
    P_ID = Column(Integer)
    SO_NUMBER = Column(Integer)
    FAIL_ID = Column(Integer)


class PROJECTHISTORY(Base):
    __tablename__ = "PROJECT_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    P_ID = Column(Integer, index=True)
    MD_ID = Column(Integer)
    PC_ID = Column(Integer)
    P_ZARA_NUMBER = Column(Unicode(10))
    P_NAME_IS_ZARA = Column(BIT)
    P_NAME = Column(Unicode(100))
    P_FOLDER = Column(Unicode(255))
    P_CUSTOMER_A = Column(Integer)
    P_CUSTOMER_B = Column(Integer)
    P_CUSTOMER_O = Column(Integer)
    P_CUST_A_IS_PRODUCER = Column(BIT)
    P_CONTACT = Column(Unicode(255))
    P_PRODUCT = Column(Unicode(255))
    P_MODEL = Column(Unicode(255))
    P_PROJECTMANAGER = Column(Integer)
    P_HANDLEDBY = Column(Integer)
    P_STATUS = Column(Integer)
    P_RETEST = Column(Integer)
    P_RETEST_OF = Column(Integer)
    P_DATE_APPOINTMENT = Column(DateTime)
    P_FOCUSDOCUMENT = Column(Unicode(255))
    P_COMMENT = Column(Unicode(50))
    P_DATE_READY = Column(DateTime)
    P_READYBY = Column(Integer)
    P_DATE_CHECK = Column(DateTime)
    P_CHECKBY = Column(Integer)
    P_DATE_ORDER = Column(DateTime)
    P_DEADLINE = Column(DateTime)
    P_DATE_DISPO = Column(DateTime)
    P_DATE_DONE = Column(DateTime)
    P_DONEBY = Column(Integer)
    RES_ID = Column(Integer)
    P_DELAY = Column(DECIMAL(18, 0))
    DELR_ID = Column(Integer)
    P_ORDERTEXT = Column(Unicode(2048))
    P_PROJECTINFO = Column(Unicode(4000))
    P_TOKEN = Column(Unicode(60))
    P_KIND_OF_PRODUCER = Column(Integer)
    KOT_ID = Column(Integer)
    KOB_ID = Column(Integer)
    P_ACTION = Column(BIT)
    P_URGENT = Column(BIT)
    P_DOCTYPE = Column(Integer)
    P_ORDERSIZE = Column(DECIMAL(18, 2))
    P_INVOICE = Column(DECIMAL(18, 2))
    P_SALERATE = Column(DECIMAL(18, 2))
    P_USE_PLAN = Column(BIT)
    P_PLAN_SPENDS = Column(DECIMAL(18, 10))
    P_PLAN_EXTERNAL = Column(DECIMAL(18, 10))
    P_PLAN_SUBORDER = Column(DECIMAL(18, 10))
    P_PLAN_TRAVEL = Column(MONEY)
    P_PLAN_LICENCE = Column(DECIMAL(18, 10))
    P_FACTOR = Column(DECIMAL(18, 2))
    P_ACC_SALE = Column(DECIMAL(18, 10))
    P_ACC_LAB = Column(DECIMAL(18, 10))
    P_ACC_SAFETY = Column(DECIMAL(18, 10))
    P_ACC_SALERATE = Column(MONEY)
    P_ACC_SPENDS = Column(MONEY)
    P_ACC_EXTERNAL = Column(MONEY)
    P_ACC_SUBORDER = Column(MONEY)
    P_ACC_TRAVEL = Column(MONEY)
    P_ACC_LICENCE = Column(MONEY)
    P_ACC_INTERNAL = Column(MONEY)
    P_HOURLY_RATE = Column(DECIMAL(18, 10))
    P_FORECAST = Column(DECIMAL(18, 2))
    P_TO_WEB = Column(BIT)
    P_TO_CDS = Column(BIT)
    P_INTERN = Column(BIT)
    P_PREDATE = Column(DateTime)
    P_PREDATE_REMINDER = Column(BIT)
    P_PREDATEINFO = Column(Unicode(255))
    P_PROCESSPHASE = Column(Integer)
    P_REGBY = Column(Integer)
    P_REGDATE = Column(DateTime)
    P_UPDATEBY = Column(Integer)
    P_UPDATE = Column(DateTime)
    P_ORDER_ORIGIN = Column(Unicode(20))
    P_TRANSFERPROJECT = Column(Integer)
    P_TRANSFERSUBORDER = Column(Integer)
    P_EU_TS_ID = Column(Integer)
    P_TRANSFERUACONTACT = Column(Integer)
    P_TRANSFERUADEPARTMENT = Column(Integer)
    P_TRANSFERUA_REGION_ID = Column(Integer)
    P_TRANSFERUASTATUS = Column(NCHAR(1))
    P_TRANSFERUASOURCEPATH = Column(NCHAR(1))
    P_TRANSFERROOTSERVERID = Column(Integer)
    P_TRANSFERACTIONNUMBER = Column(Integer)
    P_DISABLED = Column(BIT)
    P_CURRENCYRATE = Column(DECIMAL(18, 0))
    P_WC_ID = Column(UNIQUEIDENTIFIER)
    P_CONTACTPERSON_REGIONID = Column(UNIQUEIDENTIFIER)
    P_ASSIGNEDPERSON_TEAMID = Column(UNIQUEIDENTIFIER)
    P_PSOBJECT_TERM = Column(Unicode(50))
    P_CUR_ID = Column(NCHAR(3))
    P_CUR_SHORT = Column(NCHAR(3))
    P_PSOBJECT_LANGUAGEID = Column(Integer)
    P_FOLDER_OLD = Column(NCHAR(1))
    P_PROJECTFOLDERCREATED = Column(BIT)
    P_IS_LEGACY = Column(BIT)
    P_CBW_EXPORT = Column(Unicode(6))
    P_ACC_MAINPOS = Column(Unicode(8))
    P_PRODGRP_ID = Column(Integer)
    P_PRODGRP2_ID = Column(Integer)
    P_PRODUCT2 = Column(Unicode(255))
    P_DOCU_DONE = Column(BIT)
    PLAN_ACTUAL_HOUR = Column(DECIMAL(18, 2))
    ACC_ACTUAL_HOUR = Column(DECIMAL(18, 2))
    ORDER_POSITION = Column(Unicode(6))
    P_CUSTOMER_R = Column(Integer)
    E_ID = Column(Integer)
    P_CHECKBY_TEAM = Column(Integer)
    P_DONEBY_TEAM = Column(Integer)
    P_HANDLEDBY_TEAM = Column(Integer)
    P_PROJECTMANAGER_TEAM = Column(Integer)
    P_READYBY_TEAM = Column(Integer)
    P_REGBY_TEAM = Column(Integer)
    P_UPDATEBY_TEAM = Column(Integer)
    AL_ID = Column(Integer)
    P_TUV_CERT_EXISTS = Column(BIT)
    P_EXTERNAL_CERT_EXISTS = Column(BIT)
    P_CERT_COMMENT = Column(Unicode(512))
    P_IS_QUOTATION = Column(BIT)
    P_IS_OLD_PROJECT = Column(BIT)
    P_QUOTATION_PROBABILITY = Column(DECIMAL(18, 2))
    P_QUOTATION_VALID_UNTIL = Column(DateTime)
    P_EXPECTED_TS_RECEIPT = Column(DateTime)
    P_NUMBER_OF_TESTSAMPLES = Column(Integer)
    CC_ID = Column(Unicode(10))
    P_INVOICE_RECIPIENT = Column(Integer)
    P_QUOTATION_LINK = Column(Integer)
    P_VERTRIEBSWEG = Column(Integer)
    P_RESPONSIBLE_AGENT = Column(Integer)
    P_SALES_REPRESENTATIVE = Column(Integer)
    P_SIGNATURE_LEFT = Column(Integer)
    P_STDSATZ = Column(DECIMAL(18, 2))
    P_POSTINGS_ALLOWED = Column(BIT)
    P_PLANNED_ORDERSIZE = Column(DECIMAL(18, 2))
    TC_P_ID = Column(Integer)
    BANF_REQUEST = Column(DateTime)
    BANF_ORDER = Column(DateTime)
    P_ABGS = Column(BIT)
    P_VORK = Column(BIT)
    P_PROJECT_NUMBER = Column(Unicode(50))
    SAP_QUOTATION_NUMBER = Column(Unicode(10))
    P_TS_RECEIPT_ADVISED = Column(BIT)
    P_IC = Column(NCHAR(2))
    P_SAP_INDUSTRY = Column(Unicode(3))
    P_FOREIGN_CURRENCY = Column(NCHAR(3))
    P_EXCHANGE_RATE = Column(DECIMAL(18, 10))
    P_GLOBAL_PARTNER = Column(Integer)
    P_PRICING_DATE = Column(DateTime)
    P_CLIENT_REMARK = Column(Unicode(2048))
    P_CONTACT_CUC_ID = Column(Integer)
    P_REMARK = Column(Unicode(1024))
    P_OTC_NAME_1 = Column(Unicode(40))
    P_OTC_NAME_2 = Column(Unicode(40))
    P_OTC_NAME_AT = Column(Unicode(40))
    P_OTC_NAME_CP = Column(Unicode(35))
    P_OTC_CO = Column(Unicode(40))
    P_OTC_STREET_1 = Column(Unicode(35))
    P_OTC_STREET_2 = Column(Unicode(40))
    P_OTC_STREET_3 = Column(Unicode(40))
    P_OTC_STREET_4 = Column(Unicode(40))
    P_OTC_STREET_5 = Column(Unicode(40))
    P_OTC_PO_BOX = Column(Unicode(10))
    P_OTC_POSTAL_CODE = Column(Unicode(10))
    P_OTC_CITY_1 = Column(Unicode(40))
    P_OTC_CITY_2 = Column(Unicode(40))
    P_OTC_REGION = Column(Unicode(3))
    P_OTC_COUNTRY = Column(Unicode(3))
    P_SIGNATURE_RIGHT = Column(Integer)
    P_WARRANTY_INFO = Column(Unicode(2048))
    CRM_ID = Column(Unicode(16))
    RUN_ID = Column(Integer)
    P_B2B = Column(BIT)
    P_COORDINATOR = Column(Integer)
    P_OTHER_DELAY_REASON = Column(Unicode(256))
    P_AUDIT_DATE = Column(DateTime)
    P_AUDIT_DATE_IS_CONFIRMED = Column(BIT)
    P_AUDIT_DATE_LINKED_SUBORDER = Column(Integer)
    P_DATE_ROLLUP = Column(DateTime)
    STARLIMS_SITE = Column(Unicode(20))
    STARLIMS_ATTENTION = Column(Unicode(255))
    STARLIMS_BUSINESS_TYPE = Column(Unicode(50))
    STARLIMS_SERVICE_TYPE = Column(Unicode(50))
    FROM_STARLIMS = Column(BIT)
    REGULATOR = Column(Integer)
    GOODS_RECIPIENT = Column(Integer)
    CONTACT_PERSON_INVOICE_RECIPIENT = Column(Integer)
    STARLIMS_PC = Column(Integer)
    FILE_FORMAT = Column(Integer)
    ARCHIVING_STATUS = Column(Unicode(32))
    P_TEAM_ID = Column(UNIQUEIDENTIFIER)
    P_RESY_FACTOR = Column(Unicode(5))
    SALES_PACKAGE_PRICE = Column(DECIMAL(18, 2))
    P_VISIBLE_FOR = Column(Integer)
    STARLIMS_CONNECTION_TYPE = Column(Integer)
    CONTRACT_TYPE = Column(Integer)
    PERFORM_SURVEY = Column(BIT)
    SURVEY_REJECT_REASON = Column(Unicode(512))
    SURVEY_SENT = Column(DateTime)
    MANUFACTURER_CONTACT = Column(Integer)
    REPORT_RECIPIENT_CONTACT = Column(Integer)
    CRM_STATUS = Column(Integer)
    CRM_TRANSFER_DATE = Column(DateTime)
    P_INVOICE_WAS_SET = Column(BIT)
    P_IAN = Column(Unicode(256))
    HISTORY_ID = Column(Integer, primary_key=True)
    TRANSFER_FIXED_PRICE_TO_SAP = Column(BIT)
    COLLECTIVE_INVOICE = Column(BIT)
    P_POSTING_DONE_DATE = Column(DateTime)
    CATEGORY_ID = Column(Integer)
    P_DATE_READY_REASON = Column(Unicode(512))
    P_DATE_READY_CHANGED = Column(DateTime)
    P_DATE_CHECK_REASON = Column(Unicode(512))
    P_DATE_CHECK_CHANGED = Column(DateTime)
    REPORT_SENT = Column(DateTime)
    P_INTERNATIONAL = Column(BIT)
    P_COORDINATOR_TEAM = Column(Integer)
    BATCH_NUMBER = Column(Unicode(16))
    COLLECTIVE_INVOICE_SENT = Column(DateTime)
    PROJECT_TYPE = Column(Integer)
    OPPORTUNITY_ID = Column(Unicode(10))
    NECESSARY_DOCUMENTATION_AVAILABLE = Column(BIT)
    SAP_ORDER_TYPE = Column(Unicode(8))
    P_DEPARTMENT_ID = Column(UNIQUEIDENTIFIER)
    P_CONFIDENTIAL = Column(BIT)
    P_TEMPLATEID = Column(Integer)
    PRINT_OPTION = Column(Unicode(3))
    UNLIMITED_LIABILITY = Column(BIT)
    SERVICE_RENDERED_DATE = Column(Date)


class PROJECTLINK(Base):
    __tablename__ = "PROJECT_LINK"
    __table_args__ = (
        Index("UQ_PROJECT_LINKING", "P_ID", "P_DEST_ID", unique=True),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    P_ID = Column(Integer, nullable=False)
    P_DEST_ID = Column(Integer, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)


class PROJECTPOSITIONHISTORY(Base):
    __tablename__ = "PROJECT_POSITION_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    PP_ID = Column(Integer)
    P_ID = Column(Integer, index=True)
    PP_NUMBER = Column(Integer)
    PP_DISABLED = Column(BIT)
    PP_STATUS = Column(Integer)
    PP_STATUS_CHANGED_ON = Column(DateTime)
    PP_STATUS_CHANGED_BY = Column(Integer)
    PP_TEXT = Column(Unicode(4000))
    PP_SALES_PRICE = Column(DECIMAL(18, 2))
    ZM_ID = Column(Unicode(18))
    PP_TYPE = Column(Integer)
    PP_LAST_SAP_UPDATE = Column(DateTime)
    PP_CANCELLATION_FLAG = Column(BIT)
    PP_CREATED = Column(DateTime)
    PP_CREATED_BY = Column(Integer)
    PP_UPDATED = Column(DateTime)
    PP_UPDATED_BY = Column(Integer)
    PP_PREPAYMENT_PRICE = Column(DECIMAL(18, 2))
    PP_PRINTING_FLAG = Column(Unicode(5))
    PP_SINGLE_PRICE = Column(DECIMAL(18, 2))
    PP_TARGET_COUNT = Column(DECIMAL(18, 2))
    PP_SP_FOREIGN = Column(DECIMAL(18, 2))
    FROM_PS_CONFIG = Column(BIT)
    PP_UNIT = Column(Unicode(3))
    FROM_STARLIMS = Column(BIT)
    PP_FI_FACTOR = Column(Unicode(5))
    PP_INTERNAL_NOTE = Column(Unicode(1024))
    PP_CANCELLATION_REASON = Column(Integer)
    CRM_TRANSFER_DATE = Column(DateTime)
    PP_DISCOUNT = Column(DECIMAL(18, 2))
    PP_PLANT = Column(Integer)
    PP_TAXABLE = Column(BIT)
    PP_IS_QUOTATION_POSITION = Column(BIT)
    PP_DISCOUNT_PERCENTAGE = Column(DECIMAL(19, 10))
    PP_START_DATE = Column(Date)
    PP_END_DATE = Column(Date)


class PROJECTSTARLIMSHISTORY(Base):
    __tablename__ = "PROJECT_STARLIMS_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    P_ID = Column(Integer, index=True)
    STARLIMS_PROJECT_NUMBER = Column(Unicode(25))
    ID = Column(Integer)


class PROKALKMODULHISTORY(Base):
    __tablename__ = "PROKALKMODUL_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    PKM_ID = Column(Integer)
    P_ID = Column(Integer, index=True)
    KALM_ID = Column(Integer)
    KAL_ID = Column(Integer)
    PKM_TYP = Column(Integer)
    PKM_NAME = Column(Unicode(1024))
    PKM_IS_UA = Column(BIT)
    PKM_TAGE_UA = Column(Integer)
    TP_ID = Column(Integer)
    PKM_TESTDAUER = Column(Integer)
    PKM_EINHEITEN = Column(DECIMAL(18, 2))
    PKM_SATZ = Column(DECIMAL(18, 2))
    PKM_AUFWAND = Column(DECIMAL(18, 2))
    PKM_FAKTOR = Column(DECIMAL(18, 2))
    PKM_VK = Column(DECIMAL(18, 2))
    PKM_AUFTRAGSTEXT = Column(Unicode(1024))
    PKM_KOMMENTAR = Column(Unicode(1024))
    PKM_REIHE = Column(Integer)
    PKM_UA = Column(Integer)
    MIT_ID = Column(Integer)
    PKM_REGDATE = Column(DateTime)
    PKM_REGBY = Column(Integer)
    PKM_UPDATE = Column(DateTime)
    PKM_UPDATEBY = Column(Integer)
    MIT_ID_TEAM = Column(Integer)
    PKM_REGBY_TEAM = Column(Integer)
    PKM_UPDATEBY_TEAM = Column(Integer)
    AL_ID = Column(Integer)
    PKM_DISABLED = Column(BIT)
    FROM_PS_CONFIG = Column(BIT)


class PROKALKUNTERMODULHISTORY(Base):
    __tablename__ = "PROKALKUNTERMODUL_HISTORY"
    __table_args__ = (
        Index("IX_PROKALKUNTERMODUL_HISTORY_P_ID_SO_NO", "P_ID", "SO_NUMBER"),
        {"schema": "dbo"},
    )

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    PKUM_ID = Column(Integer)
    PKM_ID = Column(Integer)
    P_ID = Column(Integer)
    SO_NUMBER = Column(Integer)
    PKUM_QUOTATION_POSITION = Column(Integer)
    PKUM_TESTING_POSITION = Column(Integer)
    ST_ID = Column(Integer)
    PKUM_NAME = Column(Unicode(1024))
    PKUM_DAYS_TO_START = Column(Integer)
    PKUM_DURATION = Column(Integer)
    TP_ID = Column(Integer)
    PKUM_PLANNED_HOURS = Column(DECIMAL(18, 2))
    PKUM_PLANNED_EXPENSES = Column(DECIMAL(18, 2))
    PKUM_FACTOR = Column(DECIMAL(18, 2))
    PKUM_PLANNED_TRAVEL_COSTS = Column(DECIMAL(18, 2))
    PKUM_RECOMMENDED_PRICE = Column(DECIMAL(18, 2))
    PKUM_COMMENT = Column(Unicode(2000))
    PKUM_ORDER_TEXT = Column(Unicode(1024))
    PKUM_ADDITIONAL_TEXT = Column(Unicode(1024))
    PKUM_SAP_TRANSFER = Column(DateTime)
    PKUM_SORT = Column(Integer)
    PKUM_DISABLED = Column(BIT)
    PKUM_CREATED = Column(DateTime)
    PKUM_CREATED_BY = Column(Integer)
    PKUM_UPDATED = Column(DateTime)
    PKUM_UPDATED_BY = Column(Integer)
    PKUM_SO_TRANSFER_PRICE = Column(DECIMAL(18, 2))
    PKUM_SP_PRICELIST = Column(DECIMAL(18, 2))
    PKUM_TRAVELTIME = Column(DECIMAL(18, 2))
    PKUM_SP_FOREIGN = Column(DECIMAL(18, 10))
    ZM_ID = Column(Unicode(18))
    PKUM_BULKTEST = Column(BIT)
    PKUM_SP_PRICELIST_ORG = Column(DECIMAL(18, 2))
    PKUM_CANCELLED = Column(BIT)
    FROM_PS_CONFIG = Column(BIT)
    FROM_SUBORDER = Column(Integer)
    PKUM_RATE = Column(DECIMAL(18, 2))
    PKUM_KPI = Column(BIT)
    PKUM_S_KPI_NUMBER = Column(Integer)
    PKUM_PLANNED_SUBCONTRACTING = Column(DECIMAL(18, 2))


class PSEXKEY(Base):
    __tablename__ = "PSEX_KEY"
    __table_args__ = {"schema": "dbo"}

    PSK_ID = Column(Integer, nullable=False)
    MD_ID = Column(Integer, primary_key=True, nullable=False)
    PSK_KEY = Column(Unicode(32), primary_key=True, nullable=False)
    PSQ_ID = Column(Integer, nullable=False)
    PSK_TYPE = Column(NCHAR(1), nullable=False)
    PSK_HEADER_DE = Column(Unicode(100))
    PSK_HEADER_EN = Column(Unicode(100))
    PSK_HEADER_FR = Column(Unicode(100))
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)
    DESCRIPTION_DE = Column(Unicode(256))
    DESCRIPTION_EN = Column(Unicode(256))
    DESCRIPTION_FR = Column(Unicode(256))


class PSEXLOG(Base):
    __tablename__ = "PSEX_LOG"
    __table_args__ = (
        Index("IX_PSEX_LOG_MESSAGE", "Form", "Pos", "Created", "Message"),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    Type = Column(Integer, nullable=False)
    Issued = Column(DATETIME2, nullable=False)
    Form = Column(Unicode(64), nullable=False)
    Pos = Column(Unicode(64))
    Message = Column(Unicode)
    Args = Column(Unicode(4000))
    DomainName = Column(Unicode(100))
    MachineName = Column(Unicode(16))
    Created = Column(DATETIME2)
    ExStack = Column(Unicode)
    WorkingCluster = Column(UNIQUEIDENTIFIER)
    ISSUED_LOCAL = Column(DATETIME2)
    CLIENT_VERSION = Column(Unicode(100))
    WORKING_CLUSTER_ID = Column(BigInteger)


class PSEXQUERY(Base):
    __tablename__ = "PSEX_QUERY"
    __table_args__ = {"schema": "dbo"}

    PSQ_ID = Column(Integer, primary_key=True)
    MD_ID = Column(Integer, nullable=False)
    PSQ_Query = Column(Unicode)
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)


class PSEXSETTING(Base):
    __tablename__ = "PSEX_SETTINGS"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    MD_ID = Column(Integer, nullable=False)
    ANONYMIZATION_INTERVALL = Column(Integer)
    RETENTION_PERIOD = Column(Integer)
    HOUR_FORMAT = Column(Unicode(50))


class PSEXTAB(Base):
    __tablename__ = "PSEX_TAB"
    __table_args__ = {"schema": "dbo"}

    PST_ID = Column(Integer, primary_key=True)
    MD_ID = Column(Integer, nullable=False)
    PST_NO = Column(Integer)
    PST_WIDTH = Column(Integer)
    PST_DEFAULT = Column(Unicode(100))
    PSQ_ID = Column(Integer)
    PST_COLHEADER_DE = Column(Unicode(150))
    PST_COLHEADER_EN = Column(Unicode(150))
    PST_COLHEADER_FR = Column(Unicode(150))
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)
    PST_BOLD = Column(BIT, nullable=False)
    PST_HORIZONTAL_ALIGNMENT = Column(Unicode(10))
    PST_VERTICAL_MERGE = Column(BIT, nullable=False)
    PST_CHECKBOX = Column(BIT, nullable=False)
    PST_HORIZONTAL_HEADER_ALIGNMENT = Column(Unicode(10))


class QUERY(Base):
    __tablename__ = "QUERY"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    MD_ID = Column(Integer, nullable=False)
    QUERY = Column(Unicode, nullable=False)
    PROTECT_PERSONAL_DATA = Column(BIT, nullable=False)
    DESCRIPTION = Column(Unicode(1000))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)
    DISABLED = Column(BIT, nullable=False)


class REPORTCOLUMN(Base):
    __tablename__ = "REPORTCOLUMN"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    REPORT = Column(Unicode(30), nullable=False)
    FIELDNAME = Column(Unicode(50))
    FUNC = Column(Unicode(100))
    RESOURCE_ID = Column(Integer, nullable=False)
    SORT = Column(Integer, nullable=False)
    REMARK = Column(Unicode(100))
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime, nullable=False)


class REPORTSTYLE(Base):
    __tablename__ = "REPORTSTYLE"
    __table_args__ = {"schema": "dbo"}

    STYLE_NAME = Column(Unicode(30), primary_key=True)
    FONT_NAME = Column(Unicode(30))
    FONT_SIZE = Column(Integer)
    FONT_IS_BOLD = Column(BIT)
    TEXT_COLOR_ID = Column(Integer)
    TEXT_IS_WRAPPED = Column(BIT)
    BACK_COLOR_ID = Column(Integer)
    FRAME_STYLE = Column(Unicode(30))
    HORIZONTAL_ALIGN = Column(NCHAR(1))
    VERTICAL_ALIGN = Column(NCHAR(1))
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime, nullable=False)


class REPORTTEMPLATE(Base):
    __tablename__ = "REPORTTEMPLATE"
    __table_args__ = {"schema": "dbo"}

    REPORT_NAME = Column(Unicode(50), primary_key=True)
    SHEET_NAME = Column(Unicode(50))
    META_STYLE = Column(Unicode(30))
    CAPTION_STYLE = Column(Unicode(30))
    FIELD_STYLE = Column(Unicode(30))
    HAS_FILTER = Column(BIT, nullable=False)
    PAGESETUP_PORTRAIT = Column(BIT, nullable=False)
    HEADER_LEFT = Column(Unicode(100))
    HEADER_CENTER = Column(Unicode(50))
    HEADER_RIGHT = Column(Unicode(50))
    FOOTER_LEFT = Column(Unicode(50))
    FOOTER_CENTER = Column(Unicode(50))
    FOOTER_RIGHT = Column(Unicode(50))
    FIT_PAGE_WIDE = Column(BIT, nullable=False)
    FIT_PAGE_TALL = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    COL_WIDTH_MAX = Column(Integer)


class RESULTMD(Base):
    __tablename__ = "RESULT_MD"
    __table_args__ = {"schema": "dbo"}

    RES_ID = Column(Integer, primary_key=True)
    MD_ID = Column(Integer, nullable=False)
    RES_KEY = Column(Unicode(10), nullable=False)
    RES_TEXT_EN = Column(Unicode(256), nullable=False)
    RES_TEXT_DE = Column(Unicode(256), nullable=False)
    RES_TEXT_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATEDBY = Column(Integer)
    UPDATED = Column(DateTime)
    UPDATEDBY = Column(Integer)


t_RIGHTSMANAGEMENT_LASTRUN = Table(
    "RIGHTSMANAGEMENT_LASTRUN",
    metadata,
    Column("LAST_RUN", DATETIME2, nullable=False),
    Column("LAST_TEAM_RUN", DATETIME2),
    schema="dbo",
)


class RIGHTSMANAGEMENTTASK(Base):
    __tablename__ = "RIGHTSMANAGEMENT_TASK"
    __table_args__ = (
        Index(
            "IX_RIGHTSMANAGEMENT_TASK_TYPE_STATUS",
            "STATUS",
            "RIGHTSMANAGEMENTTASKTYPE",
        ),
        {"schema": "dbo"},
    )

    ID = Column(BigInteger, primary_key=True)
    STATUS = Column(Integer, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    STARTED = Column(DateTime)
    FINISHED = Column(DateTime)
    RIGHTSMANAGEMENTTASKTYPE = Column(Integer, nullable=False)
    LAST_RUN = Column(DateTime, nullable=False)


class ROLE(Base):
    __tablename__ = "ROLE"
    __table_args__ = {"schema": "dbo"}

    RS_ID = Column(Integer, primary_key=True)
    RS_ROLENAME = Column(Unicode(25), nullable=False)
    RS_IS_EDOC_ROLE = Column(BIT, nullable=False)
    RS_DESCRIPTION_DE = Column(Unicode(256))
    RS_ROLE_INFO_DE = Column(Unicode(256))
    RS_DESCRIPTION_EN = Column(Unicode(256))
    RS_ROLE_INFO_EN = Column(Unicode(256))
    RS_DESCRIPTION_FR = Column(Unicode(256))
    RS_ROLE_INFO_FR = Column(Unicode(256))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UpdateDate = Column(DateTime)
    UPDATED_BY = Column(Integer)
    MANDATOR_FLAG = Column(Integer, nullable=False)
    MD_ID = Column(Integer, nullable=False)


class SAPSYSTEM(Base):
    __tablename__ = "SAP_SYSTEM"
    __table_args__ = {"schema": "dbo"}

    ID = Column(BigInteger, primary_key=True)
    NAME = Column(Unicode(3))
    SERVER = Column(Unicode(100))
    SERVER_ID = Column(Integer)
    CLIENT = Column(Unicode(3))
    SYSTEM_NUMBER = Column(Integer, nullable=False)
    CULTURE = Column(Unicode(5))
    DATE_FORMAT = Column(Unicode(12))
    DESIGNATION_DE = Column(Unicode(30), nullable=False)
    DESIGNATION_EN = Column(Unicode(30), nullable=False)
    DESIGNATION_FR = Column(Unicode(30), nullable=False)
    IDOC_MESTYP = Column(Unicode(30))
    IDOC_NAME = Column(Unicode(30))
    IDOC_RCVPOR = Column(Unicode(12))
    IDOC_RCVPRN = Column(Unicode(12))
    IDOC_RCVPRT = Column(Unicode(12))
    IDOC_SNDPOR = Column(Unicode(12))
    IDOC_SNDPRN = Column(Unicode(12))
    IDOC_SNDPRT = Column(Unicode(12))
    RFC_LANGUAGE = Column(NCHAR(2))
    RFC_PASS = Column(Unicode(30))
    RFC_USER = Column(Unicode(8))
    TIME_FORMAT = Column(Unicode(6))
    IDOC_EXPORT = Column(BIT, nullable=False)
    CATS_MESTYP = Column(Unicode(30))
    CATS_NAME = Column(Unicode(30))
    QUOTATION_SERVICE_URL = Column(Unicode(256))
    CREATED = Column(DATETIME2)
    CREATED_BY = Column(BigInteger)
    UPDATED = Column(DATETIME2)
    UPDATED_BY = Column(BigInteger)


class SKILLGROUP(Base):
    __tablename__ = "SKILLGROUP"
    __table_args__ = {"schema": "dbo"}

    SG_ID = Column(Unicode(8), primary_key=True)
    SG_TXT = Column(Unicode(80), nullable=False)
    SG_BEGDA = Column(DateTime, nullable=False)
    SG_ENDDA = Column(DateTime, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="SKILLGROUP.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="SKILLGROUP.UPDATED_BY == STAFF.ST_ID"
    )


class SOTRANSFERFILEHISTORY(Base):
    __tablename__ = "SOTRANSFERFILE_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ID = Column(Integer, index=True)
    FILEPATH = Column(Unicode(512))
    ISFOCUS = Column(BIT)
    TRA_ID = Column(Integer)
    DATALEN = Column(Integer)
    WRITEUTC = Column(DateTime)
    STATUS = Column(Unicode(10))
    MSG = Column(Unicode)


class SOTRANSFERJOBHISTORY(Base):
    __tablename__ = "SOTRANSFERJOB_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    TRA_ID = Column(Integer)
    P_ID = Column(Integer, index=True)
    DIR = Column(NCHAR(1))
    FILENAME = Column(Unicode(512))
    CREATED = Column(DateTime)
    UPDATED = Column(DateTime)
    STATUS = Column(Unicode(10))
    SRC_FOLDER = Column(Unicode(512))
    TAR_FOLDER = Column(Unicode(512))


class STAFF(Base):
    __tablename__ = "STAFF"
    __table_args__ = (
        Index("IX_STAFF_ST_NUMBER_ST_COSTID", "ST_NUMBER", "ST_COSTID"),
        Index("IX_STAFF_ST_COSTID_ST_NUMBER", "ST_NUMBER", "ST_COSTID"),
        Index(
            "IX_STAFF_ST_ACTIVE_ST_TYPE",
            "ST_ACTIVE",
            "ST_TYPE",
            "ST_ID",
            "ST_WINDOWSID",
            "ST_DOMAIN",
        ),
        Index(
            "UIX_STAFF_ST_DOMAIN_ST_WINDOWSID",
            "ST_DOMAIN",
            "ST_WINDOWSID",
            unique=True,
        ),
        Index(
            "IX_STAFF_ST_TEAM",
            "ST_TEAM",
            "ST_ID",
            "ST_SURNAME",
            "ST_FORENAME",
            "ST_SERVERID",
        ),
        {"schema": "dbo"},
    )

    ST_ID = Column(Integer, primary_key=True)
    ST_SURNAME = Column(Unicode(60), nullable=False)
    ST_FORENAME = Column(Unicode(50))
    ST_LOCATION = Column(Unicode(50))
    ST_UNIT = Column(Unicode(12))
    ST_COSTID = Column(Unicode(10))
    ST_ACTIVE = Column(BIT, nullable=False)
    ST_NUMBER = Column(Unicode(8))
    ST_SHORT = Column(Unicode(3))
    ST_PHONE = Column(Unicode(80))
    ST_FAX = Column(Unicode(80))
    ST_EMAIL = Column(Unicode(80))
    ST_LOGIN = Column(BIT, nullable=False)
    ST_HOURS_PER_DAY = Column(Integer)
    ST_WINDOWSID = Column(Unicode(32))
    ST_SAP_ID = Column(Unicode(50))
    ST_TITLE = Column(Unicode(255))
    ST_GENDER = Column(Unicode(50))
    ST_SERVERID = Column(Integer)
    UpdateDate = Column(DateTime)
    UpdateByID = Column(Integer)
    Locale = Column(Unicode(50))
    ST_UPDATE_TYPE = Column(TINYINT)
    ST_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_ID"))
    ST_IS_LAGER = Column(BIT, nullable=False)
    ST_IS_ABTEILUNG = Column(BIT, nullable=False)
    ST_TYPE = Column(Integer, nullable=False)
    ST_DOMAIN = Column(Unicode(32))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    VERSION_TYPE = Column(Unicode(5), nullable=False)
    RUN_ID = Column(Integer)
    STAT2 = Column(NCHAR(1))
    ST_SKILLGROUP = Column(ForeignKey("dbo.SKILLGROUP.SG_ID"), nullable=False)
    ST_COSTID_CHANGED = Column(DateTime)
    PERSK = Column(NCHAR(2))
    ST_POSTING_APPROVAL_REQUIRED = Column(BIT, nullable=False)
    ST_MOBILE = Column(Unicode(80))
    ST_MARK = Column(Unicode(256))

    SKILLGROUP = relationship(
        "SKILLGROUP", primaryjoin="STAFF.ST_SKILLGROUP == SKILLGROUP.SG_ID"
    )
    HIERARCHY = relationship(
        "HIERARCHY", primaryjoin="STAFF.ST_TEAM == HIERARCHY.HR_ID"
    )


class STAFFROLEHISTORY(Base):
    __tablename__ = "STAFFROLE_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    SR_ID = Column(Integer, index=True)
    ST_ID = Column(Integer)
    RS_ID = Column(Integer)
    DISABLED = Column(BIT)
    CREATED = Column(DateTime)
    CREATED_BY = Column(Integer)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)


class STAFFHISTORY(Base):
    __tablename__ = "STAFF_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ST_ID = Column(Integer, index=True)
    ST_SURNAME = Column(Unicode(60))
    ST_FORENAME = Column(Unicode(50))
    ST_LOCATION = Column(Unicode(50))
    ST_UNIT = Column(Unicode(12))
    ST_COSTID = Column(Unicode(10))
    ST_ACTIVE = Column(BIT)
    ST_NUMBER = Column(Unicode(8))
    ST_SHORT = Column(Unicode(3))
    ST_PHONE = Column(Unicode(80))
    ST_FAX = Column(Unicode(80))
    ST_EMAIL = Column(Unicode(80))
    ST_LOGIN = Column(BIT)
    ST_HOURS_PER_DAY = Column(Integer)
    ST_WINDOWSID = Column(Unicode(32))
    ST_SAP_ID = Column(Unicode(50))
    ST_TITLE = Column(Unicode(255))
    ST_GENDER = Column(Unicode(50))
    ST_SERVERID = Column(Integer)
    UpdateDate = Column(DateTime)
    UpdateByID = Column(Integer)
    Locale = Column(Unicode(50))
    ST_UPDATE_TYPE = Column(TINYINT)
    ST_TEAM = Column(UNIQUEIDENTIFIER)
    ST_IS_LAGER = Column(BIT)
    ST_IS_ABTEILUNG = Column(BIT)
    ST_TYPE = Column(Integer)
    ST_DOMAIN = Column(Unicode(32))
    CREATED = Column(DateTime)
    CREATED_BY = Column(Integer)
    VERSION_TYPE = Column(Unicode(5))
    RUN_ID = Column(Integer)
    STAT2 = Column(NCHAR(1))
    ST_SKILLGROUP = Column(Unicode(8))
    ST_COSTID_CHANGED = Column(DateTime)
    PERSK = Column(NCHAR(2))
    ST_POSTING_APPROVAL_REQUIRED = Column(BIT)
    ST_MOBILE = Column(Unicode(80))
    ST_MARK = Column(Unicode(256))


class STARLIMSBUSINESSTYPE(Base):
    __tablename__ = "STARLIMS_BUSINESS_TYPE"
    __table_args__ = {"schema": "dbo"}

    NAME = Column(Unicode(50), primary_key=True, nullable=False)
    SITE_NAME = Column(Unicode(20), primary_key=True, nullable=False)
    CREATED = Column(DateTime, nullable=False)


class STARLIMSCONFIGURATION(Base):
    __tablename__ = "STARLIMS_CONFIGURATION"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    WORKING_CLUSTER = Column(UNIQUEIDENTIFIER, nullable=False, unique=True)
    SERVICE_URL = Column(Unicode(256), nullable=False)
    LAB_SETTLEMENT_USER_CHEMICAL = Column(Integer)
    LAB_SETTLEMENT_USER_MECHANICAL = Column(Integer)
    POSITION_NUMBER_CHEMICAL = Column(Integer)
    POSITION_NUMBER_MECHANICAL = Column(Integer)
    POSITION_TEXT_CHEMICAL = Column(Unicode(1024))
    POSITION_TEXT_MECHANICAL = Column(Unicode(1024))
    POSITION_UNIT_CHEMICAL = Column(Unicode(3))
    POSITION_UNIT_MECHANICAL = Column(Unicode(3))
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)


class STARLIMSDATUM(Base):
    __tablename__ = "STARLIMS_DATA"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    OPERATION = Column(Integer, nullable=False)
    P_ID = Column(Integer)
    SO_NUMBER = Column(Integer)
    CHECKLIST_PREPARED_BY = Column(Unicode(65))
    SERVICE_ID = Column(Integer)
    CHECKLIST_DATA = Column(Unicode(1024))
    START_DATE = Column(DateTime)
    DEADLINE_DATE = Column(DateTime)
    REMARK = Column(Unicode(1024))
    MATERIAL_CODE = Column(Unicode(18))
    PRICE = Column(DECIMAL(18, 2))
    FACTOR = Column(DECIMAL(18, 2))
    REPORT_NUMBER = Column(Unicode(256))
    OFFICER_IN_CHARGE = Column(Unicode(65))
    FOLDER = Column(Unicode(256))
    FILE_NAME = Column(Unicode(256))
    FILE_DATA = Column(LargeBinary)
    ORDERING_PARTY = Column(Unicode(10))
    MANUFACTURER = Column(Unicode(10))
    GLOBAL_PARTNER = Column(Unicode(10))
    PRODUCT = Column(Unicode(255))
    MODEL = Column(Unicode(255))
    PROJECT_MANAGER = Column(Unicode(65))
    STARLIMS_SITE = Column(Unicode(20))
    STARLIMS_ATTENTION = Column(Unicode(255))
    STARLIMS_BUSINESS_TYPE = Column(Unicode(50))
    STARLIMS_SERVICE_TYPE = Column(Unicode(50))
    CREATED = Column(DateTime, nullable=False)
    TRANSFERRED_BY = Column(Unicode(65))
    DISTINCTIVE_FLAG = Column(Integer)
    PO_NUMBER = Column(Unicode(35))
    OIC = Column(Unicode(65))
    CONTACT_PARTNER = Column(Unicode(10))
    ORDER_TEXT = Column(Unicode(2048))
    CURRENCY = Column(Unicode(3))


class STARLIMSSERVICETYPE(Base):
    __tablename__ = "STARLIMS_SERVICE_TYPE"
    __table_args__ = {"schema": "dbo"}

    NAME = Column(Unicode(50), primary_key=True, nullable=False)
    SITE_NAME = Column(Unicode(20), primary_key=True, nullable=False)
    CREATED = Column(DateTime, nullable=False)


class STARLIMSSITE(Base):
    __tablename__ = "STARLIMS_SITE"
    __table_args__ = {"schema": "dbo"}

    NAME = Column(Unicode(20), primary_key=True)
    CREATED = Column(DateTime, nullable=False)


class SUBORDERSHISTORY(Base):
    __tablename__ = "SUBORDERS_HISTORY"
    __table_args__ = (
        Index("IX_SUBORDERS_HISTORY_P_ID_SO_NO", "P_ID", "SO_NUMBER"),
        {"schema": "dbo"},
    )

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    P_ID = Column(Integer)
    SO_NUMBER = Column(Integer)
    SO_DISPOBY = Column(Integer)
    SO_CREATED = Column(DateTime)
    ST_ID = Column(Integer)
    SO_DEADLINE = Column(DateTime)
    SO_TASK = Column(Unicode(1024))
    SO_HOURS = Column(DECIMAL(18, 6))
    SO_RATE = Column(MONEY)
    SO_SPENDS = Column(MONEY)
    SO_ACC_HOURS = Column(MONEY)
    SO_ACC_SPENDS = Column(DECIMAL(18, 2))
    SO_REPORT = Column(Unicode(255))
    SO_START_MACRO = Column(BIT)
    MCO_ID = Column(Integer)
    SO_COMMENT = Column(Unicode(2000))
    SO_DATE_READY = Column(DateTime)
    SO_READYBY = Column(Integer)
    SO_DATE_CHECK = Column(DateTime)
    SO_CHECKBY = Column(Integer)
    SO_FORECAST = Column(DECIMAL(18, 2))
    SO_LANGUAGE = Column(Unicode(5))
    RES_ID = Column(Integer)
    SO_ACC_POS = Column(Unicode(10))
    SO_INTERN = Column(BIT)
    SO_PREDATE = Column(DateTime)
    SO_PREDATE_REMINDER = Column(BIT)
    SO_PREDATE_INFO = Column(Unicode(255))
    SO_WAIT = Column(BIT)
    SO_REGBY = Column(Integer)
    SO_REGDATE = Column(DateTime)
    SO_UPDATEBY = Column(Integer)
    SO_UPDATE = Column(DateTime)
    SO_TRANSFERSTATUS = Column(Unicode(50))
    SO_DISABLED = Column(BIT)
    SO_ForeignExpenditure = Column(MONEY)
    SO_PostedFromForeign = Column(MONEY)
    SO_IsTransferredBack = Column(BIT)
    UA_TRANS_PROJECT = Column(Integer)
    SO_Docu_Done = Column(BIT)
    SO_DEADLINE_REMINDER = Column(BIT)
    SO_CUSTOMER_A = Column(Integer)
    SO_CUSTOMER_B = Column(Integer)
    SO_CUSTOMER_O = Column(Integer)
    SO_PARENT = Column(Integer)
    SO_SORT = Column(Integer)
    SO_ADMINISTRATIVE = Column(BIT)
    SO_APPOINTMENTDATE = Column(DateTime)
    PLAN_ACTUAL_HOUR = Column(DECIMAL(8, 2))
    PLAN_TRAVEL = Column(DECIMAL(18, 2))
    PLAN_EXTERNAL = Column(DECIMAL(18, 2))
    ACC_EFFORT = Column(DECIMAL(18, 2))
    ACC_ACTUAL_HOUR = Column(DECIMAL(18, 2))
    ACC_TRAVEL = Column(DECIMAL(18, 2))
    ACC_EXTERNAL = Column(DECIMAL(18, 2))
    SAP_NO = Column(Unicode(10))
    ORDER_SIGN = Column(Unicode(35))
    ORDER_DATE = Column(DateTime)
    ORDER_POSITION = Column(Unicode(6))
    SO_CHECKBY_TEAM = Column(Integer)
    SO_DISPOBY_TEAM = Column(Integer)
    SO_READYBY_TEAM = Column(Integer)
    SO_REGBY_TEAM = Column(Integer)
    SO_UPDATEBY_TEAM = Column(Integer)
    ST_ID_TEAM = Column(Integer)
    AL_ID = Column(Integer)
    SO_PLANNED_MATERIAL = Column(DECIMAL(18, 2))
    SO_PLANNED_LICENSE = Column(DECIMAL(18, 2))
    BANF_REQUEST = Column(DateTime)
    BANF_ORDER = Column(DateTime)
    B2B = Column(BIT)
    SO_REPORT_NUMBER = Column(Unicode(256))
    ZM_ID = Column(Unicode(18))
    SO_REMARK = Column(Unicode(1024))
    SO_POST_OUT_DATE = Column(DateTime)
    SO_CONFIRMED_DATE = Column(DateTime)
    LIMS_STATUS = Column(Unicode(16))
    LIMS_REMARK = Column(Unicode(256))
    SOC_ID = Column(Integer)
    RFAE_ID = Column(Integer)
    FROM_STARLIMS = Column(BIT)
    SO_COORDINATOR = Column(Integer)
    STARLIMS_DISTINCTIVE_FLAG = Column(Integer)
    DEADLINE_CALCULATION_WITHOUT_HOLIDAYS = Column(BIT)
    SO_MODEL = Column(Unicode(255))
    TRANSFER_TO_STARLIMS = Column(DateTime)
    STARLIMS_PROJECT_NUMBER = Column(Unicode(25))
    URGENT = Column(BIT)
    SO_POSTING_DONE_DATE = Column(DateTime)
    KPI = Column(BIT)
    SO_DATE_READY_REASON = Column(Unicode(512))
    SO_DATE_READY_CHANGED = Column(DateTime)
    SO_DATE_CHECK_REASON = Column(Unicode(512))
    SO_DATE_CHECK_CHANGED = Column(DateTime)
    REPORT_SENT = Column(DateTime)
    S_KPI_NUMBER = Column(Integer)
    SO_TUV_CERT_EXISTS = Column(BIT)
    SO_EXTERNAL_CERT_EXISTS = Column(BIT)
    SO_CERT_COMMENT = Column(Unicode(512))


class SUBORDERLAGERELEMENTHISTORY(Base):
    __tablename__ = "SUBORDER_LAGERELEMENT_HISTORY"
    __table_args__ = (
        Index(
            "IX_SUBORDER_LAGERELEMENT_HISTORY_P_ID_SO_NO", "P_ID", "SO_NUMBER"
        ),
        {"schema": "dbo"},
    )

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ID = Column(Integer)
    P_ID = Column(Integer)
    SO_NUMBER = Column(Integer)
    LGEL_ID = Column(Integer)
    DISABLED = Column(BIT)
    CREATED = Column(DateTime)
    CREATED_BY = Column(Integer)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)


class SUBORDERSAMPLEHISTORY(Base):
    __tablename__ = "SUBORDER_SAMPLE_HISTORY"
    __table_args__ = (
        Index("IX_SUBORDER_SAMPLE_HISTORY_P_ID_SO_NO", "P_ID", "SO_NUMBER"),
        {"schema": "dbo"},
    )

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ID = Column(Integer)
    P_ID = Column(Integer)
    SO_NUMBER = Column(Integer)
    SAMPLE_NUMBER = Column(Unicode(16))
    SAMPLE_DESCRIPTION = Column(Unicode(256))
    REMARK = Column(Unicode(512))
    DISABLED = Column(BIT)
    CREATED = Column(DateTime)
    CREATED_BY = Column(Integer)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)


class SUBORDERTESTMETHODHISTORY(Base):
    __tablename__ = "SUBORDER_TEST_METHOD_HISTORY"
    __table_args__ = (
        Index(
            "IX_SUBORDER_TEST_METHOD_HISTORY_P_ID_SO_NO", "P_ID", "SO_NUMBER"
        ),
        {"schema": "dbo"},
    )

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ID = Column(Integer)
    P_ID = Column(Integer)
    SO_NUMBER = Column(Integer)
    STKO_ID = Column(Integer)
    STANDARD_ANALYSIS = Column(Unicode(128))
    TEST_METHOD_ID = Column(Integer)
    TEST_METHOD_NAME = Column(Unicode(128))
    PARAMETER = Column(Unicode(128))
    DISABLED = Column(BIT)
    CREATED = Column(DateTime)
    CREATED_BY = Column(Integer)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)


class SUBORDERTESTREQUIREMENTSAMPLEHISTORY(Base):
    __tablename__ = "SUBORDER_TEST_REQUIREMENT_SAMPLE_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    ID = Column(Integer, index=True)
    METHOD_ID = Column(Integer)
    SAMPLE_ID = Column(Integer)
    MIX_SAMPLE_NUMBER = Column(Integer)
    DISABLED = Column(BIT)
    CREATED = Column(DateTime)
    CREATED_BY = Column(Integer)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)


class TASKELEMENT(Base):
    __tablename__ = "TASK_ELEMENT"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME = Column(Unicode(50), nullable=False)
    DESCR = Column(Unicode(256))


class TASKFILETRANSFER(Base):
    __tablename__ = "TASK_FILETRANSFER"
    __table_args__ = {"schema": "dbo"}

    FT_ID = Column(Integer, primary_key=True)
    SERVERID = Column(Integer, nullable=False)
    TYPE = Column(NCHAR(2), nullable=False)
    ACTIVE = Column(BIT, nullable=False)
    CMD = Column(NCHAR(2), nullable=False)
    SOURCE = Column(Unicode(256), nullable=False)
    TARGET = Column(Unicode(256), nullable=False)
    ALTERNATIVE = Column(Unicode(256))


class TASKRUN(Base):
    __tablename__ = "TASK_RUN"
    __table_args__ = {"schema": "dbo"}

    RUN_ID = Column(Integer, primary_key=True)
    SCHED_ID = Column(Integer, nullable=False)
    START = Column(DateTime, nullable=False)
    FINISH = Column(DateTime)
    STATUS = Column(Unicode(12))
    PROGRESS = Column(Integer)
    ITEMS_DONE = Column(Integer)
    ITEMS_CHANGED = Column(Integer)
    MANDT = Column(Unicode(3), nullable=False)
    DOCNUM = Column(Unicode(16), nullable=False)
    IDOCTYP = Column(Unicode(30), nullable=False)
    SNDPOR = Column(Unicode(10), nullable=False)
    SERIAL = Column(Unicode(20), nullable=False)
    FILENAME = Column(Unicode(512))
    FILESIZE = Column(BigInteger)
    MSG = Column(Unicode)
    ALREADY_DONE = Column(Integer)


class TEMPLATEFAV(Base):
    __tablename__ = "TEMPLATE_FAVS"
    __table_args__ = {"schema": "dbo"}

    TPFA_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer)
    TP_ID = Column(Integer)
    TP_DISABLED = Column(BIT, nullable=False)
    ROOT_FAWS_ID = Column(Integer)
    MD_ID = Column(Integer, nullable=False)


class TESTSAMPLECHARACTERISTICSHISTORY(Base):
    __tablename__ = "TESTSAMPLECHARACTERISTICS_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    TC_ID = Column(Integer, index=True)
    TC_NAME = Column(Unicode(2000))
    TC_VALUE = Column(Unicode(2000))
    TS_ID = Column(Integer)
    TS_DISABLED = Column(BIT)
    TC_NUMBER = Column(Integer)


class TESTSAMPLEPICTUREHISTORY(Base):
    __tablename__ = "TESTSAMPLEPICTURE_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    TSP_ID = Column(Integer, index=True)
    TS_ID = Column(Integer)
    TS_FILE = Column(Unicode(255))
    TS_DESCRIPTION = Column(Unicode(255))
    TS_DISABLED = Column(BIT)
    TSP_NUMBER = Column(Integer)


class TESTSAMPLEHISTORY(Base):
    __tablename__ = "TESTSAMPLE_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    TS_ID = Column(Integer)
    P_ID = Column(Integer, index=True)
    TS_PRODUCT = Column(Unicode(255))
    TS_MODEL = Column(Unicode(255))
    CU_ID = Column(Integer)
    TS_DATE_RECEIPT = Column(DateTime)
    TS_COUNT = Column(Integer)
    TS_FROM_MANUFACTURER = Column(BIT)
    PRP_ID = Column(Integer)
    TS_STORIX = Column(Unicode(10))
    TS_STORIXELEMENT = Column(Unicode(10))
    TS_INTEND_USE = Column(Unicode(2000))
    TS_INFO = Column(Unicode(2000))
    TS_DEFAULT_RETURN = Column(Integer)
    TS_DEFAULT_STORAGE = Column(DateTime)
    TS_COUNT_SHIPPED = Column(Integer)
    TS_COUNT_WASTE = Column(Integer)
    TS_COUNT_USE = Column(Integer)
    TS_DISABLED = Column(BIT)
    TS_UPDATEBY = Column(Integer)
    TS_UPDATE = Column(DateTime)
    TS_CREATEDBY = Column(Integer)
    TS_CREATED = Column(DateTime)
    TS_CREATEDBY_TEAM = Column(Integer)
    TS_UPDATEBY_TEAM = Column(Integer)
    AL_ID = Column(Integer)


class UCICONFIGURATION(Base):
    __tablename__ = "UCI_CONFIGURATION"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    DOCUMENTS_SERVICE_URL = Column(Unicode(256))
    DOCUMENTS_SERVICE_USER = Column(Unicode(256))
    DOCUMENTS_SERVICE_SECRET = Column(Unicode(256))
    NOTIFICATION_URL = Column(Unicode(256))
    NOTIFICATION_CLIENT_ID = Column(Unicode(256))
    NOTIFICATION_CLIENT_SECRET = Column(Unicode(256))
    ALLOWED_FILE_TYPES = Column(Unicode(512))
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)


class UCILOGDATUM(Base):
    __tablename__ = "UCI_LOG_DATA"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    OPERATION = Column(Unicode(64), nullable=False)
    PC_ID = Column(Integer)
    P_ID = Column(Integer)
    DOCUMENT_ID = Column(Integer)
    MESSAGE_ID = Column(Integer)
    MESSAGE_BY = Column(Unicode(111))
    MESSAGE_DATE = Column(DateTime)
    MESSAGE_TEXT = Column(Unicode(255))
    UPLOAD_EXTERNAL_ID = Column(Integer)
    UPLOAD_FILE_NAME = Column(Unicode(255))
    UPLOAD_FILE_SIZE = Column(Integer)
    UPLOAD_BY = Column(Unicode(111))
    UPLOAD_DATE = Column(DateTime)
    MDO_NUMBER = Column(Unicode(10))
    CREATED = Column(DateTime, nullable=False)
    TRANSFERRED_BY = Column(Unicode(128))
    RETURN_CODE = Column(Integer)
    SO_NUMBER = Column(Integer)


class USAGELOG(Base):
    __tablename__ = "USAGE_LOG"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    SCREEN_FUNCTION = Column(Unicode(1024), nullable=False)
    TRACK_ID = Column(BigInteger, nullable=False, index=True)
    WORKING_CLUSTER = Column(UNIQUEIDENTIFIER, nullable=False)
    CREATED = Column(DateTime, nullable=False)


class USERINFO(Base):
    __tablename__ = "USER_INFO"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    ENABLED = Column(BIT, nullable=False)
    MD_ID = Column(Integer, nullable=False)
    VALID_FROM = Column(DateTime, nullable=False)
    VALID_UNTIL = Column(DateTime, nullable=False)
    MESSAGE_EN = Column(Unicode(2000))
    MESSAGE_DE = Column(Unicode(2000))
    MESSAGE_FR = Column(Unicode(2000))
    INFO_EN = Column(Unicode(2000))
    INFO_DE = Column(Unicode(2000))
    INFO_FR = Column(Unicode(2000))


class VERIFICATIONDOCUMENTHISTORY(Base):
    __tablename__ = "VERIFICATION_DOCUMENT_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HISTORY_ID = Column(Integer, primary_key=True)
    HISTORY_TIMESTAMP = Column(DateTime, nullable=False)
    VD_ID = Column(Integer)
    P_ID = Column(Integer, index=True)
    VD_NAME = Column(Unicode(1024))
    VD_CATEGORY = Column(Integer)
    VD_CHECKED = Column(BIT)
    VD_SORT = Column(Integer)
    VD_DISABLED = Column(BIT)
    VD_CREATED = Column(DateTime)
    VD_CREATED_BY = Column(Integer)
    VD_UPDATED = Column(DateTime)
    VD_UPDATED_BY = Column(Integer)
    FROM_PS_CONFIG = Column(BIT)


t_V_ACCOUNTING_HISTORY = Table(
    "V_ACCOUNTING_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ACO_ID", Integer),
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("ACO_POS", Unicode(10)),
    Column("ACOT_ID", Integer),
    Column("ST_ID", Integer),
    Column("CC_ID", Unicode(10)),
    Column("ACO_DATE", DateTime),
    Column("ZP_ID", Unicode(3)),
    Column("ZO_ID", Unicode(3)),
    Column("ZP_LOCATION", NCHAR(2)),
    Column("ACO_UNITS", DECIMAL(18, 2)),
    Column("ACO_RATE", MONEY),
    Column("ACO_SPENDS", MONEY),
    Column("ACO_TOTAL", MONEY),
    Column("ACO_DESCRIPTION", Unicode(3500)),
    Column("ACO_INZARA", BIT),
    Column("CUR_ID", NCHAR(3)),
    Column("ACO_REGBY", Integer),
    Column("ACO_REGDATE", DateTime),
    Column("ACO_UPDATEBY", Integer),
    Column("ACO_UPDATE", DateTime),
    Column("ACO_DISABLED", BIT),
    Column("ACO_POSTINGSTATUS", Unicode(12)),
    Column("ZM_ID", Unicode(18)),
    Column("ACO_MEASURE", Unicode(3)),
    Column("ACO_RATE_BASECUR", MONEY),
    Column("ACO_SPENDS_BASECUR", MONEY),
    Column("ACO_TOTAL_BASECUR", MONEY),
    Column("ACO_IS_LEGACY", BIT),
    Column("ACTUAL_HOURS", DECIMAL(5, 2)),
    Column("TRAVELS", DECIMAL(8, 2)),
    Column("EXTERNALS", DECIMAL(8, 2)),
    Column("INVOICE_LOCK", BIT),
    Column("SYSTEM_MESSAGE", Unicode(512)),
    Column("ACO_IDOC_FILE", Unicode(50)),
    Column("REJECT_MESSAGE", Unicode(512)),
    Column("ACO_REGBY_TEAM", Integer),
    Column("ACO_UPDATEBY_TEAM", Integer),
    Column("ST_ID_TEAM", Integer),
    Column("AL_ID", Integer),
    Column("IDOC_ID", Integer),
    Column("ST_ID_SAPOK", Integer),
    Column("NONCLEARABLE", BIT),
    Column("INVOICE_TEXT", Unicode(512)),
    Column("ZAPFI_ID", Integer),
    Column("INVOICING_TRAVEL_COST", BIT),
    Column("RFAE_ID", Integer),
    Column("ACO_DIVERGENT_RATE", MONEY),
    Column("LAST_SAP_TRANSFER", DateTime),
    Column("NEXT_SAP_TRANSFER", DateTime),
    Column("IS_COLLECTIVE_POSTING", BIT),
    Column("STATUS_POSTED_DATE", DateTime),
    schema="dbo",
)


t_V_ACTION_HISTORY = Table(
    "V_ACTION_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("ACT_NUMBER", Integer),
    Column("ACT_DATE", DateTime),
    Column("ACT_NEWDATE", DateTime),
    Column("ST_ID", Integer),
    Column("ACTT_ID", Integer),
    Column("ACT_INFO", Unicode(512)),
    Column("ACT_FILE", Unicode(255)),
    Column("ACT_READY", SMALLDATETIME),
    Column("ACT_INTERNAL", BIT),
    Column("ACT_PREDATE", DateTime),
    Column("ACT_REMINDER", BIT),
    Column("ACT_PREDATEINFO", Unicode(255)),
    Column("ACT_REGBY", Integer),
    Column("ACT_REGDATE", DateTime),
    Column("ACT_UPDATEBY", Integer),
    Column("ACT_UPDATE", DateTime),
    Column("ACT_DISABLED", BIT),
    Column("REPORT_SENT", BIT),
    Column("ACT_FORECASTRELEVANT", BIT),
    Column("ACT_SO_DEADLINECONNECTION", BIT),
    Column("REMINDER_START_DATE", DateTime),
    Column("REMINDER_END_DATE", DateTime),
    Column("REMINDER_FREQUENCY", Integer),
    Column("REMINDER_LAST_SENT", DateTime),
    Column("ACT_ID", Integer),
    Column("REMINDER_CREATOR_IN_CC", BIT),
    schema="dbo",
)


t_V_ACTION_TYPE_HISTORY = Table(
    "V_ACTION_TYPE_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ACTT_ID", Integer),
    Column("ACTT_NAME_DE", Unicode(256)),
    Column("ACTT_NAME_EN", Unicode(256)),
    Column("ACTT_NAME_FR", Unicode(256)),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    Column("ACTT_LEVEL", Integer),
    schema="dbo",
)


t_V_ACTIVITY_TYPE = Table(
    "V_ACTIVITY_TYPE",
    metadata,
    Column("ID", BigInteger, nullable=False),
    Column("BOOKING_AREA", Unicode(4), nullable=False),
    Column("SKILLGROUP", Unicode(8), nullable=False),
    Column("ACTIVITY_TYPE_CODE", Unicode(32)),
    Column("DISABLED", Integer, nullable=False),
    Column("CREATED", DATETIME2),
    Column("CREATED_BY", BigInteger),
    Column("UPDATED", DATETIME2),
    Column("UPDATED_BY", BigInteger),
    schema="dbo",
)


t_V_CALENDAR_ENTRY_HISTORY = Table(
    "V_CALENDAR_ENTRY_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("ST_ID", Integer),
    Column("SUBJECT", Unicode(255)),
    Column("DESCRIPTION", Unicode(4000)),
    Column("START_TIME", DateTime),
    Column("END_TIME", DateTime),
    Column("ALL_DAY_EVENT", BIT),
    Column("DISABLED", BIT),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    Column("TRANSFER_STATUS", Integer),
    schema="dbo",
)


t_V_CERTIFICATE_CLIENT_HISTORY = Table(
    "V_CERTIFICATE_CLIENT_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("CERTIFICATE_ID", Integer),
    Column("TYPE", Integer),
    Column("CU_ID", Integer),
    Column("CBW_NUMBER", Integer),
    Column("NAME1", Unicode(40)),
    Column("NAME2", Unicode(40)),
    Column("NAME3", Unicode(40)),
    Column("NAME4", Unicode(40)),
    Column("STREET", Unicode(60)),
    Column("STREET_NUMBER", Unicode(10)),
    Column("STREET_ADDITION", Unicode(10)),
    Column("ADDITIONAL_STREET1", Unicode(40)),
    Column("ADDITIONAL_STREET2", Unicode(40)),
    Column("ADDITIONAL_STREET3", Unicode(40)),
    Column("ADDITIONAL_STREET4", Unicode(40)),
    Column("DISTRICT", Unicode(40)),
    Column("ZIP_CITY", Unicode(10)),
    Column("CITY", Unicode(40)),
    Column("COUNTRY_CODE", Unicode(3)),
    Column("ZIP_COMPANY", Unicode(10)),
    Column("SAP_NUMBER", Unicode(10)),
    Column("DEPARTMENT_NOTIFY", Unicode(8)),
    Column("DEPARTMENT_RESPONSIBLE", Unicode(8)),
    Column("KEY_ACCOUNT_MANAGER", Unicode(94)),
    Column("NUMBER_OF_EMPLOYEES", Integer),
    Column("PHONE", Unicode(48)),
    Column("FAX", Unicode(48)),
    Column("SALES_TAX_NUMBER", Unicode(64)),
    Column("EMAIL", Unicode(60)),
    Column("INFORMATION", Unicode(2000)),
    Column("COMPLETE_ADDRESS", Unicode(2000)),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    Column("SORT", Integer),
    schema="dbo",
)


t_V_CERTIFICATE_HISTORY = Table(
    "V_CERTIFICATE_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("NUMBER", Unicode(30)),
    Column("MAIN_CERTIFICATE", BIT),
    Column("TYPES", Unicode(256)),
    Column("HOLDER_CONTACT", Unicode(128)),
    Column("UNIT_FEES", Integer),
    Column("TECHNICAL_CERTIFIER", Unicode(60)),
    Column("TESTING_BASE", Unicode(256)),
    Column("PRODUCT", Unicode(4000)),
    Column("PRODUCT_ADDITIONAL", Unicode(120)),
    Column("MODELS", Unicode(4000)),
    Column("RESPONSIBLE_DEPARTMENT", Unicode(20)),
    Column("ISSUING_DEPARTMENT", Unicode(50)),
    Column("ISSUE_DATE", DateTime),
    Column("EXPIRATION_DATE", DateTime),
    Column("STATUS", Unicode(30)),
    Column("LAST_IMPORT_FROM_CBW", DateTime),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    schema="dbo",
)


t_V_CHANCES_HISTORY = Table(
    "V_CHANCES_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("CH_ID", Integer),
    Column("P_ID", Integer),
    Column("CHT_ID", Integer),
    Column("CH_INFO", Unicode(255)),
    Column("CH_DATE", DateTime),
    Column("CH_CHECKDATE", DateTime),
    Column("CH_CHECKBY", Integer),
    Column("CH_CHECKCOMMENT", Unicode(255)),
    Column("CH_DISABLED", BIT),
    Column("CH_CHECKBY_TEAM", Integer),
    Column("AL_ID", Integer),
    schema="dbo",
)


t_V_DISPO_HISTORY = Table(
    "V_DISPO_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("PROCESS", Integer),
    Column("ORDERING_PARTY", Integer),
    Column("MANUFACTURER", Integer),
    Column("IAN", Unicode(256)),
    Column("BATCH_NUMBER", Unicode(16)),
    Column("WEEK", Integer),
    Column("YEAR", Integer),
    Column("SHOPDATE", DateTime),
    Column("PRODUCT", Unicode(255)),
    Column("MODEL", Unicode(255)),
    Column("KEY2", Unicode(16)),
    Column("KEY3", Unicode(16)),
    Column("CATEGORY", Integer),
    Column("LIDL_QA_MEMBER", Integer),
    Column("CUSTOMERCONTACT", Integer),
    Column("LOTSIZE", Integer),
    Column("DISABLED", DateTime),
    Column("FILE_NAME", Unicode(256)),
    Column("FILE_CONTENT", LargeBinary),
    Column("READY_TO_SHOP", Integer),
    Column("PROCESSDESIGNATION", Unicode(255)),
    Column("WOC", UNIQUEIDENTIFIER),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    Column("ORDERDATE", DateTime),
    schema="dbo",
)


t_V_EDOC_B2B = Table(
    "V_EDOC_B2B",
    metadata,
    Column("EDOC_ITEM", Unicode),
    Column("EDOC_PHASE", Unicode(256)),
    Column("EDOC_REQUIREMENT", Unicode(2004)),
    Column("EDOC_RESULT", Unicode(4000)),
    Column("EDOC_VALUE", Unicode(5)),
    Column("SHOW_DOWNLOAD", Integer, nullable=False),
    Column("SHOW_UPLOAD", Integer, nullable=False),
    Column("EMIP_ID", Integer, nullable=False),
    Column("P_ID", Integer),
    Column("E_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_EDOC_B2B_ANNEX = Table(
    "V_EDOC_B2B_ANNEX",
    metadata,
    Column("EMIPA_ID", Integer, nullable=False),
    Column("EMIP_ID", Integer),
    Column("EMIPA_NAME_DE", Unicode(500)),
    Column("EMIPA_NAME_EN", Unicode(500)),
    Column("EMIPA_FILENAME", Unicode(255)),
    Column("EMIPA_CHECKSUM", Unicode(32)),
    Column("EMIPA_DATA", IMAGE),
    Column("EMIPA_UPLOAD", DateTime),
    Column("EMIPA_UPLOAD_BY", Integer),
    schema="dbo",
)


t_V_EDOC_BASE = Table(
    "V_EDOC_BASE",
    metadata,
    Column("B_ID", Integer, nullable=False),
    Column("STANDARDCODE", Unicode(512)),
    Column("B_NAME_DE", Unicode(512)),
    Column("B_NAME_EN", Unicode(512)),
    Column("BT_ID", Integer),
    Column("VALID_UNTIL", DATETIME2),
    Column("CREATED", DateTime, nullable=False),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DateTime, nullable=False),
    Column("UPDATED_BY", Integer),
    schema="dbo",
)


t_V_EDOC_DOMAIN = Table(
    "V_EDOC_DOMAIN",
    metadata,
    Column("ND_ID", Integer, nullable=False),
    Column("ND_SHORT", Unicode(10)),
    Column("VALID_UNTIL", DATETIME2),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    schema="dbo",
)


t_V_EDOC_HEADER = Table(
    "V_EDOC_HEADER",
    metadata,
    Column("HEAD_ID", Integer, nullable=False),
    Column("HEAD_NAME", Unicode(120)),
    Column("CREATED", DateTime, nullable=False),
    Column("CREATED_BY", Integer, nullable=False),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    schema="dbo",
)


t_V_EDOC_MODULE = Table(
    "V_EDOC_MODULE",
    metadata,
    Column("DM_ID", Integer, nullable=False),
    Column("DM_NAME", Unicode(255)),
    Column("DM_LETTER", Unicode(10)),
    Column("TPSC_ID", Integer),
    Column("TPT_ID", Integer),
    Column("HEAD_ID", Integer),
    Column("DM_IS_MASTER", BIT),
    Column("DM_NAME_EN", Unicode(255)),
    Column("ND_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_EDOC_MODULHISTORY = Table(
    "V_EDOC_MODULHISTORY",
    metadata,
    Column("MH_ID", Integer, nullable=False),
    Column("DM_ID", Integer),
    Column("MH_COMMENT", Unicode(1000)),
    Column("DM_VERSION", Integer),
    Column("MH_REG", DateTime),
    Column("MH_REGBY", Integer),
    schema="dbo",
)


t_V_EDOC_TABLE_TRANSEDOC = Table(
    "V_EDOC_TABLE_TRANSEDOC",
    metadata,
    Column("TE_ID", Integer, nullable=False),
    Column("TE_NAME", Unicode(50)),
    Column("HEAD_ID", Integer),
    Column("TE_YN_SYMBOL", BIT, nullable=False),
    Column("E_ID", Integer),
    schema="dbo",
)


t_V_EDOC_TABLE_TRANSEDOC_MODULE = Table(
    "V_EDOC_TABLE_TRANSEDOC_MODULE",
    metadata,
    Column("TEM_ID", Integer, nullable=False),
    Column("TE_ID", Integer, nullable=False),
    Column("TEM_NUMBER", Integer, nullable=False),
    Column("DM_ID", Integer, nullable=False),
    Column("TEM_NAME", Unicode(100)),
    schema="dbo",
)


t_V_EDOC_TABLE_TRANSEDOC_MODULE_PHASE = Table(
    "V_EDOC_TABLE_TRANSEDOC_MODULE_PHASE",
    metadata,
    Column("TEMP_ID", Integer, nullable=False),
    Column("TEM_ID", Integer, nullable=False),
    Column("TE_ID", Integer, nullable=False),
    Column("TEP_ID", Integer, nullable=False),
    Column("ST_ID", Integer, nullable=False),
    Column("SO_NUMBER", Integer),
    schema="dbo",
)


t_V_EDOC_TABLE_TRANSEDOC_PHASE = Table(
    "V_EDOC_TABLE_TRANSEDOC_PHASE",
    metadata,
    Column("TEP_ID", Integer, nullable=False),
    Column("TE_ID", Integer, nullable=False),
    Column("PRP_ID", Integer, nullable=False),
    Column("TEP_PHASE_ORDER", Integer, nullable=False),
    Column("P_ID", Integer),
    Column("TEP_SAP", Unicode(20)),
    schema="dbo",
)


t_V_FAZ_HISTORY = Table(
    "V_FAZ_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("FAZ_ID", Integer),
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("FAZ_CERTNUMBER", Unicode(30)),
    Column("FAZ_REMARK", Unicode(255)),
    Column("FAZ_CLEAR", Unicode(255)),
    Column("FAZ_DATE", DateTime),
    Column("FAZ_BY", Unicode(30)),
    Column("FAZ_DISABLED", BIT),
    Column("ZETY_TYP", Unicode(100)),
    Column("FAZ_PSOBJECT_TERM", Unicode(50)),
    Column("FAZ_CERT_OWNER", Integer),
    Column("TS_ID", Integer),
    Column("FAZ_POSTING_STATUS", Unicode(50)),
    Column("RM_ID", Integer),
    schema="dbo",
)


t_V_FOCUSDOCUMENT_HISTORY = Table(
    "V_FOCUSDOCUMENT_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("PROJECT", Integer),
    Column("SUBORDER", Integer),
    Column("PATH", Unicode(1024)),
    Column("NAME", Unicode(1024)),
    Column("FOCUS", BIT),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    Column("DISABLED", DateTime),
    schema="dbo",
)


t_V_GMA_ENTRY_HISTORY = Table(
    "V_GMA_ENTRY_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DATETIME2, nullable=False),
    Column("INSERTED_HIST_DB", DATETIME2),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("COUNTRY_ID", Integer),
    Column("STATUS_ID", Integer),
    Column("RESULT_ID", Integer),
    Column("COMMENT", Unicode(256)),
    Column("STATUS_DATE", Date),
    Column("DISABLED", BIT),
    Column("CREATED", DATETIME2),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DATETIME2),
    Column("UPDATED_BY", Integer),
    schema="dbo",
)


t_V_KUNDE_PARTNER = Table(
    "V_KUNDE_PARTNER",
    metadata,
    Column("ID", BigInteger, nullable=False),
    Column("CU_ID", Integer, nullable=False),
    Column("VTWEG", NCHAR(2), nullable=False),
    Column("PARVW", NCHAR(2), nullable=False),
    Column("KUNN2", Integer),
    Column("PARNR", Integer),
    Column("PHASE", Integer),
    schema="dbo",
)


t_V_LAGER = Table(
    "V_LAGER",
    metadata,
    Column("LG_ID", Integer, nullable=False),
    Column("LG_EINGANG", DateTime),
    Column("LG_ERF_USER", Unicode(60)),
    Column("LG_ERF_DATUM", DateTime),
    Column("LG_AEND_USER", Unicode(60)),
    Column("LG_AEND_DATUM", DateTime),
    Column("LG_PRODUKT", Unicode(255)),
    Column("LG_MODELL", Unicode(255)),
    Column("LG_KUNDE_NAME", Unicode(40)),
    Column("LG_KUNDE_STR", Unicode(40)),
    Column("LG_KUNDE_PLZ", Unicode(10)),
    Column("LG_KUNDE_ORT", Unicode(40)),
    Column("LG_KUNDE_LAND", Unicode(3)),
    Column("LG_MASTERPROJECT", Integer),
    schema="dbo",
)


t_V_LAGERELEMENT = Table(
    "V_LAGERELEMENT",
    metadata,
    Column("LGEL_ID", Integer, nullable=False),
    Column("LGEL_NR", Integer),
    Column("LG_ID", Integer),
    Column("LGEL_BEZEICHNUNG", Unicode(255)),
    Column("LGEL_ZUSTAND", Unicode(255)),
    Column("LGEL_ARCHIV", DateTime),
    Column("LGEL_ARCHIVIERT", BIT, nullable=False),
    Column("LGEL_LAGERTERMIN", DateTime),
    Column("LGEL_NACHLAGERTERMIN", Unicode(60)),
    Column("LGEL_ERLEDIGT", BIT, nullable=False),
    Column("BR_SHORT", Unicode(5)),
    Column("LGEL_LAGERORT", Unicode(60)),
    Column("LGEL_AEND_USER", Unicode(60)),
    Column("LGEL_AEND_DATUM", DateTime),
    Column("LGEL_ERF_USER", Unicode(60)),
    Column("LGEL_ERF_DATUM", DateTime),
    Column("LGEL_SERIENNUMMER", Unicode(60)),
    Column("LGEL_STORIXREFERENZ", Unicode(255)),
    Column("LGEL_ARCHIVLAGER", Unicode(60)),
    Column("LGEL_BEMERKUNG", Unicode(255)),
    Column("LGEL_VERANTWORTLICH", Unicode(60)),
    Column("LGEL_ENDE_DURCH", Integer),
    Column("LGEL_VERSANDADRESSE", Unicode(255)),
    Column("LGEL_PROJEKTLEITER", Unicode(60)),
    Column("LGEL_PSEX", Integer),
    Column("LGEL_RESERVIERT_VON", Unicode(60)),
    Column("LGEL_RESERVIERT_AM", DateTime),
    Column("LGEL_AUFTRAGSNR", Unicode(60)),
    Column("LGEL_AUFTRAGGEBER", Unicode(60)),
    Column("LGEL_AUFTRAGGEBER_KNR", Unicode(20)),
    Column("RV_KOMMENTAR", Unicode(255)),
    Column("RV_ID", Integer),
    Column("B_BESTELLT_VON", Unicode(60)),
    Column("B_BESTELLT_AM", DateTime),
    Column("B_BESTELLT_FUER", Unicode(60)),
    Column("B_KOMMENTAR", Unicode(500)),
    Column("DBZ_ID", Integer),
    Column("B_ID", Integer),
    Column("DBZ_NAME", Unicode(100)),
    Column("LGEL_ZUSTAND_DE", Unicode(60)),
    Column("LGEL_ZUSTAND_EN", Unicode(60)),
    Column("LGEL_ZUSTAND_FR", Unicode(60)),
    Column("LGEL_NACHLAGERTERMIN_DE", Unicode(60)),
    Column("LGEL_NACHLAGERTERMIN_EN", Unicode(60)),
    Column("LGEL_NACHLAGERTERMIN_FR", Unicode(60)),
    Column("DZU_ID", Integer),
    Column("DRV_ID", Integer),
    schema="dbo",
)


t_V_LAGER_DEFAULT_ARCHIVLAGER = Table(
    "V_LAGER_DEFAULT_ARCHIVLAGER",
    metadata,
    Column("DAR_ID", Integer, nullable=False),
    Column("DAR_BEZ_DE", Unicode(60)),
    Column("DAR_BEZ_EN", Unicode(60)),
    Column("DAR_BEZ_FR", Unicode(60)),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer, nullable=False),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer, nullable=False),
    schema="dbo",
)


t_V_LAGER_DEFAULT_RUECKVERSAND = Table(
    "V_LAGER_DEFAULT_RUECKVERSAND",
    metadata,
    Column("DRV_ID", Integer, nullable=False),
    Column("DRV_BEZ_DE", Unicode(60)),
    Column("DRV_BEZ_EN", Unicode(60)),
    Column("DRV_BEZ_FR", Unicode(60)),
    Column("DRV_DEFAULT", BIT),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer, nullable=False),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer, nullable=False),
    schema="dbo",
)


t_V_LAGER_ZUSTAND = Table(
    "V_LAGER_ZUSTAND",
    metadata,
    Column("DZU_ID", Integer, nullable=False),
    Column("DZU_BEZ_DE", Unicode(60)),
    Column("DZU_BEZ_EN", Unicode(60)),
    Column("DZU_BEZ_FR", Unicode(60)),
    Column("DZU_DEFAULT", BIT),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer, nullable=False),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer, nullable=False),
    schema="dbo",
)


t_V_MACHINE_POSTINGS = Table(
    "V_MACHINE_POSTINGS",
    metadata,
    Column("NAME", Unicode(112)),
    Column("POSTINGTYPE_DE", Unicode(256), nullable=False),
    Column("POSTINGTYPE_EN", Unicode(256), nullable=False),
    Column("POSTINGDATE", DateTime),
    Column("SAPNO", Unicode(10)),
    Column("ITEM", Unicode(10)),
    Column("PROJNO", Integer, nullable=False),
    Column("SO", Integer, nullable=False),
    Column("HOURS", DECIMAL(18, 2)),
    Column("UNITS", DECIMAL(18, 2)),
    Column("MEASURE", Unicode(3)),
    Column("RATE", MONEY),
    Column("EXPENDITURE", MONEY),
    Column("GRANDTOTAL", MONEY),
    Column("CURRENCY", NCHAR(3)),
    Column("MATERIALCODE", Unicode(18)),
    Column("DESCRIPTION", Unicode(3500)),
    Column("INZARA", Unicode(1), nullable=False),
    Column("ORDERINGPARTY", Unicode(165), nullable=False),
    Column("STID", Integer, nullable=False),
    Column("WOC", UNIQUEIDENTIFIER),
    schema="dbo",
)


t_V_MHS_PROJECTDATA_CODE_HISTORY = Table(
    "V_MHS_PROJECTDATA_CODE_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("MHSPROJECTDATA", Integer),
    Column("CODE", Integer),
    schema="dbo",
)


t_V_MHS_PROJECTDATA_HISTORY = Table(
    "V_MHS_PROJECTDATA_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("PROJECT", Integer),
    Column("JUSTIFICATION", Unicode),
    Column("DEVICE", Integer),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    schema="dbo",
)


t_V_PORTAL = Table(
    "V_PORTAL",
    metadata,
    Column("Prozess", Integer),
    Column("Projekt", Integer),
    Column("Produkt", Unicode(255)),
    Column("Modell", Unicode(255)),
    Column("Auftragstext", Unicode(2048)),
    Column("Hersteller", Unicode(165)),
    Column("Fertigstellung", DateTime),
    Column("Manager", Unicode(112)),
    Column("Los", Integer),
    Column("Statustext", String(17, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Bezeichnung", Unicode(255)),
    Column("Ladentermin", DateTime),
    Column("Hauptkunde", Integer, nullable=False),
    Column("Zulieferer", Integer, nullable=False),
    Column("VisibleFor", Integer),
    Column("Auftragsnummer", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("ZeigeAuftragsnummer", Integer, nullable=False),
    schema="dbo",
)


t_V_PORTAL_ID = Table(
    "V_PORTAL_ID",
    metadata,
    Column("PORTAL_ID", Integer, nullable=False),
    Column("PORTAL_NAME", Unicode(64), nullable=False),
    Column("SUPPLIER_ID", Integer, nullable=False),
    Column("SUPPLIER_NAME", Unicode(64), nullable=False),
    schema="dbo",
)


t_V_PORTAL_OVERVIEW = Table(
    "V_PORTAL_OVERVIEW",
    metadata,
    Column("FULL_USER_NAME", Unicode(256), nullable=False),
    Column("PORTAL_ID", Integer, nullable=False),
    Column("PORTAL_NAME", Unicode(64), nullable=False),
    Column("Parent", Integer),
    schema="dbo",
)


t_V_PROCESSFOLDER_HISTORY = Table(
    "V_PROCESSFOLDER_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("PCF_ID", Integer),
    Column("PZ_ID", Integer),
    Column("TPT_ID", Integer),
    Column("PCF_VERSION", Integer),
    Column("PCF_CURRENTVERSION", BIT),
    Column("PCF_FILENAME", Unicode(255)),
    Column("PCF_COMMENT", Unicode(255)),
    Column("PCF_REGDATE", DateTime),
    Column("PCF_REGBY", Integer),
    Column("PCF_UPDATE", DateTime),
    Column("PCF_UPDATEBY", Integer),
    Column("PCF_CHECKOUTBY", Integer),
    Column("PCF_CHECKOUT", DateTime),
    Column("PCF_WEBNAME", Unicode(255)),
    Column("PCF_CHECKOUTBY_TEAM", Integer),
    Column("PCF_REGBY_TEAM", Integer),
    Column("PCF_UPDATEBY_TEAM", Integer),
    Column("AL_ID", Integer),
    schema="dbo",
)


t_V_PROCESSPORTAL_FILES_HISTORY = Table(
    "V_PROCESSPORTAL_FILES_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("PZPF", Integer),
    Column("PZPI_ID", Integer),
    Column("PZ_ID", Integer),
    Column("P_ID", Integer),
    Column("PZPF_PATH", Unicode(255)),
    Column("PZPF_EXIST", BIT),
    Column("PZPF_EXTERNAL_ID", Integer),
    Column("PZPF_FILE_SIZE", Integer),
    schema="dbo",
)


t_V_PROCESSPORTAL_IN_HISTORY = Table(
    "V_PROCESSPORTAL_IN_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("PZPI_ID", Integer),
    Column("PZ_ID", Integer),
    Column("P_ID", Integer),
    Column("PZPI_NAME", Unicode(60)),
    Column("PZPI_COMPANY", Unicode(90)),
    Column("PZPI_CUST_TEXT", Unicode(1000)),
    Column("PZPI_REGDATE", DateTime),
    Column("PZPI_COMMENT", Unicode(255)),
    Column("PZPI_PROCESSED_BY", Integer),
    Column("PZPI_PROCESSED_DATE", DateTime),
    Column("SEND_NOTIFICATION", BIT),
    Column("NOTIFICATION_SENT", DateTime),
    schema="dbo",
)


t_V_PROCESS_FILES_HISTORY = Table(
    "V_PROCESS_FILES_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("PCF_ID", BigInteger),
    Column("PC_ID", Integer),
    Column("P_ID", Integer),
    Column("PCF_FOLDER", Unicode(255)),
    Column("PCF_DATE", DateTime),
    Column("PRP_ID", Integer),
    Column("PCF_FILE", Unicode(255)),
    Column("PCF_PATH", Unicode(255)),
    Column("PCF_LAST_TRANSFER", DateTime),
    Column("PCF_SOURCE", Unicode(2056)),
    schema="dbo",
)


t_V_PROCESS_HISTORY = Table(
    "V_PROCESS_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("PC_ID", Integer),
    Column("PC_WC_ID", UNIQUEIDENTIFIER),
    Column("PC_CLIENT", Integer),
    Column("PC_PRODUCT", Unicode(255)),
    Column("PC_MODEL", Unicode(255)),
    Column("PC_NAME", Unicode(255)),
    Column("PC_ORDERTEXT", Unicode(255)),
    Column("PC_PROJECTMANAGER", Integer),
    Column("PC_LOTSIZE", Integer),
    Column("PC_STATUS", Integer),
    Column("PC_READY_TO_SHOP", Integer),
    Column("PC_SHOPDATE", DateTime),
    Column("PC_PATH", Unicode(50)),
    Column("PC_FILE_MEASUREMENT", Unicode(255)),
    Column("PC_FILE_DOCS", Unicode(255)),
    Column("PC_REGDATE", DateTime),
    Column("PC_CREATEDBY", Integer),
    Column("PC_UPDATE", DateTime),
    Column("PC_UPDATEBY", Integer),
    Column("PC_DISABLED", BIT),
    Column("PC_VISIBLE_FOR", Integer),
    Column("PC_CREATEDBY_TEAM", Integer),
    Column("PC_UPDATEBY_TEAM", Integer),
    Column("AL_ID", Integer),
    Column("PC_REPEATER_OF", Integer),
    Column("PC_CERT_TYPE", Unicode(255)),
    Column("PC_IAN", Unicode(256)),
    Column("PC_LIDL_QA_MEMBER", Unicode(256)),
    Column("PROTOCOL_PROJECT", Integer),
    Column("PC_KEY2", Unicode(16)),
    Column("PC_KEY3", Unicode(16)),
    Column("FILE_FORMAT", Integer),
    Column("ARCHIVING_STATUS", Unicode(32)),
    Column("PC_PROJECTMANAGER_TEAM", Integer),
    Column("IS_FST_PROCESS", BIT),
    Column("FACILITY_NUMBER", Integer),
    Column("NACE_CODE", Unicode(256)),
    Column("COLLECTIVE_INVOICE_SENT", DateTime),
    Column("BATCH_NUMBER", Unicode(16)),
    Column("DISCOUNT_PERCENTAGE", DECIMAL(19, 10)),
    schema="dbo",
)


t_V_PROJECT_ADDON_HISTORY = Table(
    "V_PROJECT_ADDON_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("PA_ID", Integer),
    Column("P_ID", Integer),
    Column("PA_DISPATCHER", Integer),
    Column("OC_ID", Integer),
    Column("PA_PART_NUMBER", Unicode(255)),
    Column("PA_RFN", Unicode(255)),
    Column("PA_MANUFACTURER_NUMBER", Unicode(255)),
    Column("PA_DRAFT_NUMBER", Unicode(255)),
    Column("RRTB_ID", Integer),
    Column("PCAT_ID", Integer),
    Column("PMOD_ID", Integer),
    Column("PA_MAIN_DIMENSIONS", Unicode(255)),
    Column("CERT_APPL_ID", Integer),
    Column("PA_OPERATORS_IDENTIFICATION", Unicode(255)),
    Column("PA_BUILDING", Unicode(255)),
    schema="dbo",
)


t_V_PROJECT_ADDON_ROOMSPECIFICDATA_HISTORY = Table(
    "V_PROJECT_ADDON_ROOMSPECIFICDATA_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("PAR_ID", Integer),
    Column("P_ID", Integer),
    Column("PAR_COLUMN", Integer),
    Column("RD_ID", Integer),
    Column("PAR_PRESSURE", Unicode(50)),
    Column("PU_ID", Integer),
    Column("PAR_TEMPERATURE", Unicode(50)),
    Column("PAR_VOLUME", Unicode(50)),
    Column("PAR_VOLUME_UNIT", Unicode(50)),
    Column("PAR_MEDIUM", Unicode(50)),
    Column("SOA_ID", Integer),
    Column("PAR_SUBSTANCE1", Unicode(50)),
    Column("PAR_SUBSTANCE2", Unicode(50)),
    Column("PAR_CATEGORY_ID", Integer),
    Column("PAR_FLUIDGROUP_ID", Integer),
    schema="dbo",
)


t_V_PROJECT_APPLICATION_FORM_HISTORY = Table(
    "V_PROJECT_APPLICATION_FORM_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DATETIME2, nullable=False),
    Column("INSERTED_HIST_DB", DATETIME2),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("P_ID", Integer),
    Column("APPLICATION_FORM", Integer),
    Column("DISABLED", BIT),
    Column("CREATED", DATETIME2),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DATETIME2),
    Column("UPDATED_BY", Integer),
    schema="dbo",
)


t_V_PROJECT_CONTACT_HISTORY = Table(
    "V_PROJECT_CONTACT_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("PRC_ID", Integer),
    Column("PRC_P_ID", Integer),
    Column("PRC_TYPE", NCHAR(1)),
    Column("PRC_CU_ID", Integer),
    Column("PRC_CUC_ID", Integer),
    Column("PRC_ORDER_ID", Integer),
    Column("PRC_LAST_UPDATED", DateTime),
    Column("PRC_SO_NUMBER", Integer),
    schema="dbo",
)


t_V_PROJECT_FAILURE_REL_HISTORY = Table(
    "V_PROJECT_FAILURE_REL_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("FAIL_ID", Integer),
    schema="dbo",
)


t_V_PROJECT_HISTORY = Table(
    "V_PROJECT_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("P_ID", Integer),
    Column("MD_ID", Integer),
    Column("PC_ID", Integer),
    Column("P_ZARA_NUMBER", Unicode(10)),
    Column("P_NAME_IS_ZARA", BIT),
    Column("P_NAME", Unicode(100)),
    Column("P_FOLDER", Unicode(255)),
    Column("P_CUSTOMER_A", Integer),
    Column("P_CUSTOMER_B", Integer),
    Column("P_CUSTOMER_O", Integer),
    Column("P_CUST_A_IS_PRODUCER", BIT),
    Column("P_CONTACT", Unicode(255)),
    Column("P_PRODUCT", Unicode(255)),
    Column("P_MODEL", Unicode(255)),
    Column("P_PROJECTMANAGER", Integer),
    Column("P_HANDLEDBY", Integer),
    Column("P_STATUS", Integer),
    Column("P_RETEST", Integer),
    Column("P_RETEST_OF", Integer),
    Column("P_DATE_APPOINTMENT", DateTime),
    Column("P_FOCUSDOCUMENT", Unicode(255)),
    Column("P_COMMENT", Unicode(50)),
    Column("P_DATE_READY", DateTime),
    Column("P_READYBY", Integer),
    Column("P_DATE_CHECK", DateTime),
    Column("P_CHECKBY", Integer),
    Column("P_DATE_ORDER", DateTime),
    Column("P_DEADLINE", DateTime),
    Column("P_DATE_DISPO", DateTime),
    Column("P_DATE_DONE", DateTime),
    Column("P_DONEBY", Integer),
    Column("RES_ID", Integer),
    Column("P_DELAY", DECIMAL(18, 0)),
    Column("DELR_ID", Integer),
    Column("P_ORDERTEXT", Unicode(2048)),
    Column("P_PROJECTINFO", Unicode(4000)),
    Column("P_TOKEN", Unicode(60)),
    Column("P_KIND_OF_PRODUCER", Integer),
    Column("KOT_ID", Integer),
    Column("KOB_ID", Integer),
    Column("P_ACTION", BIT),
    Column("P_URGENT", BIT),
    Column("P_DOCTYPE", Integer),
    Column("P_ORDERSIZE", DECIMAL(18, 2)),
    Column("P_INVOICE", DECIMAL(18, 2)),
    Column("P_SALERATE", DECIMAL(18, 2)),
    Column("P_USE_PLAN", BIT),
    Column("P_PLAN_SPENDS", DECIMAL(18, 10)),
    Column("P_PLAN_EXTERNAL", DECIMAL(18, 10)),
    Column("P_PLAN_SUBORDER", DECIMAL(18, 10)),
    Column("P_PLAN_TRAVEL", MONEY),
    Column("P_PLAN_LICENCE", DECIMAL(18, 10)),
    Column("P_FACTOR", DECIMAL(18, 2)),
    Column("P_ACC_SALE", DECIMAL(18, 10)),
    Column("P_ACC_LAB", DECIMAL(18, 10)),
    Column("P_ACC_SAFETY", DECIMAL(18, 10)),
    Column("P_ACC_SALERATE", MONEY),
    Column("P_ACC_SPENDS", MONEY),
    Column("P_ACC_EXTERNAL", MONEY),
    Column("P_ACC_SUBORDER", MONEY),
    Column("P_ACC_TRAVEL", MONEY),
    Column("P_ACC_LICENCE", MONEY),
    Column("P_ACC_INTERNAL", MONEY),
    Column("P_HOURLY_RATE", DECIMAL(18, 10)),
    Column("P_FORECAST", DECIMAL(18, 2)),
    Column("P_TO_WEB", BIT),
    Column("P_TO_CDS", BIT),
    Column("P_INTERN", BIT),
    Column("P_PREDATE", DateTime),
    Column("P_PREDATE_REMINDER", BIT),
    Column("P_PREDATEINFO", Unicode(255)),
    Column("P_PROCESSPHASE", Integer),
    Column("P_REGBY", Integer),
    Column("P_REGDATE", DateTime),
    Column("P_UPDATEBY", Integer),
    Column("P_UPDATE", DateTime),
    Column("P_ORDER_ORIGIN", Unicode(20)),
    Column("P_TRANSFERPROJECT", Integer),
    Column("P_TRANSFERSUBORDER", Integer),
    Column("P_EU_TS_ID", Integer),
    Column("P_TRANSFERUACONTACT", Integer),
    Column("P_TRANSFERUADEPARTMENT", Integer),
    Column("P_TRANSFERUA_REGION_ID", Integer),
    Column("P_TRANSFERUASTATUS", NCHAR(1)),
    Column("P_TRANSFERUASOURCEPATH", NCHAR(1)),
    Column("P_TRANSFERROOTSERVERID", Integer),
    Column("P_TRANSFERACTIONNUMBER", Integer),
    Column("P_DISABLED", BIT),
    Column("P_CURRENCYRATE", DECIMAL(18, 0)),
    Column("P_WC_ID", UNIQUEIDENTIFIER),
    Column("P_CONTACTPERSON_REGIONID", UNIQUEIDENTIFIER),
    Column("P_ASSIGNEDPERSON_TEAMID", UNIQUEIDENTIFIER),
    Column("P_PSOBJECT_TERM", Unicode(50)),
    Column("P_CUR_ID", NCHAR(3)),
    Column("P_CUR_SHORT", NCHAR(3)),
    Column("P_PSOBJECT_LANGUAGEID", Integer),
    Column("P_FOLDER_OLD", NCHAR(1)),
    Column("P_PROJECTFOLDERCREATED", BIT),
    Column("P_IS_LEGACY", BIT),
    Column("P_CBW_EXPORT", Unicode(6)),
    Column("P_ACC_MAINPOS", Unicode(8)),
    Column("P_PRODGRP_ID", Integer),
    Column("P_PRODGRP2_ID", Integer),
    Column("P_PRODUCT2", Unicode(255)),
    Column("P_DOCU_DONE", BIT),
    Column("PLAN_ACTUAL_HOUR", DECIMAL(18, 2)),
    Column("ACC_ACTUAL_HOUR", DECIMAL(18, 2)),
    Column("ORDER_POSITION", Unicode(6)),
    Column("P_CUSTOMER_R", Integer),
    Column("E_ID", Integer),
    Column("P_CHECKBY_TEAM", Integer),
    Column("P_DONEBY_TEAM", Integer),
    Column("P_HANDLEDBY_TEAM", Integer),
    Column("P_PROJECTMANAGER_TEAM", Integer),
    Column("P_READYBY_TEAM", Integer),
    Column("P_REGBY_TEAM", Integer),
    Column("P_UPDATEBY_TEAM", Integer),
    Column("AL_ID", Integer),
    Column("P_TUV_CERT_EXISTS", BIT),
    Column("P_EXTERNAL_CERT_EXISTS", BIT),
    Column("P_CERT_COMMENT", Unicode(512)),
    Column("P_IS_QUOTATION", BIT),
    Column("P_IS_OLD_PROJECT", BIT),
    Column("P_QUOTATION_PROBABILITY", DECIMAL(18, 2)),
    Column("P_QUOTATION_VALID_UNTIL", DateTime),
    Column("P_EXPECTED_TS_RECEIPT", DateTime),
    Column("P_NUMBER_OF_TESTSAMPLES", Integer),
    Column("CC_ID", Unicode(10)),
    Column("P_INVOICE_RECIPIENT", Integer),
    Column("P_QUOTATION_LINK", Integer),
    Column("P_RESPONSIBLE_AGENT", Integer),
    Column("P_SALES_REPRESENTATIVE", Integer),
    Column("P_SIGNATURE_LEFT", Integer),
    Column("P_VERTRIEBSWEG", Integer),
    Column("P_STDSATZ", DECIMAL(18, 2)),
    Column("P_POSTINGS_ALLOWED", BIT),
    Column("P_PLANNED_ORDERSIZE", DECIMAL(18, 2)),
    Column("TC_P_ID", Integer),
    Column("BANF_REQUEST", DateTime),
    Column("BANF_ORDER", DateTime),
    Column("P_ABGS", BIT),
    Column("P_VORK", BIT),
    Column("P_PROJECT_NUMBER", Unicode(50)),
    Column("SAP_QUOTATION_NUMBER", Unicode(10)),
    Column("P_TS_RECEIPT_ADVISED", BIT),
    Column("P_IC", NCHAR(2)),
    Column("P_SAP_INDUSTRY", Unicode(3)),
    Column("P_FOREIGN_CURRENCY", NCHAR(3)),
    Column("P_EXCHANGE_RATE", DECIMAL(18, 10)),
    Column("P_GLOBAL_PARTNER", Integer),
    Column("P_PRICING_DATE", DateTime),
    Column("P_CLIENT_REMARK", Unicode(2048)),
    Column("P_CONTACT_CUC_ID", Integer),
    Column("P_REMARK", Unicode(1024)),
    Column("P_OTC_NAME_1", Unicode(40)),
    Column("P_OTC_NAME_2", Unicode(40)),
    Column("P_OTC_NAME_AT", Unicode(40)),
    Column("P_OTC_NAME_CP", Unicode(35)),
    Column("P_OTC_CO", Unicode(40)),
    Column("P_OTC_STREET_1", Unicode(35)),
    Column("P_OTC_STREET_2", Unicode(40)),
    Column("P_OTC_STREET_3", Unicode(40)),
    Column("P_OTC_STREET_4", Unicode(40)),
    Column("P_OTC_STREET_5", Unicode(40)),
    Column("P_OTC_PO_BOX", Unicode(10)),
    Column("P_OTC_POSTAL_CODE", Unicode(10)),
    Column("P_OTC_CITY_1", Unicode(40)),
    Column("P_OTC_CITY_2", Unicode(40)),
    Column("P_OTC_REGION", Unicode(3)),
    Column("P_OTC_COUNTRY", Unicode(3)),
    Column("P_SIGNATURE_RIGHT", Integer),
    Column("P_WARRANTY_INFO", Unicode(2048)),
    Column("CRM_ID", Unicode(16)),
    Column("RUN_ID", Integer),
    Column("P_B2B", BIT),
    Column("P_COORDINATOR", Integer),
    Column("P_COORDINATOR_TEAM", Integer),
    Column("P_OTHER_DELAY_REASON", Unicode(256)),
    Column("P_AUDIT_DATE", DateTime),
    Column("P_AUDIT_DATE_IS_CONFIRMED", BIT),
    Column("P_AUDIT_DATE_LINKED_SUBORDER", Integer),
    Column("P_DATE_ROLLUP", DateTime),
    Column("STARLIMS_SITE", Unicode(20)),
    Column("STARLIMS_ATTENTION", Unicode(255)),
    Column("STARLIMS_BUSINESS_TYPE", Unicode(50)),
    Column("STARLIMS_SERVICE_TYPE", Unicode(50)),
    Column("FROM_STARLIMS", BIT),
    Column("REGULATOR", Integer),
    Column("GOODS_RECIPIENT", Integer),
    Column("CONTACT_PERSON_INVOICE_RECIPIENT", Integer),
    Column("STARLIMS_PC", Integer),
    Column("FILE_FORMAT", Integer),
    Column("ARCHIVING_STATUS", Unicode(32)),
    Column("P_TEAM_ID", UNIQUEIDENTIFIER),
    Column("P_RESY_FACTOR", Unicode(5)),
    Column("SALES_PACKAGE_PRICE", DECIMAL(18, 2)),
    Column("P_VISIBLE_FOR", Integer),
    Column("STARLIMS_CONNECTION_TYPE", Integer),
    Column("CONTRACT_TYPE", Integer),
    Column("PERFORM_SURVEY", BIT),
    Column("SURVEY_REJECT_REASON", Unicode(512)),
    Column("SURVEY_SENT", DateTime),
    Column("MANUFACTURER_CONTACT", Integer),
    Column("REPORT_RECIPIENT_CONTACT", Integer),
    Column("CRM_STATUS", Integer),
    Column("CRM_TRANSFER_DATE", DateTime),
    Column("P_INVOICE_WAS_SET", BIT),
    Column("P_IAN", Unicode(256)),
    Column("TRANSFER_FIXED_PRICE_TO_SAP", BIT),
    Column("COLLECTIVE_INVOICE", BIT),
    Column("CATEGORY_ID", Integer),
    Column("P_POSTING_DONE_DATE", DateTime),
    Column("P_DATE_READY_REASON", Unicode(512)),
    Column("P_DATE_READY_CHANGED", DateTime),
    Column("P_DATE_CHECK_REASON", Unicode(512)),
    Column("P_DATE_CHECK_CHANGED", DateTime),
    Column("P_INTERNATIONAL", BIT),
    Column("REPORT_SENT", DateTime),
    Column("BATCH_NUMBER", Unicode(16)),
    Column("COLLECTIVE_INVOICE_SENT", DateTime),
    Column("PROJECT_TYPE", Integer),
    Column("OPPORTUNITY_ID", Unicode(10)),
    Column("NECESSARY_DOCUMENTATION_AVAILABLE", BIT),
    Column("SAP_ORDER_TYPE", Unicode(8)),
    Column("P_DEPARTMENT_ID", UNIQUEIDENTIFIER),
    Column("P_CONFIDENTIAL", BIT),
    Column("P_TEMPLATEID", Integer),
    Column("PRINT_OPTION", Unicode(3)),
    Column("UNLIMITED_LIABILITY", BIT),
    Column("SERVICE_RENDERED_DATE", Date),
    schema="dbo",
)


t_V_PROJECT_POSITION_HISTORY = Table(
    "V_PROJECT_POSITION_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("PP_ID", Integer),
    Column("P_ID", Integer),
    Column("PP_IS_QUOTATION_POSITION", BIT),
    Column("PP_NUMBER", Integer),
    Column("PP_DISABLED", BIT),
    Column("PP_STATUS", Integer),
    Column("PP_STATUS_CHANGED_ON", DateTime),
    Column("PP_STATUS_CHANGED_BY", Integer),
    Column("PP_TEXT", Unicode(4000)),
    Column("PP_SALES_PRICE", DECIMAL(18, 2)),
    Column("ZM_ID", Unicode(18)),
    Column("PP_TYPE", Integer),
    Column("PP_LAST_SAP_UPDATE", DateTime),
    Column("PP_CANCELLATION_FLAG", BIT),
    Column("PP_CREATED", DateTime),
    Column("PP_CREATED_BY", Integer),
    Column("PP_UPDATED", DateTime),
    Column("PP_UPDATED_BY", Integer),
    Column("PP_PREPAYMENT_PRICE", DECIMAL(18, 2)),
    Column("PP_PRINTING_FLAG", Unicode(5)),
    Column("PP_SINGLE_PRICE", DECIMAL(18, 2)),
    Column("PP_TARGET_COUNT", DECIMAL(18, 2)),
    Column("PP_SP_FOREIGN", DECIMAL(18, 2)),
    Column("FROM_PS_CONFIG", BIT),
    Column("PP_UNIT", Unicode(3)),
    Column("FROM_STARLIMS", BIT),
    Column("PP_FI_FACTOR", Unicode(5)),
    Column("PP_INTERNAL_NOTE", Unicode(1024)),
    Column("PP_CANCELLATION_REASON", Integer),
    Column("CRM_TRANSFER_DATE", DateTime),
    Column("PP_DISCOUNT", DECIMAL(18, 2)),
    Column("PP_PLANT", Integer),
    Column("PP_TAXABLE", BIT),
    Column("PP_DISCOUNT_PERCENTAGE", DECIMAL(19, 10)),
    Column("PP_START_DATE", DATETIME2),
    Column("PP_END_DATE", DATETIME2),
    schema="dbo",
)


t_V_PROJECT_STARLIMS_HISTORY = Table(
    "V_PROJECT_STARLIMS_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("P_ID", Integer),
    Column("STARLIMS_PROJECT_NUMBER", Unicode(25)),
    schema="dbo",
)


t_V_PROKALKMODUL_HISTORY = Table(
    "V_PROKALKMODUL_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("PKM_ID", Integer),
    Column("P_ID", Integer),
    Column("KALM_ID", Integer),
    Column("KAL_ID", Integer),
    Column("PKM_TYP", Integer),
    Column("PKM_NAME", Unicode(1024)),
    Column("PKM_IS_UA", BIT),
    Column("PKM_TAGE_UA", Integer),
    Column("TP_ID", Integer),
    Column("PKM_TESTDAUER", Integer),
    Column("PKM_EINHEITEN", DECIMAL(18, 2)),
    Column("PKM_SATZ", DECIMAL(18, 2)),
    Column("PKM_AUFWAND", DECIMAL(18, 2)),
    Column("PKM_FAKTOR", DECIMAL(18, 2)),
    Column("PKM_VK", DECIMAL(18, 2)),
    Column("PKM_AUFTRAGSTEXT", Unicode(1024)),
    Column("PKM_KOMMENTAR", Unicode(1024)),
    Column("PKM_REIHE", Integer),
    Column("PKM_UA", Integer),
    Column("MIT_ID", Integer),
    Column("PKM_REGDATE", DateTime),
    Column("PKM_REGBY", Integer),
    Column("PKM_UPDATE", DateTime),
    Column("PKM_UPDATEBY", Integer),
    Column("MIT_ID_TEAM", Integer),
    Column("PKM_REGBY_TEAM", Integer),
    Column("PKM_UPDATEBY_TEAM", Integer),
    Column("AL_ID", Integer),
    Column("PKM_DISABLED", BIT),
    Column("FROM_PS_CONFIG", BIT),
    schema="dbo",
)


t_V_PROKALKUNTERMODUL_HISTORY = Table(
    "V_PROKALKUNTERMODUL_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("PKUM_ID", Integer),
    Column("PKM_ID", Integer),
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("PKUM_QUOTATION_POSITION", Integer),
    Column("PKUM_TESTING_POSITION", Integer),
    Column("ST_ID", Integer),
    Column("PKUM_NAME", Unicode(1024)),
    Column("PKUM_DAYS_TO_START", Integer),
    Column("PKUM_DURATION", Integer),
    Column("TP_ID", Integer),
    Column("PKUM_PLANNED_HOURS", DECIMAL(18, 2)),
    Column("PKUM_RATE", DECIMAL(18, 2)),
    Column("PKUM_PLANNED_EXPENSES", DECIMAL(18, 2)),
    Column("PKUM_FACTOR", DECIMAL(18, 2)),
    Column("PKUM_PLANNED_TRAVEL_COSTS", DECIMAL(18, 2)),
    Column("PKUM_RECOMMENDED_PRICE", DECIMAL(18, 2)),
    Column("PKUM_COMMENT", Unicode(2000)),
    Column("PKUM_ORDER_TEXT", Unicode(1024)),
    Column("PKUM_ADDITIONAL_TEXT", Unicode(1024)),
    Column("PKUM_SAP_TRANSFER", DateTime),
    Column("PKUM_SORT", Integer),
    Column("PKUM_DISABLED", BIT),
    Column("PKUM_CREATED", DateTime),
    Column("PKUM_CREATED_BY", Integer),
    Column("PKUM_UPDATED", DateTime),
    Column("PKUM_UPDATED_BY", Integer),
    Column("PKUM_SO_TRANSFER_PRICE", DECIMAL(18, 2)),
    Column("PKUM_SP_PRICELIST", DECIMAL(18, 2)),
    Column("PKUM_SP_PRICELIST_ORG", DECIMAL(18, 2)),
    Column("PKUM_TRAVELTIME", DECIMAL(18, 2)),
    Column("PKUM_SP_FOREIGN", DECIMAL(18, 10)),
    Column("ZM_ID", Unicode(18)),
    Column("PKUM_BULKTEST", BIT),
    Column("PKUM_CANCELLED", BIT),
    Column("FROM_PS_CONFIG", BIT),
    Column("FROM_SUBORDER", Integer),
    Column("PKUM_KPI", BIT),
    Column("PKUM_S_KPI_NUMBER", Integer),
    Column("PKUM_PLANNED_SUBCONTRACTING", DECIMAL(18, 2)),
    schema="dbo",
)


t_V_PSEX_PRIMARYKEYS = Table(
    "V_PSEX_PRIMARYKEYS",
    metadata,
    Column("TABLE_NAME", Unicode(128), nullable=False),
    Column("COLUMN_NAME", Unicode(128)),
    schema="dbo",
)


t_V_SOTRANSFERFILE_HISTORY = Table(
    "V_SOTRANSFERFILE_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("FILEPATH", Unicode(512)),
    Column("ISFOCUS", BIT),
    Column("TRA_ID", Integer),
    Column("DATALEN", Integer),
    Column("WRITEUTC", DateTime),
    Column("STATUS", Unicode(10)),
    Column("MSG", Unicode),
    schema="dbo",
)


t_V_SOTRANSFERJOB_HISTORY = Table(
    "V_SOTRANSFERJOB_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("TRA_ID", Integer),
    Column("P_ID", Integer),
    Column("DIR", NCHAR(1)),
    Column("FILENAME", Unicode(512)),
    Column("CREATED", DateTime),
    Column("UPDATED", DateTime),
    Column("STATUS", Unicode(10)),
    Column("SRC_FOLDER", Unicode(512)),
    Column("TAR_FOLDER", Unicode(512)),
    schema="dbo",
)


t_V_STAFFROLE_HISTORY = Table(
    "V_STAFFROLE_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("SR_ID", Integer),
    Column("ST_ID", Integer),
    Column("RS_ID", Integer),
    Column("DISABLED", BIT),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    schema="dbo",
)


t_V_STAFF_HISTORY = Table(
    "V_STAFF_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ST_ID", Integer),
    Column("ST_SURNAME", Unicode(60)),
    Column("ST_FORENAME", Unicode(50)),
    Column("ST_LOCATION", Unicode(50)),
    Column("ST_UNIT", Unicode(12)),
    Column("ST_COSTID", Unicode(10)),
    Column("ST_ACTIVE", BIT),
    Column("ST_NUMBER", Unicode(8)),
    Column("ST_SHORT", Unicode(3)),
    Column("ST_PHONE", Unicode(80)),
    Column("ST_FAX", Unicode(80)),
    Column("ST_EMAIL", Unicode(80)),
    Column("ST_LOGIN", BIT),
    Column("ST_HOURS_PER_DAY", Integer),
    Column("ST_WINDOWSID", Unicode(32)),
    Column("ST_SAP_ID", Unicode(50)),
    Column("ST_TITLE", Unicode(255)),
    Column("ST_GENDER", Unicode(50)),
    Column("ST_SERVERID", Integer),
    Column("UpdateDate", DateTime),
    Column("UpdateByID", Integer),
    Column("Locale", Unicode(50)),
    Column("ST_UPDATE_TYPE", TINYINT),
    Column("ST_TEAM", UNIQUEIDENTIFIER),
    Column("ST_IS_LAGER", BIT),
    Column("ST_IS_ABTEILUNG", BIT),
    Column("ST_TYPE", Integer),
    Column("ST_DOMAIN", Unicode(32)),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer),
    Column("VERSION_TYPE", Unicode(5)),
    Column("RUN_ID", Integer),
    Column("STAT2", NCHAR(1)),
    Column("ST_SKILLGROUP", Unicode(8)),
    Column("ST_COSTID_CHANGED", DateTime),
    Column("PERSK", NCHAR(2)),
    Column("ST_POSTING_APPROVAL_REQUIRED", BIT),
    Column("ST_MOBILE", Unicode(80)),
    Column("ST_MARK", Unicode(256)),
    schema="dbo",
)


t_V_STORIX_LAGERELEMENT = Table(
    "V_STORIX_LAGERELEMENT",
    metadata,
    Column("LGEL_ID", Integer, nullable=False),
    Column("LG_ID", Integer),
    Column("LGEL_NR", Integer),
    Column("LGEL_BEZEICHNUNG", Unicode(255)),
    Column("LGEL_ZUSTAND", Unicode(255)),
    Column("LGEL_SERIENNUMMER", Unicode(60)),
    Column("LGEL_STORIXREFERENZ", Unicode(255)),
    Column("LGEL_ARCHIV", DateTime),
    Column("LGEL_ARCHIVLAGER", Unicode(60)),
    Column("LGEL_ARCHIVIERT", BIT, nullable=False),
    Column("LGEL_LAGERTERMIN", DateTime),
    Column("LGEL_NACHLAGERTERMIN", Unicode(60)),
    Column("LGEL_BEMERKUNG", Unicode(255)),
    Column("LGEL_VERANTWORTLICH", Unicode(60)),
    Column("LGEL_ERLEDIGT", BIT, nullable=False),
    Column("LGEL_ENDE_DURCH", Integer),
    Column("LGEL_VERSANDADRESSE", Unicode(255)),
    Column("LGEL_LAGERORT", Unicode(60)),
    Column("LGEL_BEWEGUNGEN", Integer),
    Column("LGEL_ERF_USER", Unicode(60)),
    Column("LGEL_ERF_DATUM", DateTime),
    Column("LGEL_AEND_USER", Unicode(60)),
    Column("LGEL_AEND_DATUM", DateTime),
    Column("LGEL_AUFTRAGGEBER", Unicode(60)),
    Column("LGEL_AUFTRAGGEBER_KNR", Unicode(20)),
    Column("LGEL_AUFTRAGSNR", Unicode(60)),
    Column("LGEL_PSEX", Integer),
    Column("LGEL_PROJEKTLEITER", Unicode(60)),
    Column("LGEL_RESERVIERT_VON", Unicode(60)),
    Column("LGEL_PSI_NUMMER", Unicode(15)),
    Column("LGEL_RESERVIERT_AM", DateTime),
    Column("BR_SHORT", Unicode(5)),
    Column("RV_ID", Integer),
    Column("LGEL_WEITERGEGEBEN", BIT),
    Column("LGEL_BESITZER", Unicode(60)),
    Column("LGEL_BESITZERABTEILUNG", Unicode(60)),
    Column("AUSL_ID", Integer),
    Column("LGEL_ERLEDIGT_AM", DateTime),
    Column("LGEL_ARCHIVIERT_AM", DateTime),
    Column("B_ID", Integer),
    Column("DZU_ID", Integer),
    Column("DRV_ID", Integer),
    Column("LGEL_MODEL", Unicode(255)),
    Column("LGEL_PARTNUMBER", Unicode(255)),
    Column("LGEL_HARDWAREVERSION", Unicode(255)),
    Column("LGEL_SOFTWAREVERSION", Unicode(255)),
    Column("LGEL_DRAWINGNUMBER", Unicode(255)),
    Column("LGEL_BUILDSTATUS", Unicode(255)),
    Column("LGEL_HIGHESTFREQUENCY", Unicode(255)),
    Column("DMU_ID", Integer, nullable=False),
    Column("LGEL_IS_ACCESSORY", BIT, nullable=False),
    schema="dbo",
)


t_V_STORIX_STATUS_ERLEDIGT = Table(
    "V_STORIX_STATUS_ERLEDIGT",
    metadata,
    Column("STE_ID", Integer, nullable=False),
    Column("LG_ID", Integer),
    Column("LGEL_NR", Integer),
    Column("STE_ERLEDIGT", BIT),
    Column("STE_GEAENDERT_VON", Unicode(60)),
    Column("STE_GEAENDERT_AM", DateTime),
    schema="dbo",
)


t_V_SUBORDERS_HISTORY = Table(
    "V_SUBORDERS_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("SO_DISPOBY", Integer),
    Column("SO_CREATED", DateTime),
    Column("ST_ID", Integer),
    Column("SO_DEADLINE", DateTime),
    Column("SO_TASK", Unicode(1024)),
    Column("SO_HOURS", DECIMAL(18, 6)),
    Column("SO_RATE", MONEY),
    Column("SO_SPENDS", MONEY),
    Column("SO_ACC_HOURS", MONEY),
    Column("SO_ACC_SPENDS", DECIMAL(18, 2)),
    Column("SO_REPORT", Unicode(255)),
    Column("SO_START_MACRO", BIT),
    Column("MCO_ID", Integer),
    Column("SO_COMMENT", Unicode(2000)),
    Column("SO_DATE_READY", DateTime),
    Column("SO_READYBY", Integer),
    Column("SO_DATE_CHECK", DateTime),
    Column("SO_CHECKBY", Integer),
    Column("SO_FORECAST", DECIMAL(18, 2)),
    Column("SO_LANGUAGE", Unicode(5)),
    Column("RES_ID", Integer),
    Column("SO_ACC_POS", Unicode(10)),
    Column("SO_INTERN", BIT),
    Column("SO_PREDATE", DateTime),
    Column("SO_PREDATE_REMINDER", BIT),
    Column("SO_PREDATE_INFO", Unicode(255)),
    Column("SO_WAIT", BIT),
    Column("SO_REGBY", Integer),
    Column("SO_REGDATE", DateTime),
    Column("SO_UPDATEBY", Integer),
    Column("SO_UPDATE", DateTime),
    Column("SO_TRANSFERSTATUS", Unicode(50)),
    Column("SO_DISABLED", BIT),
    Column("SO_ForeignExpenditure", MONEY),
    Column("SO_PostedFromForeign", MONEY),
    Column("SO_IsTransferredBack", BIT),
    Column("UA_TRANS_PROJECT", Integer),
    Column("SO_Docu_Done", BIT),
    Column("SO_DEADLINE_REMINDER", BIT),
    Column("SO_CUSTOMER_A", Integer),
    Column("SO_CUSTOMER_B", Integer),
    Column("SO_CUSTOMER_O", Integer),
    Column("SO_PARENT", Integer),
    Column("SO_SORT", Integer),
    Column("SO_ADMINISTRATIVE", BIT),
    Column("SO_APPOINTMENTDATE", DateTime),
    Column("PLAN_ACTUAL_HOUR", DECIMAL(8, 2)),
    Column("PLAN_TRAVEL", DECIMAL(8, 2)),
    Column("PLAN_EXTERNAL", DECIMAL(8, 2)),
    Column("ACC_EFFORT", DECIMAL(8, 2)),
    Column("ACC_ACTUAL_HOUR", DECIMAL(8, 2)),
    Column("ACC_TRAVEL", DECIMAL(8, 2)),
    Column("ACC_EXTERNAL", DECIMAL(8, 2)),
    Column("SAP_NO", Unicode(10)),
    Column("ORDER_SIGN", Unicode(35)),
    Column("ORDER_DATE", DateTime),
    Column("ORDER_POSITION", Unicode(6)),
    Column("SO_CHECKBY_TEAM", Integer),
    Column("SO_DISPOBY_TEAM", Integer),
    Column("SO_READYBY_TEAM", Integer),
    Column("SO_REGBY_TEAM", Integer),
    Column("SO_UPDATEBY_TEAM", Integer),
    Column("ST_ID_TEAM", Integer),
    Column("AL_ID", Integer),
    Column("SO_PLANNED_MATERIAL", DECIMAL(18, 2)),
    Column("SO_PLANNED_LICENSE", DECIMAL(18, 2)),
    Column("BANF_REQUEST", DateTime),
    Column("BANF_ORDER", DateTime),
    Column("B2B", BIT),
    Column("SO_REPORT_NUMBER", Unicode(256)),
    Column("ZM_ID", Unicode(18)),
    Column("SO_REMARK", Unicode(1024)),
    Column("SO_POST_OUT_DATE", DateTime),
    Column("SO_CONFIRMED_DATE", DateTime),
    Column("LIMS_STATUS", Unicode(16)),
    Column("LIMS_REMARK", Unicode(256)),
    Column("SOC_ID", Integer),
    Column("RFAE_ID", Integer),
    Column("FROM_STARLIMS", BIT),
    Column("SO_COORDINATOR", Integer),
    Column("STARLIMS_DISTINCTIVE_FLAG", Integer),
    Column("DEADLINE_CALCULATION_WITHOUT_HOLIDAYS", BIT),
    Column("SO_MODEL", Unicode(255)),
    Column("TRANSFER_TO_STARLIMS", DateTime),
    Column("STARLIMS_PROJECT_NUMBER", Unicode(25)),
    Column("URGENT", BIT),
    Column("SO_POSTING_DONE_DATE", DateTime),
    Column("KPI", BIT),
    Column("SO_DATE_READY_REASON", Unicode(512)),
    Column("SO_DATE_READY_CHANGED", DateTime),
    Column("SO_DATE_CHECK_REASON", Unicode(512)),
    Column("SO_DATE_CHECK_CHANGED", DateTime),
    Column("REPORT_SENT", DateTime),
    Column("S_KPI_NUMBER", Integer),
    Column("SO_TUV_CERT_EXISTS", BIT),
    Column("SO_EXTERNAL_CERT_EXISTS", BIT),
    Column("SO_CERT_COMMENT", Unicode(512)),
    schema="dbo",
)


t_V_SUBORDER_LAGERELEMENT_HISTORY = Table(
    "V_SUBORDER_LAGERELEMENT_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("LGEL_ID", Integer),
    Column("DISABLED", BIT),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    schema="dbo",
)


t_V_SUBORDER_SAMPLE_HISTORY = Table(
    "V_SUBORDER_SAMPLE_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("SAMPLE_NUMBER", Unicode(16)),
    Column("SAMPLE_DESCRIPTION", Unicode(256)),
    Column("REMARK", Unicode(512)),
    Column("DISABLED", BIT),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    schema="dbo",
)


t_V_SUBORDER_TEST_METHOD_HISTORY = Table(
    "V_SUBORDER_TEST_METHOD_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("STKO_ID", Integer),
    Column("STANDARD_ANALYSIS", Unicode(128)),
    Column("TEST_METHOD_ID", Integer),
    Column("TEST_METHOD_NAME", Unicode(128)),
    Column("PARAMETER", Unicode(128)),
    Column("DISABLED", BIT),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    schema="dbo",
)


t_V_SUBORDER_TEST_REQUIREMENT_SAMPLE_HISTORY = Table(
    "V_SUBORDER_TEST_REQUIREMENT_SAMPLE_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("ID", Integer),
    Column("METHOD_ID", Integer),
    Column("SAMPLE_ID", Integer),
    Column("MIX_SAMPLE_NUMBER", Integer),
    Column("DISABLED", BIT),
    Column("CREATED", DateTime),
    Column("CREATED_BY", Integer),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    schema="dbo",
)


t_V_TESTSAMPLECHARACTERISTICS_HISTORY = Table(
    "V_TESTSAMPLECHARACTERISTICS_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("TC_ID", Integer),
    Column("TC_NAME", Unicode(2000)),
    Column("TC_VALUE", Unicode(2000)),
    Column("TS_ID", Integer),
    Column("TS_DISABLED", BIT),
    Column("TC_NUMBER", Integer),
    schema="dbo",
)


t_V_TESTSAMPLEPICTURE_HISTORY = Table(
    "V_TESTSAMPLEPICTURE_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("TSP_ID", Integer),
    Column("TS_ID", Integer),
    Column("TS_FILE", Unicode(255)),
    Column("TS_DESCRIPTION", Unicode(255)),
    Column("TS_DISABLED", BIT),
    Column("TSP_NUMBER", Integer),
    schema="dbo",
)


t_V_TESTSAMPLE_HISTORY = Table(
    "V_TESTSAMPLE_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("TS_ID", Integer),
    Column("P_ID", Integer),
    Column("TS_PRODUCT", Unicode(255)),
    Column("TS_MODEL", Unicode(255)),
    Column("CU_ID", Integer),
    Column("TS_DATE_RECEIPT", DateTime),
    Column("TS_COUNT", Integer),
    Column("TS_FROM_MANUFACTURER", BIT),
    Column("PRP_ID", Integer),
    Column("TS_STORIX", Unicode(10)),
    Column("TS_STORIXELEMENT", Unicode(10)),
    Column("TS_INTEND_USE", Unicode(2000)),
    Column("TS_INFO", Unicode(2000)),
    Column("TS_DEFAULT_RETURN", Integer),
    Column("TS_DEFAULT_STORAGE", DateTime),
    Column("TS_COUNT_SHIPPED", Integer),
    Column("TS_COUNT_WASTE", Integer),
    Column("TS_COUNT_USE", Integer),
    Column("TS_DISABLED", BIT),
    Column("TS_UPDATEBY", Integer),
    Column("TS_UPDATE", DateTime),
    Column("TS_CREATEDBY", Integer),
    Column("TS_CREATED", DateTime),
    Column("TS_CREATEDBY_TEAM", Integer),
    Column("TS_UPDATEBY_TEAM", Integer),
    Column("AL_ID", Integer),
    schema="dbo",
)


t_V_VERIFICATION_DOCUMENT_HISTORY = Table(
    "V_VERIFICATION_DOCUMENT_HISTORY",
    metadata,
    Column("HISTORY_ID", Integer, nullable=False),
    Column("HISTORY_TIMESTAMP", DateTime, nullable=False),
    Column("INSERTED_HIST_DB", DateTime),
    Column("IN_HIST_DB", Integer, nullable=False),
    Column("VD_ID", Integer),
    Column("P_ID", Integer),
    Column("VD_NAME", Unicode(1024)),
    Column("VD_CATEGORY", Integer),
    Column("VD_CHECKED", BIT),
    Column("VD_SORT", Integer),
    Column("VD_DISABLED", BIT),
    Column("VD_CREATED", DateTime),
    Column("VD_CREATED_BY", Integer),
    Column("VD_UPDATED", DateTime),
    Column("VD_UPDATED_BY", Integer),
    Column("FROM_PS_CONFIG", BIT),
    schema="dbo",
)


t_V_WORKINGCLUSTERS_TO_ANONYMIZE = Table(
    "V_WORKINGCLUSTERS_TO_ANONYMIZE",
    metadata,
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_LOCATION", Unicode(40)),
    Column("HR_TYPE", Unicode(50)),
    Column("HR_PARENT", UNIQUEIDENTIFIER),
    Column("HR_ACTIVE", BIT, nullable=False),
    schema="dbo",
)


class VersionInfo(Base):
    __tablename__ = "VersionInfo"
    __table_args__ = (
        Index(
            "IX_VersionInfo_TYPE_RELEASE_SEQ_ObsoleteDate",
            "TYPE",
            "RELEASE_SEQ",
            "ObsoleteDate",
            "FullVersionPath",
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    Sequence = Column(Integer, nullable=False)
    VersionNumber = Column(Unicode(100), nullable=False, unique=True)
    RELEASE_SEQ = Column(Integer, nullable=False)
    ObsoleteDate = Column(DateTime)
    OutOfOrderDate = Column(DateTime)
    TYPE = Column(Unicode(5), nullable=False)
    FullVersionPath = Column(Unicode(150))
    ObsoleteMessage_EN = Column(Unicode(150))
    ObsoleteMessage_DE = Column(Unicode(150))
    ObsoleteMessage_FR = Column(Unicode(150))
    OutOfOrderMessage_EN = Column(Unicode(150))
    OutOfOrderMessage_DE = Column(Unicode(150))
    OutOfOrderMessage_FR = Column(Unicode(150))
    ApplicationName_EN = Column(Unicode(50))
    ApplicationName_DE = Column(Unicode(50))
    ApplicationName_FR = Column(Unicode(50))
    CreateDate = Column(DateTime, nullable=False)
    CreatedByID = Column(Integer)
    UpdateDate = Column(DateTime, nullable=False)
    UpdateByID = Column(Integer)
    KEEP_LOCAL_CACHE = Column(BIT, nullable=False)


class ZARAMATERIAL(Base):
    __tablename__ = "ZARA_MATERIAL"
    __table_args__ = (
        Index(
            "UQ_DEFAULT_FOR_PP_TYPE",
            "MD_ID",
            "ZM_BOOKING_AREA",
            "DEFAULT_FOR_PP_TYPE",
            unique=True,
        ),
        Index(
            "IX_ZARA_MATERIAL_MD_ID_ZM_BOOKING_AREA_SERVERID",
            "MD_ID",
            "ZM_BOOKING_AREA",
            "SERVERID",
            "STATUS",
            "STATUS_FROM",
            "LVORM",
            "ZM_ID",
            "ACOT_ID",
            "ZM_MATERIAL_GROUP",
            "CREATED",
            "UPDATED",
            "POSTABLE",
            "SET_INVOICINGTRAVELCOST",
        ),
        Index(
            "IX_ZARA_MATERIAL_MD_ID_BOOKING_AREA",
            "MD_ID",
            "ZM_BOOKING_AREA",
            "ZM_ID",
            "ACOT_ID",
            "SERVERID",
            "ZM_MATERIAL_GROUP",
            "CREATED",
            "UPDATED",
            "POSTABLE",
            "STATUS",
            "STATUS_FROM",
            "LVORM",
            "STAFF_POSTABLE",
            "DISABLED",
        ),
        {"schema": "dbo"},
    )

    ZM_ID = Column(Unicode(18), primary_key=True, nullable=False)
    MD_ID = Column(Integer, nullable=False)
    ZM_BOOKING_AREA = Column(Unicode(4), primary_key=True, nullable=False)
    ACOT_ID = Column(Integer, nullable=False)
    ZM_PRODUCT = Column(Unicode(5))
    ZM_OBJECT = Column(Unicode(5))
    ZM_LOCATION = Column(Unicode(5))
    ZM_SUBLOCATION = Column(Unicode(4))
    SERVERID = Column(Integer, primary_key=True, nullable=False)
    ZM_MATERIAL_GROUP = Column(Unicode(9))
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)
    POSTABLE = Column(BIT, nullable=False)
    RUN_ID = Column(Integer)
    STATUS = Column(NCHAR(2))
    STATUS_FROM = Column(DateTime)
    LVORM = Column(BIT)
    STAFF_POSTABLE = Column(BIT, nullable=False)
    DISABLED = Column(DateTime)
    SET_INVOICINGTRAVELCOST = Column(BIT, nullable=False)
    DEFAULT_FOR_PP_TYPE = Column(Integer)


class ZPSBEGRIFF(Base):
    __tablename__ = "ZPS_BEGRIFF"
    __table_args__ = {"schema": "dbo"}

    BEGR_ID = Column(Integer, primary_key=True)
    BEGR_BAUNR = Column(Unicode(255))
    BEGR_ERF_DATUM = Column(DateTime, nullable=False)
    BEGR_AEND_DATUM = Column(DateTime)
    BEGR_EBENE = Column(Integer)


class ZVANGEBOT(Base):
    __tablename__ = "ZVANGEBOT"
    __table_args__ = {"schema": "dbo"}

    VBELN = Column(Unicode(10), primary_key=True, nullable=False)
    MD_ID = Column(Integer, primary_key=True, nullable=False)
    SERVERID = Column(Integer, primary_key=True, nullable=False)
    ANGDT = Column(Unicode(8))
    BNDDT = Column(Unicode(8))
    BSTDK = Column(Unicode(8))
    BSTKD = Column(Unicode(35))
    FBUDA = Column(Unicode(8))
    KUNNR = Column(Unicode(10))
    REKUNNR = Column(Unicode(10))
    SPART = Column(NCHAR(2))
    SPRAS = Column(NCHAR(2))
    VKBUR = Column(Unicode(4))
    VKGRP = Column(Unicode(3))
    VKORG = Column(Unicode(4))
    VTWEG = Column(NCHAR(2))
    Z1_PERNR = Column(Unicode(8))
    Z2_PERNR = Column(Unicode(8))
    ZM_PERNR = Column(Unicode(8))
    CREATED_FROM_PSE = Column(DateTime)
    CREATED_FROM_PSE_BY = Column(Integer)
    UPDATED_FROM_PSE = Column(DateTime)
    UPDATED_FROM_PSE_BY = Column(Integer)
    ZG_KUNNR = Column(Unicode(10))
    PRSDT = Column(Unicode(8))
    WAERK_H = Column(Unicode(5))
    AP_PARTNER_NR = Column(Unicode(10))
    CPD_ADRESSE_NAME1 = Column(Unicode(40))
    CPD_ADRESSE_NAME2 = Column(Unicode(40))
    CPD_ADRESSE_NAME3 = Column(Unicode(40))
    CPD_ADRESSE_NAME_CO = Column(Unicode(40))
    CPD_ADRESSE_STREET = Column(Unicode(35))
    CPD_ADRESSE_STR_SUPPL1 = Column(Unicode(40))
    CPD_ADRESSE_STR_SUPPL2 = Column(Unicode(40))
    CPD_ADRESSE_STR_SUPPL3 = Column(Unicode(40))
    CPD_ADRESSE_LOCATION = Column(Unicode(40))
    CPD_ADRESSE_NAME_AP = Column(Unicode(35))
    CPD_ADRESSE_PO_BOX = Column(Unicode(10))
    CPD_ADRESSE_POST_CODE = Column(Unicode(10))
    CPD_ADRESSE_CITY1 = Column(Unicode(40))
    CPD_ADRESSE_CITY2 = Column(Unicode(40))
    CPD_ADRESSE_REGION = Column(Unicode(3))
    CPD_ADRESSE_COUNTRY = Column(Unicode(3))
    VE_PERNR = Column(Unicode(8))
    KOSTL = Column(Unicode(10))
    NETWR = Column(DECIMAL(18, 2))
    ORDER_TEXT = Column(Unicode(2048))
    CRM_ID = Column(Unicode(16))
    KURSK = Column(DECIMAL(18, 2))
    CREATED_FROM_SAP = Column(DateTime)
    UPDATED_FROM_SAP = Column(DateTime)
    RUN_ID = Column(Integer)
    ZC_PERNR = Column(Unicode(8))
    DOCUMENTS_FOLDER = Column(Unicode(2048))


class ZVSKILLGRUPPE(Base):
    __tablename__ = "ZVSKILLGRUPPE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(BigInteger, primary_key=True)
    BUKRS = Column(Unicode(4), nullable=False)
    SKGRP = Column(Unicode(8), nullable=False)
    LSTAR = Column(Unicode(32))
    BEGDA = Column(Date, nullable=False)
    ENDDA = Column(Date, nullable=False)
    SKGTX = Column(Unicode(1000))
    CREATED = Column(DATETIME2)
    CREATED_BY = Column(BigInteger)
    UPDATED = Column(DATETIME2)
    UPDATED_BY = Column(BigInteger)
    RUN_ID = Column(Integer)


class Dtproperty(Base):
    __tablename__ = "dtproperties"
    __table_args__ = {"schema": "dbo"}

    id = Column(Integer, primary_key=True, nullable=False)
    objectid = Column(Integer)
    property = Column(
        String(64, "SQL_Latin1_General_CP1_CI_AS"),
        primary_key=True,
        nullable=False,
    )
    value = Column(String(255, "SQL_Latin1_General_CP1_CI_AS"))
    uvalue = Column(Unicode(255))
    lvalue = Column(IMAGE)
    version = Column(Integer, nullable=False)


class Sysdiagram(Base):
    __tablename__ = "sysdiagrams"
    __table_args__ = (
        Index("UK_principal_name", "principal_id", "name", unique=True),
        {"schema": "dbo"},
    )

    name = Column(Unicode(128), nullable=False)
    principal_id = Column(Integer, nullable=False)
    diagram_id = Column(Integer, primary_key=True)
    version = Column(Integer)
    definition = Column(LargeBinary)


class ACCOUNTTYPE(Base):
    __tablename__ = "ACCOUNTTYPE"
    __table_args__ = {"schema": "dbo"}

    ACOT_ID = Column(Integer, primary_key=True)
    ACOT_NAME_DE = Column(Unicode(256), nullable=False)
    ACOT_NAME_EN = Column(Unicode(256), nullable=False)
    ACOT_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="ACCOUNTTYPE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="ACCOUNTTYPE.UPDATED_BY == STAFF.ST_ID"
    )


class ACTIONTYPE(Base):
    __tablename__ = "ACTION_TYPE"
    __table_args__ = {"schema": "dbo"}

    ACTT_ID = Column(Integer, primary_key=True)
    ACTT_NAME_DE = Column(Unicode(256), nullable=False)
    ACTT_NAME_EN = Column(Unicode(256), nullable=False)
    ACTT_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    ACTT_LEVEL = Column(Integer, nullable=False)

    STAFF = relationship(
        "STAFF", primaryjoin="ACTIONTYPE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="ACTIONTYPE.UPDATED_BY == STAFF.ST_ID"
    )


class ACTIVITYTYPE(Base):
    __tablename__ = "ACTIVITY_TYPE"
    __table_args__ = (
        Index(
            "UIX_ACTIVITY_TYPE_BOOKING_AREA_SKILLGROUP_DISABLED",
            "BOOKING_AREA",
            "SKILLGROUP",
            "DISABLED",
            unique=True,
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    BOOKING_AREA = Column(Unicode(4), nullable=False)
    SKILLGROUP = Column(Unicode(8))
    ACTIVITY_TYPE_CODE = Column(Unicode(32), nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="ACTIVITYTYPE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="ACTIVITYTYPE.UPDATED_BY == STAFF.ST_ID"
    )


class ADDITIONALCOSTCENTER(Base):
    __tablename__ = "ADDITIONAL_COST_CENTER"
    __table_args__ = (
        Index(
            "UIX_ADDITIONAL_COST_CENTER_ORDER_COST_CENTER_ADDITIONAL_COST_CENTER",
            "ORDER_COST_CENTER",
            "ADDITIONAL_COST_CENTER",
            unique=True,
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    ORDER_COST_CENTER = Column(ForeignKey("dbo.KST.CC_ID"), nullable=False)
    ADDITIONAL_COST_CENTER = Column(
        ForeignKey("dbo.KST.CC_ID"), nullable=False
    )
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    KST = relationship(
        "KST",
        primaryjoin="ADDITIONALCOSTCENTER.ADDITIONAL_COST_CENTER == KST.CC_ID",
    )
    STAFF = relationship(
        "STAFF", primaryjoin="ADDITIONALCOSTCENTER.CREATED_BY == STAFF.ST_ID"
    )
    KST1 = relationship(
        "KST",
        primaryjoin="ADDITIONALCOSTCENTER.ORDER_COST_CENTER == KST.CC_ID",
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="ADDITIONALCOSTCENTER.UPDATED_BY == STAFF.ST_ID"
    )


class APPLICATIONFORM(Base):
    __tablename__ = "APPLICATION_FORM"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME = Column(Unicode(256), nullable=False)
    VALUE = Column(Unicode(256), nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DATETIME2, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DATETIME2, nullable=False)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)

    STAFF = relationship(
        "STAFF", primaryjoin="APPLICATIONFORM.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="APPLICATIONFORM.UPDATED_BY == STAFF.ST_ID"
    )


class CALCULATIONAREA(Base):
    __tablename__ = "CALCULATION_AREA"
    __table_args__ = {"schema": "dbo"}

    WORKING_CLUSTER = Column(
        ForeignKey("dbo.HIERARCHY.HR_ID"), primary_key=True, nullable=False
    )
    CA_ID = Column(Integer, primary_key=True, nullable=False)
    CA_NAME_DE = Column(Unicode(64), nullable=False)
    CA_NAME_EN = Column(Unicode(64), nullable=False)
    CA_NAME_FR = Column(Unicode(64), nullable=False)
    CA_CREATED = Column(DateTime, nullable=False)
    CA_CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    CA_UPDATED = Column(DateTime)
    CA_UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    DISABLED = Column(DateTime)
    CALC_AREA_ID = Column(Integer, nullable=False, unique=True)

    STAFF = relationship(
        "STAFF", primaryjoin="CALCULATIONAREA.CA_CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="CALCULATIONAREA.CA_UPDATED_BY == STAFF.ST_ID"
    )
    HIERARCHY = relationship("HIERARCHY")


class CANCELLATIONREASON(Base):
    __tablename__ = "CANCELLATION_REASON"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    KEY_FOR_SAP = Column(Unicode(3), nullable=False)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_EN = Column(Unicode(256), nullable=False)
    NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="CANCELLATIONREASON.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="CANCELLATIONREASON.UPDATED_BY == STAFF.ST_ID"
    )


class CATEGORY(Base):
    __tablename__ = "CATEGORY"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME = Column(Unicode(256), nullable=False)
    ZM_ID = Column(Unicode(18))
    CU_ID = Column(Integer)
    KOB_ID = Column(Integer)
    DEFAULT_PRICE = Column(DECIMAL(18, 2))
    DEFAULT_SALES_RATE = Column(DECIMAL(18, 2))
    DEFAULT_SPENDS = Column(DECIMAL(18, 2))
    DEFAULT_EXTERNALS = Column(DECIMAL(18, 2))
    DEFAULT_SUBORDERS = Column(DECIMAL(18, 2))
    DEFAULT_LICENSES = Column(DECIMAL(18, 2))
    DEFAULT_TRAVELS = Column(DECIMAL(18, 2))
    DEFAULT_CORRECTION_FACTOR = Column(DECIMAL(18, 2))
    CC_ID = Column(Unicode(10))
    IS_FOR_AUDIT_PROJECTS = Column(BIT, nullable=False)
    IS_DEFAULT_FOR_NEW_PROJECTS = Column(BIT, nullable=False)
    PARENT = Column(ForeignKey("dbo.CATEGORY.ID"))
    SORT = Column(Integer)
    DISABLED = Column(DateTime)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="CATEGORY.CREATED_BY == STAFF.ST_ID"
    )
    parent = relationship("CATEGORY", remote_side=[ID])
    STAFF1 = relationship(
        "STAFF", primaryjoin="CATEGORY.UPDATED_BY == STAFF.ST_ID"
    )


class CERTAPPLTC(Base):
    __tablename__ = "CERT_APPL_TCS"
    __table_args__ = {"schema": "dbo"}

    APPL_ID = Column(Integer, primary_key=True)
    APPL_NAME = Column(Unicode(30), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATEBY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATEBY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    DISABLED = Column(DateTime)

    STAFF = relationship(
        "STAFF", primaryjoin="CERTAPPLTC.CREATEBY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="CERTAPPLTC.UPDATEBY == STAFF.ST_ID"
    )


class CHANCETYPE(Base):
    __tablename__ = "CHANCETYPE"
    __table_args__ = {"schema": "dbo"}

    CHT_ID = Column(Integer, primary_key=True)
    CHT_NAME_DE = Column(Unicode(256), nullable=False)
    CHT_NAME_EN = Column(Unicode(256), nullable=False)
    CHT_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="CHANCETYPE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="CHANCETYPE.UPDATED_BY == STAFF.ST_ID"
    )


class CHECKVIEWMD(Base):
    __tablename__ = "CHECKVIEW_MD"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    BOX_ID = Column(Integer, nullable=False)
    ITEM_EN = Column(Unicode(256), nullable=False)
    ITEM_DE = Column(Unicode(256), nullable=False)
    ITEM_FR = Column(Unicode(256), nullable=False)
    SORT = Column(Integer)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="CHECKVIEWMD.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="CHECKVIEWMD.UPDATED_BY == STAFF.ST_ID"
    )


class CODETYPE(Base):
    __tablename__ = "CODE_TYPE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_EN = Column(Unicode(256), nullable=False)
    CODE = Column(Unicode(256), nullable=False)
    DISABLED = Column(Date)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)
    CODESEGMENT = Column(ForeignKey("dbo.CODESEGMENT_TYPE.ID"), nullable=False)

    CODESEGMENT_TYPE = relationship("CODESEGMENTTYPE")


class CONTRACTTYPE(Base):
    __tablename__ = "CONTRACT_TYPE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    SHORT_TERM = Column(Unicode(4), nullable=False)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_EN = Column(Unicode(256), nullable=False)
    NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="CONTRACTTYPE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="CONTRACTTYPE.UPDATED_BY == STAFF.ST_ID"
    )


class CONTRACTTYPEDEFAULT(Base):
    __tablename__ = "CONTRACT_TYPE_DEFAULT"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    HR_ID = Column(UNIQUEIDENTIFIER, nullable=False)
    CONTRACT_TYPE = Column(Integer, nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="CONTRACTTYPEDEFAULT.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="CONTRACTTYPEDEFAULT.UPDATED_BY == STAFF.ST_ID"
    )


class CRMLOGDATAPOSITION(Base):
    __tablename__ = "CRM_LOG_DATA_POSITION"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    LOG_ID = Column(ForeignKey("dbo.CRM_LOG_DATA.ID"), nullable=False)
    NUMBER = Column(Integer)
    TEXT = Column(Unicode(1024))
    SINGLE_PRICE = Column(DECIMAL(18, 2))
    FACTOR = Column(DECIMAL(18, 2))
    INTERNAL_NOTE = Column(Unicode(1024))
    TYPE = Column(Integer)
    MATERIAL_CODE = Column(Unicode(18))
    UNIT = Column(Unicode(3))
    DISCOUNT = Column(DECIMAL(18, 2))

    CRM_LOG_DATUM = relationship("CRMLOGDATUM")


class CURRENCY(Base):
    __tablename__ = "CURRENCY"
    __table_args__ = {"schema": "dbo"}

    CUR_ID = Column(NCHAR(3), primary_key=True)
    CUR_SHORT = Column(NCHAR(3), nullable=False)
    CUR_NAME = Column(Unicode(256), nullable=False)
    CUR_SIGN = Column(Unicode(4), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    CUR_DECIMAL_PLACES = Column(Integer, nullable=False)
    RUN_ID = Column(Integer)
    CUR_SIGN_IS_TRAILING = Column(BIT)

    STAFF = relationship(
        "STAFF", primaryjoin="CURRENCY.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="CURRENCY.UPDATED_BY == STAFF.ST_ID"
    )


class CUSTOMER(Base):
    __tablename__ = "CUSTOMER"
    __table_args__ = (
        Index(
            "IX_CUSTOMER_MD_ID_CU_ACTIVE_CU_ID",
            "MD_ID",
            "CU_ACTIVE",
            "CU_ID",
            "CU_NUMBER",
            "CU_LOCKED",
            "CU_BOOKING_AREA",
            "CU_SERVERID",
            "CU_LANGUAGE",
            "CU_USER_STATE",
        ),
        Index(
            "IX_CUSTOMER_MD_ID_CU_ACTIVE_CU_KTOKD_CU_ID_CU_NUMBER",
            "MD_ID",
            "CU_ACTIVE",
            "CU_KTOKD",
            "CU_ID",
            "CU_NUMBER",
            "CU_LOCKED",
            "CU_SERVERID",
            "CU_LANGUAGE",
            "CU_USER_STATE",
        ),
        Index("IX_CUSTOMER_MDO_NUMBER_CU_NUMBER", "MDO_NUMBER", "CU_NUMBER"),
        Index(
            "IX_CUSTOMER_CU_BOOKING_AREA_CU_MARK",
            "CU_BOOKING_AREA",
            "CU_MARK",
            "CU_ID",
            "CU_NUMBER",
        ),
        {"schema": "dbo"},
    )

    CU_ID = Column(Integer, primary_key=True)
    MD_ID = Column(ForeignKey("dbo.MANDATOR.ID"), nullable=False)
    CU_NUMBER = Column(Unicode(10), index=True)
    CU_ACTIVE = Column(BIT)
    CU_AUTHORIZATION = Column(Unicode(30))
    CU_SUPPLIER_NO = Column(Unicode(24))
    CU_CLASS = Column(NCHAR(2))
    CU_ATTENDENT = Column(Unicode(40))
    CU_DATE = Column(DateTime)
    CU_UPDATE = Column(DateTime)
    CU_LOCKED = Column(NCHAR(2))
    CU_BOOKING_AREA = Column(Unicode(4))
    CU_SERVERID = Column(Integer)
    CU_UPDATE_TYPE = Column(TINYINT)
    CU_ISSUPPLIER = Column(BIT)
    CU_LANGUAGE = Column(NCHAR(2))
    CU_USER_STATE = Column(Unicode(5))
    CU_VBUND = Column(Unicode(40))
    CU_LOEKZ = Column(NCHAR(1))
    RUN_ID = Column(Integer)
    CU_KTOKD = Column(Unicode(10))
    DEFAULT_CONTACT_PERSON = Column(Integer)
    IS_SURVEY_PARTICIPANT = Column(BIT, nullable=False)
    SURVEY_REJECT_REASON = Column(Unicode(512))
    SEND_SURVEYS_TO_MANUFACTURER = Column(BIT, nullable=False)
    TAX_ID_NUMBER = Column(Unicode(64))
    CU_MARK = Column(Unicode(256))
    CU_DISABLED_PSE = Column(DateTime)
    MDO_NUMBER = Column(Unicode(10))
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    DUNSNUMBER = Column(Unicode(10))
    EINVOICING_RELEVANCE = Column(Unicode(10))
    PRINT_OPTION = Column(Unicode(3))

    STAFF = relationship(
        "STAFF", primaryjoin="CUSTOMER.CREATED_BY == STAFF.ST_ID"
    )
    MANDATOR = relationship("MANDATOR")
    STAFF1 = relationship(
        "STAFF", primaryjoin="CUSTOMER.UPDATED_BY == STAFF.ST_ID"
    )


class CUSTOMERMANUFACTURER(CUSTOMER):
    __tablename__ = "CUSTOMER_MANUFACTURER"
    __table_args__ = {"schema": "dbo"}

    CU_ID = Column(ForeignKey("dbo.CUSTOMER.CU_ID"), primary_key=True)
    AUDIT_PLANNED = Column(BIT)
    TRAFFIC_LIGHT = Column(Integer)
    COMMENT = Column(Unicode(2000))


class CUSTOMERCONTACTFUNCTION(Base):
    __tablename__ = "CUSTOMER_CONTACT_FUNCTION"
    __table_args__ = {"schema": "dbo"}

    CCF_ID = Column(Integer, primary_key=True)
    MD_ID = Column(Integer, nullable=False)
    CUC_SCOPE = Column(Unicode(60), nullable=False)
    CCF_NAME_DE = Column(Unicode(256), nullable=False)
    CCF_NAME_EN = Column(Unicode(256), nullable=False)
    CCF_NAME_FR = Column(Unicode(256), nullable=False)
    CCF_CREATED = Column(DateTime, nullable=False)
    CCF_CREATEDBY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    CCF_UPDATED = Column(DateTime, nullable=False)
    CCF_UPDATEDBY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF",
        primaryjoin="CUSTOMERCONTACTFUNCTION.CCF_CREATEDBY == STAFF.ST_ID",
    )
    STAFF1 = relationship(
        "STAFF",
        primaryjoin="CUSTOMERCONTACTFUNCTION.CCF_UPDATEDBY == STAFF.ST_ID",
    )


class CUSTOMERREGION(Base):
    __tablename__ = "CUSTOMER_REGION"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    COUNTRY = Column(Unicode(3), nullable=False)
    NATION = Column(NCHAR(1), nullable=False)
    REGION = Column(Unicode(3), nullable=False)
    NAME = Column(Unicode(1024), nullable=False)
    DISABLED = Column(DateTime)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)

    STAFF = relationship(
        "STAFF", primaryjoin="CUSTOMERREGION.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="CUSTOMERREGION.UPDATED_BY == STAFF.ST_ID"
    )


class DEADLINEDEFAULT(Base):
    __tablename__ = "DEADLINE_DEFAULT"
    __table_args__ = {"schema": "dbo"}

    DD_ID = Column(Integer, primary_key=True)
    DD_DAYS = Column(Integer, nullable=False)
    DD_NAME_DE = Column(Unicode(256), nullable=False)
    DD_NAME_EN = Column(Unicode(256), nullable=False)
    DD_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="DEADLINEDEFAULT.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="DEADLINEDEFAULT.UPDATED_BY == STAFF.ST_ID"
    )


class DELAYREASON(Base):
    __tablename__ = "DELAYREASON"
    __table_args__ = {"schema": "dbo"}

    DELR_ID = Column(Integer, primary_key=True)
    DELR_NAME_DE = Column(Unicode(256), nullable=False)
    DELR_NAME_EN = Column(Unicode(256), nullable=False)
    DELR_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="DELAYREASON.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="DELAYREASON.UPDATED_BY == STAFF.ST_ID"
    )


class DEVICETYPE(Base):
    __tablename__ = "DEVICE_TYPE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_EN = Column(Unicode(256), nullable=False)
    DISABLED = Column(Date)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)

    STAFF = relationship(
        "STAFF", primaryjoin="DEVICETYPE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="DEVICETYPE.UPDATED_BY == STAFF.ST_ID"
    )


class DIRECTORY(Base):
    __tablename__ = "DIRECTORIES"
    __table_args__ = {"schema": "dbo"}

    DIR_ID = Column(Integer, primary_key=True)
    MD_ID = Column(ForeignKey("dbo.MANDATOR.ID"), nullable=False)
    DIR_PFAD = Column(Unicode(256), nullable=False)
    DIR_TYPE = Column(Unicode(256), nullable=False)
    DIR_VISIBLE = Column(BIT, nullable=False)
    PORTAL_TYPE = Column(Unicode(256))
    VALID_UNTIL = Column(DateTime)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    WORKING_CLUSTER = Column(ForeignKey("dbo.HIERARCHY.HR_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="DIRECTORY.CREATED_BY == STAFF.ST_ID"
    )
    MANDATOR = relationship("MANDATOR")
    STAFF1 = relationship(
        "STAFF", primaryjoin="DIRECTORY.UPDATED_BY == STAFF.ST_ID"
    )
    HIERARCHY = relationship("HIERARCHY")


class DISPODATASECTIONRULE(Base):
    __tablename__ = "DISPO_DATASECTION_RULE"
    __table_args__ = {"schema": "dbo"}

    DATA_SECTION = Column(Unicode(100), primary_key=True, nullable=False)
    CUSTOMER = Column(
        ForeignKey("dbo.DISPO_KNOWN_CUSTOMERS.ID"),
        primary_key=True,
        nullable=False,
    )
    TEST_TYPE = Column(Unicode(100), nullable=False)
    RULE = Column(Unicode(4000), nullable=False)
    OPTIONS = Column(Unicode(4000))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)
    DISABLED = Column(DateTime)

    DISPO_KNOWN_CUSTOMER = relationship("DISPOKNOWNCUSTOMER")


class DOCTYPE(Base):
    __tablename__ = "DOCTYPE"
    __table_args__ = {"schema": "dbo"}

    DOCT_ID = Column(Integer, primary_key=True)
    DOCT_NAME_DE = Column(Unicode(256), nullable=False)
    DOCT_NAME_EN = Column(Unicode(256), nullable=False)
    DOCT_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="DOCTYPE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="DOCTYPE.UPDATED_BY == STAFF.ST_ID"
    )


class EMAILSUBJECT(Base):
    __tablename__ = "EMAIL_SUBJECT"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    MD_ID = Column(ForeignKey("dbo.MANDATOR.ID"), nullable=False)
    HR_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"))
    FORM_NAME = Column(Unicode(50))
    SUBJECT_ID = Column(Integer, nullable=False, unique=True)
    MENU_TEXT_DE = Column(Unicode(256), nullable=False)
    MENU_TEXT_EN = Column(Unicode(256), nullable=False)
    SORT_ORDER = Column(Integer, nullable=False)
    PROJECT_TYPE = Column(Integer, nullable=False)
    FORMAT_STRING_DE = Column(Unicode(256), nullable=False)
    FORMAT_STRING_EN = Column(Unicode(256), nullable=False)
    RULE_ID = Column(Integer, nullable=False)
    DISABLED = Column(DATETIME2)
    CREATED = Column(DATETIME2, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DATETIME2)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="EMAILSUBJECT.CREATED_BY == STAFF.ST_ID"
    )
    HIERARCHY = relationship("HIERARCHY")
    MANDATOR = relationship("MANDATOR")
    STAFF1 = relationship(
        "STAFF", primaryjoin="EMAILSUBJECT.UPDATED_BY == STAFF.ST_ID"
    )


class ERRORCOMMENT(Base):
    __tablename__ = "ERRORCOMMENT"
    __table_args__ = {"schema": "dbo"}

    ERR_ID = Column(Integer, primary_key=True)
    ERR_NAME_DE = Column(Unicode(256), nullable=False)
    ERR_NAME_EN = Column(Unicode(256), nullable=False)
    ERR_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="ERRORCOMMENT.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="ERRORCOMMENT.UPDATED_BY == STAFF.ST_ID"
    )


t_FILE_FORMAT = Table(
    "FILE_FORMAT",
    metadata,
    Column("WORKING_CLUSTER", UNIQUEIDENTIFIER),
    Column("ID", Integer, nullable=False),
    Column("NAME_DE", Unicode(256), nullable=False),
    Column("NAME_EN", Unicode(256), nullable=False),
    Column("NAME_FR", Unicode(256), nullable=False),
    Column("VALUE", Unicode(256), nullable=False),
    Column("DISABLED", DateTime),
    Column("CREATED", DateTime, nullable=False),
    Column("CREATED_BY", ForeignKey("dbo.STAFF.ST_ID"), nullable=False),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", ForeignKey("dbo.STAFF.ST_ID")),
    schema="dbo",
)


class FILEFORMATREGISTER(Base):
    __tablename__ = "FILE_FORMAT_REGISTER"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    FILE_FORMAT_ID = Column(Integer, nullable=False)
    REGISTER_NAME = Column(Unicode(256), nullable=False)
    VALUE = Column(Unicode(256))
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="FILEFORMATREGISTER.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="FILEFORMATREGISTER.UPDATED_BY == STAFF.ST_ID"
    )


class GMACOUNTRY(Base):
    __tablename__ = "GMA_COUNTRY"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_EN = Column(Unicode(256), nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DATETIME2, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)

    STAFF = relationship("STAFF")


class GMAENTRY(Base):
    __tablename__ = "GMA_ENTRY"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    P_ID = Column(Integer, nullable=False)
    SO_NUMBER = Column(Integer, nullable=False)
    COUNTRY_ID = Column(Integer, nullable=False)
    STATUS_ID = Column(Integer, nullable=False)
    RESULT_ID = Column(Integer)
    COMMENT = Column(Unicode(256))
    STATUS_DATE = Column(Date)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DATETIME2, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DATETIME2)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="GMAENTRY.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="GMAENTRY.UPDATED_BY == STAFF.ST_ID"
    )


class GMARESULT(Base):
    __tablename__ = "GMA_RESULT"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_EN = Column(Unicode(256), nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DATETIME2, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)

    STAFF = relationship("STAFF")


class GMASTATU(Base):
    __tablename__ = "GMA_STATUS"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_EN = Column(Unicode(256), nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DATETIME2, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)

    STAFF = relationship("STAFF")


class HIERARCHYOPTION(Base):
    __tablename__ = "HIERARCHY_OPTION"
    __table_args__ = (
        Index(
            "UIX_HIERARCHY_OPTION_HR_ID_OPTION_KEY_DISABLED",
            "HR_ID",
            "OPTION_KEY",
            "DISABLED",
            unique=True,
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    HR_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"), nullable=False)
    OPTION_KEY = Column(Unicode(64), nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)
    IS_INTERNATIONAL_AWARE = Column(BIT, nullable=False)
    VALID_FROM = Column(DATETIME2, nullable=False)

    HIERARCHY = relationship("HIERARCHY")


class HOLIDAY(Base):
    __tablename__ = "HOLIDAY"
    __table_args__ = (
        Index(
            "UIX_HOLIDAY_H_HOLIDAYDATE_H_DISABLED_HR_ID",
            "H_HOLIDAYDATE",
            "HR_ID",
            unique=True,
        ),
        {"schema": "dbo"},
    )

    H_ID = Column(Integer, primary_key=True)
    H_HOLIDAYDATE = Column(DateTime)
    H_DISABLED = Column(BIT, nullable=False)
    HR_ID = Column(UNIQUEIDENTIFIER)
    H_HOLIDAY_NAME = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="HOLIDAY.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="HOLIDAY.UPDATED_BY == STAFF.ST_ID"
    )


class ICTRANSACTION(Base):
    __tablename__ = "IC_TRANSACTION"
    __table_args__ = {"schema": "dbo"}

    Id = Column(Integer, primary_key=True)
    ICTR_ID = Column(NCHAR(2), nullable=False)
    ICTR_DESCRIPTION_DE = Column(Unicode(256), nullable=False)
    ICTR_DESCRIPTION_EN = Column(Unicode(256), nullable=False)
    ICTR_DESCRIPTION_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="ICTRANSACTION.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="ICTRANSACTION.UPDATED_BY == STAFF.ST_ID"
    )


class INSPECTIONCYCLE(Base):
    __tablename__ = "INSPECTION_CYCLE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="INSPECTIONCYCLE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="INSPECTIONCYCLE.UPDATED_BY == STAFF.ST_ID"
    )


class INTERNALNOTE(Base):
    __tablename__ = "INTERNAL_NOTE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_EN = Column(Unicode(256), nullable=False)
    NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="INTERNALNOTE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="INTERNALNOTE.UPDATED_BY == STAFF.ST_ID"
    )


class KALK(Base):
    __tablename__ = "KALK"
    __table_args__ = {"schema": "dbo"}

    KAL_ID = Column(Integer, primary_key=True)
    MD_ID = Column(ForeignKey("dbo.MANDATOR.ID"), nullable=False)
    KAL_NAME_DE = Column(Unicode(60))
    KAL_NAME_EN = Column(Unicode(60))
    KAL_NAME_FR = Column(Unicode(60))
    PRP_ID = Column(Integer, nullable=False)
    TPSC_ID = Column(Integer, nullable=False)
    PRIC_ID = Column(Integer, nullable=False)
    KAL_KOMMENTAR = Column(Unicode(255))
    KAL_IS_TEMPLATE = Column(BIT, nullable=False)
    KAL_REGDATE = Column(DateTime, nullable=False)
    KAL_REGBY = Column(Integer)
    KAL_UPDATE = Column(DateTime)
    KAL_UPDATEBY = Column(Integer)
    KAL_SUM_VK = Column(DECIMAL(18, 2), nullable=False)
    KAL_SUM_HK = Column(DECIMAL(18, 2), nullable=False)
    KAL_SUM_ADDON_VK = Column(DECIMAL(18, 2), nullable=False)
    KAL_SUM_ADDON_HK = Column(DECIMAL(18, 2), nullable=False)
    KAL_SUM_BASIC_VK = Column(DECIMAL(18, 2), nullable=False)
    KAL_SUM_BASIC_HK = Column(DECIMAL(18, 2), nullable=False)
    KAL_SUM_CERTIFICATE_PC = Column(DECIMAL(18, 2), nullable=False)
    KAL_SUM_CERTIFICATE_RP = Column(DECIMAL(18, 2), nullable=False)
    KAL_SUM_LICENSE_PC = Column(DECIMAL(18, 2), nullable=False)
    KAL_SUM_LICENSE_RP = Column(DECIMAL(18, 2), nullable=False)
    KAL_SUM_MANUFACTURING_PC = Column(DECIMAL(18, 2), nullable=False)
    KAL_SUM_MANUFACTURING_RP = Column(DECIMAL(18, 2), nullable=False)
    KAL_USES_SUBMODULES = Column(BIT, nullable=False)

    MANDATOR = relationship("MANDATOR")


class KALKMODUL(Base):
    __tablename__ = "KALKMODUL"
    __table_args__ = {"schema": "dbo"}

    KALM_ID = Column(Integer, primary_key=True)
    KAL_ID = Column(Integer, nullable=False)
    KALM_TYP = Column(Integer)
    KALM_IS_MASTER = Column(BIT, nullable=False)
    KALM_NAME_DE = Column(Unicode(256))
    KALM_NAME_EN = Column(Unicode(256))
    KALM_NAME_FR = Column(Unicode(256))
    KALM_IS_UA = Column(BIT, nullable=False)
    KALM_TAGE_UA = Column(Integer, nullable=False)
    TP_ID = Column(Integer)
    KALM_TESTDAUER = Column(Integer)
    KALM_EINHEITEN = Column(DECIMAL(18, 2), nullable=False)
    KALM_SATZ = Column(DECIMAL(18, 2), nullable=False)
    KALM_AUFWAND = Column(DECIMAL(18, 2), nullable=False)
    KALM_FAKTOR = Column(DECIMAL(18, 2), nullable=False)
    KALM_VK = Column(DECIMAL(18, 2), nullable=False)
    KALM_AUFTRAGSTEXT = Column(Unicode(500))
    KALM_KOMMENTAR = Column(Unicode(500))
    KALM_REIHE = Column(Integer, nullable=False)
    KALM_REGDATE = Column(DateTime, nullable=False)
    KALM_REGBY = Column(Integer)
    KALM_UPDATE = Column(DateTime)
    KALM_UPDATEBY = Column(Integer)
    WORKING_CLUSTER = Column(ForeignKey("dbo.HIERARCHY.HR_ID"))

    HIERARCHY = relationship("HIERARCHY")


class KEYWORD(Base):
    __tablename__ = "KEYWORD"
    __table_args__ = (
        Index("UK_KEYWORD_MD_KEY", "MD_ID", "KEY", unique=True),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    MD_ID = Column(ForeignKey("dbo.MANDATOR.ID"), nullable=False)
    KEY = Column(Unicode(30), nullable=False)
    QUERY = Column(ForeignKey("dbo.QUERY.ID"), nullable=False)
    KEYWORD_TYPE = Column(ForeignKey("dbo.KEYWORD_TYPE.ID"), nullable=False)
    HEADERLINE_RESOURCE = Column(Unicode(100))
    DESCRIPTION_DE = Column(Unicode(256), nullable=False)
    DESCRIPTION_EN = Column(Unicode(256), nullable=False)
    ADDITIONALPARAM = Column(Unicode(1000))
    HAS_HEADER = Column(BIT, nullable=False)
    FOOTERS = Column(Integer, nullable=False)
    PADDING = Column(Float(53), nullable=False)
    PARAGRAPH_SPACING = Column(Float(53), nullable=False)
    TABLE_LEFT_INDENT = Column(DECIMAL(18, 2), nullable=False)
    PREFERREDWIDTH = Column(DECIMAL(18, 2))
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)

    KEYWORD_TYPE1 = relationship("KEYWORDTYPE")
    MANDATOR = relationship("MANDATOR")
    QUERY1 = relationship("QUERY")


class KINDOFBILL(Base):
    __tablename__ = "KIND_OF_BILL"
    __table_args__ = {"schema": "dbo"}

    KOB_ID = Column(Integer, primary_key=True)
    KOB_NAME_DE = Column(Unicode(256), nullable=False)
    KOB_NAME_EN = Column(Unicode(256), nullable=False)
    KOB_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    DISABLED = Column(DateTime)

    STAFF = relationship(
        "STAFF", primaryjoin="KINDOFBILL.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="KINDOFBILL.UPDATED_BY == STAFF.ST_ID"
    )


class KINDOFPRODUCT(Base):
    __tablename__ = "KIND_OF_PRODUCT"
    __table_args__ = {"schema": "dbo"}

    KOP_ID = Column(Integer, primary_key=True)
    KOP_NAME_DE = Column(Unicode(256), nullable=False)
    KOP_NAME_EN = Column(Unicode(256), nullable=False)
    KOP_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    DISABLED = Column(DateTime)

    STAFF = relationship(
        "STAFF", primaryjoin="KINDOFPRODUCT.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="KINDOFPRODUCT.UPDATED_BY == STAFF.ST_ID"
    )


class KINDOFTEST(Base):
    __tablename__ = "KIND_OF_TEST"
    __table_args__ = {"schema": "dbo"}

    WORKING_CLUSTER = Column(
        ForeignKey("dbo.HIERARCHY.HR_ID"), primary_key=True, nullable=False
    )
    KOT_ID = Column(Integer, primary_key=True, nullable=False)
    KOT_SHORT = Column(Unicode(256), nullable=False)
    KOT_NAME_DE = Column(Unicode(1024))
    KOT_NAME_EN = Column(Unicode(1024))
    KOT_NAME_FR = Column(Unicode(1024))
    DISABLED = Column(DateTime)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="KINDOFTEST.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="KINDOFTEST.UPDATED_BY == STAFF.ST_ID"
    )
    HIERARCHY = relationship("HIERARCHY")


class LIDLQAMEMBER(Base):
    __tablename__ = "LIDL_QA_MEMBER"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME = Column(Unicode(128), nullable=False)
    EMAIL_ADDRESS = Column(Unicode(256), nullable=False)
    DISABLED = Column(DateTime)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    INITIALS = Column(Unicode(20))

    STAFF = relationship(
        "STAFF", primaryjoin="LIDLQAMEMBER.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="LIDLQAMEMBER.UPDATED_BY == STAFF.ST_ID"
    )


class LIMSSTANDARDANALYSI(Base):
    __tablename__ = "LIMS_STANDARD_ANALYSIS"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    STKO_ID = Column(Integer, nullable=False)
    STANDARD_ANALYSIS = Column(Unicode(128), nullable=False)
    TEST_METHOD_ID = Column(
        ForeignKey("dbo.LIMS_TEST_METHOD.ID"), nullable=False
    )
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)

    LIMS_TEST_METHOD = relationship("LIMSTESTMETHOD")


class LOCATIONSERVER(Base):
    __tablename__ = "LOCATIONSERVER"
    __table_args__ = {"schema": "dbo"}

    LS_ID = Column(Integer, primary_key=True)
    HR_ID = Column(
        ForeignKey("dbo.HIERARCHY.HR_ID"), nullable=False, unique=True
    )
    MD_ID = Column(ForeignKey("dbo.MANDATOR.ID"), nullable=False)
    LS_SERVERPATH = Column(Unicode(255), nullable=False)
    LS_REMARK = Column(Unicode(255))
    LS_WEBSERVER = Column(Unicode(255))
    LS_DECENTRALIZED_STORAGE = Column(Unicode(255))
    LS_EXPORT_STORAGE = Column(Unicode(255))
    LS_SAPSERVER = Column(Integer)
    LS_DEPLOYPATH = Column(Unicode(255))
    LS_BASE_CURRENCY = Column(NCHAR(3))
    LS_TTI = Column(Unicode(64))
    LS_QDOC = Column(Unicode(64))
    LS_RATE_RECOMM_PRICE = Column(DECIMAL(19, 4))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    USAGE_LOGGING_ENABLED = Column(BIT, nullable=False)
    COUNTRY_CODE = Column(NCHAR(2))
    SEARCH_RESTRICTION_ENABLED = Column(BIT, nullable=False)
    VKORG = Column(Unicode(4), nullable=False)
    ACTION_START_DATE_OFFSET = Column(Integer, nullable=False)
    ACTION_DEADLINE_DATE_OFFSET = Column(Integer, nullable=False)
    CONTRACT_TYPE_LIMIT = Column(DECIMAL(18, 2))
    PLANT_PER_POSITION_ENABLED = Column(BIT, nullable=False)
    POSTING_APPROVAL_REQUIRED = Column(BIT, nullable=False)
    LANGUAGE = Column(ForeignKey("dbo.LANGUAGE_TYPE.ID"), nullable=False)
    CENTRAL_MAILBOX = Column(Unicode(256))
    ORDER_TEXT_WORD_WRAP = Column(Integer)
    POSITION_TEXT_WORD_WRAP = Column(Integer)
    LS_INTERNATIONAL_SERVERPATH = Column(Unicode(255))
    LS_TEAM_OU = Column(Unicode(1000))
    LS_DOMAIN = Column(Unicode(32))
    FAZ_TEMPLATE_NAME = Column(Unicode(256))
    MDO_NUMBER = Column(Unicode(10))
    LS_CULTURE = Column(Unicode(50))
    LS_TEMPLATE_SERVERPATH = Column(Unicode(255))
    DEFAULT_PRINT_OPTION = Column(Unicode(3))
    EXCHANGE_WS_URL = Column(Unicode(1024))
    CONTRACT_TYPE_MANDATORY = Column(Integer, nullable=False)

    STAFF = relationship(
        "STAFF", primaryjoin="LOCATIONSERVER.CREATED_BY == STAFF.ST_ID"
    )
    HIERARCHY = relationship("HIERARCHY")
    LANGUAGE_TYPE = relationship("LANGUAGETYPE")
    MANDATOR = relationship("MANDATOR")
    STAFF1 = relationship(
        "STAFF", primaryjoin="LOCATIONSERVER.UPDATED_BY == STAFF.ST_ID"
    )


class MAINGRIDINIT(Base):
    __tablename__ = "MAINGRIDINIT"
    __table_args__ = {"schema": "dbo"}

    WC_ID = Column(
        ForeignKey("dbo.HIERARCHY.HR_ID"), primary_key=True, nullable=False
    )
    ColumnName = Column(Unicode(30), primary_key=True, nullable=False)
    FixedWidth = Column(BIT, nullable=False)
    Width = Column(Integer, nullable=False)
    VisibleIndex = Column(Integer, nullable=False)
    IsMapped = Column(BIT, nullable=False)
    ResourcePage = Column(Unicode(256), primary_key=True, nullable=False)
    ResourceName = Column(Unicode(256))
    BestFit = Column(BIT)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="MAINGRIDINIT.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="MAINGRIDINIT.UPDATED_BY == STAFF.ST_ID"
    )
    HIERARCHY = relationship("HIERARCHY")


class NOTIFICATION(Base):
    __tablename__ = "NOTIFICATION"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    TARGET = Column(Integer, nullable=False)
    RELATES_TO_KIND = Column(Integer, nullable=False)
    RELATES_TO_PRIMARY = Column(Integer, nullable=False)
    RELATES_TO_SECONDARY = Column(Integer)
    NOTIFIED = Column(DATETIME2)
    CREATED = Column(DATETIME2, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)

    STAFF = relationship("STAFF")


class OBJECTCATEGORYMD(Base):
    __tablename__ = "OBJECTCATEGORY_MD"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_EN = Column(Unicode(256), nullable=False)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_FR = Column(Unicode(256), nullable=False)
    SORT = Column(Integer, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="OBJECTCATEGORYMD.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="OBJECTCATEGORYMD.UPDATED_BY == STAFF.ST_ID"
    )


class PERIODFILTER(Base):
    __tablename__ = "PERIODFILTER"
    __table_args__ = {"schema": "dbo"}

    PER_ID = Column(Integer, primary_key=True)
    PER_NAME_DE = Column(Unicode(256), nullable=False)
    PER_NAME_EN = Column(Unicode(256), nullable=False)
    PER_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="PERIODFILTER.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PERIODFILTER.UPDATED_BY == STAFF.ST_ID"
    )


class PERMISSION(Base):
    __tablename__ = "PERMISSION"
    __table_args__ = {"schema": "dbo"}

    PS_ID = Column(Integer, primary_key=True)
    PS_CONTROLNAME = Column(Unicode(256), nullable=False)
    PS_PARENT = Column(Unicode(256), nullable=False)
    PS_TYPE = Column(Integer, nullable=False)
    PS_ACTION_RIGHT_DE = Column(Unicode(256), nullable=False)
    PS_ACTION_RIGHT_EN = Column(Unicode(256), nullable=False)
    PS_ACTION_RIGHT_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UpdateDate = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="PERMISSION.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PERMISSION.UPDATED_BY == STAFF.ST_ID"
    )


class PLANT(Base):
    __tablename__ = "PLANT"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    KEY_FOR_SAP = Column(Unicode(4), nullable=False)
    DISPLAY_NAME = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="PLANT.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PLANT.UPDATED_BY == STAFF.ST_ID"
    )


class PORTAL(Base):
    __tablename__ = "PORTAL"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME = Column(Unicode(64), nullable=False)
    PATH = Column(Unicode(256))
    MAIN_PORTAL_ID = Column(ForeignKey("dbo.PORTAL.ID"))
    EMAIL_RECIPIENT = Column(Unicode(128))
    SHOW_SAP_NUMBER = Column(BIT, nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    UCI_URL = Column(Unicode(256))

    STAFF = relationship(
        "STAFF", primaryjoin="PORTAL.CREATED_BY == STAFF.ST_ID"
    )
    parent = relationship("PORTAL", remote_side=[ID])
    STAFF1 = relationship(
        "STAFF", primaryjoin="PORTAL.UPDATED_BY == STAFF.ST_ID"
    )


class PORTALCUSTOMER(Base):
    __tablename__ = "PORTAL_CUSTOMER"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    PORTAL_ID = Column(Integer, nullable=False)
    CU_ID = Column(Integer, nullable=False)
    TYPE = Column(Integer, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    DISABLED = Column(BIT, nullable=False)

    STAFF = relationship(
        "STAFF", primaryjoin="PORTALCUSTOMER.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PORTALCUSTOMER.UPDATED_BY == STAFF.ST_ID"
    )


class PRESSUREUNITMD(Base):
    __tablename__ = "PRESSUREUNIT_MD"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_EN = Column(Unicode(256), nullable=False)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_FR = Column(Unicode(256), nullable=False)
    SORT = Column(Integer, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="PRESSUREUNITMD.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PRESSUREUNITMD.UPDATED_BY == STAFF.ST_ID"
    )


class PRICELIST(Base):
    __tablename__ = "PRICELIST"
    __table_args__ = {"schema": "dbo"}

    PRIC_ID = Column(Integer, primary_key=True)
    PRIC_NAME_DE = Column(Unicode(256), nullable=False)
    PRIC_NAME_EN = Column(Unicode(256), nullable=False)
    PRIC_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="PRICELIST.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PRICELIST.UPDATED_BY == STAFF.ST_ID"
    )


class PROCESSFOLDER(Base):
    __tablename__ = "PROCESSFOLDER"
    __table_args__ = {"schema": "dbo"}

    PCF_ID = Column(Integer, primary_key=True)
    PZ_ID = Column(Integer)
    TPT_ID = Column(Integer)
    PCF_VERSION = Column(Integer)
    PCF_CURRENTVERSION = Column(BIT, nullable=False)
    PCF_FILENAME = Column(Unicode(255))
    PCF_COMMENT = Column(Unicode(255))
    PCF_REGDATE = Column(DateTime)
    PCF_REGBY = Column(Integer)
    PCF_UPDATE = Column(DateTime)
    PCF_UPDATEBY = Column(Integer)
    PCF_CHECKOUTBY = Column(Integer)
    PCF_CHECKOUT = Column(DateTime)
    PCF_WEBNAME = Column(Unicode(255))
    PCF_CHECKOUTBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    PCF_REGBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    PCF_UPDATEBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    AL_ID = Column(ForeignKey("dbo.ANONYMIZATION_LOG.AL_ID"))

    ANONYMIZATION_LOG = relationship("ANONYMIZATIONLOG")
    HIERARCHY = relationship(
        "HIERARCHY",
        primaryjoin="PROCESSFOLDER.PCF_CHECKOUTBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    HIERARCHY1 = relationship(
        "HIERARCHY",
        primaryjoin="PROCESSFOLDER.PCF_REGBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    HIERARCHY2 = relationship(
        "HIERARCHY",
        primaryjoin="PROCESSFOLDER.PCF_UPDATEBY_TEAM == HIERARCHY.HR_NEW_ID",
    )


class PROCESSPHASE(Base):
    __tablename__ = "PROCESSPHASE"
    __table_args__ = {"schema": "dbo"}

    PRP_ID = Column(Integer, primary_key=True)
    PRP_NAME_DE = Column(Unicode(256))
    PRP_NAME_EN = Column(Unicode(256))
    PRP_NAME_FR = Column(Unicode(256))
    PRP_SHORT_DE = Column(Unicode(256))
    PRP_SHORT_EN = Column(Unicode(256))
    PRP_SHORT_FR = Column(Unicode(256))
    PRP_SORT = Column(Integer, nullable=False)
    PRP_SHOW_IN_PSEX = Column(BIT, nullable=False)
    PRP_EDOC_ACTIVE = Column(BIT, nullable=False)
    PRP_EDOC_NAME_DE = Column(Unicode(256))
    PRP_EDOC_NAME_EN = Column(Unicode(256))
    PRP_EDOC_NAME_FR = Column(Unicode(256))
    PRP_EDOC_SHORT_DE = Column(Unicode(256))
    PRP_EDOC_SHORT_EN = Column(Unicode(256))
    PRP_EDOC_SHORT_FR = Column(Unicode(256))
    PRP_EDOC_NUMBER = Column(Integer)
    PRP_EDOC_IS_REFERENCE = Column(BIT, nullable=False)
    PRP_EDOC_IS_DEFAULT = Column(BIT, nullable=False)
    PRP_PUBLISH_BY_DEFAULT = Column(BIT, nullable=False)
    PRP_SET_COLLECTIVE_INVOICE = Column(BIT, nullable=False)
    PRP_SET_BY_DEFAULT = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="PROCESSPHASE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PROCESSPHASE.UPDATED_BY == STAFF.ST_ID"
    )


class PROCESSSTATU(Base):
    __tablename__ = "PROCESSSTATUS"
    __table_args__ = {"schema": "dbo"}

    PS_ID = Column(Integer, primary_key=True)
    PS_NAME_DE = Column(Unicode(256), nullable=False)
    PS_NAME_EN = Column(Unicode(256), nullable=False)
    PS_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="PROCESSSTATU.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PROCESSSTATU.UPDATED_BY == STAFF.ST_ID"
    )


class PRODUCTGROUPMD(Base):
    __tablename__ = "PRODUCTGROUP_MD"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_EN = Column(Unicode(256), nullable=False)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_FR = Column(Unicode(256), nullable=False)
    SORT = Column(Integer, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="PRODUCTGROUPMD.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PRODUCTGROUPMD.UPDATED_BY == STAFF.ST_ID"
    )


class PROJECTCATEGORYMD(Base):
    __tablename__ = "PROJECTCATEGORY_MD"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_EN = Column(Unicode(256), nullable=False)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_FR = Column(Unicode(256), nullable=False)
    SORT = Column(Integer, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="PROJECTCATEGORYMD.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PROJECTCATEGORYMD.UPDATED_BY == STAFF.ST_ID"
    )


class PROJECTFLUIDGROUPMD(Base):
    __tablename__ = "PROJECTFLUIDGROUP_MD"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_EN = Column(Unicode(256), nullable=False)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_FR = Column(Unicode(256), nullable=False)
    SORT = Column(Integer, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="PROJECTFLUIDGROUPMD.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PROJECTFLUIDGROUPMD.UPDATED_BY == STAFF.ST_ID"
    )


class PROJECTMODULEMD(Base):
    __tablename__ = "PROJECTMODULE_MD"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_EN = Column(Unicode(256), nullable=False)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_FR = Column(Unicode(256), nullable=False)
    SORT = Column(Integer, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    DISABLED = Column(DateTime)

    STAFF = relationship(
        "STAFF", primaryjoin="PROJECTMODULEMD.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PROJECTMODULEMD.UPDATED_BY == STAFF.ST_ID"
    )


class PROJECTPERIODFILTER(Base):
    __tablename__ = "PROJECTPERIODFILTER"
    __table_args__ = {"schema": "dbo"}

    PP_ID = Column(Integer, primary_key=True)
    PP_NAME_DE = Column(Unicode(256), nullable=False)
    PP_NAME_EN = Column(Unicode(256), nullable=False)
    PP_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="PROJECTPERIODFILTER.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PROJECTPERIODFILTER.UPDATED_BY == STAFF.ST_ID"
    )


class PROTOCOLEXCELEXPORT(Base):
    __tablename__ = "PROTOCOL_EXCEL_EXPORT"
    __table_args__ = {"schema": "dbo"}

    PRE_ID = Column(Integer, primary_key=True)
    PRE_AGENT = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    PRE_EXPORT_DATE = Column(DateTime, nullable=False)
    PRE_EXPORT_CALL_FROM = Column(Unicode(500), nullable=False)
    PRE_SERVER_DIRECTORY = Column(Unicode(500), nullable=False)
    PRE_EXPORT_FIELDS = Column(Unicode(500))

    STAFF = relationship("STAFF")


class PSEXCREDENTIAL(Base):
    __tablename__ = "PSEX_CREDENTIAL"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True, unique=True)
    NAME = Column(Unicode(256), nullable=False)
    IDENTITY = Column(Unicode(256), nullable=False)
    PWD = Column(Unicode(256))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    IDENTITY365 = Column(Unicode(1024))

    STAFF = relationship(
        "STAFF", primaryjoin="PSEXCREDENTIAL.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PSEXCREDENTIAL.UPDATED_BY == STAFF.ST_ID"
    )


class REASONFORADDITIONALEFFORT(Base):
    __tablename__ = "REASON_FOR_ADDITIONAL_EFFORT"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_EN = Column(Unicode(256), nullable=False)
    NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF",
        primaryjoin="REASONFORADDITIONALEFFORT.CREATED_BY == STAFF.ST_ID",
    )
    STAFF1 = relationship(
        "STAFF",
        primaryjoin="REASONFORADDITIONALEFFORT.UPDATED_BY == STAFF.ST_ID",
    )


class RECOMMENDEDORDERTEXT(Base):
    __tablename__ = "RECOMMENDEDORDERTEXT"
    __table_args__ = {"schema": "dbo"}

    ROT_ID = Column(Integer, primary_key=True, nullable=False)
    MD_ID = Column(
        ForeignKey("dbo.MANDATOR.ID"), primary_key=True, nullable=False
    )
    ROT_NAME_DE = Column(Unicode(256), nullable=False)
    ROT_NAME_EN = Column(Unicode(256), nullable=False)
    ROT_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    DISABLED = Column(BIT, nullable=False)

    STAFF = relationship(
        "STAFF", primaryjoin="RECOMMENDEDORDERTEXT.CREATED_BY == STAFF.ST_ID"
    )
    MANDATOR = relationship("MANDATOR")
    STAFF1 = relationship(
        "STAFF", primaryjoin="RECOMMENDEDORDERTEXT.UPDATED_BY == STAFF.ST_ID"
    )


class RELEASEMETHOD(Base):
    __tablename__ = "RELEASEMETHOD"
    __table_args__ = {"schema": "dbo"}

    RM_ID = Column(Integer, primary_key=True)
    RM_NAME_DE = Column(Unicode(256), nullable=False)
    RM_NAME_EN = Column(Unicode(256), nullable=False)
    RM_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    IS_APPROVAL = Column(BIT, nullable=False)

    STAFF = relationship(
        "STAFF", primaryjoin="RELEASEMETHOD.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="RELEASEMETHOD.UPDATED_BY == STAFF.ST_ID"
    )


class REPORTRELEVANTTESTBASISMD(Base):
    __tablename__ = "REPORTRELEVANTTESTBASIS_MD"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_EN = Column(Unicode(256), nullable=False)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_FR = Column(Unicode(256), nullable=False)
    SORT = Column(Integer, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    DISABLED = Column(DateTime)

    STAFF = relationship(
        "STAFF",
        primaryjoin="REPORTRELEVANTTESTBASISMD.CREATED_BY == STAFF.ST_ID",
    )
    STAFF1 = relationship(
        "STAFF",
        primaryjoin="REPORTRELEVANTTESTBASISMD.UPDATED_BY == STAFF.ST_ID",
    )


class RETURNADDRES(Base):
    __tablename__ = "RETURN_ADDRESS"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    WORKING_CLUSTER = Column(ForeignKey("dbo.HIERARCHY.HR_ID"), nullable=False)
    NAME = Column(Unicode(512))
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)

    STAFF = relationship(
        "STAFF", primaryjoin="RETURNADDRES.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="RETURNADDRES.UPDATED_BY == STAFF.ST_ID"
    )
    HIERARCHY = relationship("HIERARCHY")


class ROH(Base):
    __tablename__ = "ROHS"
    __table_args__ = {"schema": "dbo"}

    ROHS_ID = Column(Integer, primary_key=True)
    ROHS_LIMIT = Column(DECIMAL(18, 0), nullable=False)
    ROHS_NAME_DE = Column(Unicode(256), nullable=False)
    ROHS_NAME_EN = Column(Unicode(256), nullable=False)
    ROHS_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship("STAFF", primaryjoin="ROH.CREATED_BY == STAFF.ST_ID")
    STAFF1 = relationship("STAFF", primaryjoin="ROH.UPDATED_BY == STAFF.ST_ID")


class ROOMDESIGNATIONMD(Base):
    __tablename__ = "ROOMDESIGNATION_MD"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_EN = Column(Unicode(256), nullable=False)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_FR = Column(Unicode(256), nullable=False)
    SORT = Column(Integer, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="ROOMDESIGNATIONMD.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="ROOMDESIGNATIONMD.UPDATED_BY == STAFF.ST_ID"
    )


class SEARCHLEVEL(Base):
    __tablename__ = "SEARCH_LEVEL"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    ST_ID = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    HR_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"), nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="SEARCHLEVEL.CREATED_BY == STAFF.ST_ID"
    )
    HIERARCHY = relationship("HIERARCHY")
    STAFF1 = relationship(
        "STAFF", primaryjoin="SEARCHLEVEL.ST_ID == STAFF.ST_ID"
    )
    STAFF2 = relationship(
        "STAFF", primaryjoin="SEARCHLEVEL.UPDATED_BY == STAFF.ST_ID"
    )


class SIRIGHTSMANAGEMENTTASKDATUM(Base):
    __tablename__ = "SIRIGHTSMANAGEMENT_TASK_DATA"
    __table_args__ = {"schema": "dbo"}

    ID = Column(BigInteger, primary_key=True)
    RIGHTSMANAGEMENTTASK = Column(BigInteger, nullable=False)
    ROLE = Column(ForeignKey("dbo.ROLE.RS_ID"), nullable=False)

    ROLE1 = relationship("ROLE")


class SPECIALTYPE(Base):
    __tablename__ = "SPECIAL_TYPE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_EN = Column(Unicode(256), nullable=False)
    DISABLED = Column(Date)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)

    STAFF = relationship(
        "STAFF", primaryjoin="SPECIALTYPE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="SPECIALTYPE.UPDATED_BY == STAFF.ST_ID"
    )


class STAFFHIERARCHY(Base):
    __tablename__ = "STAFFHIERARCHY"
    __table_args__ = {"schema": "dbo"}

    SH_ID = Column(Integer, primary_key=True)
    ST_ID = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    HR_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"), nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="STAFFHIERARCHY.CREATED_BY == STAFF.ST_ID"
    )
    HIERARCHY = relationship("HIERARCHY")
    STAFF1 = relationship(
        "STAFF", primaryjoin="STAFFHIERARCHY.ST_ID == STAFF.ST_ID"
    )
    STAFF2 = relationship(
        "STAFF", primaryjoin="STAFFHIERARCHY.UPDATED_BY == STAFF.ST_ID"
    )


class STAFFROLE(Base):
    __tablename__ = "STAFFROLE"
    __table_args__ = (
        Index("UQ_STAFFROLE_ST_ID_RS_ID", "ST_ID", "RS_ID", unique=True),
        Index("IX_STAFFROLE_ST_ID_DISABLED", "ST_ID", "RS_ID", "DISABLED"),
        {"schema": "dbo"},
    )

    SR_ID = Column(Integer, primary_key=True)
    ST_ID = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    RS_ID = Column(ForeignKey("dbo.ROLE.RS_ID"), nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="STAFFROLE.CREATED_BY == STAFF.ST_ID"
    )
    ROLE = relationship("ROLE")
    STAFF1 = relationship(
        "STAFF", primaryjoin="STAFFROLE.ST_ID == STAFF.ST_ID"
    )
    STAFF2 = relationship(
        "STAFF", primaryjoin="STAFFROLE.UPDATED_BY == STAFF.ST_ID"
    )


class STAFFFAVORITE(Base):
    __tablename__ = "STAFF_FAVORITES"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    STAFF_ID = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    STAFF_FAV_ID = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="STAFFFAVORITE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="STAFFFAVORITE.STAFF_FAV_ID == STAFF.ST_ID"
    )
    STAFF2 = relationship(
        "STAFF", primaryjoin="STAFFFAVORITE.STAFF_ID == STAFF.ST_ID"
    )
    STAFF3 = relationship(
        "STAFF", primaryjoin="STAFFFAVORITE.UPDATED_BY == STAFF.ST_ID"
    )


class STAFFSETTING(Base):
    __tablename__ = "STAFF_SETTING"
    __table_args__ = {"schema": "dbo"}

    STS_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer, nullable=False)
    STS_KEY = Column(Unicode(50), nullable=False)
    STS_DATA = Column(Unicode)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    STS_DISABLED = Column(BIT, nullable=False)
    STS_DEFAULT = Column(BIT)
    STS_NAME = Column(Unicode(50))

    STAFF = relationship(
        "STAFF", primaryjoin="STAFFSETTING.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="STAFFSETTING.UPDATED_BY == STAFF.ST_ID"
    )


class STAFFVERSIONCHECK(Base):
    __tablename__ = "STAFF_VERSION_CHECK"
    __table_args__ = {"schema": "dbo"}

    STVC_ID = Column(Integer, primary_key=True)
    ST_ID = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UI_ID = Column(ForeignKey("dbo.USER_INFO.ID"), nullable=False)
    CHECKED = Column(DateTime, nullable=False)

    STAFF = relationship("STAFF")
    USER_INFO = relationship("USERINFO")


class STARLIMSDATAPROJECT(Base):
    __tablename__ = "STARLIMS_DATA_PROJECT"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    DATA_ID = Column(ForeignKey("dbo.STARLIMS_DATA.ID"), nullable=False)
    STARLIMS_PROJECT_NUMBER = Column(Unicode(25), nullable=False)

    STARLIMS_DATUM = relationship("STARLIMSDATUM")


class STATEOFAGGREGATIONMD(Base):
    __tablename__ = "STATEOFAGGREGATION_MD"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_EN = Column(Unicode(256), nullable=False)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_FR = Column(Unicode(256), nullable=False)
    SORT = Column(Integer, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="STATEOFAGGREGATIONMD.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="STATEOFAGGREGATIONMD.UPDATED_BY == STAFF.ST_ID"
    )


class STRINGRESOURCE(Base):
    __tablename__ = "STRINGRESOURCE"
    __table_args__ = (
        Index("IX_STRINGRESOURCE_UNIQ", "MD_ID", "Page", "Name", unique=True),
        Index("IX_STRINGRESOURCE", "MD_ID", "Page"),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    MD_ID = Column(ForeignKey("dbo.MANDATOR.ID"), nullable=False)
    Page = Column(Unicode(50), nullable=False)
    Item = Column(Unicode(50))
    Name = Column(Unicode(100), nullable=False, index=True)
    Text_EN = Column(Unicode(3000), nullable=False)
    Text_DE = Column(Unicode(3000), nullable=False)
    Text_FR = Column(Unicode(3000), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)

    MANDATOR = relationship("MANDATOR")


class SUBORDERCATEGORY(Base):
    __tablename__ = "SUBORDER_CATEGORY"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_EN = Column(Unicode(256), nullable=False)
    NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="SUBORDERCATEGORY.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="SUBORDERCATEGORY.UPDATED_BY == STAFF.ST_ID"
    )


class SURVEYORDERSIZE(Base):
    __tablename__ = "SURVEY_ORDER_SIZE"
    __table_args__ = (
        Index(
            "IX_SURVEY_ORDER_SIZE_HR_ID_VALID_FROM_VALID_UNTIL",
            "HR_ID",
            "VALID_FROM",
            "VALID_UNTIL",
            "ORDER_SIZE",
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    HR_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"), nullable=False)
    ORDER_SIZE = Column(DECIMAL(18, 2), nullable=False)
    VALID_FROM = Column(DateTime, nullable=False)
    VALID_UNTIL = Column(DateTime, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="SURVEYORDERSIZE.CREATED_BY == STAFF.ST_ID"
    )
    HIERARCHY = relationship("HIERARCHY")
    STAFF1 = relationship(
        "STAFF", primaryjoin="SURVEYORDERSIZE.UPDATED_BY == STAFF.ST_ID"
    )


class TASKFILETRANSFERPROTO(Base):
    __tablename__ = "TASK_FILETRANSFER_PROTO"
    __table_args__ = {"schema": "dbo"}

    ID = Column(BigInteger, primary_key=True)
    FT_ID = Column(ForeignKey("dbo.TASK_FILETRANSFER.FT_ID"), nullable=False)
    TYPE = Column(NCHAR(1), nullable=False)
    ALTERNATE = Column(BIT)
    FILENAME = Column(Unicode(256))
    MESSAGE = Column(Unicode)
    ISSUED = Column(DateTime, nullable=False)
    EX_MSG = Column(Unicode)

    TASK_FILETRANSFER = relationship("TASKFILETRANSFER")


class TASKPROTOCOL(Base):
    __tablename__ = "TASK_PROTOCOL"
    __table_args__ = {"schema": "dbo"}

    TPROT_ID = Column(BigInteger, primary_key=True)
    RUN_ID = Column(ForeignKey("dbo.TASK_RUN.RUN_ID"), nullable=False)
    PROT_TYPE = Column(NCHAR(1), nullable=False)
    MESSAGE = Column(Unicode)
    ISSUED = Column(DateTime, nullable=False)
    ITEM_ID = Column(Unicode(100))

    TASK_RUN = relationship("TASKRUN")


class TASKROOTMAP(Base):
    __tablename__ = "TASK_ROOTMAP"
    __table_args__ = {"schema": "dbo"}

    TASK_ID = Column(Integer, primary_key=True)
    TASKNAME = Column(Unicode(50), nullable=False)
    ELEMENT_ID = Column(ForeignKey("dbo.TASK_ELEMENT.ID"))
    PREFIX = Column(NCHAR(2), nullable=False)

    TASK_ELEMENT = relationship("TASKELEMENT")


class TASKTABLEMAP(Base):
    __tablename__ = "TASK_TABLEMAP"
    __table_args__ = {"schema": "dbo"}

    TBL_ID = Column(Integer, primary_key=True)
    TABLENAME = Column(Unicode(50), nullable=False)
    PARENT_ID = Column(ForeignKey("dbo.TASK_ELEMENT.ID"))
    ELEMENT_ID = Column(ForeignKey("dbo.TASK_ELEMENT.ID"))
    DODELETE = Column(BIT, nullable=False)
    DISABLE_COLUMN = Column(Unicode(30))

    TASK_ELEMENT = relationship(
        "TASKELEMENT", primaryjoin="TASKTABLEMAP.ELEMENT_ID == TASKELEMENT.ID"
    )
    TASK_ELEMENT1 = relationship(
        "TASKELEMENT", primaryjoin="TASKTABLEMAP.PARENT_ID == TASKELEMENT.ID"
    )


class TEAMRIGHTSMANAGEMENTTASKDATUM(Base):
    __tablename__ = "TEAMRIGHTSMANAGEMENT_TASK_DATA"
    __table_args__ = (
        Index(
            "IX_TEAMRIGHTSMANAGEMENT_TASK_DATA", "RIGHTSMANAGEMENTTASK", "TEAM"
        ),
        {"schema": "dbo"},
    )

    ID = Column(BigInteger, primary_key=True)
    RIGHTSMANAGEMENTTASK = Column(
        ForeignKey("dbo.RIGHTSMANAGEMENT_TASK.ID"), nullable=False
    )
    TEAM = Column(UNIQUEIDENTIFIER, nullable=False)

    RIGHTSMANAGEMENT_TASK = relationship("RIGHTSMANAGEMENTTASK")


class TEMPLATEFORMAT(Base):
    __tablename__ = "TEMPLATE_FORMAT"
    __table_args__ = {"schema": "dbo"}

    TPF_ID = Column(Integer, primary_key=True)
    TPF_NAME_DE = Column(Unicode(256), nullable=False)
    TPF_NAME_EN = Column(Unicode(256), nullable=False)
    TPF_NAME_FR = Column(Unicode(256), nullable=False)
    TPF_SHORT_DE = Column(Unicode(256), nullable=False)
    TPF_SHORT_EN = Column(Unicode(256), nullable=False)
    TPF_SHORT_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="TEMPLATEFORMAT.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="TEMPLATEFORMAT.UPDATED_BY == STAFF.ST_ID"
    )


class TEMPLATESCOPE(Base):
    __tablename__ = "TEMPLATE_SCOPE"
    __table_args__ = {"schema": "dbo"}

    TPSC_ID = Column(Integer, primary_key=True)
    TPSC_NAME_DE = Column(Unicode(256), nullable=False)
    TPSC_NAME_EN = Column(Unicode(256), nullable=False)
    TPSC_NAME_FR = Column(Unicode(256), nullable=False)
    TPSC_SHORT_DE = Column(Unicode(256), nullable=False)
    TPSC_SHORT_EN = Column(Unicode(256), nullable=False)
    TPSC_SHORT_FR = Column(Unicode(256), nullable=False)
    TPSC_PATH = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="TEMPLATESCOPE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="TEMPLATESCOPE.UPDATED_BY == STAFF.ST_ID"
    )


class TEMPLATESTATU(Base):
    __tablename__ = "TEMPLATE_STATUS"
    __table_args__ = {"schema": "dbo"}

    TPST_ID = Column(Integer, primary_key=True)
    TPST_NAME_DE = Column(Unicode(256), nullable=False)
    TPST_NAME_EN = Column(Unicode(256), nullable=False)
    TPST_NAME_FR = Column(Unicode(256), nullable=False)
    TPST_SHORT_DE = Column(Unicode(256), nullable=False)
    TPST_SHORT_EN = Column(Unicode(256), nullable=False)
    TPST_SHORT_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="TEMPLATESTATU.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="TEMPLATESTATU.UPDATED_BY == STAFF.ST_ID"
    )


class TEMPLATETYPE(Base):
    __tablename__ = "TEMPLATE_TYPE"
    __table_args__ = {"schema": "dbo"}

    TPT_ID = Column(Integer, primary_key=True)
    TPT_NAME_DE = Column(Unicode(256), nullable=False)
    TPT_NAME_EN = Column(Unicode(256), nullable=False)
    TPT_NAME_FR = Column(Unicode(256), nullable=False)
    TPT_SHORT_DE = Column(Unicode(256), nullable=False)
    TPT_SHORT_EN = Column(Unicode(256), nullable=False)
    TPT_SHORT_FR = Column(Unicode(256), nullable=False)
    TPT_PATH = Column(Unicode(256), nullable=False)
    TPT_PREFIX = Column(Unicode(256), nullable=False)
    TPT_MODULETYPE = Column(Unicode(256))
    TPT_SHOWINPROZESSFOLDER = Column(BIT, nullable=False)
    TPT_SHOWINTEMPLATEMANAGER = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    TPT_INCLUDE_IN_TRADE_REPORT = Column(BIT, nullable=False)

    STAFF = relationship(
        "STAFF", primaryjoin="TEMPLATETYPE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="TEMPLATETYPE.UPDATED_BY == STAFF.ST_ID"
    )


class TESTSAMPLE(Base):
    __tablename__ = "TESTSAMPLE"
    __table_args__ = {"schema": "dbo"}

    TS_ID = Column(Integer, primary_key=True)
    P_ID = Column(Integer, index=True)
    TS_PRODUCT = Column(Unicode(255))
    TS_MODEL = Column(Unicode(255))
    CU_ID = Column(Integer)
    TS_DATE_RECEIPT = Column(DateTime)
    TS_COUNT = Column(Integer)
    TS_FROM_MANUFACTURER = Column(BIT)
    PRP_ID = Column(Integer)
    TS_STORIX = Column(Unicode(10))
    TS_STORIXELEMENT = Column(Unicode(10))
    TS_INTEND_USE = Column(Unicode(2000))
    TS_INFO = Column(Unicode(2000))
    TS_DEFAULT_RETURN = Column(Integer)
    TS_DEFAULT_STORAGE = Column(DateTime)
    TS_COUNT_SHIPPED = Column(Integer)
    TS_COUNT_WASTE = Column(Integer)
    TS_COUNT_USE = Column(Integer)
    TS_DISABLED = Column(BIT, nullable=False)
    TS_UPDATEBY = Column(Integer)
    TS_UPDATE = Column(DateTime)
    TS_CREATEDBY = Column(Integer)
    TS_CREATED = Column(DateTime)
    TS_CREATEDBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    TS_UPDATEBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    AL_ID = Column(ForeignKey("dbo.ANONYMIZATION_LOG.AL_ID"))

    ANONYMIZATION_LOG = relationship("ANONYMIZATIONLOG")
    HIERARCHY = relationship(
        "HIERARCHY",
        primaryjoin="TESTSAMPLE.TS_CREATEDBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    HIERARCHY1 = relationship(
        "HIERARCHY",
        primaryjoin="TESTSAMPLE.TS_UPDATEBY_TEAM == HIERARCHY.HR_NEW_ID",
    )


class TESTSAMPLEPICTUREDESCRIPTION(Base):
    __tablename__ = "TESTSAMPLEPICTUREDESCRIPTION"
    __table_args__ = {"schema": "dbo"}

    TSPD_ID = Column(Integer, primary_key=True)
    TSPD_NAME_DE = Column(Unicode(256), nullable=False)
    TSPD_NAME_EN = Column(Unicode(256), nullable=False)
    TSPD_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF",
        primaryjoin="TESTSAMPLEPICTUREDESCRIPTION.CREATED_BY == STAFF.ST_ID",
    )
    STAFF1 = relationship(
        "STAFF",
        primaryjoin="TESTSAMPLEPICTUREDESCRIPTION.UPDATED_BY == STAFF.ST_ID",
    )


class TYPEOFFILE(Base):
    __tablename__ = "TYPE_OF_FILE"
    __table_args__ = {"schema": "dbo"}

    TOF_ID = Column(Integer, primary_key=True)
    TOF_ABBREVIATION = Column(Unicode(16), nullable=False)
    TOF_NAME_DE = Column(Unicode(256), nullable=False)
    TOF_NAME_EN = Column(Unicode(256), nullable=False)
    TOF_NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="TYPEOFFILE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="TYPEOFFILE.UPDATED_BY == STAFF.ST_ID"
    )


class VERSIONINFO(Base):
    __tablename__ = "VERSION_INFO"
    __table_args__ = (
        Index(
            "UQ_VERSION_INFO_MD_ID_VERSION_NUMBER",
            "MD_ID",
            "VERSION_NUMBER",
            unique=True,
        ),
        Index("UIX_VERSION_INFO", "MD_ID", "VERSION_NUMBER", unique=True),
        {"schema": "dbo"},
    )

    ID = Column(BigInteger, primary_key=True)
    MD_ID = Column(ForeignKey("dbo.MANDATOR.ID"), nullable=False)
    VERSION_NUMBER = Column(Unicode(16), nullable=False)
    VALID_FROM = Column(DATETIME2, nullable=False)
    VERSION_PATH = Column(Unicode(128), nullable=False)
    CREATED = Column(DATETIME2)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    UPDATED = Column(DATETIME2)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="VERSIONINFO.CREATED_BY == STAFF.ST_ID"
    )
    MANDATOR = relationship("MANDATOR")
    STAFF1 = relationship(
        "STAFF", primaryjoin="VERSIONINFO.UPDATED_BY == STAFF.ST_ID"
    )


class WORKFLOWMESSAGE(Base):
    __tablename__ = "WORKFLOW_MESSAGE"
    __table_args__ = {"schema": "dbo"}

    WM_ID = Column(Integer, primary_key=True)
    WM_TYPE = Column(Integer, nullable=False)
    WI_ID = Column(Integer)
    WM_TEXT = Column(Unicode(255))
    WM_RELATES_TO_KIND = Column(Integer, nullable=False)
    WM_RELATES_TO_PRIMARY = Column(Integer, nullable=False)
    WM_RELATES_TO_SECONDARY = Column(Integer)
    WM_STAFF_MEMBER = Column(Integer)
    WM_DISABLED = Column(BIT, nullable=False)
    WM_CREATED = Column(DateTime, nullable=False)
    WM_CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    WM_UPDATED = Column(DateTime)
    WM_UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="WORKFLOWMESSAGE.WM_CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="WORKFLOWMESSAGE.WM_UPDATED_BY == STAFF.ST_ID"
    )


class ZARAMATERIALCONDITION(Base):
    __tablename__ = "ZARA_MATERIAL_CONDITIONS"
    __table_args__ = (
        ForeignKeyConstraint(
            ["ZM_ID", "ZARA_BOOKING_AREA", "SERVERID"],
            [
                "dbo.ZARA_MATERIAL.ZM_ID",
                "dbo.ZARA_MATERIAL.ZM_BOOKING_AREA",
                "dbo.ZARA_MATERIAL.SERVERID",
            ],
        ),
        Index(
            "IX_ZARA_MATERIAL_CONDITIONS_ZM_ID_SERVERID_BOOKINGAREA",
            "SERVERID",
            "ZARA_BOOKING_AREA",
            "ZM_ID",
            "ZMC_RATE",
            "ZMC_UNIT",
            "ZMC_FROM",
            "ZMC_UNTIL",
        ),
        {"schema": "dbo"},
    )

    ZMC_ID = Column(Unicode(10))
    ZM_ID = Column(Unicode(18), primary_key=True, nullable=False, index=True)
    ZMC_RATE = Column(DECIMAL(18, 2))
    ZMC_UNIT = Column(Unicode(3))
    SERVERID = Column(Integer, primary_key=True, nullable=False, index=True)
    ZARA_BOOKING_AREA = Column(
        Unicode(4), primary_key=True, nullable=False, index=True
    )
    ZMC_FROM = Column(DateTime)
    ZMC_UNTIL = Column(DateTime)
    KPEIN = Column(Unicode(50))
    KMEIN = Column(Unicode(50))
    KNUMH = Column(Unicode(45), primary_key=True, nullable=False)
    RUN_ID = Column(Integer)

    ZARA_MATERIAL = relationship("ZARAMATERIAL")


class ZARAMATERIALCONDITIONSCUST(Base):
    __tablename__ = "ZARA_MATERIAL_CONDITIONS_CUST"
    __table_args__ = (
        ForeignKeyConstraint(
            ["ZM_ID", "ZARA_BOOKING_AREA", "SERVERID"],
            [
                "dbo.ZARA_MATERIAL.ZM_ID",
                "dbo.ZARA_MATERIAL.ZM_BOOKING_AREA",
                "dbo.ZARA_MATERIAL.SERVERID",
            ],
        ),
        {"schema": "dbo"},
    )

    ZARA_BOOKING_AREA = Column(Unicode(4), primary_key=True, nullable=False)
    CU_NUMBER = Column(Unicode(10), index=True)
    ZM_ID = Column(Unicode(18), primary_key=True, nullable=False)
    ZMCC_VRKME = Column(Unicode(3))
    ZMCC_RATE = Column(DECIMAL(18, 2))
    ZMCC_UNTIL = Column(DateTime)
    ZMCC_FROM = Column(DateTime)
    SERVERID = Column(Integer, primary_key=True, nullable=False)
    ZMCC_KNUMH = Column(Unicode(45), primary_key=True, nullable=False)
    ZMCC_VKGRP = Column(Unicode(3))
    RUN_ID = Column(Integer)

    ZARA_MATERIAL = relationship("ZARAMATERIAL")


class ZARAMATERIALTEXT(Base):
    __tablename__ = "ZARA_MATERIAL_TEXT"
    __table_args__ = (
        ForeignKeyConstraint(
            ["ZM_ID", "ZARA_BOOKING_AREA", "SERVERID"],
            [
                "dbo.ZARA_MATERIAL.ZM_ID",
                "dbo.ZARA_MATERIAL.ZM_BOOKING_AREA",
                "dbo.ZARA_MATERIAL.SERVERID",
            ],
        ),
        Index(
            "IX_ZARA_MATERIAL_TEXT_SERVERID_BOOKING_AREA",
            "SERVERID",
            "ZARA_BOOKING_AREA",
            "ZMT_LANGUAGE",
            "ZMT_TEXT",
        ),
        {"schema": "dbo"},
    )

    ZM_ID = Column(Unicode(18), primary_key=True, nullable=False)
    ZMT_LANGUAGE = Column(NCHAR(2), primary_key=True, nullable=False)
    ZMT_TEXT = Column(Unicode(255))
    SERVERID = Column(Integer, primary_key=True, nullable=False)
    ZARA_BOOKING_AREA = Column(Unicode(4), primary_key=True, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)
    RUN_ID = Column(Integer)

    ZARA_MATERIAL = relationship("ZARAMATERIAL")


class ZARAMATERIALUNIT(Base):
    __tablename__ = "ZARA_MATERIAL_UNITS"
    __table_args__ = (
        ForeignKeyConstraint(
            ["ZM_ID", "ZARA_BOOKING_AREA", "SERVERID"],
            [
                "dbo.ZARA_MATERIAL.ZM_ID",
                "dbo.ZARA_MATERIAL.ZM_BOOKING_AREA",
                "dbo.ZARA_MATERIAL.SERVERID",
            ],
        ),
        Index(
            "IX_ZARA_MATERIAL_UNITS_SERVERID",
            "SERVERID",
            "ZM_ID",
            "ZMU_UNIT",
            "ZMU_IS_DEFAULT",
            "ZARA_BOOKING_AREA",
            "CREATED",
            "UPDATED",
        ),
        Index(
            "IX_ZARA_MATERIAL_UNITS_SERVERID_BOOKING_AREA",
            "SERVERID",
            "ZARA_BOOKING_AREA",
        ),
        {"schema": "dbo"},
    )

    ZMU_ID = Column(Integer, primary_key=True, nullable=False)
    ZM_ID = Column(Unicode(18), primary_key=True, nullable=False)
    ZMU_UNIT = Column(Unicode(3))
    ZMU_IS_DEFAULT = Column(BIT)
    SERVERID = Column(Integer, primary_key=True, nullable=False)
    ZARA_BOOKING_AREA = Column(Unicode(4), primary_key=True, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)
    RUN_ID = Column(Integer)

    ZARA_MATERIAL = relationship("ZARAMATERIAL")


class ZARAMATERIALVTEXT(Base):
    __tablename__ = "ZARA_MATERIAL_VTEXT"
    __table_args__ = (
        ForeignKeyConstraint(
            ["ZM_ID", "BOOKING_AREA", "SERVERID"],
            [
                "dbo.ZARA_MATERIAL.ZM_ID",
                "dbo.ZARA_MATERIAL.ZM_BOOKING_AREA",
                "dbo.ZARA_MATERIAL.SERVERID",
            ],
        ),
        {"schema": "dbo"},
    )

    ZM_ID = Column(Unicode(18), primary_key=True, nullable=False)
    LANGUAGE = Column(NCHAR(2), primary_key=True, nullable=False)
    SERVERID = Column(Integer, primary_key=True, nullable=False)
    BOOKING_AREA = Column(Unicode(4), primary_key=True, nullable=False)
    ROW = Column(Integer, primary_key=True, nullable=False)
    TEXTLINE = Column(Unicode(256))
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)
    RUN_ID = Column(Integer)

    ZARA_MATERIAL = relationship("ZARAMATERIAL")


class ZLOCATION(Base):
    __tablename__ = "ZLOCATION"
    __table_args__ = {"schema": "dbo"}

    ZM_LOCATION = Column(Unicode(5), primary_key=True, nullable=False)
    ZM_LOCATION_NAME = Column(Unicode(255))
    ZM_LOCATION_LANGUAGE = Column(NCHAR(2), primary_key=True, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="ZLOCATION.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="ZLOCATION.UPDATED_BY == STAFF.ST_ID"
    )


class ZOBJECT(Base):
    __tablename__ = "ZOBJECT"
    __table_args__ = {"schema": "dbo"}

    ZM_OBJECT = Column(Unicode(5), primary_key=True, nullable=False)
    ZM_OBJECT_NAME = Column(Unicode(255))
    ZM_OBJECT_LANGUAGE = Column(NCHAR(2), primary_key=True, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="ZOBJECT.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="ZOBJECT.UPDATED_BY == STAFF.ST_ID"
    )


class ZPRODUCT(Base):
    __tablename__ = "ZPRODUCT"
    __table_args__ = {"schema": "dbo"}

    ZM_PRODUCT = Column(Unicode(5), primary_key=True, nullable=False)
    ZM_PROUDCT_NAME = Column(Unicode(255))
    ZM_PRODUCT_LANGUAGE = Column(NCHAR(2), primary_key=True, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="ZPRODUCT.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="ZPRODUCT.UPDATED_BY == STAFF.ST_ID"
    )


class ZPSBEGRIFFBEZ(Base):
    __tablename__ = "ZPS_BEGRIFF_BEZ"
    __table_args__ = {"schema": "dbo"}

    BEBE_BEGR_ID = Column(
        ForeignKey("dbo.ZPS_BEGRIFF.BEGR_ID"), primary_key=True, nullable=False
    )
    BEBE_SP_ID = Column(Integer, primary_key=True, nullable=False)
    BEBE_BEZ_EX = Column(Unicode(255))
    BEBE_ERF_DATUM = Column(DateTime, nullable=False)
    BEBE_AEND_DATUM = Column(DateTime)

    ZPS_BEGRIFF = relationship("ZPSBEGRIFF")


class ZPSZERTIFIZIERGEBIET(Base):
    __tablename__ = "ZPS_ZERTIFIZIERGEBIET"
    __table_args__ = {"schema": "dbo"}

    ZEGE_ID = Column(Integer, primary_key=True)
    ZEGE_KUERZEL = Column(Unicode(255), nullable=False)
    ZEGE_GUELTIG_VON = Column(DateTime, nullable=False)
    ZEGE_GUELTIG_BIS = Column(DateTime, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="ZPSZERTIFIZIERGEBIET.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="ZPSZERTIFIZIERGEBIET.UPDATED_BY == STAFF.ST_ID"
    )


class ZSUBLOCATION(Base):
    __tablename__ = "ZSUBLOCATION"
    __table_args__ = {"schema": "dbo"}

    ZM_SUBLOCATION = Column(Unicode(6), primary_key=True, nullable=False)
    ZM_SUBLOCATION_NAME = Column(Unicode(256), nullable=False)
    ZM_SUBLOCATION_LANGUAGE = Column(
        NCHAR(2), primary_key=True, nullable=False
    )
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="ZSUBLOCATION.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="ZSUBLOCATION.UPDATED_BY == STAFF.ST_ID"
    )


class ZVANGEBOTPOSITION(Base):
    __tablename__ = "ZVANGEBOT_POSITION"
    __table_args__ = (
        ForeignKeyConstraint(
            ["VBELN", "MD_ID", "SERVERID"],
            [
                "dbo.ZVANGEBOT.VBELN",
                "dbo.ZVANGEBOT.MD_ID",
                "dbo.ZVANGEBOT.SERVERID",
            ],
        ),
        {"schema": "dbo"},
    )

    VBELN = Column(Unicode(10), primary_key=True, nullable=False)
    POSNR = Column(Unicode(6), primary_key=True, nullable=False)
    MD_ID = Column(Integer, primary_key=True, nullable=False)
    SERVERID = Column(Integer, primary_key=True, nullable=False)
    ABGRU = Column(NCHAR(2))
    AWAHR = Column(Unicode(3))
    KBETR = Column(Unicode(15))
    KWMENG = Column(Unicode(15))
    MVGR4 = Column(Unicode(3))
    MATNR = Column(Unicode(18))
    PSTYV = Column(Unicode(4))
    CREATED_FROM_PSE = Column(DateTime)
    CREATED_FROM_PSE_BY = Column(Integer)
    UPDATED_FROM_PSE = Column(DateTime)
    UPDATED_FROM_PSE_BY = Column(Integer)
    WAERK = Column(Unicode(5))
    VRKME = Column(Unicode(3))
    NETPR = Column(DECIMAL(18, 2))
    NETWR = Column(DECIMAL(18, 2))
    PRCTR = Column(Unicode(10))
    TEXT = Column(Unicode(1024))
    CREATED_FROM_SAP = Column(DateTime)
    UPDATED_FROM_SAP = Column(DateTime)
    RUN_ID = Column(Integer)

    ZVANGEBOT = relationship("ZVANGEBOT")


class ZVAUFTRAGKOPF(Base):
    __tablename__ = "ZVAUFTRAG_KOPF"
    __table_args__ = {"schema": "dbo"}

    VBELN = Column(Unicode(10), primary_key=True, nullable=False)
    MD_ID = Column(
        ForeignKey("dbo.MANDATOR.ID"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    AUDAT = Column(DateTime)
    NETWR = Column(DECIMAL(18, 2))
    WAERK = Column(Unicode(50))
    VDATU = Column(DateTime)
    BSTNK = Column(Unicode(35))
    KOKRS = Column(Unicode(4))
    XBLNR = Column(Unicode(16))
    KURSK = Column(DECIMAL(18, 5))
    BSTDK = Column(DateTime)
    SREG = Column(NCHAR(1))
    KOSTL = Column(Unicode(10))
    FPLNR = Column(Integer)
    SERVERID = Column(Integer, primary_key=True, nullable=False, index=True)
    VKGRP = Column(Unicode(3))
    VKBUR = Column(Unicode(4))
    FAKSK = Column(NCHAR(2))
    ZSPERRE = Column(NCHAR(2))
    STDSATZ = Column(DECIMAL(18, 2), nullable=False)
    LAST_IMPORT_FROM_SAP = Column(DateTime)
    CREATED_FROM_PSE = Column(DateTime)
    CREATED_FROM_PSE_BY = Column(Integer)
    UPDATED_FROM_PSE = Column(DateTime)
    UPDATED_FROM_PSE_BY = Column(Integer)
    ZTATWR = Column(DECIMAL(18, 3))
    ABGS = Column(NCHAR(1))
    VORK = Column(NCHAR(1))
    RUN_ID = Column(Integer)
    BWAERK = Column(Unicode(5))
    RK_FAKTOR = Column(DECIMAL(18, 3))
    SCHLUSSR_DATUM = Column(DateTime)
    TEIL_FKDAT = Column(DateTime)
    END_FKDAT = Column(DateTime)
    CLEAR_DAT = Column(DateTime)
    RECHN_NUM = Column(Unicode(16))

    MANDATOR = relationship("MANDATOR")


class ZVVERTRIEBSWEG(Base):
    __tablename__ = "ZVVERTRIEBSWEG"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    VKORG = Column(Unicode(4), nullable=False)
    VTWEG = Column(NCHAR(2), nullable=False)
    NAME_DE = Column(Unicode(256), nullable=False)
    NAME_EN = Column(Unicode(256), nullable=False)
    NAME_FR = Column(Unicode(256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    VWEG = Column(NCHAR(2))
    BEZEICHNUNG = Column(Unicode(50))

    STAFF = relationship(
        "STAFF", primaryjoin="ZVVERTRIEBSWEG.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="ZVVERTRIEBSWEG.UPDATED_BY == STAFF.ST_ID"
    )


class ACTIONTYPEHIERARCHY(Base):
    __tablename__ = "ACTION_TYPE_HIERARCHY"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    ACTION_TYPE_ID = Column(
        ForeignKey("dbo.ACTION_TYPE.ACTT_ID"), nullable=False
    )
    HR_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"), nullable=False)
    DISABLED = Column(DateTime)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    SORT_ORDER = Column(Integer, nullable=False)

    ACTION_TYPE = relationship("ACTIONTYPE")
    STAFF = relationship(
        "STAFF", primaryjoin="ACTIONTYPEHIERARCHY.CREATED_BY == STAFF.ST_ID"
    )
    HIERARCHY = relationship("HIERARCHY")
    STAFF1 = relationship(
        "STAFF", primaryjoin="ACTIONTYPEHIERARCHY.UPDATED_BY == STAFF.ST_ID"
    )


class CALCULATIONAREADEPARTMENT(Base):
    __tablename__ = "CALCULATION_AREA_DEPARTMENT"
    __table_args__ = (
        Index(
            "IX_CALCULATION_AREA_DEPARTMENT",
            "DEPARTMENT_ID",
            "CALC_AREA_ID",
            unique=True,
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    DEPARTMENT_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"), nullable=False)
    CALC_AREA_ID = Column(
        ForeignKey("dbo.CALCULATION_AREA.CALC_AREA_ID"), nullable=False
    )
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    CALCULATION_AREA = relationship("CALCULATIONAREA")
    STAFF = relationship(
        "STAFF",
        primaryjoin="CALCULATIONAREADEPARTMENT.CREATED_BY == STAFF.ST_ID",
    )
    HIERARCHY = relationship("HIERARCHY")
    STAFF1 = relationship(
        "STAFF",
        primaryjoin="CALCULATIONAREADEPARTMENT.UPDATED_BY == STAFF.ST_ID",
    )


class CATEGORYHIERARCHY(Base):
    __tablename__ = "CATEGORY_HIERARCHY"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    CATEGORY_ID = Column(ForeignKey("dbo.CATEGORY.ID"), nullable=False)
    WORKING_CLUSTER_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"))
    DEPARTMENT_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"))
    DISABLED = Column(DATETIME2)
    CREATED = Column(DATETIME2)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    UPDATED = Column(DATETIME2)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    CATEGORY = relationship("CATEGORY")
    STAFF = relationship(
        "STAFF", primaryjoin="CATEGORYHIERARCHY.CREATED_BY == STAFF.ST_ID"
    )
    HIERARCHY = relationship(
        "HIERARCHY",
        primaryjoin="CATEGORYHIERARCHY.DEPARTMENT_ID == HIERARCHY.HR_ID",
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="CATEGORYHIERARCHY.UPDATED_BY == STAFF.ST_ID"
    )
    HIERARCHY1 = relationship(
        "HIERARCHY",
        primaryjoin="CATEGORYHIERARCHY.WORKING_CLUSTER_ID == HIERARCHY.HR_ID",
    )


class CATEGORYWORKINGCLUSTER(Base):
    __tablename__ = "CATEGORY_WORKING_CLUSTER"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    CATEGORY_ID = Column(ForeignKey("dbo.CATEGORY.ID"), nullable=False)
    WORKING_CLUSTER_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"))
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    CATEGORY = relationship("CATEGORY")
    STAFF = relationship(
        "STAFF", primaryjoin="CATEGORYWORKINGCLUSTER.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="CATEGORYWORKINGCLUSTER.UPDATED_BY == STAFF.ST_ID"
    )
    HIERARCHY = relationship("HIERARCHY")


class CERTIFICATECLIENT(Base):
    __tablename__ = "CERTIFICATE_CLIENT"
    __table_args__ = (
        Index("IX_CERTIFICATE_CLIENT", "CERTIFICATE_ID", "TYPE", "CBW_NUMBER"),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    CERTIFICATE_ID = Column(Integer)
    TYPE = Column(Integer, nullable=False)
    CU_ID = Column(ForeignKey("dbo.CUSTOMER.CU_ID"))
    CBW_NUMBER = Column(Integer)
    NAME1 = Column(Unicode(40))
    NAME2 = Column(Unicode(40))
    NAME3 = Column(Unicode(40))
    NAME4 = Column(Unicode(40))
    STREET = Column(Unicode(60))
    STREET_NUMBER = Column(Unicode(10))
    STREET_ADDITION = Column(Unicode(10))
    ADDITIONAL_STREET1 = Column(Unicode(40))
    ADDITIONAL_STREET2 = Column(Unicode(40))
    ADDITIONAL_STREET3 = Column(Unicode(40))
    ADDITIONAL_STREET4 = Column(Unicode(40))
    DISTRICT = Column(Unicode(40))
    ZIP_CITY = Column(Unicode(10))
    CITY = Column(Unicode(40))
    COUNTRY_CODE = Column(Unicode(3))
    ZIP_COMPANY = Column(Unicode(10))
    SAP_NUMBER = Column(Unicode(10))
    DEPARTMENT_NOTIFY = Column(Unicode(8))
    DEPARTMENT_RESPONSIBLE = Column(Unicode(8))
    KEY_ACCOUNT_MANAGER = Column(Unicode(94))
    NUMBER_OF_EMPLOYEES = Column(Integer)
    PHONE = Column(Unicode(48))
    FAX = Column(Unicode(48))
    SALES_TAX_NUMBER = Column(Unicode(64))
    EMAIL = Column(Unicode(60))
    INFORMATION = Column(Unicode(2000))
    COMPLETE_ADDRESS = Column(Unicode(2000))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    SORT = Column(Integer)

    STAFF = relationship(
        "STAFF", primaryjoin="CERTIFICATECLIENT.CREATED_BY == STAFF.ST_ID"
    )
    CUSTOMER = relationship("CUSTOMER")
    STAFF1 = relationship(
        "STAFF", primaryjoin="CERTIFICATECLIENT.UPDATED_BY == STAFF.ST_ID"
    )


class CHARTEMPLATE(Base):
    __tablename__ = "CHAR_TEMPLATE"
    __table_args__ = {"schema": "dbo"}

    CHAT_ID = Column(Integer, primary_key=True)
    MD_ID = Column(ForeignKey("dbo.MANDATOR.ID"), nullable=False)
    CHAT_DESCRIPTION = Column(Unicode(256), nullable=False)
    CHAT_VALUE = Column(Unicode(2000), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    CATEGORY_ID = Column(ForeignKey("dbo.CATEGORY.ID"))

    CATEGORY = relationship("CATEGORY")
    STAFF = relationship(
        "STAFF", primaryjoin="CHARTEMPLATE.CREATED_BY == STAFF.ST_ID"
    )
    MANDATOR = relationship("MANDATOR")
    STAFF1 = relationship(
        "STAFF", primaryjoin="CHARTEMPLATE.UPDATED_BY == STAFF.ST_ID"
    )


class CHECKVIEWCHECK(Base):
    __tablename__ = "CHECKVIEW_CHECK"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    CU_ID = Column(ForeignKey("dbo.CUSTOMER.CU_ID"), nullable=False)
    CV_ID = Column(ForeignKey("dbo.CHECKVIEW_MD.ID"), nullable=False)

    CUSTOMER = relationship("CUSTOMER")
    CHECKVIEW_MD = relationship("CHECKVIEWMD")


class CURRENCYRATE(Base):
    __tablename__ = "CURRENCY_RATE"
    __table_args__ = (
        Index(
            "IX_CURRENCY_RATE_VALUE",
            "VALUE",
            "CUR_FROM",
            "CUR_TO",
            "VALID_FROM",
        ),
        Index(
            "IX_CURRENCY_RATE_CUR_FROM_CUR_TO_VALID_FROM",
            "CUR_FROM",
            "CUR_TO",
            "VALID_FROM",
            "VALUE",
        ),
        {"schema": "dbo"},
    )

    CUR_FROM = Column(
        ForeignKey("dbo.CURRENCY.CUR_ID"), primary_key=True, nullable=False
    )
    CUR_TO = Column(
        ForeignKey("dbo.CURRENCY.CUR_ID"), primary_key=True, nullable=False
    )
    VALID_FROM = Column(Date, primary_key=True, nullable=False)
    VALUE = Column(DECIMAL(18, 10), nullable=False)
    INSERTED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    RUN_ID = Column(Integer)

    CURRENCY = relationship(
        "CURRENCY", primaryjoin="CURRENCYRATE.CUR_FROM == CURRENCY.CUR_ID"
    )
    CURRENCY1 = relationship(
        "CURRENCY", primaryjoin="CURRENCYRATE.CUR_TO == CURRENCY.CUR_ID"
    )


class CUSTOMERADDRES(Base):
    __tablename__ = "CUSTOMER_ADDRESS"
    __table_args__ = (
        Index(
            "UIX_CUSTOMER_ADDRESS_CU_ID_CA_NATION",
            "CU_ID",
            "CA_NATION",
            unique=True,
        ),
        Index("IX_CUSTOMER_ADDRESS_CA_NAME", "CA_NAME", "CU_ID", "CA_NATION"),
        Index(
            "IX_CUSTOMER_ADDRESS_CA_NATION", "CA_NATION", "CU_ID", "CA_NAME"
        ),
        Index(
            "IX_CUSTOMER_ADDRESS_CA_NATION_CA_NAME",
            "CA_NATION",
            "CA_NAME",
            "CU_ID",
            "CA_CITY",
            "CA_STREET1",
            "CA_HOUSE_NUM1",
        ),
        {"schema": "dbo"},
    )

    CA_ID = Column(Integer, primary_key=True)
    CU_ID = Column(ForeignKey("dbo.CUSTOMER.CU_ID"), nullable=False)
    CA_ADDRNUMBER = Column(Unicode(10))
    CA_NATION = Column(NCHAR(1), nullable=False)
    CA_TITLE = Column(Unicode(4))
    CA_NAME = Column(Unicode(165), nullable=False)
    CA_NAME_SHORT = Column(Unicode(60), nullable=False)
    CA_NAME1 = Column(Unicode(40))
    CA_NAME2 = Column(Unicode(40))
    CA_NAME3 = Column(Unicode(40))
    CA_NAME4 = Column(Unicode(40))
    CA_CITY = Column(Unicode(40))
    CA_DISTRICT = Column(Unicode(50))
    CA_COUNTRY = Column(Unicode(3))
    CA_LANGUAGE = Column(NCHAR(2))
    CA_REGION = Column(Unicode(3))
    CA_PHONE = Column(Unicode(60))
    CA_PHONE2 = Column(Unicode(60))
    CA_FAX = Column(Unicode(60))
    CA_FAX2 = Column(Unicode(60))
    CA_ZIPCODE = Column(Unicode(10))
    CA_PO_POSTCODE = Column(Unicode(10))
    CA_CO_POSTCODE = Column(Unicode(50))
    CA_STREET = Column(Unicode(100))
    CA_STREET1 = Column(Unicode(60))
    CA_PO_BOX = Column(Unicode(10))
    CA_PO_BOX_LOC = Column(Unicode(40))
    CA_PO_BOX_REG = Column(Unicode(3))
    CA_PO_BOX_CTY = Column(Unicode(3))
    CA_HOUSE_NUM1 = Column(Unicode(10))
    CA_HOUSE_NUM2 = Column(Unicode(10))
    CA_HOUSE_NUM3 = Column(Unicode(10))
    CA_STR_SUPPL1 = Column(Unicode(40))
    CA_STR_SUPPL2 = Column(Unicode(40))
    CA_STR_SUPPL3 = Column(Unicode(40))
    CA_LOCATION = Column(Unicode(40))
    CA_BUILDING = Column(Unicode(20))
    CA_FLOOR = Column(Unicode(10))
    CA_ROOMNUMBER = Column(Unicode(10))
    CA_CREATED = Column(DateTime, nullable=False)
    CA_UPDATED = Column(DateTime, nullable=False)
    CA_PHONE1 = Column(Unicode(60))
    CA_FAX1 = Column(Unicode(60))
    CA_MAIL = Column(Unicode(255))
    CA_COMMENT = Column(Unicode(2000))
    RUN_ID = Column(Integer)

    CUSTOMER = relationship("CUSTOMER")


class CUSTOMERALTERNATIVE(Base):
    __tablename__ = "CUSTOMER_ALTERNATIVE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    CU_ID = Column(ForeignKey("dbo.CUSTOMER.CU_ID"), nullable=False)
    ALTERNATIVE_ID = Column(ForeignKey("dbo.CUSTOMER.CU_ID"), nullable=False)

    CUSTOMER = relationship(
        "CUSTOMER",
        primaryjoin="CUSTOMERALTERNATIVE.ALTERNATIVE_ID == CUSTOMER.CU_ID",
    )
    CUSTOMER1 = relationship(
        "CUSTOMER", primaryjoin="CUSTOMERALTERNATIVE.CU_ID == CUSTOMER.CU_ID"
    )


class CUSTOMERCONTACT(Base):
    __tablename__ = "CUSTOMER_CONTACT"
    __table_args__ = (
        Index(
            "IX_CUSTOMER_CONTACT_CU_ID_CUC_PARNR",
            "CU_ID",
            "CUC_PARNR",
            "CUC_ID",
            "CUC_FORENAME",
            "CUC_SURNAME",
            "CUC_PHONE",
            "LOCATION",
            "BUILDING",
            "RUN_ID",
            "CUC_DEPARTMENT_NO",
            "CUC_COMMENTS",
            "CUC_TITLE",
            "CUC_UPDATE_TYPE",
            "CUC_SERVERID",
            "CUC_LAST_UPDATED",
            "CUC_FAX",
            "CUC_MOBILE",
            "CUC_MAIL",
            "CUC_SCOPE",
            "CUC_DISABLE",
            "CUC_DEPARTMENT",
        ),
        {"schema": "dbo"},
    )

    CUC_ID = Column(Integer, primary_key=True)
    CU_ID = Column(ForeignKey("dbo.CUSTOMER.CU_ID"), nullable=False)
    CUC_FORENAME = Column(Unicode(50))
    CUC_SURNAME = Column(Unicode(35))
    CUC_PHONE = Column(Unicode(50))
    CUC_PHONE_EXTENS = Column(Unicode(50))
    CUC_FAX = Column(Unicode(50))
    CUC_FAX_EXTENS = Column(Unicode(50))
    CUC_MOBILE = Column(Unicode(50))
    CUC_MAIL = Column(Unicode(255))
    CUC_SCOPE = Column(Unicode(60))
    CUC_DISABLE = Column(BIT, nullable=False)
    CUC_PARNR = Column(Unicode(10), index=True)
    CUC_DEPARTMENT = Column(Unicode(255))
    CUC_DEPARTMENT_NO = Column(Unicode(255))
    CUC_COMMENTS = Column(Unicode(255))
    CUC_TITLE = Column(Unicode(255))
    CUC_UPDATE_TYPE = Column(TINYINT)
    CUC_SERVERID = Column(Integer)
    CUC_LAST_UPDATED = Column(DateTime)
    LOCATION = Column(Unicode(60))
    BUILDING = Column(Unicode(60))
    RUN_ID = Column(Integer)
    CUC_SALUTATION = Column(Integer)
    CUC_ADDRESS_FREETEXT = Column(Unicode(1000))
    SURVEY_OPT_OUT = Column(DateTime)
    ANRED = Column(Unicode(30))
    CREATED = Column(DateTime)
    CREATED_BY = Column(Integer)
    UPDATED_BY = Column(Integer)
    CRM_NUMBER = Column(Unicode(10))
    CUC_DISABLED_PSE = Column(DateTime)
    CUC_LANGUAGE = Column(NCHAR(2))
    INITIALS = Column(Unicode(20))

    CUSTOMER = relationship("CUSTOMER")


class CUSTOMERDEFAULTPARTNER(Base):
    __tablename__ = "CUSTOMER_DEFAULT_PARTNER"
    __table_args__ = (
        Index(
            "UIX_CUSTOMER_DEFAULT_PARTNER_CU_ID_PRP_ID",
            "CU_ID",
            "PRP_ID",
            unique=True,
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    CU_ID = Column(ForeignKey("dbo.CUSTOMER.CU_ID"), nullable=False)
    PRP_ID = Column(ForeignKey("dbo.PROCESSPHASE.PRP_ID"))
    MANUFACTURER = Column(ForeignKey("dbo.CUSTOMER.CU_ID"))
    REPORT_RECIPIENT = Column(ForeignKey("dbo.CUSTOMER.CU_ID"))
    INVOICE_RECIPIENT = Column(ForeignKey("dbo.CUSTOMER.CU_ID"))
    REGULATOR = Column(ForeignKey("dbo.CUSTOMER.CU_ID"))
    GOODS_RECIPIENT = Column(ForeignKey("dbo.CUSTOMER.CU_ID"))
    GLOBAL_PARTNER = Column(ForeignKey("dbo.CUSTOMER.CU_ID"))

    CUSTOMER = relationship(
        "CUSTOMER",
        primaryjoin="CUSTOMERDEFAULTPARTNER.CU_ID == CUSTOMER.CU_ID",
    )
    CUSTOMER1 = relationship(
        "CUSTOMER",
        primaryjoin="CUSTOMERDEFAULTPARTNER.GLOBAL_PARTNER == CUSTOMER.CU_ID",
    )
    CUSTOMER2 = relationship(
        "CUSTOMER",
        primaryjoin="CUSTOMERDEFAULTPARTNER.GOODS_RECIPIENT == CUSTOMER.CU_ID",
    )
    CUSTOMER3 = relationship(
        "CUSTOMER",
        primaryjoin="CUSTOMERDEFAULTPARTNER.INVOICE_RECIPIENT == CUSTOMER.CU_ID",
    )
    CUSTOMER4 = relationship(
        "CUSTOMER",
        primaryjoin="CUSTOMERDEFAULTPARTNER.MANUFACTURER == CUSTOMER.CU_ID",
    )
    PROCESSPHASE = relationship("PROCESSPHASE")
    CUSTOMER5 = relationship(
        "CUSTOMER",
        primaryjoin="CUSTOMERDEFAULTPARTNER.REGULATOR == CUSTOMER.CU_ID",
    )
    CUSTOMER6 = relationship(
        "CUSTOMER",
        primaryjoin="CUSTOMERDEFAULTPARTNER.REPORT_RECIPIENT == CUSTOMER.CU_ID",
    )


class DISPOPHASE(Base):
    __tablename__ = "DISPO_PHASE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    DISPO = Column(ForeignKey("dbo.DISPO.ID"), nullable=False)
    PROCESS_PHASE = Column(
        ForeignKey("dbo.PROCESSPHASE.PRP_ID"), nullable=False
    )
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)
    DISABLED = Column(DateTime)

    DISPO1 = relationship("DISPO")
    PROCESSPHASE = relationship("PROCESSPHASE")


class DISPOPHASEDEFAULT(Base):
    __tablename__ = "DISPO_PHASEDEFAULT"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    CUSTOMER = Column(
        ForeignKey("dbo.DISPO_KNOWN_CUSTOMERS.ID"), nullable=False
    )
    PHASE = Column(ForeignKey("dbo.PROCESSPHASE.PRP_ID"), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)
    DISABLED = Column(DateTime)

    DISPO_KNOWN_CUSTOMER = relationship("DISPOKNOWNCUSTOMER")
    PROCESSPHASE = relationship("PROCESSPHASE")


class DISPOPHASERULE(Base):
    __tablename__ = "DISPO_PHASE_RULE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    PHASE = Column(
        ForeignKey("dbo.PROCESSPHASE.PRP_ID"), nullable=False, unique=True
    )
    DATA_SECTION = Column(Unicode(100), nullable=False)
    TEST_TYPE = Column(Unicode(100), nullable=False)
    RULE = Column(Unicode(4000), nullable=False)
    OPTIONS = Column(Unicode(4000))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)
    DISABLED = Column(DateTime)

    PROCESSPHASE = relationship("PROCESSPHASE")


class DISPOPRODUCTGROUP(Base):
    __tablename__ = "DISPO_PRODUCTGROUP"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Unicode(100), primary_key=True)
    CUSTOMER = Column(
        ForeignKey("dbo.DISPO_KNOWN_CUSTOMERS.ID"), nullable=False
    )
    CATEGORY = Column(ForeignKey("dbo.CATEGORY.ID"))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)
    DISABLED = Column(DateTime)

    CATEGORY1 = relationship("CATEGORY")
    DISPO_KNOWN_CUSTOMER = relationship("DISPOKNOWNCUSTOMER")


class EMAILCONTENT(Base):
    __tablename__ = "EMAIL_CONTENT"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    MD_ID = Column(ForeignKey("dbo.MANDATOR.ID"), nullable=False)
    HR_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"))
    EMAIL_SUBJECT_ID = Column(
        ForeignKey("dbo.EMAIL_SUBJECT.SUBJECT_ID"), nullable=False
    )
    CONTENT_STRING_DE = Column(Unicode(4000), nullable=False)
    CONTENT_STRING_EN = Column(Unicode(4000), nullable=False)
    CONTAINS_SIGNATURE = Column(BIT, nullable=False)
    RULE_ID = Column(Integer, nullable=False)
    DISABLED = Column(DATETIME2)
    CREATED = Column(DATETIME2, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DATETIME2)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="EMAILCONTENT.CREATED_BY == STAFF.ST_ID"
    )
    EMAIL_SUBJECT = relationship("EMAILSUBJECT")
    HIERARCHY = relationship("HIERARCHY")
    MANDATOR = relationship("MANDATOR")
    STAFF1 = relationship(
        "STAFF", primaryjoin="EMAILCONTENT.UPDATED_BY == STAFF.ST_ID"
    )


class KEYWORDFORMAT(Base):
    __tablename__ = "KEYWORD_FORMAT"
    __table_args__ = (
        Index(
            "UK_FORMAT_KEYWORD_COL_TABLE", "KEYWORD", "COL_TABLE", unique=True
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    MD_ID = Column(Integer, nullable=False)
    KEYWORD = Column(ForeignKey("dbo.KEYWORD.ID"), nullable=False)
    KEYWORD_TYPE = Column(ForeignKey("dbo.KEYWORD_TYPE.ID"), nullable=False)
    HEADER_RESOURCE = Column(Unicode(100))
    COL_SQL = Column(Unicode(256))
    COL_TABLE = Column(Integer, nullable=False)
    DEFAULT_VALUE = Column(Unicode)
    PREFERREDWIDTH = Column(DECIMAL(18, 2))
    FONT = Column(Unicode(200))
    HALIGN = Column(Integer)
    VALIGN = Column(Integer)
    VMERGE = Column(BIT, nullable=False)
    LINESTYLE = Column(Integer, nullable=False)
    LINEWIDTH = Column(DECIMAL(18, 2))
    HEADER_HALIGN = Column(Integer)
    HEADER_VALIGN = Column(Integer)
    HEADER_FONT = Column(Unicode(200))
    HEADER_LINEWIDTH = Column(DECIMAL(18, 2))
    FOOTER_FONT = Column(Unicode(200))
    FOOTER_HALIGN = Column(Integer)
    FOOTER_VALIGN = Column(Integer)
    FOOTER_LINEWIDTH = Column(DECIMAL(18, 2))
    DESCRIPTION = Column(Unicode(3000))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)
    DISABLED = Column(BIT, nullable=False)

    KEYWORD1 = relationship("KEYWORD")
    KEYWORD_TYPE1 = relationship("KEYWORDTYPE")


class KEYWORDSYNONYM(Base):
    __tablename__ = "KEYWORD_SYNONYM"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True, unique=True)
    KEYWORD = Column(ForeignKey("dbo.KEYWORD.ID"), nullable=False)
    SYNONYM = Column(Unicode(30), nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)

    KEYWORD1 = relationship("KEYWORD")


class KSTRATE(Base):
    __tablename__ = "KST_RATE"
    __table_args__ = (
        Index(
            "UIX_KST_RATE_ENTRY",
            "CC_ID",
            "SG_ID",
            "CCR_VALID_FROM",
            unique=True,
        ),
        {"schema": "dbo"},
    )

    CCR_ID = Column(Integer, primary_key=True, nullable=False)
    CC_ID = Column(ForeignKey("dbo.KST.CC_ID"), nullable=False)
    CCR_PRODUCTIVE_RATE = Column(DECIMAL(18, 2), nullable=False)
    CCR_UNPRODUCTIVE_RATE = Column(DECIMAL(18, 2), nullable=False)
    CUR_ID = Column(ForeignKey("dbo.CURRENCY.CUR_ID"))
    CCR_VALID_FROM = Column(DateTime)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    SG_ID = Column(
        ForeignKey("dbo.SKILLGROUP.SG_ID"), primary_key=True, nullable=False
    )
    RUN_ID = Column(ForeignKey("dbo.TASK_RUN.RUN_ID"))
    CCR_DISABLED = Column(BIT, nullable=False)

    KST = relationship("KST")
    STAFF = relationship(
        "STAFF", primaryjoin="KSTRATE.CREATED_BY == STAFF.ST_ID"
    )
    CURRENCY = relationship("CURRENCY")
    TASK_RUN = relationship("TASKRUN")
    SKILLGROUP = relationship("SKILLGROUP")
    STAFF1 = relationship(
        "STAFF", primaryjoin="KSTRATE.UPDATED_BY == STAFF.ST_ID"
    )


class PMPORTALRIGHT(Base):
    __tablename__ = "PM_PORTALRIGHTS"
    __table_args__ = {"schema": "dbo"}

    ID = Column(BigInteger, primary_key=True)
    FullUserName = Column(Unicode(256), nullable=False)
    PORTAL_ID = Column(ForeignKey("dbo.PORTAL.ID"), nullable=False)
    CU_ID = Column(ForeignKey("dbo.CUSTOMER.CU_ID"))

    CUSTOMER = relationship("CUSTOMER")
    PORTAL = relationship("PORTAL")


class PORTALLOG(Base):
    __tablename__ = "PORTAL_LOG"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    TIMESTAMP = Column(DateTime, nullable=False)
    OPERATION = Column(Integer, nullable=False)
    USER_ID = Column(Unicode(32), nullable=False)
    USER_NAME = Column(Unicode(256))
    FILE_PATH = Column(Unicode(2056), nullable=False)
    PORTAL_ID = Column(ForeignKey("dbo.PORTAL.ID"), nullable=False)

    PORTAL = relationship("PORTAL")


class PROCES(Base):
    __tablename__ = "PROCESS"
    __table_args__ = (
        Index(
            "IX_PROCESS_ARCHIVING_STATUS", "ARCHIVING_STATUS", "PC_DISABLED"
        ),
        Index(
            "IX_PROCESS_PC_DISABLED_COLLECTIVE_INVOICE_SENT",
            "PC_DISABLED",
            "COLLECTIVE_INVOICE_SENT",
        ),
        Index(
            "IX_PROCESS_PC_DISABLED_PC_VISIBLE_FOR",
            "PC_DISABLED",
            "PC_VISIBLE_FOR",
            "PC_ID",
        ),
        {"schema": "dbo"},
    )

    PC_ID = Column(Integer, primary_key=True)
    PC_WC_ID = Column(UNIQUEIDENTIFIER)
    PC_CLIENT = Column(ForeignKey("dbo.CUSTOMER.CU_ID"))
    PC_PRODUCT = Column(Unicode(255))
    PC_MODEL = Column(Unicode(255))
    PC_NAME = Column(Unicode(255))
    PC_ORDERTEXT = Column(Unicode(255))
    PC_PROJECTMANAGER = Column(ForeignKey("dbo.STAFF.ST_ID"))
    PC_LOTSIZE = Column(Integer)
    PC_STATUS = Column(Integer)
    PC_READY_TO_SHOP = Column(Integer)
    PC_SHOPDATE = Column(DateTime)
    PC_PATH = Column(Unicode(50))
    PC_FILE_MEASUREMENT = Column(Unicode(255))
    PC_FILE_DOCS = Column(Unicode(255))
    PC_REGDATE = Column(DateTime)
    PC_CREATEDBY = Column(Integer)
    PC_UPDATE = Column(DateTime)
    PC_UPDATEBY = Column(Integer)
    PC_DISABLED = Column(BIT, nullable=False)
    PC_VISIBLE_FOR = Column(ForeignKey("dbo.PORTAL.ID"))
    PC_CREATEDBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    PC_UPDATEBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    AL_ID = Column(ForeignKey("dbo.ANONYMIZATION_LOG.AL_ID"))
    PC_REPEATER_OF = Column(Integer, nullable=False)
    PC_CERT_TYPE = Column(Unicode(255))
    PC_IAN = Column(Unicode(256))
    PC_LIDL_QA_MEMBER = Column(Unicode(256))
    PROTOCOL_PROJECT = Column(Integer)
    PC_KEY2 = Column(Unicode(16))
    PC_KEY3 = Column(Unicode(16))
    FILE_FORMAT = Column(Integer)
    ARCHIVING_STATUS = Column(Unicode(32))
    PC_PROJECTMANAGER_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    IS_FST_PROCESS = Column(BIT, nullable=False)
    FACILITY_NUMBER = Column(Integer)
    NACE_CODE = Column(Unicode(256))
    COLLECTIVE_INVOICE_SENT = Column(DateTime)
    BATCH_NUMBER = Column(Unicode(16))
    DISCOUNT_PERCENTAGE = Column(DECIMAL(19, 10), nullable=False)

    ANONYMIZATION_LOG = relationship("ANONYMIZATIONLOG")
    CUSTOMER = relationship("CUSTOMER")
    HIERARCHY = relationship(
        "HIERARCHY",
        primaryjoin="PROCES.PC_CREATEDBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    STAFF = relationship("STAFF")
    HIERARCHY1 = relationship(
        "HIERARCHY",
        primaryjoin="PROCES.PC_PROJECTMANAGER_TEAM == HIERARCHY.HR_NEW_ID",
    )
    HIERARCHY2 = relationship(
        "HIERARCHY",
        primaryjoin="PROCES.PC_UPDATEBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    PORTAL = relationship("PORTAL")


class PROCESSDEFAULT(Base):
    __tablename__ = "PROCESS_DEFAULTS"
    __table_args__ = {"schema": "dbo"}

    PCD_ID = Column(Integer, primary_key=True)
    CU_ID = Column(ForeignKey("dbo.CUSTOMER.CU_ID"))
    PRP_ID = Column(ForeignKey("dbo.PROCESSPHASE.PRP_ID"))
    PCD_DAYS_DEADLINE = Column(Integer)
    PCD_DAYS_PREDATE = Column(Integer)
    PCD_PREDATE_INFO_DE = Column(Unicode(256))
    PCD_PREDATE_INFO_EN = Column(Unicode(256))
    PCD_PREDATE_INFO_FR = Column(Unicode(256))
    PCD_REMINDER = Column(BIT, nullable=False)
    PCD_ACTION = Column(BIT, nullable=False)
    PCD_ACTION_INFO_DE = Column(Unicode(256))
    PCD_ACTION_INFO_EN = Column(Unicode(256))
    PCD_ACTION_INFO_FR = Column(Unicode(256))
    PCD_ACTION_DATE = Column(Integer)
    PCD_ACTION_INTERNAL = Column(BIT, nullable=False)
    PCD_ACTION_REMINDER = Column(BIT, nullable=False)
    PCD_ACTION_PREDATE = Column(Integer)
    PCD_ACTION_PREDATE_INFO_DE = Column(Unicode(256))
    PCD_ACTION_PREDATE_INFO_EN = Column(Unicode(256))
    PCD_ACTION_PREDATE_INFO_FR = Column(Unicode(256))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="PROCESSDEFAULT.CREATED_BY == STAFF.ST_ID"
    )
    CUSTOMER = relationship("CUSTOMER")
    PROCESSPHASE = relationship("PROCESSPHASE")
    STAFF1 = relationship(
        "STAFF", primaryjoin="PROCESSDEFAULT.UPDATED_BY == STAFF.ST_ID"
    )


class PROJECTADDONROOMSPECIFICDATUM(Base):
    __tablename__ = "PROJECT_ADDON_ROOMSPECIFICDATA"
    __table_args__ = {"schema": "dbo"}

    PAR_ID = Column(Integer, primary_key=True)
    P_ID = Column(Integer, nullable=False)
    PAR_COLUMN = Column(Integer, nullable=False)
    RD_ID = Column(Integer, nullable=False)
    PAR_PRESSURE = Column(Unicode(50))
    PU_ID = Column(Integer, nullable=False)
    PAR_TEMPERATURE = Column(Unicode(50))
    PAR_VOLUME = Column(Unicode(50))
    PAR_VOLUME_UNIT = Column(Unicode(50), nullable=False)
    PAR_MEDIUM = Column(Unicode(50))
    SOA_ID = Column(Integer, nullable=False)
    PAR_SUBSTANCE1 = Column(Unicode(50))
    PAR_SUBSTANCE2 = Column(Unicode(50))
    PAR_CATEGORY_ID = Column(ForeignKey("dbo.PROJECTCATEGORY_MD.ID"))
    PAR_FLUIDGROUP_ID = Column(ForeignKey("dbo.PROJECTFLUIDGROUP_MD.ID"))

    PROJECTCATEGORY_MD = relationship("PROJECTCATEGORYMD")
    PROJECTFLUIDGROUP_MD = relationship("PROJECTFLUIDGROUPMD")


class PSEKUNDEPARTNER(Base):
    __tablename__ = "PSEKUNDE_PARTNER"
    __table_args__ = {"schema": "dbo"}

    ID = Column(BigInteger, primary_key=True)
    CU_ID = Column(ForeignKey("dbo.CUSTOMER.CU_ID"), nullable=False)
    VKORG = Column(Unicode(4), nullable=False)
    VTWEG = Column(NCHAR(2), nullable=False)
    PARVW = Column(NCHAR(2), nullable=False)
    PARZA = Column(Integer, nullable=False)
    KUNN2 = Column(Unicode(10))
    PERNR = Column(Unicode(8))
    PARNR = Column(Unicode(10))
    PHASE = Column(Integer)

    CUSTOMER = relationship("CUSTOMER")


class ROLEPERMISSION(Base):
    __tablename__ = "ROLEPERMISSION"
    __table_args__ = {"schema": "dbo"}

    PS_ID = Column(
        ForeignKey("dbo.PERMISSION.PS_ID"), primary_key=True, nullable=False
    )
    RS_ID = Column(
        ForeignKey("dbo.ROLE.RS_ID"), primary_key=True, nullable=False
    )
    IsPermitted = Column(BIT)
    RP_UPDATE_TYPE = Column(TINYINT)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UpdateDate = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="ROLEPERMISSION.CREATED_BY == STAFF.ST_ID"
    )
    PERMISSION = relationship("PERMISSION")
    ROLE = relationship("ROLE")
    STAFF1 = relationship(
        "STAFF", primaryjoin="ROLEPERMISSION.UPDATED_BY == STAFF.ST_ID"
    )


class STAFFRATE(Base):
    __tablename__ = "STAFF_RATE"
    __table_args__ = {"schema": "dbo"}

    SRA_ID = Column(Integer, primary_key=True)
    ST_ID = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    RATE = Column(DECIMAL(8, 2), nullable=False)
    CUR_ID = Column(ForeignKey("dbo.CURRENCY.CUR_ID"), nullable=False)
    FROMDATE = Column(DateTime, nullable=False)
    TODATE = Column(DateTime, nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="STAFFRATE.CREATED_BY == STAFF.ST_ID"
    )
    CURRENCY = relationship("CURRENCY")
    STAFF1 = relationship(
        "STAFF", primaryjoin="STAFFRATE.ST_ID == STAFF.ST_ID"
    )
    STAFF2 = relationship(
        "STAFF", primaryjoin="STAFFRATE.UPDATED_BY == STAFF.ST_ID"
    )


class SURVEYNOTIFICATIONTEMPLATE(Base):
    __tablename__ = "SURVEY_NOTIFICATION_TEMPLATE"
    __table_args__ = (
        Index(
            "UIX_SURVEY_NOTIFICATION_TEMPLATE_HR_ID_LANGUAGE_CU_ID",
            "HR_ID",
            "LANGUAGE",
            "CU_ID",
            unique=True,
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    HR_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"))
    CU_ID = Column(ForeignKey("dbo.CUSTOMER.CU_ID"))
    LANGUAGE = Column(NCHAR(2), nullable=False)
    SENDER = Column(Unicode(256), nullable=False)
    SUBJECT = Column(Unicode(1024), nullable=False)
    SALUTATION_UNSPECIFIC = Column(Unicode(256), nullable=False)
    SALUTATION_FEMALE = Column(Unicode(256), nullable=False)
    SALUTATION_MALE = Column(Unicode(256), nullable=False)
    PROJECT_INFO = Column(Unicode(1024), nullable=False)
    ALTERNATIVE_VIEW_LINK = Column(Unicode(256), nullable=False)
    BASE_LINK = Column(Unicode(256), nullable=False)
    OPT_OUT_LINK = Column(Unicode(256), nullable=False)
    BODY_FILE_HTML = Column(Unicode(256), nullable=False)
    BODY_FILE_PLAIN = Column(Unicode(256), nullable=False)

    CUSTOMER = relationship("CUSTOMER")
    HIERARCHY = relationship("HIERARCHY")


class TASKCOLUMNMAP(Base):
    __tablename__ = "TASK_COLUMNMAP"
    __table_args__ = {"schema": "dbo"}

    COL_ID = Column(Integer, primary_key=True)
    TBL_ID = Column(ForeignKey("dbo.TASK_TABLEMAP.TBL_ID"), nullable=False)
    COLUMNNAME = Column(Unicode(50), nullable=False)
    PARSE = Column(Unicode(50))
    ELEMENT_ID = Column(ForeignKey("dbo.TASK_ELEMENT.ID"), nullable=False)
    ISEXTKEY = Column(BIT, nullable=False)
    DEFAULTVALUE = Column(Unicode(10))

    TASK_ELEMENT = relationship("TASKELEMENT")
    TASK_TABLEMAP = relationship("TASKTABLEMAP")


class TCPROJECT(Base):
    __tablename__ = "TC_PROJECT"
    __table_args__ = {"schema": "dbo"}

    P_ID = Column(Integer, primary_key=True)
    P_CUSTOMER_A = Column(ForeignKey("dbo.CUSTOMER.CU_ID"), nullable=False)
    P_PRODUCT = Column(Unicode(255), nullable=False)
    P_DEADLINE = Column(DateTime, nullable=False)
    P_PROJECTINFO = Column(Unicode(1024), nullable=False)
    P_PLANNED_ORDERSIZE = Column(DECIMAL(18, 2), nullable=False)
    P_PREDATE = Column(DateTime, nullable=False)
    P_REGBY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    P_WC_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"), nullable=False)
    P_PSOBJECT_TERM = Column(ForeignKey("dbo.ZPS_BEGRIFF.BEGR_ID"))
    P_PSOBJECT_LANGUAGEID = Column(Integer)
    E_ID = Column(Integer)
    P_IS_QUOTATION = Column(BIT, nullable=False)
    P_NUMBER_OF_TESTSAMPLES = Column(Integer, nullable=False)

    CUSTOMER = relationship("CUSTOMER")
    ZPS_BEGRIFF = relationship("ZPSBEGRIFF")
    STAFF = relationship("STAFF")
    HIERARCHY = relationship("HIERARCHY")


class TEMPLATE(Base):
    __tablename__ = "TEMPLATE"
    __table_args__ = (
        Index("IX_TEMPLATE_TP_DISABLED_DM_ID", "TP_DISABLED", "DM_ID"),
        {"schema": "dbo"},
    )

    TP_ID = Column(Integer, primary_key=True)
    MD_ID = Column(ForeignKey("dbo.MANDATOR.ID"), nullable=False)
    TPST_ID = Column(ForeignKey("dbo.TEMPLATE_STATUS.TPST_ID"))
    TPT_ID = Column(ForeignKey("dbo.TEMPLATE_TYPE.TPT_ID"))
    TPSC_ID = Column(ForeignKey("dbo.TEMPLATE_SCOPE.TPSC_ID"))
    TPF_ID = Column(ForeignKey("dbo.TEMPLATE_FORMAT.TPF_ID"))
    TP_NAME_D = Column(Unicode(255))
    TP_NAME_E = Column(Unicode(255))
    TP_TIME_HOURS = Column(Float(53))
    TP_TIME_DAYS = Column(Float(53))
    TP_COSTS = Column(DECIMAL(18, 2))
    TP_TESTPERSON_REQUIRED = Column(BIT, nullable=False)
    TP_COMMENT = Column(Unicode(255))
    TP_VERSION = Column(Integer)
    TP_LANGUAGE = Column(Unicode(255))
    TP_CLEARINGDATE = Column(DateTime)
    TP_CLEARINGBY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    TP_FILENAME = Column(Unicode(255))
    TP_REGDATE = Column(DateTime)
    TP_REGBY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    TP_UPDATE = Column(DateTime)
    TP_UPDATEBY = Column(Integer)
    TP_ISGLOBAL = Column(BIT)
    TP_DISABLED = Column(BIT, nullable=False)
    TP_TRANSFER_STATUS = Column(Unicode(50))
    TP_ORIGINATING_SERVERID = Column(Integer)
    TP_ROOT_TEMPLATE_ID = Column(Integer)
    TP_FILE_EXPORTED = Column(NCHAR(1), nullable=False)
    TP_UTC = Column(DateTime)
    TP_WORKINGCLUSTER = Column(UNIQUEIDENTIFIER)
    DM_ID = Column(Integer, index=True)
    TP_OLD_TP = Column(Integer)

    MANDATOR = relationship("MANDATOR")
    TEMPLATE_FORMAT = relationship("TEMPLATEFORMAT")
    TEMPLATE_SCOPE = relationship("TEMPLATESCOPE")
    TEMPLATE_STATU = relationship("TEMPLATESTATU")
    TEMPLATE_TYPE = relationship("TEMPLATETYPE")
    STAFF = relationship(
        "STAFF", primaryjoin="TEMPLATE.TP_CLEARINGBY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="TEMPLATE.TP_REGBY == STAFF.ST_ID"
    )


class TESTSAMPLECHARACTERISTIC(Base):
    __tablename__ = "TESTSAMPLECHARACTERISTICS"
    __table_args__ = (
        Index(
            "IX_TESTSAMPLECHARACTERISTICS_TS_ID_TS_DISABLED",
            "TS_ID",
            "TS_DISABLED",
        ),
        {"schema": "dbo"},
    )

    TC_ID = Column(Integer, primary_key=True)
    TC_NAME = Column(Unicode(2000))
    TC_VALUE = Column(Unicode(2000))
    TS_ID = Column(ForeignKey("dbo.TESTSAMPLE.TS_ID"), nullable=False)
    TS_DISABLED = Column(BIT, nullable=False)
    TC_NUMBER = Column(Integer, nullable=False)

    TESTSAMPLE = relationship("TESTSAMPLE")


class TESTSAMPLEPICTURE(Base):
    __tablename__ = "TESTSAMPLEPICTURE"
    __table_args__ = (
        Index(
            "IX_TESTSAMPLEPICTURE_TS_ID_TS_DISABLED", "TS_ID", "TS_DISABLED"
        ),
        {"schema": "dbo"},
    )

    TSP_ID = Column(Integer, primary_key=True)
    TS_ID = Column(ForeignKey("dbo.TESTSAMPLE.TS_ID"), nullable=False)
    TS_FILE = Column(Unicode(255), nullable=False)
    TS_DESCRIPTION = Column(Unicode(255))
    TS_DISABLED = Column(BIT)
    TSP_NUMBER = Column(Integer)

    TESTSAMPLE = relationship("TESTSAMPLE")


class WORKFLOWASSIGNMENT(Base):
    __tablename__ = "WORKFLOW_ASSIGNMENT"
    __table_args__ = {"schema": "dbo"}

    WA_ID = Column(Integer, primary_key=True)
    WM_ID = Column(ForeignKey("dbo.WORKFLOW_MESSAGE.WM_ID"), nullable=False)
    WA_ASSIGNED_TO = Column(
        ForeignKey("dbo.STAFF.ST_ID"), nullable=False, index=True
    )
    WA_ACCEPTED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    WA_DISABLED = Column(BIT, nullable=False)
    WA_CREATED = Column(DateTime, nullable=False)
    WA_CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    WA_UPDATED = Column(DateTime)
    WA_UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="WORKFLOWASSIGNMENT.WA_ACCEPTED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="WORKFLOWASSIGNMENT.WA_ASSIGNED_TO == STAFF.ST_ID"
    )
    STAFF2 = relationship(
        "STAFF", primaryjoin="WORKFLOWASSIGNMENT.WA_CREATED_BY == STAFF.ST_ID"
    )
    STAFF3 = relationship(
        "STAFF", primaryjoin="WORKFLOWASSIGNMENT.WA_UPDATED_BY == STAFF.ST_ID"
    )
    WORKFLOW_MESSAGE = relationship("WORKFLOWMESSAGE")


class ZCOILV30(Base):
    __tablename__ = "ZCOILV30"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    MANDT = Column(Integer, nullable=False)
    KOSTL = Column(Unicode(10), nullable=False)
    SKGRP = Column(Unicode(8), nullable=False)
    CO_ART = Column(NCHAR(1))
    DATAB = Column(DateTime, nullable=False)
    CUR_ID = Column(ForeignKey("dbo.CURRENCY.CUR_ID"))
    PROD_FIX = Column(DECIMAL(18, 2))
    PROD_VAR = Column(DECIMAL(18, 2))
    UNPROD_FIX = Column(DECIMAL(18, 2))
    UNPROD_VAR = Column(DECIMAL(18, 2))
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)
    RUN_ID = Column(Integer)

    CURRENCY = relationship("CURRENCY")


class ZCOILV50(Base):
    __tablename__ = "ZCOILV50"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    MANDT = Column(Integer, nullable=False)
    VKORG = Column(Unicode(4), nullable=False)
    ZM_ID = Column(Unicode(18), nullable=False)
    WERT_FIX = Column(DECIMAL(18, 2), nullable=False)
    WERT_VAR = Column(DECIMAL(18, 2), nullable=False)
    CUR_ID = Column(ForeignKey("dbo.CURRENCY.CUR_ID"))
    EINHEIT = Column(Unicode(3))
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)
    RUN_ID = Column(Integer)

    CURRENCY = relationship("CURRENCY")


class ZPSZERTTYPE(Base):
    __tablename__ = "ZPS_ZERT_TYPES"
    __table_args__ = {"schema": "dbo"}

    ZETY_TYP = Column(Unicode(255), primary_key=True)
    ZETY_BEZEICHNUNG = Column(Unicode(255), nullable=False)
    ZETY_GUELTIGVON = Column(DateTime, nullable=False)
    ZETY_GUELTIGBIS = Column(DateTime, nullable=False)
    ZETY_BEZEICHNUNG_E = Column(Unicode(255), nullable=False)
    ZETY_ZEGE_ID = Column(
        ForeignKey("dbo.ZPS_ZERTIFIZIERGEBIET.ZEGE_ID"), nullable=False
    )
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="ZPSZERTTYPE.CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="ZPSZERTTYPE.UPDATED_BY == STAFF.ST_ID"
    )
    ZPS_ZERTIFIZIERGEBIET = relationship("ZPSZERTIFIZIERGEBIET")


class ZVAUFTRAGSPO(Base):
    __tablename__ = "ZVAUFTRAGSPOS"
    __table_args__ = (
        ForeignKeyConstraint(
            ["VBELN", "MD_ID", "SERVERID"],
            [
                "dbo.ZVAUFTRAG_KOPF.VBELN",
                "dbo.ZVAUFTRAG_KOPF.MD_ID",
                "dbo.ZVAUFTRAG_KOPF.SERVERID",
            ],
        ),
        {"schema": "dbo"},
    )

    VBELN = Column(Unicode(10), primary_key=True, nullable=False, index=True)
    POSNR = Column(Unicode(10), primary_key=True, nullable=False)
    MATNR = Column(Unicode(18))
    ARKTX = Column(Unicode(40))
    PSTYV = Column(Unicode(4))
    UEPOS = Column(Integer)
    NETWR = Column(DECIMAL(18, 2))
    AEDAT = Column(DateTime)
    FPLNR = Column(Integer)
    SERVERID = Column(Integer, primary_key=True, nullable=False)
    MD_ID = Column(Integer, primary_key=True, nullable=False)
    BSTKD = Column(Unicode(35))
    BSTDK = Column(Unicode(8))
    PERNR = Column(Unicode(8))
    LAST_IMPORT_FROM_SAP = Column(DateTime)
    CREATED_FROM_PSE = Column(DateTime)
    CREATED_FROM_PSE_BY = Column(Integer)
    UPDATED_FROM_PSE = Column(DateTime)
    UPDATED_FROM_PSE_BY = Column(Integer)
    PRCTR = Column(Unicode(9))
    ERDAT = Column(DateTime)
    ZIEME = Column(Unicode(8))
    ZMENG = Column(Unicode(16))
    WAERK = Column(Unicode(16))
    RUN_ID = Column(Integer)
    FI_FAKTOR = Column(DECIMAL(18, 3))

    ZVAUFTRAG_KOPF = relationship("ZVAUFTRAGKOPF")


class ZVAUFTRAGFREISCHALT(Base):
    __tablename__ = "ZVAUFTRAG_FREISCHALT"
    __table_args__ = (
        ForeignKeyConstraint(
            ["BEARBAUFNR", "MD_ID", "SERVERID"],
            [
                "dbo.ZVAUFTRAG_KOPF.VBELN",
                "dbo.ZVAUFTRAG_KOPF.MD_ID",
                "dbo.ZVAUFTRAG_KOPF.SERVERID",
            ],
        ),
        {"schema": "dbo"},
    )

    BEARBAUFNR = Column(Unicode(10), primary_key=True, nullable=False)
    KOSTL = Column(Unicode(10))
    ZPOSITION = Column(Unicode(50))
    SERVERID = Column(Integer, primary_key=True, nullable=False)
    ZAEHLER = Column(NCHAR(10), primary_key=True, nullable=False)
    MD_ID = Column(Integer, primary_key=True, nullable=False)
    RUN_ID = Column(Integer)

    ZVAUFTRAG_KOPF = relationship("ZVAUFTRAGKOPF")


class ZVAUFTRAGILV(Base):
    __tablename__ = "ZVAUFTRAG_ILV"
    __table_args__ = (
        ForeignKeyConstraint(
            ["BEARBAUFNR", "MD_ID", "SERVERID"],
            [
                "dbo.ZVAUFTRAG_KOPF.VBELN",
                "dbo.ZVAUFTRAG_KOPF.MD_ID",
                "dbo.ZVAUFTRAG_KOPF.SERVERID",
            ],
        ),
        {"schema": "dbo"},
    )

    BEARBAUFNR = Column(Unicode(10), primary_key=True, nullable=False)
    ZAEHLER = Column(Integer, primary_key=True, nullable=False)
    KOSTL = Column(Unicode(10))
    FESTPREIS = Column(DECIMAL(18, 0))
    SERVERID = Column(Integer, primary_key=True, nullable=False)
    MD_ID = Column(Integer, primary_key=True, nullable=False)
    RUN_ID = Column(Integer)

    ZVAUFTRAG_KOPF = relationship("ZVAUFTRAGKOPF")


class ZVAUFTRAGPARTNER(Base):
    __tablename__ = "ZVAUFTRAG_PARTNER"
    __table_args__ = (
        ForeignKeyConstraint(
            ["VBELN", "MD_ID", "SERVERID"],
            [
                "dbo.ZVAUFTRAG_KOPF.VBELN",
                "dbo.ZVAUFTRAG_KOPF.MD_ID",
                "dbo.ZVAUFTRAG_KOPF.SERVERID",
            ],
        ),
        Index(
            "IX_ZVAUFTRAG_PARTNER_MD_ID",
            "MD_ID",
            "VBELN",
            "PARVW",
            "KUNNR",
            "PARNR",
            "SERVERID",
            "PERNR",
        ),
        {"schema": "dbo"},
    )

    VBELN = Column(Unicode(10), primary_key=True, nullable=False)
    PARVW = Column(NCHAR(2), primary_key=True, nullable=False)
    KUNNR = Column(Unicode(10))
    PARNR = Column(Unicode(10))
    SERVERID = Column(Integer, primary_key=True, nullable=False)
    MD_ID = Column(Integer, primary_key=True, nullable=False)
    PERNR = Column(Unicode(8))
    ADRNR = Column(Unicode(10))
    RUN_ID = Column(Integer)

    ZVAUFTRAG_KOPF = relationship("ZVAUFTRAGKOPF")


class ZVAUFTRAGTEXTE(Base):
    __tablename__ = "ZVAUFTRAG_TEXTE"
    __table_args__ = (
        ForeignKeyConstraint(
            ["VBELN", "MD_ID", "SERVERID"],
            [
                "dbo.ZVAUFTRAG_KOPF.VBELN",
                "dbo.ZVAUFTRAG_KOPF.MD_ID",
                "dbo.ZVAUFTRAG_KOPF.SERVERID",
            ],
        ),
        Index(
            "IX_ZVAUFTRAG_TEXTE_MD_ID_VBELN_LAISO_ID",
            "MD_ID",
            "VBELN",
            "LAISO",
            "ID",
            "TDLINE",
            "TDOBJECT",
            "TDID",
        ),
        Index(
            "IX_ZVAUFTRAG_TEXTE_LAISO_VBELN_MD_ID",
            "LAISO",
            "VBELN",
            "MD_ID",
            "ID",
            "TDLINE",
        ),
        {"schema": "dbo"},
    )

    ID = Column(Unicode(110), primary_key=True, nullable=False)
    SERVERID = Column(Integer, primary_key=True, nullable=False)
    TDOBJECT = Column(Unicode(50), nullable=False)
    TDID = Column(Unicode(50), nullable=False)
    LAISO = Column(Unicode(50), nullable=False)
    VBELN = Column(Unicode(10), primary_key=True, nullable=False)
    TDLINE = Column(Unicode(255))
    MD_ID = Column(Integer, primary_key=True, nullable=False)
    RUN_ID = Column(Integer)

    ZVAUFTRAG_KOPF = relationship("ZVAUFTRAGKOPF")


class ZVKUNDEPARTNER(Base):
    __tablename__ = "ZVKUNDE_PARTNER"
    __table_args__ = (
        Index(
            "IX_ZVKUNDE_PARTNER_ALL",
            "CU_ID",
            "VKORG",
            "VTWEG",
            "PARVW",
            "PARZA",
            "PHASE",
            unique=True,
        ),
        {"schema": "dbo"},
    )

    ID = Column(BigInteger, primary_key=True)
    CU_ID = Column(ForeignKey("dbo.CUSTOMER.CU_ID"), nullable=False)
    VKORG = Column(Unicode(4), nullable=False)
    VTWEG = Column(NCHAR(2), nullable=False)
    PARVW = Column(NCHAR(2), nullable=False)
    PARZA = Column(Integer, nullable=False)
    KUNN2 = Column(Unicode(10))
    PERNR = Column(Unicode(8))
    PARNR = Column(Unicode(10))
    PHASE = Column(Integer)

    CUSTOMER = relationship("CUSTOMER")


class CATEGORYWORKINGCLUSTERDEPARTMENT(Base):
    __tablename__ = "CATEGORY_WORKING_CLUSTER_DEPARTMENT"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    CATEGORY_WORKING_CLUSTER_ID = Column(
        ForeignKey("dbo.CATEGORY_WORKING_CLUSTER.ID"), nullable=False
    )
    DEPARTMENT_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"), nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    CATEGORY_WORKING_CLUSTER = relationship("CATEGORYWORKINGCLUSTER")
    STAFF = relationship(
        "STAFF",
        primaryjoin="CATEGORYWORKINGCLUSTERDEPARTMENT.CREATED_BY == STAFF.ST_ID",
    )
    HIERARCHY = relationship("HIERARCHY")
    STAFF1 = relationship(
        "STAFF",
        primaryjoin="CATEGORYWORKINGCLUSTERDEPARTMENT.UPDATED_BY == STAFF.ST_ID",
    )


class KALKUNTERMODUL(Base):
    __tablename__ = "KALKUNTERMODUL"
    __table_args__ = {"schema": "dbo"}

    KALUM_ID = Column(Integer, primary_key=True)
    KALM_ID = Column(ForeignKey("dbo.KALKMODUL.KALM_ID"), nullable=False)
    KALUM_NAME_DE = Column(Unicode(1024), nullable=False)
    KALUM_NAME_EN = Column(Unicode(1024), nullable=False)
    KALUM_NAME_FR = Column(Unicode(1024))
    KALUM_DAYS_TO_START = Column(Integer, nullable=False)
    KALUM_DURATION = Column(Integer, nullable=False)
    TP_ID = Column(ForeignKey("dbo.TEMPLATE.TP_ID"))
    KALUM_PLANNED_HOURS = Column(DECIMAL(18, 2), nullable=False)
    KALUM_PLANNED_EXPENSES = Column(DECIMAL(18, 2), nullable=False)
    KALUM_FACTOR = Column(DECIMAL(18, 2), nullable=False)
    KALUM_PLANNED_TRAVEL_COSTS = Column(DECIMAL(18, 2), nullable=False)
    KALUM_RECOMMENDED_PRICE = Column(DECIMAL(18, 2), nullable=False)
    KALUM_COMMENT = Column(Unicode(2000))
    KALUM_ORDER_TEXT_DE = Column(Unicode(1024))
    KALUM_ORDER_TEXT_EN = Column(Unicode(1024))
    KALUM_ORDER_TEXT_FR = Column(Unicode(1024))
    KALUM_ADDITIONAL_TEXT = Column(Unicode(1024))
    KALUM_POSITION_NUMBER = Column(Integer)
    KALUM_POSITION_TEXT_DE = Column(Unicode(1024))
    KALUM_POSITION_TEXT_EN = Column(Unicode(1024))
    KALUM_POSITION_TEXT_FR = Column(Unicode(1024))
    ZM_ID = Column(Unicode(18))
    KALUM_SORT = Column(Integer, nullable=False)
    KALUM_IS_MASTER = Column(BIT, nullable=False)
    KALUM_CREATED = Column(DateTime, nullable=False)
    KALUM_CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    KALUM_UPDATED = Column(DateTime)
    KALUM_UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    WORKING_CLUSTER = Column(ForeignKey("dbo.HIERARCHY.HR_ID"))
    KALUM_KPI = Column(BIT, nullable=False)
    KALUM_S_KPI_NUMBER = Column(Integer)
    KALUM_PLANNED_SUBCONTRACTING = Column(DECIMAL(18, 2))
    KALUM_SP_PRICELIST = Column(DECIMAL(18, 2))
    KALUM_TRAVELTIME = Column(DECIMAL(18, 2))
    KALUM_SO_TRANSFER_PRICE = Column(DECIMAL(18, 2))
    KALUM_BULKTEST = Column(BIT, nullable=False)

    KALKMODUL = relationship("KALKMODUL")
    STAFF = relationship(
        "STAFF", primaryjoin="KALKUNTERMODUL.KALUM_CREATED_BY == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="KALKUNTERMODUL.KALUM_UPDATED_BY == STAFF.ST_ID"
    )
    TEMPLATE = relationship("TEMPLATE")
    HIERARCHY = relationship("HIERARCHY")


class PROJECT(Base):
    __tablename__ = "PROJECT"
    __table_args__ = (
        Index(
            "IX_PROJECT_MD_ID_P_PROJECTMANAGER_P_DATE_READY_P_DISABLED_P_DEADLINE_P_PROCESSPHASE",
            "MD_ID",
            "P_PROJECTMANAGER",
            "P_DATE_READY",
            "P_DISABLED",
            "P_DEADLINE",
            "P_PROCESSPHASE",
        ),
        Index(
            "IX_PROJECT_IAN_SEARCH",
            "P_DISABLED",
            "P_WC_ID",
            "P_IAN",
            "P_MODEL",
            "P_ID",
            "P_PREDATE",
            "P_DEADLINE",
            "P_CUSTOMER_A",
        ),
        Index(
            "IX_PROJECT_MD_ID_P_TRANSFERPROJECT_P_DISABLED_P_ZARA_NUMBER_P_IS_OLD_PROJECT",
            "MD_ID",
            "P_TRANSFERPROJECT",
            "P_DISABLED",
            "P_ZARA_NUMBER",
            "P_IS_OLD_PROJECT",
            "P_CUR_ID",
            "P_FOREIGN_CURRENCY",
            "P_PRICING_DATE",
        ),
        Index(
            "IX_PROJECT_MD_ID_P_DISABLED_P_WC_ID",
            "MD_ID",
            "P_DISABLED",
            "P_WC_ID",
            "P_ID",
            "PC_ID",
            "P_ZARA_NUMBER",
            "P_FOLDER",
            "P_PRODUCT",
            "P_MODEL",
            "P_DATE_DONE",
            "P_URGENT",
            "P_INTERN",
            "P_TRANSFERPROJECT",
            "P_TRANSFERSUBORDER",
            "P_CUR_ID",
            "E_ID",
            "P_TUV_CERT_EXISTS",
            "P_EXTERNAL_CERT_EXISTS",
            "P_IS_QUOTATION",
            "P_IS_OLD_PROJECT",
            "CC_ID",
            "P_VERTRIEBSWEG",
            "P_PROJECT_NUMBER",
            "SAP_QUOTATION_NUMBER",
            "P_SAP_INDUSTRY",
            "P_FOREIGN_CURRENCY",
            "P_EXCHANGE_RATE",
            "P_PRICING_DATE",
            "CRM_ID",
            "CATEGORY_ID",
        ),
        Index(
            "IX_PROJECT_SURVEY_NOTIFICATION",
            "P_INTERN",
            "P_DISABLED",
            "P_IS_QUOTATION",
            "PERFORM_SURVEY",
            "SURVEY_SENT",
            "P_ZARA_NUMBER",
            "P_DATE_DONE",
            "CATEGORY_ID",
            "P_ID",
            "MD_ID",
            "PC_ID",
            "P_CUSTOMER_A",
            "P_CUSTOMER_B",
            "P_ORDERSIZE",
            "P_WC_ID",
            "P_PROJECTMANAGER_TEAM",
            "P_CONTACT_CUC_ID",
            "MANUFACTURER_CONTACT",
        ),
        Index(
            "IX_PROJECT_P_DISABLED_P_WC_ID",
            "P_DISABLED",
            "P_WC_ID",
            "P_ID",
            "P_ZARA_NUMBER",
            "P_IS_QUOTATION",
            "SAP_QUOTATION_NUMBER",
        ),
        Index(
            "IX_PROJECT_P_TRANSFERPROJECT_P_ZARA_NUMBER_MD_ID_P_DISABLED",
            "P_TRANSFERPROJECT",
            "P_ZARA_NUMBER",
            "MD_ID",
            "P_DISABLED",
        ),
        Index(
            "IX_PROJECT_MD_ID_P_DATE_DONE_P_TRANSFERPROJECT_P_DISABLED_P_IS_OLD_PROJECT",
            "MD_ID",
            "P_DATE_DONE",
            "P_TRANSFERPROJECT",
            "P_DISABLED",
            "P_IS_OLD_PROJECT",
        ),
        Index(
            "IX_PROJECT_P_WC_ID_MD_ID_P_DISABLED",
            "P_WC_ID",
            "MD_ID",
            "P_DISABLED",
            "P_ID",
            "PC_ID",
            "P_ZARA_NUMBER",
            "P_NAME",
            "P_FOLDER",
            "P_CUSTOMER_A",
            "P_PRODUCT",
            "P_MODEL",
            "P_PROJECTMANAGER",
            "P_HANDLEDBY",
            "P_DATE_APPOINTMENT",
            "P_DATE_READY",
            "P_DATE_CHECK",
            "P_DEADLINE",
            "P_DATE_DONE",
            "P_ACTION",
            "P_URGENT",
            "P_ORDERSIZE",
            "P_FORECAST",
            "P_INTERN",
            "P_PREDATE",
            "P_REGDATE",
            "P_TRANSFERPROJECT",
            "P_TRANSFERSUBORDER",
            "P_CUR_ID",
            "E_ID",
            "P_HANDLEDBY_TEAM",
            "P_PROJECTMANAGER_TEAM",
            "P_TUV_CERT_EXISTS",
            "P_EXTERNAL_CERT_EXISTS",
            "P_IS_QUOTATION",
            "P_IS_OLD_PROJECT",
            "CC_ID",
            "P_QUOTATION_LINK",
            "P_VERTRIEBSWEG",
            "SAP_QUOTATION_NUMBER",
            "P_FOREIGN_CURRENCY",
            "P_EXCHANGE_RATE",
            "P_GLOBAL_PARTNER",
            "P_PRICING_DATE",
            "P_REMARK",
            "P_COORDINATOR",
            "P_AUDIT_DATE",
            "P_AUDIT_DATE_IS_CONFIRMED",
            "CATEGORY_ID",
        ),
        Index(
            "IX_PROJECT_ARCHIVING_STATUS_P_DISABLED",
            "ARCHIVING_STATUS",
            "P_DISABLED",
        ),
        Index("IX_TEMP", "P_DISABLED", "P_IAN", "P_PROCESSPHASE", "P_ID"),
        {"schema": "dbo"},
    )

    P_ID = Column(Integer, primary_key=True)
    MD_ID = Column(ForeignKey("dbo.MANDATOR.ID"), nullable=False, index=True)
    PC_ID = Column(Integer, index=True)
    P_ZARA_NUMBER = Column(Unicode(10), index=True)
    P_NAME_IS_ZARA = Column(BIT, nullable=False)
    P_NAME = Column(Unicode(100))
    P_FOLDER = Column(Unicode(255))
    P_CUSTOMER_A = Column(Integer, index=True)
    P_CUSTOMER_B = Column(Integer)
    P_CUSTOMER_O = Column(Integer)
    P_CUST_A_IS_PRODUCER = Column(BIT)
    P_CONTACT = Column(Unicode(255))
    P_PRODUCT = Column(Unicode(255))
    P_MODEL = Column(Unicode(255), index=True)
    P_PROJECTMANAGER = Column(Integer)
    P_HANDLEDBY = Column(Integer, index=True)
    P_STATUS = Column(Integer)
    P_RETEST = Column(Integer, nullable=False)
    P_RETEST_OF = Column(Integer)
    P_DATE_APPOINTMENT = Column(DateTime)
    P_FOCUSDOCUMENT = Column(Unicode(255))
    P_COMMENT = Column(Unicode(50))
    P_DATE_READY = Column(DateTime)
    P_READYBY = Column(Integer)
    P_DATE_CHECK = Column(DateTime)
    P_CHECKBY = Column(Integer)
    P_DATE_ORDER = Column(DateTime)
    P_DEADLINE = Column(DateTime)
    P_DATE_DISPO = Column(DateTime)
    P_DATE_DONE = Column(DateTime)
    P_DONEBY = Column(Integer)
    RES_ID = Column(Integer)
    P_DELAY = Column(DECIMAL(18, 0))
    DELR_ID = Column(Integer)
    P_ORDERTEXT = Column(Unicode(2048))
    P_PROJECTINFO = Column(Unicode(4000))
    P_TOKEN = Column(Unicode(60))
    P_KIND_OF_PRODUCER = Column(Integer)
    KOT_ID = Column(Integer)
    KOB_ID = Column(Integer)
    P_ACTION = Column(BIT)
    P_URGENT = Column(BIT)
    P_DOCTYPE = Column(Integer)
    P_ORDERSIZE = Column(DECIMAL(18, 2))
    P_INVOICE = Column(DECIMAL(18, 2))
    P_SALERATE = Column(DECIMAL(18, 2))
    P_USE_PLAN = Column(BIT)
    P_PLAN_SPENDS = Column(DECIMAL(18, 10))
    P_PLAN_EXTERNAL = Column(DECIMAL(18, 10))
    P_PLAN_SUBORDER = Column(DECIMAL(18, 10))
    P_PLAN_TRAVEL = Column(MONEY)
    P_PLAN_LICENCE = Column(DECIMAL(18, 10))
    P_FACTOR = Column(DECIMAL(18, 2))
    P_ACC_SALE = Column(DECIMAL(18, 10))
    P_ACC_LAB = Column(DECIMAL(18, 10))
    P_ACC_SAFETY = Column(DECIMAL(18, 10))
    P_ACC_SALERATE = Column(MONEY)
    P_ACC_SPENDS = Column(MONEY)
    P_ACC_EXTERNAL = Column(MONEY)
    P_ACC_SUBORDER = Column(MONEY)
    P_ACC_TRAVEL = Column(MONEY)
    P_ACC_LICENCE = Column(MONEY)
    P_ACC_INTERNAL = Column(MONEY)
    P_HOURLY_RATE = Column(DECIMAL(18, 10))
    P_FORECAST = Column(DECIMAL(18, 2))
    P_TO_WEB = Column(BIT)
    P_TO_CDS = Column(BIT)
    P_INTERN = Column(BIT)
    P_PREDATE = Column(DateTime)
    P_PREDATE_REMINDER = Column(BIT)
    P_PREDATEINFO = Column(Unicode(255))
    P_PROCESSPHASE = Column(Integer)
    P_REGBY = Column(Integer)
    P_REGDATE = Column(DateTime)
    P_UPDATEBY = Column(Integer)
    P_UPDATE = Column(DateTime)
    P_ORDER_ORIGIN = Column(Unicode(20))
    P_TRANSFERPROJECT = Column(Integer)
    P_TRANSFERSUBORDER = Column(Integer)
    P_EU_TS_ID = Column(ForeignKey("dbo.TESTSAMPLE.TS_ID"))
    P_TRANSFERUACONTACT = Column(Integer)
    P_TRANSFERUADEPARTMENT = Column(Integer)
    P_TRANSFERUA_REGION_ID = Column(Integer)
    P_TRANSFERUASTATUS = Column(NCHAR(1))
    P_TRANSFERUASOURCEPATH = Column(NCHAR(1))
    P_TRANSFERROOTSERVERID = Column(Integer)
    P_TRANSFERACTIONNUMBER = Column(Integer)
    P_DISABLED = Column(BIT, nullable=False)
    P_CURRENCYRATE = Column(DECIMAL(18, 0))
    P_WC_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"), index=True)
    P_CONTACTPERSON_REGIONID = Column(UNIQUEIDENTIFIER)
    P_ASSIGNEDPERSON_TEAMID = Column(UNIQUEIDENTIFIER)
    P_PSOBJECT_TERM = Column(Unicode(50))
    P_CUR_ID = Column(ForeignKey("dbo.CURRENCY.CUR_ID"))
    P_CUR_SHORT = Column(NCHAR(3))
    P_PSOBJECT_LANGUAGEID = Column(Integer)
    P_FOLDER_OLD = Column(NCHAR(1))
    P_PROJECTFOLDERCREATED = Column(BIT, nullable=False)
    P_IS_LEGACY = Column(BIT, nullable=False)
    P_CBW_EXPORT = Column(Unicode(6))
    P_ACC_MAINPOS = Column(Unicode(8))
    P_PRODGRP_ID = Column(Integer)
    P_PRODGRP2_ID = Column(Integer)
    P_PRODUCT2 = Column(Unicode(255))
    P_DOCU_DONE = Column(BIT)
    PLAN_ACTUAL_HOUR = Column(DECIMAL(18, 2))
    ACC_ACTUAL_HOUR = Column(DECIMAL(18, 2))
    ORDER_POSITION = Column(Unicode(6))
    P_CUSTOMER_R = Column(Integer)
    E_ID = Column(Integer)
    P_CHECKBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    P_DONEBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    P_HANDLEDBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    P_PROJECTMANAGER_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    P_READYBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    P_REGBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    P_UPDATEBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    AL_ID = Column(ForeignKey("dbo.ANONYMIZATION_LOG.AL_ID"))
    P_TUV_CERT_EXISTS = Column(BIT, nullable=False)
    P_EXTERNAL_CERT_EXISTS = Column(BIT, nullable=False)
    P_CERT_COMMENT = Column(Unicode(512))
    P_IS_QUOTATION = Column(BIT, nullable=False)
    P_IS_OLD_PROJECT = Column(BIT, nullable=False)
    P_QUOTATION_PROBABILITY = Column(DECIMAL(18, 2), nullable=False)
    P_QUOTATION_VALID_UNTIL = Column(DateTime)
    P_EXPECTED_TS_RECEIPT = Column(DateTime)
    P_NUMBER_OF_TESTSAMPLES = Column(Integer)
    CC_ID = Column(ForeignKey("dbo.KST.CC_ID"))
    P_INVOICE_RECIPIENT = Column(ForeignKey("dbo.CUSTOMER.CU_ID"))
    P_QUOTATION_LINK = Column(ForeignKey("dbo.PROJECT.P_ID"))
    P_RESPONSIBLE_AGENT = Column(ForeignKey("dbo.STAFF.ST_ID"))
    P_SALES_REPRESENTATIVE = Column(ForeignKey("dbo.STAFF.ST_ID"))
    P_SIGNATURE_LEFT = Column(ForeignKey("dbo.STAFF.ST_ID"))
    P_VERTRIEBSWEG = Column(ForeignKey("dbo.ZVVERTRIEBSWEG.ID"))
    P_STDSATZ = Column(DECIMAL(18, 2), nullable=False)
    P_POSTINGS_ALLOWED = Column(BIT, nullable=False)
    P_PLANNED_ORDERSIZE = Column(DECIMAL(18, 2))
    TC_P_ID = Column(ForeignKey("dbo.TC_PROJECT.P_ID"))
    BANF_REQUEST = Column(DateTime)
    BANF_ORDER = Column(DateTime)
    P_ABGS = Column(BIT, nullable=False)
    P_VORK = Column(BIT, nullable=False)
    P_PROJECT_NUMBER = Column(Unicode(50))
    SAP_QUOTATION_NUMBER = Column(Unicode(10))
    P_TS_RECEIPT_ADVISED = Column(BIT, nullable=False)
    P_IC = Column(NCHAR(2))
    P_SAP_INDUSTRY = Column(Unicode(3), nullable=False)
    P_FOREIGN_CURRENCY = Column(ForeignKey("dbo.CURRENCY.CUR_ID"))
    P_EXCHANGE_RATE = Column(DECIMAL(18, 10))
    P_GLOBAL_PARTNER = Column(Integer)
    P_PRICING_DATE = Column(DateTime, nullable=False)
    P_CLIENT_REMARK = Column(Unicode(2048))
    P_CONTACT_CUC_ID = Column(Integer)
    P_REMARK = Column(Unicode(1024))
    P_OTC_NAME_1 = Column(Unicode(40))
    P_OTC_NAME_2 = Column(Unicode(40))
    P_OTC_NAME_AT = Column(Unicode(40))
    P_OTC_NAME_CP = Column(Unicode(35))
    P_OTC_CO = Column(Unicode(40))
    P_OTC_STREET_1 = Column(Unicode(35))
    P_OTC_STREET_2 = Column(Unicode(40))
    P_OTC_STREET_3 = Column(Unicode(40))
    P_OTC_STREET_4 = Column(Unicode(40))
    P_OTC_STREET_5 = Column(Unicode(40))
    P_OTC_PO_BOX = Column(Unicode(10))
    P_OTC_POSTAL_CODE = Column(Unicode(10))
    P_OTC_CITY_1 = Column(Unicode(40))
    P_OTC_CITY_2 = Column(Unicode(40))
    P_OTC_REGION = Column(Unicode(3))
    P_OTC_COUNTRY = Column(Unicode(3))
    P_SIGNATURE_RIGHT = Column(ForeignKey("dbo.STAFF.ST_ID"))
    P_WARRANTY_INFO = Column(Unicode(2048))
    CRM_ID = Column(Unicode(16))
    RUN_ID = Column(Integer)
    P_B2B = Column(BIT, nullable=False)
    P_COORDINATOR = Column(Integer)
    P_OTHER_DELAY_REASON = Column(Unicode(256))
    P_AUDIT_DATE = Column(DateTime)
    P_AUDIT_DATE_IS_CONFIRMED = Column(BIT, nullable=False)
    P_AUDIT_DATE_LINKED_SUBORDER = Column(Integer)
    P_DATE_ROLLUP = Column(DateTime)
    STARLIMS_SITE = Column(Unicode(20))
    STARLIMS_ATTENTION = Column(Unicode(255))
    STARLIMS_BUSINESS_TYPE = Column(Unicode(50))
    STARLIMS_SERVICE_TYPE = Column(Unicode(50))
    FROM_STARLIMS = Column(BIT, nullable=False)
    REGULATOR = Column(Integer)
    GOODS_RECIPIENT = Column(Integer)
    CONTACT_PERSON_INVOICE_RECIPIENT = Column(Integer)
    STARLIMS_PC = Column(Integer)
    FILE_FORMAT = Column(Integer)
    ARCHIVING_STATUS = Column(Unicode(32))
    P_TEAM_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"))
    P_RESY_FACTOR = Column(Unicode(5))
    SALES_PACKAGE_PRICE = Column(DECIMAL(18, 2))
    P_VISIBLE_FOR = Column(ForeignKey("dbo.PORTAL.ID"))
    STARLIMS_CONNECTION_TYPE = Column(Integer)
    CONTRACT_TYPE = Column(ForeignKey("dbo.CONTRACT_TYPE.ID"))
    PERFORM_SURVEY = Column(BIT, nullable=False)
    SURVEY_REJECT_REASON = Column(Unicode(512))
    SURVEY_SENT = Column(DateTime)
    MANUFACTURER_CONTACT = Column(Integer)
    REPORT_RECIPIENT_CONTACT = Column(Integer)
    CRM_STATUS = Column(Integer)
    CRM_TRANSFER_DATE = Column(DateTime)
    P_INVOICE_WAS_SET = Column(BIT, nullable=False)
    P_IAN = Column(Unicode(256))
    TRANSFER_FIXED_PRICE_TO_SAP = Column(BIT, nullable=False)
    COLLECTIVE_INVOICE = Column(BIT, nullable=False)
    P_POSTING_DONE_DATE = Column(DateTime)
    CATEGORY_ID = Column(
        ForeignKey("dbo.CATEGORY.ID"), nullable=False, index=True
    )
    P_DATE_READY_REASON = Column(Unicode(512))
    P_DATE_READY_CHANGED = Column(DateTime)
    P_DATE_CHECK_REASON = Column(Unicode(512))
    P_DATE_CHECK_CHANGED = Column(DateTime)
    REPORT_SENT = Column(DateTime)
    P_INTERNATIONAL = Column(BIT, nullable=False)
    P_COORDINATOR_TEAM = Column(Integer)
    BATCH_NUMBER = Column(Unicode(16))
    COLLECTIVE_INVOICE_SENT = Column(DateTime)
    PROJECT_TYPE = Column(Integer, nullable=False)
    OPPORTUNITY_ID = Column(Unicode(10))
    NECESSARY_DOCUMENTATION_AVAILABLE = Column(BIT)
    SAP_ORDER_TYPE = Column(Unicode(8))
    P_DEPARTMENT_ID = Column(UNIQUEIDENTIFIER)
    P_CONFIDENTIAL = Column(BIT, nullable=False)
    P_TEMPLATEID = Column(Integer)
    PRINT_OPTION = Column(Unicode(3))
    UNLIMITED_LIABILITY = Column(BIT, nullable=False)
    SERVICE_RENDERED_DATE = Column(Date)

    ANONYMIZATION_LOG = relationship("ANONYMIZATIONLOG")
    CATEGORY = relationship("CATEGORY")
    KST = relationship("KST")
    CONTRACT_TYPE1 = relationship("CONTRACTTYPE")
    MANDATOR = relationship("MANDATOR")
    HIERARCHY = relationship(
        "HIERARCHY",
        primaryjoin="PROJECT.P_CHECKBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    CURRENCY = relationship(
        "CURRENCY", primaryjoin="PROJECT.P_CUR_ID == CURRENCY.CUR_ID"
    )
    HIERARCHY1 = relationship(
        "HIERARCHY", primaryjoin="PROJECT.P_DONEBY_TEAM == HIERARCHY.HR_NEW_ID"
    )
    TESTSAMPLE = relationship("TESTSAMPLE")
    CURRENCY1 = relationship(
        "CURRENCY", primaryjoin="PROJECT.P_FOREIGN_CURRENCY == CURRENCY.CUR_ID"
    )
    HIERARCHY2 = relationship(
        "HIERARCHY",
        primaryjoin="PROJECT.P_HANDLEDBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    CUSTOMER = relationship("CUSTOMER")
    HIERARCHY3 = relationship(
        "HIERARCHY",
        primaryjoin="PROJECT.P_PROJECTMANAGER_TEAM == HIERARCHY.HR_NEW_ID",
    )
    parent = relationship("PROJECT", remote_side=[P_ID])
    HIERARCHY4 = relationship(
        "HIERARCHY",
        primaryjoin="PROJECT.P_READYBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    HIERARCHY5 = relationship(
        "HIERARCHY", primaryjoin="PROJECT.P_REGBY_TEAM == HIERARCHY.HR_NEW_ID"
    )
    STAFF = relationship(
        "STAFF", primaryjoin="PROJECT.P_RESPONSIBLE_AGENT == STAFF.ST_ID"
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PROJECT.P_SALES_REPRESENTATIVE == STAFF.ST_ID"
    )
    STAFF2 = relationship(
        "STAFF", primaryjoin="PROJECT.P_SIGNATURE_LEFT == STAFF.ST_ID"
    )
    STAFF3 = relationship(
        "STAFF", primaryjoin="PROJECT.P_SIGNATURE_RIGHT == STAFF.ST_ID"
    )
    HIERARCHY6 = relationship(
        "HIERARCHY", primaryjoin="PROJECT.P_TEAM_ID == HIERARCHY.HR_ID"
    )
    HIERARCHY7 = relationship(
        "HIERARCHY",
        primaryjoin="PROJECT.P_UPDATEBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    ZVVERTRIEBSWEG = relationship("ZVVERTRIEBSWEG")
    PORTAL = relationship("PORTAL")
    HIERARCHY8 = relationship(
        "HIERARCHY", primaryjoin="PROJECT.P_WC_ID == HIERARCHY.HR_ID"
    )
    TC_PROJECT = relationship("TCPROJECT")


class TCPROJECTPOSITION(Base):
    __tablename__ = "TC_PROJECT_POSITION"
    __table_args__ = (
        Index(
            "UC_TC_PROJECT_POSITION_P_ID_PP_NUMBER",
            "P_ID",
            "PP_NUMBER",
            unique=True,
        ),
        {"schema": "dbo"},
    )

    PP_ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.TC_PROJECT.P_ID"), nullable=False)
    PP_NUMBER = Column(Integer, nullable=False)
    PP_TEXT = Column(Unicode(1024))
    PP_SALES_PRICE = Column(DECIMAL(18, 2))
    ZM_ID = Column(Unicode(18))
    PP_TYPE = Column(Integer, nullable=False)

    TC_PROJECT = relationship("TCPROJECT")


class TCPROKALKMODUL(Base):
    __tablename__ = "TC_PROKALKMODUL"
    __table_args__ = {"schema": "dbo"}

    PKM_ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.TC_PROJECT.P_ID"), nullable=False)
    PKM_TYP = Column(Integer, nullable=False)
    PKM_NAME = Column(Unicode(256), nullable=False)
    PKM_REIHE = Column(Integer, nullable=False)

    TC_PROJECT = relationship("TCPROJECT")


class TCVERIFICATIONDOCUMENT(Base):
    __tablename__ = "TC_VERIFICATION_DOCUMENT"
    __table_args__ = {"schema": "dbo"}

    VD_ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.TC_PROJECT.P_ID"), nullable=False)
    VD_NAME = Column(Unicode(1024), nullable=False)
    VD_CATEGORY = Column(Integer, nullable=False)
    VD_SORT = Column(Integer, nullable=False)

    TC_PROJECT = relationship("TCPROJECT")


class TEMPLATEDATUM(Base):
    __tablename__ = "TEMPLATE_DATA"
    __table_args__ = {"schema": "dbo"}

    TPD_ID = Column(Integer, primary_key=True)
    TP_ID = Column(ForeignKey("dbo.TEMPLATE.TP_ID"), nullable=False)
    TPD_DATA = Column(IMAGE, nullable=False)

    TEMPLATE = relationship("TEMPLATE")


class TEMPLATEKEY(Base):
    __tablename__ = "TEMPLATE_KEY"
    __table_args__ = {"schema": "dbo"}

    TPK_ID = Column(Integer, primary_key=True)
    TP_ID = Column(ForeignKey("dbo.TEMPLATE.TP_ID"), index=True)
    TP_KEY = Column(Unicode(255))
    TP_DISABLED = Column(BIT, nullable=False)
    TP_ROOT_TPK_ID = Column(Integer)

    TEMPLATE = relationship("TEMPLATE")


class ZVAUFTRAGSPOSFAKT(Base):
    __tablename__ = "ZVAUFTRAGSPOS_FAKT"
    __table_args__ = (
        ForeignKeyConstraint(
            ["VBELN", "POSNR", "SERVERID", "MD_ID"],
            [
                "dbo.ZVAUFTRAGSPOS.VBELN",
                "dbo.ZVAUFTRAGSPOS.POSNR",
                "dbo.ZVAUFTRAGSPOS.SERVERID",
                "dbo.ZVAUFTRAGSPOS.MD_ID",
            ],
        ),
        {"schema": "dbo"},
    )

    VBELN = Column(Unicode(10), primary_key=True, nullable=False)
    POSNR = Column(Unicode(10), primary_key=True, nullable=False)
    FPLNR = Column(Integer, primary_key=True, nullable=False)
    FPLTR = Column(Integer, primary_key=True, nullable=False)
    TETXT = Column(Unicode(4))
    KURFP = Column(DECIMAL(18, 2))
    FAKWR = Column(DECIMAL(18, 2))
    FKSAF = Column(NCHAR(1))
    SERVERID = Column(Integer, primary_key=True, nullable=False)
    MD_ID = Column(Integer, primary_key=True, nullable=False)
    FAREG = Column(Integer)
    RUN_ID = Column(Integer)
    TEIL_FKDAT = Column(DateTime)
    BILL_TYPE = Column(Unicode(8))
    BILL_DATE = Column(DateTime)
    CLEAR_DATE = Column(DateTime)
    DOC_NO = Column(Unicode(16))
    CANCELLED = Column(Unicode(8))
    DOC_TYPE = Column(Unicode(8))

    ZVAUFTRAGSPO = relationship("ZVAUFTRAGSPO")


class ZVAUFTRAGSPOSFAKTDEB(Base):
    __tablename__ = "ZVAUFTRAGSPOS_FAKT_DEB"
    __table_args__ = (
        ForeignKeyConstraint(
            ["VBELN", "POSNR", "SERVERID", "MD_ID"],
            [
                "dbo.ZVAUFTRAGSPOS.VBELN",
                "dbo.ZVAUFTRAGSPOS.POSNR",
                "dbo.ZVAUFTRAGSPOS.SERVERID",
                "dbo.ZVAUFTRAGSPOS.MD_ID",
            ],
        ),
        {"schema": "dbo"},
    )

    VBELN = Column(Unicode(10), primary_key=True, nullable=False)
    POSNR = Column(Unicode(10), primary_key=True, nullable=False)
    SERVERID = Column(Integer, primary_key=True, nullable=False)
    MD_ID = Column(Integer, primary_key=True, nullable=False)
    BELNR = Column(Unicode(10), primary_key=True, nullable=False)
    BLART = Column(NCHAR(2), nullable=False)
    BLDAT = Column(DateTime, nullable=False)
    BUDAT = Column(DateTime, nullable=False)
    BUKRS = Column(Unicode(4), nullable=False)
    GJAHR = Column(Integer, nullable=False)
    BUZEI = Column(Integer, nullable=False)
    WRBTR = Column(DECIMAL(18, 2), nullable=False)
    SHKZG = Column(NCHAR(1), nullable=False)
    ZUONR = Column(Unicode(18))
    SGTXT = Column(Unicode(50))
    VBUND = Column(Unicode(6))
    KOSTL = Column(Unicode(10))
    VBEL2 = Column(Unicode(10))
    POSN2 = Column(Unicode(6))
    SAKNR = Column(Unicode(10))
    HKONT = Column(Unicode(10))
    LIFNR = Column(Unicode(10))
    KSTAR = Column(Unicode(10))
    RUN_ID = Column(Integer)

    ZVAUFTRAGSPO = relationship("ZVAUFTRAGSPO")


class ZVAUFTRAGSPOSFI(Base):
    __tablename__ = "ZVAUFTRAGSPOS_FI"
    __table_args__ = (
        ForeignKeyConstraint(
            ["VBELN", "POSNR", "SERVERID", "MD_ID"],
            [
                "dbo.ZVAUFTRAGSPOS.VBELN",
                "dbo.ZVAUFTRAGSPOS.POSNR",
                "dbo.ZVAUFTRAGSPOS.SERVERID",
                "dbo.ZVAUFTRAGSPOS.MD_ID",
            ],
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, nullable=False)
    VBELN = Column(Unicode(10), primary_key=True, nullable=False)
    POSNR = Column(Unicode(10), primary_key=True, nullable=False)
    SERVERID = Column(Integer, primary_key=True, nullable=False)
    MD_ID = Column(Integer, primary_key=True, nullable=False)
    BUKRS = Column(Unicode(4), primary_key=True, nullable=False)
    BELNR = Column(Unicode(10), primary_key=True, nullable=False)
    GJAHR = Column(Integer, primary_key=True, nullable=False)
    BUZEI = Column(Integer, primary_key=True, nullable=False)
    BLART = Column(NCHAR(2))
    BUDAT = Column(DateTime)
    DMBTR = Column(DECIMAL(18, 2))
    LIFNR = Column(Unicode(10))
    LIFNR_NAME = Column(Unicode(256))
    SGTXT = Column(Unicode(50))
    RUN_ID = Column(Integer)
    ALREADY_POSTED = Column(DateTime)
    ALREADY_POSTED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    SHKZG = Column(NCHAR(10))

    STAFF = relationship("STAFF")
    ZVAUFTRAGSPO = relationship("ZVAUFTRAGSPO")


class ACCOUNTING(Base):
    __tablename__ = "ACCOUNTING"
    __table_args__ = (
        Index(
            "IX_ACCOUNTING_P_ID_SO_NUMBER_ACO_DISABLED",
            "P_ID",
            "SO_NUMBER",
            "ACO_DISABLED",
            "ACO_MEASURE",
            "ACO_UNITS",
            "ACO_DIVERGENT_RATE",
        ),
        Index("IX_ACCOUNTING_P_ID_SO_NUMBER", "P_ID", "SO_NUMBER"),
        Index(
            "UIX_ACCOUNTING_ZAPFI_ID_ACO_DISABLED",
            "ZAPFI_ID",
            "ACO_DISABLED",
            unique=True,
        ),
        {"schema": "dbo"},
    )

    ACO_ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False, index=True)
    SO_NUMBER = Column(Integer)
    ACO_POS = Column(Unicode(10))
    ACOT_ID = Column(ForeignKey("dbo.ACCOUNTTYPE.ACOT_ID"), nullable=False)
    ST_ID = Column(ForeignKey("dbo.STAFF.ST_ID"), index=True)
    CC_ID = Column(ForeignKey("dbo.KST.CC_ID"))
    ACO_DATE = Column(DateTime, index=True)
    ZP_ID = Column(Unicode(3))
    ZO_ID = Column(Unicode(3))
    ZP_LOCATION = Column(NCHAR(2))
    ACO_UNITS = Column(DECIMAL(18, 2))
    ACO_RATE = Column(MONEY)
    ACO_SPENDS = Column(MONEY)
    ACO_TOTAL = Column(MONEY)
    ACO_DESCRIPTION = Column(Unicode(3500))
    ACO_INZARA = Column(BIT)
    CUR_ID = Column(ForeignKey("dbo.CURRENCY.CUR_ID"))
    ACO_REGBY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    ACO_REGDATE = Column(DateTime)
    ACO_UPDATEBY = Column(Integer)
    ACO_UPDATE = Column(DateTime)
    ACO_DISABLED = Column(BIT, nullable=False)
    ACO_POSTINGSTATUS = Column(Unicode(12), index=True)
    ZM_ID = Column(Unicode(18))
    ACO_MEASURE = Column(Unicode(3))
    ACO_RATE_BASECUR = Column(MONEY)
    ACO_SPENDS_BASECUR = Column(MONEY)
    ACO_TOTAL_BASECUR = Column(MONEY)
    ACO_IS_LEGACY = Column(BIT, nullable=False)
    ACTUAL_HOURS = Column(DECIMAL(5, 2))
    TRAVELS = Column(DECIMAL(8, 2))
    EXTERNALS = Column(DECIMAL(8, 2))
    INVOICE_LOCK = Column(BIT)
    SYSTEM_MESSAGE = Column(Unicode(512))
    ACO_IDOC_FILE = Column(Unicode(50))
    REJECT_MESSAGE = Column(Unicode(512))
    ACO_REGBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    ACO_UPDATEBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    ST_ID_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    AL_ID = Column(ForeignKey("dbo.ANONYMIZATION_LOG.AL_ID"))
    IDOC_ID = Column(Integer)
    ST_ID_SAPOK = Column(ForeignKey("dbo.STAFF.ST_ID"))
    NONCLEARABLE = Column(BIT)
    INVOICE_TEXT = Column(Unicode(512))
    ZAPFI_ID = Column(Integer)
    INVOICING_TRAVEL_COST = Column(BIT)
    RFAE_ID = Column(ForeignKey("dbo.REASON_FOR_ADDITIONAL_EFFORT.ID"))
    ACO_DIVERGENT_RATE = Column(MONEY, nullable=False)
    LAST_SAP_TRANSFER = Column(DateTime)
    NEXT_SAP_TRANSFER = Column(DateTime)
    IS_COLLECTIVE_POSTING = Column(BIT, nullable=False)
    STATUS_POSTED_DATE = Column(DateTime)

    ACCOUNTTYPE = relationship("ACCOUNTTYPE")
    STAFF = relationship(
        "STAFF", primaryjoin="ACCOUNTING.ACO_REGBY == STAFF.ST_ID"
    )
    HIERARCHY = relationship(
        "HIERARCHY",
        primaryjoin="ACCOUNTING.ACO_REGBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    HIERARCHY1 = relationship(
        "HIERARCHY",
        primaryjoin="ACCOUNTING.ACO_UPDATEBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    ANONYMIZATION_LOG = relationship("ANONYMIZATIONLOG")
    KST = relationship("KST")
    CURRENCY = relationship("CURRENCY")
    PROJECT = relationship("PROJECT")
    REASON_FOR_ADDITIONAL_EFFORT = relationship("REASONFORADDITIONALEFFORT")
    STAFF1 = relationship(
        "STAFF", primaryjoin="ACCOUNTING.ST_ID == STAFF.ST_ID"
    )
    STAFF2 = relationship(
        "STAFF", primaryjoin="ACCOUNTING.ST_ID_SAPOK == STAFF.ST_ID"
    )
    HIERARCHY2 = relationship(
        "HIERARCHY", primaryjoin="ACCOUNTING.ST_ID_TEAM == HIERARCHY.HR_NEW_ID"
    )


class CALENDARENTRY(Base):
    __tablename__ = "CALENDAR_ENTRY"
    __table_args__ = (
        Index(
            "IX_CALENDAR_ENTRY_P_ID_SO_NUMBER_DISABLED",
            "P_ID",
            "SO_NUMBER",
            "DISABLED",
            "TRANSFER_STATUS",
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    SO_NUMBER = Column(Integer, nullable=False)
    ST_ID = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    SUBJECT = Column(Unicode(255))
    DESCRIPTION = Column(Unicode(4000))
    START_TIME = Column(DateTime)
    END_TIME = Column(DateTime)
    ALL_DAY_EVENT = Column(BIT, nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    TRANSFER_STATUS = Column(Integer, nullable=False)

    STAFF = relationship(
        "STAFF", primaryjoin="CALENDARENTRY.CREATED_BY == STAFF.ST_ID"
    )
    PROJECT = relationship("PROJECT")
    STAFF1 = relationship(
        "STAFF", primaryjoin="CALENDARENTRY.ST_ID == STAFF.ST_ID"
    )
    STAFF2 = relationship(
        "STAFF", primaryjoin="CALENDARENTRY.UPDATED_BY == STAFF.ST_ID"
    )


class CERTIFICATE(Base):
    __tablename__ = "CERTIFICATE"
    __table_args__ = (
        Index(
            "UIX_CERTIFICATE_P_ID_SO_NUMBER_MAIN_CERTIFICATE",
            "P_ID",
            "SO_NUMBER",
            "MAIN_CERTIFICATE",
            unique=True,
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    SO_NUMBER = Column(Integer)
    NUMBER = Column(Unicode(30))
    MAIN_CERTIFICATE = Column(BIT, nullable=False)
    TYPES = Column(Unicode(256))
    HOLDER_CONTACT = Column(Unicode(128))
    UNIT_FEES = Column(Integer)
    TECHNICAL_CERTIFIER = Column(Unicode(60))
    TESTING_BASE = Column(Unicode(2000))
    PRODUCT = Column(Unicode(4000))
    PRODUCT_ADDITIONAL = Column(Unicode(120))
    MODELS = Column(Unicode(4000))
    RESPONSIBLE_DEPARTMENT = Column(Unicode(20))
    ISSUING_DEPARTMENT = Column(Unicode(50))
    ISSUE_DATE = Column(DateTime)
    EXPIRATION_DATE = Column(DateTime)
    STATUS = Column(Unicode(30))
    LAST_IMPORT_FROM_CBW = Column(DateTime)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="CERTIFICATE.CREATED_BY == STAFF.ST_ID"
    )
    PROJECT = relationship("PROJECT")
    STAFF1 = relationship(
        "STAFF", primaryjoin="CERTIFICATE.UPDATED_BY == STAFF.ST_ID"
    )


class CHANCE(Base):
    __tablename__ = "CHANCES"
    __table_args__ = {"schema": "dbo"}

    CH_ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    CHT_ID = Column(ForeignKey("dbo.CHANCETYPE.CHT_ID"))
    CH_INFO = Column(Unicode(255))
    CH_DATE = Column(DateTime)
    CH_CHECKDATE = Column(DateTime)
    CH_CHECKBY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    CH_CHECKCOMMENT = Column(Unicode(255))
    CH_DISABLED = Column(BIT, nullable=False)
    CH_CHECKBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    AL_ID = Column(ForeignKey("dbo.ANONYMIZATION_LOG.AL_ID"))

    ANONYMIZATION_LOG = relationship("ANONYMIZATIONLOG")
    CHANCETYPE = relationship("CHANCETYPE")
    STAFF = relationship("STAFF")
    HIERARCHY = relationship("HIERARCHY")
    PROJECT = relationship("PROJECT")


class FAZ(Base):
    __tablename__ = "FAZ"
    __table_args__ = (
        Index(
            "IX_FAZ_P_ID_SO_NUMBER_FAZ_DISABLED",
            "P_ID",
            "SO_NUMBER",
            "FAZ_DISABLED",
        ),
        {"schema": "dbo"},
    )

    FAZ_ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"))
    SO_NUMBER = Column(Integer)
    FAZ_CERTNUMBER = Column(Unicode(30))
    FAZ_REMARK = Column(Unicode(255))
    FAZ_CLEAR = Column(Unicode(255))
    FAZ_DATE = Column(DateTime)
    FAZ_BY = Column(Unicode(30))
    FAZ_DISABLED = Column(BIT, nullable=False)
    ZETY_TYP = Column(Unicode(100))
    FAZ_PSOBJECT_TERM = Column(Unicode(50))
    FAZ_CERT_OWNER = Column(Integer)
    TS_ID = Column(ForeignKey("dbo.TESTSAMPLE.TS_ID"))
    FAZ_POSTING_STATUS = Column(Unicode(50))
    RM_ID = Column(Integer, nullable=False)

    PROJECT = relationship("PROJECT")
    TESTSAMPLE = relationship("TESTSAMPLE")


class FILESYSTEMLOG(Base):
    __tablename__ = "FILE_SYSTEM_LOG"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    TIMESTAMP = Column(DateTime, nullable=False)
    PC_ID = Column(ForeignKey("dbo.PROCESS.PC_ID"))
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"))
    OPERATION = Column(Integer, nullable=False)
    FULL_PATH = Column(Unicode(2056), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)

    STAFF = relationship("STAFF")
    PROCES = relationship("PROCES")
    PROJECT = relationship("PROJECT")


class FOCUSDOCUMENT(Base):
    __tablename__ = "FOCUSDOCUMENT"
    __table_args__ = (
        Index("IX_FOCUSDOCUMENT_PROJECT_SUBORDER", "PROJECT", "SUBORDER"),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    PROJECT = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    SUBORDER = Column(Integer)
    PATH = Column(Unicode(1024), nullable=False)
    NAME = Column(Unicode(1024), nullable=False)
    FOCUS = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime, nullable=False)
    UPDATED_BY = Column(Integer, nullable=False)
    DISABLED = Column(DateTime)

    STAFF = relationship("STAFF")
    PROJECT1 = relationship("PROJECT")


class KALKUNTERMODULBEARBEITER(Base):
    __tablename__ = "KALKUNTERMODULBEARBEITER"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    KALUM_ID = Column(
        ForeignKey("dbo.KALKUNTERMODUL.KALUM_ID"), nullable=False
    )
    KALUM_WC_ID = Column(ForeignKey("dbo.HIERARCHY.HR_ID"), nullable=False)
    ST_ID = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)

    KALKUNTERMODUL = relationship("KALKUNTERMODUL")
    HIERARCHY = relationship("HIERARCHY")
    STAFF = relationship("STAFF")


class PROJECTADDON(Base):
    __tablename__ = "PROJECT_ADDON"
    __table_args__ = {"schema": "dbo"}

    PA_ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False, unique=True)
    PA_DISPATCHER = Column(Integer)
    OC_ID = Column(Integer)
    PA_PART_NUMBER = Column(Unicode(255))
    PA_RFN = Column(Unicode(255))
    PA_MANUFACTURER_NUMBER = Column(Unicode(255))
    PA_DRAFT_NUMBER = Column(Unicode(255))
    RRTB_ID = Column(Integer)
    PCAT_ID = Column(Integer)
    PMOD_ID = Column(Integer)
    PA_MAIN_DIMENSIONS = Column(Unicode(255))
    CERT_APPL_ID = Column(ForeignKey("dbo.CERT_APPL_TCS.APPL_ID"))
    PA_OPERATORS_IDENTIFICATION = Column(Unicode(255))
    PA_BUILDING = Column(Unicode(255))

    CERT_APPL_TC = relationship("CERTAPPLTC")
    PROJECT = relationship("PROJECT")


class PROJECTAPPLICATIONFORM(Base):
    __tablename__ = "PROJECT_APPLICATION_FORM"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    APPLICATION_FORM = Column(
        ForeignKey("dbo.APPLICATION_FORM.ID"), nullable=False
    )
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DATETIME2, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DATETIME2)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    APPLICATION_FORM1 = relationship("APPLICATIONFORM")
    STAFF = relationship(
        "STAFF", primaryjoin="PROJECTAPPLICATIONFORM.CREATED_BY == STAFF.ST_ID"
    )
    PROJECT = relationship("PROJECT")
    STAFF1 = relationship(
        "STAFF", primaryjoin="PROJECTAPPLICATIONFORM.UPDATED_BY == STAFF.ST_ID"
    )


class PROJECTEDOCBASEREL(Base):
    __tablename__ = "PROJECT_EDOC_BASE_REL"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    SO_NUMBER = Column(Integer)
    B_ID = Column(Integer, nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="PROJECTEDOCBASEREL.CREATED_BY == STAFF.ST_ID"
    )
    PROJECT = relationship("PROJECT")
    STAFF1 = relationship(
        "STAFF", primaryjoin="PROJECTEDOCBASEREL.UPDATED_BY == STAFF.ST_ID"
    )


class PROJECTFAILUREREL(Base):
    __tablename__ = "PROJECT_FAILURE_REL"
    __table_args__ = (
        Index("IX_PROJECT_FAILURE_REL_P_ID_SO_NUMBER", "P_ID", "SO_NUMBER"),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    SO_NUMBER = Column(Integer)
    FAIL_ID = Column(ForeignKey("dbo.FAILURE_MD.FAIL_ID"), nullable=False)

    FAILURE_MD = relationship("FAILUREMD")
    PROJECT = relationship("PROJECT")


class PROJECTFILE(Base):
    __tablename__ = "PROJECT_FILE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    FOLDER = Column(Unicode(256))
    NAME = Column(Unicode(256), nullable=False)
    DATA = Column(LargeBinary)
    SOURCE_SYSTEM = Column(Unicode(32), nullable=False)
    RETRIEVED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)

    PROJECT = relationship("PROJECT")


class PROJECTPOSITION(Base):
    __tablename__ = "PROJECT_POSITION"
    __table_args__ = (
        Index(
            "IX_PROJECT_POSITION_P_ID_PP_DISABLED",
            "P_ID",
            "PP_DISABLED",
            "PP_DISCOUNT",
        ),
        {"schema": "dbo"},
    )

    PP_ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False, index=True)
    PP_IS_QUOTATION_POSITION = Column(BIT)
    PP_NUMBER = Column(Integer, nullable=False)
    PP_DISABLED = Column(BIT, nullable=False)
    PP_STATUS = Column(Integer, nullable=False)
    PP_STATUS_CHANGED_ON = Column(DateTime)
    PP_STATUS_CHANGED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    PP_TEXT = Column(Unicode(4000))
    PP_SALES_PRICE = Column(DECIMAL(18, 2))
    ZM_ID = Column(Unicode(18))
    PP_TYPE = Column(Integer, nullable=False)
    PP_LAST_SAP_UPDATE = Column(DateTime)
    PP_CANCELLATION_FLAG = Column(BIT, nullable=False)
    PP_CREATED = Column(DateTime, nullable=False)
    PP_CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    PP_UPDATED = Column(DateTime)
    PP_UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    PP_PREPAYMENT_PRICE = Column(DECIMAL(18, 2), nullable=False)
    PP_PRINTING_FLAG = Column(Unicode(5))
    PP_SINGLE_PRICE = Column(DECIMAL(18, 2), nullable=False)
    PP_TARGET_COUNT = Column(DECIMAL(18, 2), nullable=False)
    PP_SP_FOREIGN = Column(DECIMAL(18, 2))
    FROM_PS_CONFIG = Column(BIT, nullable=False)
    PP_UNIT = Column(Unicode(3))
    FROM_STARLIMS = Column(BIT, nullable=False)
    PP_FI_FACTOR = Column(Unicode(5))
    PP_INTERNAL_NOTE = Column(Unicode(1024))
    PP_CANCELLATION_REASON = Column(ForeignKey("dbo.CANCELLATION_REASON.ID"))
    CRM_TRANSFER_DATE = Column(DateTime)
    PP_DISCOUNT = Column(DECIMAL(18, 2))
    PP_PLANT = Column(ForeignKey("dbo.PLANT.ID"))
    PP_TAXABLE = Column(BIT, nullable=False)
    PP_DISCOUNT_PERCENTAGE = Column(DECIMAL(19, 10), nullable=False)
    PP_START_DATE = Column(Date)
    PP_END_DATE = Column(Date)

    CANCELLATION_REASON = relationship("CANCELLATIONREASON")
    STAFF = relationship(
        "STAFF", primaryjoin="PROJECTPOSITION.PP_CREATED_BY == STAFF.ST_ID"
    )
    PLANT = relationship("PLANT")
    STAFF1 = relationship(
        "STAFF",
        primaryjoin="PROJECTPOSITION.PP_STATUS_CHANGED_BY == STAFF.ST_ID",
    )
    STAFF2 = relationship(
        "STAFF", primaryjoin="PROJECTPOSITION.PP_UPDATED_BY == STAFF.ST_ID"
    )
    PROJECT = relationship("PROJECT")


class PROJECTSTARLIM(Base):
    __tablename__ = "PROJECT_STARLIMS"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    STARLIMS_PROJECT_NUMBER = Column(Unicode(25), nullable=False)

    PROJECT = relationship("PROJECT")


class PROKALKMODUL(Base):
    __tablename__ = "PROKALKMODUL"
    __table_args__ = {"schema": "dbo"}

    PKM_ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False, index=True)
    KALM_ID = Column(Integer)
    KAL_ID = Column(Integer)
    PKM_TYP = Column(Integer)
    PKM_NAME = Column(Unicode(1024))
    PKM_IS_UA = Column(BIT)
    PKM_TAGE_UA = Column(Integer)
    TP_ID = Column(Integer)
    PKM_TESTDAUER = Column(Integer)
    PKM_EINHEITEN = Column(DECIMAL(18, 2))
    PKM_SATZ = Column(DECIMAL(18, 2))
    PKM_AUFWAND = Column(DECIMAL(18, 2))
    PKM_FAKTOR = Column(DECIMAL(18, 2))
    PKM_VK = Column(DECIMAL(18, 2))
    PKM_AUFTRAGSTEXT = Column(Unicode(1024))
    PKM_KOMMENTAR = Column(Unicode(1024))
    PKM_REIHE = Column(Integer)
    PKM_UA = Column(Integer)
    MIT_ID = Column(Integer)
    PKM_REGDATE = Column(DateTime)
    PKM_REGBY = Column(Integer)
    PKM_UPDATE = Column(DateTime)
    PKM_UPDATEBY = Column(Integer)
    MIT_ID_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    PKM_REGBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    PKM_UPDATEBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    AL_ID = Column(ForeignKey("dbo.ANONYMIZATION_LOG.AL_ID"))
    PKM_DISABLED = Column(BIT, nullable=False)
    FROM_PS_CONFIG = Column(BIT, nullable=False)

    ANONYMIZATION_LOG = relationship("ANONYMIZATIONLOG")
    HIERARCHY = relationship(
        "HIERARCHY",
        primaryjoin="PROKALKMODUL.MIT_ID_TEAM == HIERARCHY.HR_NEW_ID",
    )
    HIERARCHY1 = relationship(
        "HIERARCHY",
        primaryjoin="PROKALKMODUL.PKM_REGBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    HIERARCHY2 = relationship(
        "HIERARCHY",
        primaryjoin="PROKALKMODUL.PKM_UPDATEBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    PROJECT = relationship("PROJECT")


class SOTRANSFERJOB(Base):
    __tablename__ = "SOTRANSFERJOB"
    __table_args__ = (
        Index("IX_SOTRANSFERJOB_SEARCH", "STATUS", "DIR", "P_ID"),
        {"schema": "dbo"},
    )

    TRA_ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    DIR = Column(NCHAR(1), nullable=False)
    FILENAME = Column(Unicode(512), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)
    STATUS = Column(Unicode(10))
    SRC_FOLDER = Column(Unicode(512))
    TAR_FOLDER = Column(Unicode(512))

    PROJECT = relationship("PROJECT")


class SUBORDER(Base):
    __tablename__ = "SUBORDERS"
    __table_args__ = (
        Index(
            "IX_SUBORDERS_ST_ID_SO_DATE_READY_SO_DISABLED_SO_DEADLINE",
            "ST_ID",
            "SO_DATE_READY",
            "SO_DISABLED",
            "SO_DEADLINE",
        ),
        Index(
            "IX_SUBORDERS_ST_ID_SO_DATE_READY_SO_DATE_CHECK_SO_DISABLED",
            "ST_ID",
            "SO_DATE_READY",
            "SO_DATE_CHECK",
            "SO_DISABLED",
        ),
        Index(
            "IX_SUBORDERS_ST_ID_SO_DATE_CHECK_SO_DISABLED",
            "ST_ID",
            "SO_DATE_CHECK",
            "SO_DISABLED",
        ),
        Index(
            "IX_SUBORDERS_SO_DATE_READY_SO_DEADLINE_SO_DISABLED",
            "SO_DATE_READY",
            "SO_DEADLINE",
            "SO_DISABLED",
        ),
        Index(
            "IX_SUBORDERS_MAIN_SCREEN_SEARCH",
            "P_ID",
            "ST_ID",
            "SO_DISABLED",
            "SO_PREDATE",
            "SO_NUMBER",
            "SO_DEADLINE",
            "SO_FORECAST",
            "SO_WAIT",
            "SO_IsTransferredBack",
            "UA_TRANS_PROJECT",
            "SO_REPORT_NUMBER",
            "SO_REMARK",
            "SO_POST_OUT_DATE",
            "SO_CONFIRMED_DATE",
            "SO_DATE_READY",
            "SO_DATE_CHECK",
        ),
        Index(
            "IX_SUBORDERS_SO_DISABLED",
            "SO_DISABLED",
            "P_ID",
            "SO_NUMBER",
            "ST_ID",
            "SO_DEADLINE",
            "SO_DATE_READY",
            "ST_ID_TEAM",
            "BANF_REQUEST",
            "BANF_ORDER",
            "SO_COORDINATOR",
            "SO_POSTING_DONE_DATE",
            "UA_TRANS_PROJECT",
            "SO_Docu_Done",
            "SO_CUSTOMER_A",
            "SO_CUSTOMER_B",
            "SO_APPOINTMENTDATE",
            "SAP_NO",
            "SO_DATE_CHECK",
            "SO_FORECAST",
            "RES_ID",
            "SO_PREDATE",
            "SO_WAIT",
            "SO_IsTransferredBack",
        ),
        Index(
            "IX_SUBORDERS_ST_ID_SO_DISABLED",
            "ST_ID",
            "SO_DISABLED",
            "P_ID",
            "SO_NUMBER",
            "SO_DEADLINE",
            "SO_DATE_READY",
            "UA_TRANS_PROJECT",
            "SO_CONFIRMED_DATE",
            "SO_DATE_CHECK",
            "SO_FORECAST",
            "SO_PREDATE",
            "SO_WAIT",
            "SO_IsTransferredBack",
            "SO_COORDINATOR",
            "ST_ID_TEAM",
            "SO_REPORT_NUMBER",
            "ZM_ID",
            "SO_REMARK",
            "SO_POST_OUT_DATE",
        ),
        {"schema": "dbo"},
    )

    P_ID = Column(
        ForeignKey("dbo.PROJECT.P_ID"), primary_key=True, nullable=False
    )
    SO_NUMBER = Column(Integer, primary_key=True, nullable=False)
    SO_DISPOBY = Column(Integer)
    SO_CREATED = Column(DateTime)
    ST_ID = Column(Integer)
    SO_DEADLINE = Column(DateTime)
    SO_TASK = Column(Unicode(1024))
    SO_HOURS = Column(DECIMAL(18, 6))
    SO_RATE = Column(MONEY)
    SO_SPENDS = Column(MONEY)
    SO_ACC_HOURS = Column(MONEY)
    SO_ACC_SPENDS = Column(DECIMAL(18, 2))
    SO_REPORT = Column(Unicode(255))
    SO_START_MACRO = Column(BIT)
    MCO_ID = Column(Integer)
    SO_COMMENT = Column(Unicode(2000))
    SO_DATE_READY = Column(DateTime)
    SO_READYBY = Column(Integer)
    SO_DATE_CHECK = Column(DateTime)
    SO_CHECKBY = Column(Integer)
    SO_FORECAST = Column(DECIMAL(18, 2))
    SO_LANGUAGE = Column(Unicode(5))
    RES_ID = Column(Integer)
    SO_ACC_POS = Column(Unicode(10))
    SO_INTERN = Column(BIT)
    SO_PREDATE = Column(DateTime)
    SO_PREDATE_REMINDER = Column(BIT, nullable=False)
    SO_PREDATE_INFO = Column(Unicode(255))
    SO_WAIT = Column(BIT)
    SO_REGBY = Column(Integer)
    SO_REGDATE = Column(DateTime)
    SO_UPDATEBY = Column(Integer)
    SO_UPDATE = Column(DateTime)
    SO_TRANSFERSTATUS = Column(Unicode(50))
    SO_DISABLED = Column(BIT, nullable=False)
    SO_ForeignExpenditure = Column(MONEY)
    SO_PostedFromForeign = Column(MONEY)
    SO_IsTransferredBack = Column(BIT)
    UA_TRANS_PROJECT = Column(Integer)
    SO_Docu_Done = Column(BIT)
    SO_DEADLINE_REMINDER = Column(BIT)
    SO_CUSTOMER_A = Column(Integer)
    SO_CUSTOMER_B = Column(Integer)
    SO_CUSTOMER_O = Column(Integer)
    SO_PARENT = Column(Integer)
    SO_SORT = Column(Integer, nullable=False)
    SO_ADMINISTRATIVE = Column(BIT, nullable=False)
    SO_APPOINTMENTDATE = Column(DateTime)
    PLAN_ACTUAL_HOUR = Column(DECIMAL(8, 2))
    PLAN_TRAVEL = Column(DECIMAL(18, 2))
    PLAN_EXTERNAL = Column(DECIMAL(18, 2))
    ACC_EFFORT = Column(DECIMAL(18, 2))
    ACC_ACTUAL_HOUR = Column(DECIMAL(18, 2))
    ACC_TRAVEL = Column(DECIMAL(18, 2))
    ACC_EXTERNAL = Column(DECIMAL(18, 2))
    SAP_NO = Column(Unicode(10))
    ORDER_SIGN = Column(Unicode(35))
    ORDER_DATE = Column(DateTime)
    ORDER_POSITION = Column(Unicode(6))
    SO_CHECKBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    SO_DISPOBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    SO_READYBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    SO_REGBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    SO_UPDATEBY_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    ST_ID_TEAM = Column(ForeignKey("dbo.HIERARCHY.HR_NEW_ID"))
    AL_ID = Column(ForeignKey("dbo.ANONYMIZATION_LOG.AL_ID"))
    SO_PLANNED_MATERIAL = Column(DECIMAL(18, 2))
    SO_PLANNED_LICENSE = Column(DECIMAL(18, 2))
    BANF_REQUEST = Column(DateTime)
    BANF_ORDER = Column(DateTime)
    B2B = Column(BIT, nullable=False)
    SO_REPORT_NUMBER = Column(Unicode(256))
    ZM_ID = Column(Unicode(18))
    SO_REMARK = Column(Unicode(1024))
    SO_POST_OUT_DATE = Column(DateTime)
    SO_CONFIRMED_DATE = Column(DateTime)
    LIMS_STATUS = Column(Unicode(16))
    LIMS_REMARK = Column(Unicode(256))
    SOC_ID = Column(ForeignKey("dbo.SUBORDER_CATEGORY.ID"))
    RFAE_ID = Column(ForeignKey("dbo.REASON_FOR_ADDITIONAL_EFFORT.ID"))
    FROM_STARLIMS = Column(BIT, nullable=False)
    SO_COORDINATOR = Column(Integer)
    STARLIMS_DISTINCTIVE_FLAG = Column(Integer)
    DEADLINE_CALCULATION_WITHOUT_HOLIDAYS = Column(BIT, nullable=False)
    SO_MODEL = Column(Unicode(255))
    TRANSFER_TO_STARLIMS = Column(DateTime)
    STARLIMS_PROJECT_NUMBER = Column(Unicode(25))
    URGENT = Column(BIT, nullable=False)
    SO_POSTING_DONE_DATE = Column(DateTime)
    KPI = Column(BIT, nullable=False)
    SO_DATE_READY_REASON = Column(Unicode(512))
    SO_DATE_READY_CHANGED = Column(DateTime)
    SO_DATE_CHECK_REASON = Column(Unicode(512))
    SO_DATE_CHECK_CHANGED = Column(DateTime)
    REPORT_SENT = Column(DateTime)
    S_KPI_NUMBER = Column(Integer)
    SO_TUV_CERT_EXISTS = Column(BIT, nullable=False)
    SO_EXTERNAL_CERT_EXISTS = Column(BIT, nullable=False)
    SO_CERT_COMMENT = Column(Unicode(512))

    ANONYMIZATION_LOG = relationship("ANONYMIZATIONLOG")
    PROJECT = relationship("PROJECT")
    REASON_FOR_ADDITIONAL_EFFORT = relationship("REASONFORADDITIONALEFFORT")
    SUBORDER_CATEGORY = relationship("SUBORDERCATEGORY")
    HIERARCHY = relationship(
        "HIERARCHY",
        primaryjoin="SUBORDER.SO_CHECKBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    HIERARCHY1 = relationship(
        "HIERARCHY",
        primaryjoin="SUBORDER.SO_DISPOBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    HIERARCHY2 = relationship(
        "HIERARCHY",
        primaryjoin="SUBORDER.SO_READYBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    HIERARCHY3 = relationship(
        "HIERARCHY",
        primaryjoin="SUBORDER.SO_REGBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    HIERARCHY4 = relationship(
        "HIERARCHY",
        primaryjoin="SUBORDER.SO_UPDATEBY_TEAM == HIERARCHY.HR_NEW_ID",
    )
    HIERARCHY5 = relationship(
        "HIERARCHY", primaryjoin="SUBORDER.ST_ID_TEAM == HIERARCHY.HR_NEW_ID"
    )


class SUBORDERLAGERELEMENT(Base):
    __tablename__ = "SUBORDER_LAGERELEMENT"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    SO_NUMBER = Column(Integer, nullable=False)
    LGEL_ID = Column(Integer, nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="SUBORDERLAGERELEMENT.CREATED_BY == STAFF.ST_ID"
    )
    PROJECT = relationship("PROJECT")
    STAFF1 = relationship(
        "STAFF", primaryjoin="SUBORDERLAGERELEMENT.UPDATED_BY == STAFF.ST_ID"
    )


class SUBORDERLIMSIMAGE(Base):
    __tablename__ = "SUBORDER_LIMS_IMAGE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    SO_NUMBER = Column(Integer, nullable=False)
    LIMS_IMAGE_NAME = Column(Unicode(256), nullable=False)
    LIMS_IMAGE = Column(LargeBinary, nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="SUBORDERLIMSIMAGE.CREATED_BY == STAFF.ST_ID"
    )
    PROJECT = relationship("PROJECT")
    STAFF1 = relationship(
        "STAFF", primaryjoin="SUBORDERLIMSIMAGE.UPDATED_BY == STAFF.ST_ID"
    )


class SUBORDERSAMPLE(Base):
    __tablename__ = "SUBORDER_SAMPLE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    SO_NUMBER = Column(Integer, nullable=False)
    SAMPLE_NUMBER = Column(Unicode(16), nullable=False)
    SAMPLE_DESCRIPTION = Column(Unicode(256))
    REMARK = Column(Unicode(512))
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="SUBORDERSAMPLE.CREATED_BY == STAFF.ST_ID"
    )
    PROJECT = relationship("PROJECT")
    STAFF1 = relationship(
        "STAFF", primaryjoin="SUBORDERSAMPLE.UPDATED_BY == STAFF.ST_ID"
    )


class SUBORDERTESTMETHOD(Base):
    __tablename__ = "SUBORDER_TEST_METHOD"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    SO_NUMBER = Column(Integer, nullable=False)
    STKO_ID = Column(Integer)
    STANDARD_ANALYSIS = Column(Unicode(128))
    TEST_METHOD_ID = Column(
        ForeignKey("dbo.LIMS_TEST_METHOD.ID"), nullable=False
    )
    TEST_METHOD_NAME = Column(Unicode(128), nullable=False)
    PARAMETER = Column(Unicode(128), nullable=False)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF", primaryjoin="SUBORDERTESTMETHOD.CREATED_BY == STAFF.ST_ID"
    )
    PROJECT = relationship("PROJECT")
    LIMS_TEST_METHOD = relationship("LIMSTESTMETHOD")
    STAFF1 = relationship(
        "STAFF", primaryjoin="SUBORDERTESTMETHOD.UPDATED_BY == STAFF.ST_ID"
    )


class TCPROKALKUNTERMODUL(Base):
    __tablename__ = "TC_PROKALKUNTERMODUL"
    __table_args__ = {"schema": "dbo"}

    PKUM_ID = Column(Integer, primary_key=True)
    PKM_ID = Column(ForeignKey("dbo.TC_PROKALKMODUL.PKM_ID"), nullable=False)
    P_ID = Column(ForeignKey("dbo.TC_PROJECT.P_ID"), nullable=False)
    ST_ID = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    PKUM_NAME = Column(Unicode(256), nullable=False)
    PKUM_DAYS_TO_START = Column(Integer, nullable=False)
    PKUM_DURATION = Column(Integer, nullable=False)
    TP_ID = Column(ForeignKey("dbo.TEMPLATE.TP_ID"))
    PKUM_PLANNED_HOURS = Column(DECIMAL(18, 2), nullable=False)
    PKUM_PLANNED_EXPENSES = Column(DECIMAL(18, 2), nullable=False)
    PKUM_FACTOR = Column(DECIMAL(18, 2), nullable=False)
    PKUM_PLANNED_TRAVEL_COSTS = Column(DECIMAL(18, 2), nullable=False)
    PKUM_RECOMMENDED_PRICE = Column(DECIMAL(18, 2), nullable=False)
    PKUM_COMMENT = Column(Unicode(500), nullable=False)
    PKUM_ORDER_TEXT = Column(Unicode(500), nullable=False)
    PKUM_SORT = Column(Integer, nullable=False)
    PP_ID = Column(ForeignKey("dbo.TC_PROJECT_POSITION.PP_ID"))
    ZM_ID = Column(Unicode(18))
    PKUM_PLANNED_EXPENSES_EXTERNAL = Column(
        DECIMAL(18, 2), nullable=False, server_default=text("((0))")
    )

    TC_PROKALKMODUL = relationship("TCPROKALKMODUL")
    TC_PROJECT_POSITION = relationship("TCPROJECTPOSITION")
    TC_PROJECT = relationship("TCPROJECT")
    STAFF = relationship("STAFF")
    TEMPLATE = relationship("TEMPLATE")


class VERIFICATIONDOCUMENT(Base):
    __tablename__ = "VERIFICATION_DOCUMENT"
    __table_args__ = (
        Index(
            "IX_VERIFICATION_DOCUMENT_P_ID_VD_DISABLED", "P_ID", "VD_DISABLED"
        ),
        {"schema": "dbo"},
    )

    VD_ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    VD_NAME = Column(Unicode(1024), nullable=False)
    VD_CATEGORY = Column(Integer, nullable=False)
    VD_CHECKED = Column(BIT, nullable=False)
    VD_SORT = Column(Integer, nullable=False)
    VD_DISABLED = Column(BIT, nullable=False)
    VD_CREATED = Column(DateTime, nullable=False)
    VD_CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    VD_UPDATED = Column(DateTime)
    VD_UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    FROM_PS_CONFIG = Column(BIT, nullable=False)

    PROJECT = relationship("PROJECT")
    STAFF = relationship(
        "STAFF",
        primaryjoin="VERIFICATIONDOCUMENT.VD_CREATED_BY == STAFF.ST_ID",
    )
    STAFF1 = relationship(
        "STAFF",
        primaryjoin="VERIFICATIONDOCUMENT.VD_UPDATED_BY == STAFF.ST_ID",
    )


class WAITHISTORY(Base):
    __tablename__ = "WAIT_HISTORY"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False)
    SO_NUMBER = Column(Integer)
    WAIT = Column(BIT, nullable=False)
    COMMENT = Column(Unicode(512))
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)

    STAFF = relationship("STAFF")
    PROJECT = relationship("PROJECT")


class ACOIDOCEXPORT(Base):
    __tablename__ = "ACO_IDOC_EXPORT"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    ACO_ID = Column(
        ForeignKey("dbo.ACCOUNTING.ACO_ID"), nullable=False, index=True
    )
    CREATED = Column(DateTime, nullable=False)
    STATUS = Column(Unicode(10))
    DESCRIPTION = Column(Unicode(256))
    VAR1 = Column(Unicode(50))
    VAR2 = Column(Unicode(50))
    VAR3 = Column(Unicode(50))
    VAR4 = Column(Unicode(50))
    DOCNUM = Column(Unicode(16))
    MESSAGE = Column(Unicode)
    IDOC_DATA = Column(NTEXT(1073741823))
    IDOC_DATE = Column(DateTime)

    ACCOUNTING = relationship("ACCOUNTING")


class MHSPROJECTDATACODE(Base):
    __tablename__ = "MHS_PROJECTDATA_CODE"
    __table_args__ = (
        Index(
            "IX_MHS_PROJECTDATA_CODE", "MHSPROJECTDATA", "CODE", unique=True
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    MHSPROJECTDATA = Column(
        ForeignKey("dbo.MHS_PROJECTDATA.ID"), nullable=False
    )
    CODE = Column(ForeignKey("dbo.CODE_TYPE.ID"), nullable=False)

    CODE_TYPE = relationship("CODETYPE")
    MHS_PROJECTDATUM = relationship("MHSPROJECTDATUM")


class MHSPROJECTDATALANGUAGE(Base):
    __tablename__ = "MHS_PROJECTDATA_LANGUAGE"
    __table_args__ = (
        Index(
            "IX_MHS_PROJECTDATA_LANGUAGE",
            "MHSPROJECTDATA",
            "LANGUAGE",
            unique=True,
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    MHSPROJECTDATA = Column(
        ForeignKey("dbo.MHS_PROJECTDATA.ID"), nullable=False
    )
    LANGUAGE = Column(ForeignKey("dbo.LANGUAGE_TYPE.ID"), nullable=False)

    LANGUAGE_TYPE = relationship("LANGUAGETYPE")
    MHS_PROJECTDATUM = relationship("MHSPROJECTDATUM")


class MHSPROJECTDATASPECIAL(Base):
    __tablename__ = "MHS_PROJECTDATA_SPECIAL"
    __table_args__ = (
        Index(
            "IX_MHS_PROJECTDATA_SPECIAL",
            "MHSPROJECTDATA",
            "SPECIAL",
            unique=True,
        ),
        {"schema": "dbo"},
    )

    ID = Column(Integer, primary_key=True)
    MHSPROJECTDATA = Column(
        ForeignKey("dbo.MHS_PROJECTDATA.ID"), nullable=False
    )
    SPECIAL = Column(ForeignKey("dbo.SPECIAL_TYPE.ID"), nullable=False)

    MHS_PROJECTDATUM = relationship("MHSPROJECTDATUM")
    SPECIAL_TYPE = relationship("SPECIALTYPE")


class PROKALKUNTERMODUL(Base):
    __tablename__ = "PROKALKUNTERMODUL"
    __table_args__ = (
        Index(
            "IX_PROKALKUNTERMODUL_PKUM_DISABLED",
            "PKUM_DISABLED",
            "P_ID",
            "SO_NUMBER",
            "PKUM_PLANNED_HOURS",
            "PKUM_NAME",
        ),
        Index(
            "IX_PROKALKUNTERMODUL_PKM_ID_PKUM_DISABLED",
            "PKM_ID",
            "PKUM_DISABLED",
        ),
        Index(
            "IX_PROKALKUNTERMODUL_P_ID_SO_NUMBER",
            "P_ID",
            "SO_NUMBER",
            "PKUM_DISABLED",
            "PKUM_SP_PRICELIST",
            "PKUM_SP_PRICELIST_ORG",
            "PKUM_CANCELLED",
            "PKUM_PLANNED_HOURS",
        ),
        {"schema": "dbo"},
    )

    PKUM_ID = Column(Integer, primary_key=True)
    PKM_ID = Column(ForeignKey("dbo.PROKALKMODUL.PKM_ID"), nullable=False)
    P_ID = Column(ForeignKey("dbo.PROJECT.P_ID"), nullable=False, index=True)
    SO_NUMBER = Column(Integer)
    PKUM_QUOTATION_POSITION = Column(ForeignKey("dbo.PROJECT_POSITION.PP_ID"))
    PKUM_TESTING_POSITION = Column(ForeignKey("dbo.PROJECT_POSITION.PP_ID"))
    ST_ID = Column(ForeignKey("dbo.STAFF.ST_ID"))
    PKUM_NAME = Column(Unicode(1024))
    PKUM_DAYS_TO_START = Column(Integer, nullable=False)
    PKUM_DURATION = Column(Integer, nullable=False)
    TP_ID = Column(ForeignKey("dbo.TEMPLATE.TP_ID"))
    PKUM_PLANNED_HOURS = Column(DECIMAL(18, 2), nullable=False)
    PKUM_RATE = Column(DECIMAL(18, 2))
    PKUM_PLANNED_EXPENSES = Column(DECIMAL(18, 2), nullable=False)
    PKUM_FACTOR = Column(DECIMAL(18, 2), nullable=False)
    PKUM_PLANNED_TRAVEL_COSTS = Column(DECIMAL(18, 2), nullable=False)
    PKUM_RECOMMENDED_PRICE = Column(DECIMAL(18, 2), nullable=False)
    PKUM_COMMENT = Column(Unicode(2000))
    PKUM_ORDER_TEXT = Column(Unicode(1024))
    PKUM_ADDITIONAL_TEXT = Column(Unicode(1024))
    PKUM_SAP_TRANSFER = Column(DateTime)
    PKUM_SORT = Column(Integer, nullable=False)
    PKUM_DISABLED = Column(BIT, nullable=False)
    PKUM_CREATED = Column(DateTime, nullable=False)
    PKUM_CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    PKUM_UPDATED = Column(DateTime)
    PKUM_UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))
    PKUM_SO_TRANSFER_PRICE = Column(DECIMAL(18, 2), nullable=False)
    PKUM_SP_PRICELIST = Column(DECIMAL(18, 2), nullable=False)
    PKUM_SP_PRICELIST_ORG = Column(DECIMAL(18, 2), nullable=False)
    PKUM_TRAVELTIME = Column(DECIMAL(18, 2), nullable=False)
    PKUM_SP_FOREIGN = Column(DECIMAL(18, 10))
    ZM_ID = Column(Unicode(18))
    PKUM_BULKTEST = Column(BIT)
    PKUM_CANCELLED = Column(BIT, nullable=False)
    FROM_PS_CONFIG = Column(BIT, nullable=False)
    FROM_SUBORDER = Column(Integer)
    PKUM_KPI = Column(BIT, nullable=False)
    PKUM_S_KPI_NUMBER = Column(Integer)
    PKUM_PLANNED_SUBCONTRACTING = Column(DECIMAL(18, 2))

    PROKALKMODUL = relationship("PROKALKMODUL")
    STAFF = relationship(
        "STAFF", primaryjoin="PROKALKUNTERMODUL.PKUM_CREATED_BY == STAFF.ST_ID"
    )
    PROJECT_POSITION = relationship(
        "PROJECTPOSITION",
        primaryjoin="PROKALKUNTERMODUL.PKUM_QUOTATION_POSITION == PROJECTPOSITION.PP_ID",
    )
    PROJECT_POSITION1 = relationship(
        "PROJECTPOSITION",
        primaryjoin="PROKALKUNTERMODUL.PKUM_TESTING_POSITION == PROJECTPOSITION.PP_ID",
    )
    STAFF1 = relationship(
        "STAFF", primaryjoin="PROKALKUNTERMODUL.PKUM_UPDATED_BY == STAFF.ST_ID"
    )
    PROJECT = relationship("PROJECT")
    STAFF2 = relationship(
        "STAFF", primaryjoin="PROKALKUNTERMODUL.ST_ID == STAFF.ST_ID"
    )
    TEMPLATE = relationship("TEMPLATE")


class SOTRANSFERFILE(Base):
    __tablename__ = "SOTRANSFERFILE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    FILEPATH = Column(Unicode(512), nullable=False)
    ISFOCUS = Column(BIT, nullable=False)
    TRA_ID = Column(ForeignKey("dbo.SOTRANSFERJOB.TRA_ID"), nullable=False)
    DATALEN = Column(Integer, nullable=False)
    WRITEUTC = Column(DateTime, nullable=False)
    STATUS = Column(Unicode(10))
    MSG = Column(Unicode)

    SOTRANSFERJOB = relationship("SOTRANSFERJOB")


class SOTRANSFERPROTO(Base):
    __tablename__ = "SOTRANSFERPROTO"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    TRA_ID = Column(ForeignKey("dbo.SOTRANSFERJOB.TRA_ID"), nullable=False)
    SEQ = Column(Integer, nullable=False)
    MESSAGE = Column(Unicode, nullable=False)
    CREATED = Column(DateTime, nullable=False)

    SOTRANSFERJOB = relationship("SOTRANSFERJOB")


class SUBORDERTESTREQUIREMENTSAMPLE(Base):
    __tablename__ = "SUBORDER_TEST_REQUIREMENT_SAMPLE"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    METHOD_ID = Column(
        ForeignKey("dbo.SUBORDER_TEST_METHOD.ID"), nullable=False
    )
    SAMPLE_ID = Column(ForeignKey("dbo.SUBORDER_SAMPLE.ID"), nullable=False)
    MIX_SAMPLE_NUMBER = Column(Integer)
    DISABLED = Column(BIT, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"), nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(ForeignKey("dbo.STAFF.ST_ID"))

    STAFF = relationship(
        "STAFF",
        primaryjoin="SUBORDERTESTREQUIREMENTSAMPLE.CREATED_BY == STAFF.ST_ID",
    )
    SUBORDER_TEST_METHOD = relationship("SUBORDERTESTMETHOD")
    SUBORDER_SAMPLE = relationship("SUBORDERSAMPLE")
    STAFF1 = relationship(
        "STAFF",
        primaryjoin="SUBORDERTESTREQUIREMENTSAMPLE.UPDATED_BY == STAFF.ST_ID",
    )
