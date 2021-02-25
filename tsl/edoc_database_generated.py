# coding: utf-8
from sqlalchemy import (
    BigInteger,
    CHAR,
    Column,
    DECIMAL,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    NCHAR,
    Numeric,
    String,
    Table,
    Unicode,
    text,
)
from sqlalchemy.dialects.mssql import (
    BIT,
    IMAGE,
    MONEY,
    SMALLDATETIME,
    TINYINT,
    UNIQUEIDENTIFIER,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_ANALYZER_CLEARABLE_90DAYS = Table(
    "ANALYZER_CLEARABLE_90DAYS",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("StdGesamt", DECIMAL(38, 2)),
    schema="dbo",
)


t_ANALYZER_CLEARABLE_90DAYS_ASIA = Table(
    "ANALYZER_CLEARABLE_90DAYS_ASIA",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("StdGesamt", DECIMAL(38, 2)),
    schema="dbo",
)


t_ANALYZER_COUNT_STAFF = Table(
    "ANALYZER_COUNT_STAFF",
    metadata,
    Column("AnzahlMitarbeiter", BigInteger),
    Column("HR_SHORT", Unicode(10)),
    Column("HR_NEW_ID", Integer, nullable=False),
    schema="dbo",
)


t_ANALYZER_DURATION_90DAYS_CHECK = Table(
    "ANALYZER_DURATION_90DAYS_CHECK",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("P_PRODUCT", Unicode(255), nullable=False),
    Column("P_MODEL", Unicode(255), nullable=False),
    Column("HR_SHORT", Unicode(10)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("Bearbeiter", Integer),
    Column("Arbeitstage", Integer),
    Column("Datum_Check", DateTime),
    Column("TS_DATE_RECEIPT", DateTime),
    Column("KOT_ID", Integer),
    schema="dbo",
)


t_ANALYZER_DURATION_90DAYS_CHECK_UA = Table(
    "ANALYZER_DURATION_90DAYS_CHECK_UA",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("P_PRODUCT", Unicode(255), nullable=False),
    Column("P_MODEL", Unicode(255), nullable=False),
    Column("HR_SHORT", Unicode(10)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("Bearbeiter", Integer),
    Column("Arbeitstage", Integer),
    Column("Datum_Check", DateTime),
    Column("TS_DATE_RECEIPT", DateTime),
    Column("KOT_ID", Integer),
    schema="dbo",
)


t_ANALYZER_INTERN = Table(
    "ANALYZER_INTERN",
    metadata,
    Column("ACO_ID", Integer, nullable=False),
    Column("P_ID", Integer, nullable=False),
    Column("SO_NUMBER", Integer),
    Column("ACOT_ID", Integer, nullable=False),
    Column("ST_ID", Integer),
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("ACO_DATE", DateTime),
    Column("ACO_UNITS", DECIMAL(18, 2)),
    Column("ACO_RATE", MONEY),
    Column("NONCLEARABLE", BIT),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Bezeichnung", Unicode(287)),
    Column("Bearbeiter", Unicode(111)),
    Column("Team", Unicode(20)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("Abteilung", Unicode(20)),
    Column("Workingcluster", Unicode(20)),
    Column("Land", Unicode(20)),
    Column("Region", Unicode(20)),
    Column("Jahr", Integer),
    Column("Monat", Integer),
    Column("Woche", Integer),
    Column("Tag", Integer),
    Column("Art", Unicode(16), nullable=False),
    schema="dbo",
)


t_ANALYZER_TEAMS = Table(
    "ANALYZER_TEAMS",
    metadata,
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_SHORT", Unicode(20)),
    Column("HR_TYPE", Unicode(50)),
    Column("HR_PARENT", UNIQUEIDENTIFIER),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("HR_LOCATION", Unicode(40)),
    Column("HR_PREFIX", Unicode(20)),
    Column("HR_ACTIVE", BIT, nullable=False),
    Column("HR_CURRENT", BIT),
    Column("Land", Unicode(20)),
    Column("Region", Unicode(20)),
    Column("Anzahl", BigInteger),
    schema="dbo",
)


t_ANALYZER_TEAMS_ASIA = Table(
    "ANALYZER_TEAMS_ASIA",
    metadata,
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_SHORT", Unicode(20)),
    Column("HR_TYPE", Unicode(50)),
    Column("HR_PARENT", UNIQUEIDENTIFIER),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("HR_LOCATION", Unicode(40)),
    Column("HR_PREFIX", Unicode(20)),
    Column("HR_ACTIVE", BIT, nullable=False),
    Column("HR_CURRENT", BIT),
    Column("Land", Unicode(20)),
    Column("Region", Unicode(20)),
    schema="dbo",
)


t_ANALYZER_TEAMS_DE = Table(
    "ANALYZER_TEAMS_DE",
    metadata,
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_SHORT", Unicode(20)),
    Column("HR_TYPE", Unicode(50)),
    Column("HR_PARENT", UNIQUEIDENTIFIER),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("HR_LOCATION", Unicode(40)),
    Column("HR_PREFIX", Unicode(20)),
    Column("HR_ACTIVE", BIT, nullable=False),
    Column("HR_CURRENT", BIT),
    Column("Region", Unicode(20)),
    schema="dbo",
)


t_ANALYZER_TEAMS_MUC = Table(
    "ANALYZER_TEAMS_MUC",
    metadata,
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_SHORT", Unicode(20)),
    Column("HR_TYPE", Unicode(50)),
    Column("HR_PARENT", UNIQUEIDENTIFIER),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("HR_LOCATION", Unicode(40)),
    Column("HR_PREFIX", Unicode(20)),
    Column("HR_ACTIVE", BIT, nullable=False),
    Column("HR_CURRENT", BIT),
    Column("Land", Unicode(20)),
    schema="dbo",
)


t_ANALYZER_TEAM_REGION = Table(
    "ANALYZER_TEAM_REGION",
    metadata,
    Column("ST_ID", Integer, nullable=False),
    Column("Team", Integer, nullable=False),
    Column("Region", Integer, nullable=False),
    schema="dbo",
)


class ANALYZECAPA(Base):
    __tablename__ = "ANALYZE_CAPA"
    __table_args__ = {"schema": "dbo"}

    ACA_ID = Column(
        Integer,
        primary_key=True,
        doc="This is the doc string that should be written to the documentation.",
    )
    HR_NEW_ID = Column(Integer, index=True)
    ACA_DATE = Column(DateTime)
    ACA_WEEK = Column(Integer, index=True)
    ACA_YEAR = Column(Integer, index=True)
    ACA_HOURS_WEEK = Column(DECIMAL(18, 2), server_default=text("((5))"))


class ANALYZECAPADEFAULT(Base):
    __tablename__ = "ANALYZE_CAPA_DEFAULT"
    __table_args__ = {"schema": "dbo"}

    ACAD_ID = Column(Integer, primary_key=True)
    HR_NEW_ID = Column(Integer, index=True)
    ACAD_HOURS_WEEK = Column(DECIMAL(18, 2), server_default=text("((5))"))


class ANALYZECOMMAND(Base):
    __tablename__ = "ANALYZE_COMMANDS"
    __table_args__ = {"schema": "dbo"}

    AC_ID = Column(Integer, primary_key=True)
    AC_NAME_DE = Column(Unicode(256))
    AC_NAME_EN = Column(Unicode(256))
    AC_COMMAND_NO = Column(Integer)
    AC_IS_HEADER = Column(BIT, nullable=False, server_default=text("((0))"))
    AC_DISABLED_ROLE_0_EUR = Column(
        BIT, nullable=False, server_default=text("((0))")
    )
    AC_DISABLED_ROLE_1_EUR = Column(
        BIT, nullable=False, server_default=text("((0))")
    )
    AC_DISABLED_ROLE_2_EUR = Column(
        BIT, nullable=False, server_default=text("((0))")
    )
    AC_DISABLED_ROLE_3_EUR = Column(
        BIT, nullable=False, server_default=text("((0))")
    )
    AC_DISABLED_ROLE_0_ASIA = Column(
        BIT, nullable=False, server_default=text("((0))")
    )
    AC_DISABLED_ROLE_1_ASIA = Column(
        BIT, nullable=False, server_default=text("((1))")
    )
    AC_DISABLED_ROLE_2_ASIA = Column(
        BIT, nullable=False, server_default=text("((0))")
    )
    AC_DISABLED_ROLE_3_ASIA = Column(
        BIT, nullable=False, server_default=text("((0))")
    )
    AC_ORDER = Column(Integer)


class ANALYZECUSTOMER(Base):
    __tablename__ = "ANALYZE_CUSTOMER"
    __table_args__ = {"schema": "dbo"}

    ACU_ID = Column(Integer, primary_key=True)
    CU_ID = Column(Integer, index=True)
    ACU_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))


class ANALYZEREALTIME(Base):
    __tablename__ = "ANALYZE_REALTIME"
    __table_args__ = {"schema": "dbo"}

    ART_ID = Column(Integer, primary_key=True)
    HR_NEW_ID = Column(Integer)
    ART_DATE = Column(DateTime)
    ART_WEEK = Column(Integer)
    ART_YEAR = Column(Integer)
    ART_HOURS_WEEK = Column(DECIMAL(18, 2))


class ANALYZESTAFF(Base):
    __tablename__ = "ANALYZE_STAFF"
    __table_args__ = {"schema": "dbo"}

    AS_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer, index=True)
    AS_ROLE = Column(Integer, server_default=text("((2))"))
    AS_COUNT = Column(Integer, server_default=text("((0))"))


class ANALYZESTAFFPIPE(Base):
    __tablename__ = "ANALYZE_STAFF_PIPE"
    __table_args__ = {"schema": "dbo"}

    ASP_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer)
    ASP_DETAILS = Column(Unicode(200))
    ASP_DATE_FROM = Column(Date)
    ASP_DATE_TO = Column(Date)


class ANALYZESTAFFREGION(Base):
    __tablename__ = "ANALYZE_STAFF_REGION"
    __table_args__ = {"schema": "dbo"}

    ASR_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer)
    ASR_REGION = Column(Integer)


class ANALYZESTAFFTEAM(Base):
    __tablename__ = "ANALYZE_STAFF_TEAM"
    __table_args__ = {"schema": "dbo"}

    AST_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer, index=True)
    HR_NEW_ID = Column(Integer)


class ANNEXTYPE(Base):
    __tablename__ = "ANNEX_TYPE"
    __table_args__ = {"schema": "dbo"}

    AT_ID = Column(Integer, primary_key=True)
    AT_NAME_DE = Column(Unicode(128))
    AT_NAME_EN = Column(Unicode(128))


class ANONYMISIERUNG(Base):
    __tablename__ = "ANONYMISIERUNG"
    __table_args__ = {"schema": "dbo"}

    AN_ID = Column(Integer, primary_key=True)
    AN_REG = Column(DateTime, server_default=text("(getdate())"))
    AN_REGBY = Column(Integer)


class APPSTYPE(Base):
    __tablename__ = "APPS_TYPE"
    __table_args__ = {"schema": "dbo"}

    APPST_ID = Column(Integer, primary_key=True)
    APPST_NAME = Column(Unicode(50))


class BASE(Base):
    __tablename__ = "BASE"
    __table_args__ = {"schema": "dbo"}

    B_ID = Column(Integer, primary_key=True)
    B_NAME_DE = Column(Unicode(512))
    B_NAME_EN = Column(Unicode(512))
    B_NAME_FR = Column(Unicode(512))
    DI_ID = Column(Integer)
    BT_ID = Column(Integer, index=True)
    PLK_SHORT = Column(Unicode(10))
    B_REG = Column(DateTime)
    B_REGBY = Column(Integer)
    B_UPDATE = Column(DateTime)
    B_UPDATEBY = Column(Integer)
    HRC_ID = Column(Integer, nullable=False, server_default=text("((1))"))
    B_PARENT = Column(Integer, index=True)
    B_SHORT_DE = Column(Unicode(512))
    B_SHORT_EN = Column(Unicode(512))
    B_SHORT_FR = Column(Unicode(512))
    B_DOW = Column(DateTime)
    B_COMMENT_DE = Column(Unicode(512))
    B_COMMENT_EN = Column(Unicode(512))
    B_COMMENT_FR = Column(Unicode(512))
    B_DOA = Column(Integer, nullable=False, server_default=text("((0))"))


class BASETYPE(Base):
    __tablename__ = "BASE_TYPE"
    __table_args__ = {"schema": "dbo"}

    BT_ID = Column(Integer, primary_key=True)
    BT_SHORT = Column(Unicode(6))
    BT_NAME_DE = Column(Unicode(50))
    BT_NAME_EN = Column(Unicode(50))
    BT_NAME_FR = Column(Unicode(50))
    GT_ID = Column(Integer)


t_BIG_DATA_TEST = Table(
    "BIG_DATA_TEST",
    metadata,
    Column("N_ID", Integer, nullable=False),
    Column("N_NAME_DE", Unicode(120)),
    Column("NP_ID", Integer, nullable=False),
    Column("NP_NAME_DE", Unicode(150)),
    Column("DM_ID", Integer),
    Column("DM_NAME", Unicode(255)),
    Column("DI_ID", Integer),
    Column("DI_NAME", Unicode(100)),
    Column("Total", BigInteger),
    Column("Passed", Integer),
    Column("Failed", Integer),
    Column("Fehlerrate", Float(53)),
    Column("Prüfminuten", DECIMAL(18, 2)),
    Column("Level", Unicode(30)),
    Column("InModulen", BigInteger),
    Column("NL_LEVEL", Integer),
    Column("Land", Unicode),
    Column("Produkt", Unicode),
    Column("DI_PRICE_EUR", DECIMAL(18, 2)),
    Column("DMI_NUMBER", Integer),
    schema="dbo",
)


t_BIG_DATA_TEST_COMPLETE = Table(
    "BIG_DATA_TEST_COMPLETE",
    metadata,
    Column("N_ID", Integer, nullable=False),
    Column("N_NAME_DE", Unicode(120)),
    Column("NP_ID", Integer, nullable=False),
    Column("NP_NAME_DE", Unicode(150)),
    Column("DM_ID", Integer),
    Column("DM_NAME", Unicode(255)),
    Column("DI_ID", Integer),
    Column("DI_NAME", Unicode(100)),
    Column("Total", BigInteger),
    Column("Passed", Integer),
    Column("Failed", Integer),
    Column("Fehlerrate", Float(53)),
    Column("Prüfminuten", DECIMAL(18, 2)),
    Column("Level", Unicode(30)),
    Column("InModulen", BigInteger),
    Column("TotalDiesesModul", BigInteger),
    Column("FehlerDiesesModul", Integer),
    Column("FehlerrateDiesesModul", Float(53)),
    Column("NL_LEVEL", Integer),
    Column("Land", Unicode),
    Column("Produkt", Unicode),
    Column("DI_PRICE_EUR", DECIMAL(18, 2)),
    schema="dbo",
)


t_BIG_DATA_TEST_RESULT_MODULE = Table(
    "BIG_DATA_TEST_RESULT_MODULE",
    metadata,
    Column("Total", BigInteger),
    Column("DI_ID", Integer),
    Column("Passed", Integer),
    Column("Failed", Integer),
    Column("DM_ID", Integer),
    schema="dbo",
)


class CLEARINGCHECK(Base):
    __tablename__ = "CLEARING_CHECK"
    __table_args__ = {"schema": "dbo"}

    CLCL_ID = Column(Integer, primary_key=True)
    CLP_ID = Column(Integer, index=True)
    CLCLD_ID = Column(Integer)
    CLCL_ACTIVE = Column(BIT, server_default=text("((1))"))
    CLCL_RESULT_DE = Column(Unicode(800))
    CLCL_RESULT_EN = Column(Unicode(800))
    CLCL_RESULT_FR = Column(Unicode(800))
    ER_ID = Column(Integer, server_default=text("((1))"))
    CLCL_UPDATE = Column(DateTime, server_default=text("(getdate())"))
    CLCL_UPDATE_BY = Column(Integer, server_default=text("((1))"))


class CLEARINGCHECKDEFAULT(Base):
    __tablename__ = "CLEARING_CHECK_DEFAULT"
    __table_args__ = {"schema": "dbo"}

    CLCLD_ID = Column(Integer, primary_key=True)
    CLCLD_REQUIREMENT_DE = Column(Unicode(500))
    CLCLD_REQUIREMENT_EN = Column(Unicode(500))
    CLCLD_REQUIREMENT_FR = Column(Unicode(500))
    CLCLD_NUMBER = Column(Integer)
    CLCLD_IS_HEADER = Column(BIT, server_default=text("((0))"))
    CLCLD_ACTIVE = Column(BIT, server_default=text("((1))"))


class CLEARPAS(Base):
    __tablename__ = "CLEARPASS"
    __table_args__ = {"schema": "dbo"}

    CLP_ID = Column(Integer, primary_key=True)
    C_ID = Column(Integer)
    P_ID = Column(Integer)
    CLP_REG = Column(DateTime, server_default=text("(getdate())"))
    CLP_REGBY = Column(Integer, server_default=text("((1))"))
    CLP_DELETED = Column(BIT, nullable=False, server_default=text("((0))"))


class CLEARPASSACTION(Base):
    __tablename__ = "CLEARPASS_ACTION"
    __table_args__ = {"schema": "dbo"}

    CLPA_ID = Column(Integer, primary_key=True)
    CLP_ID = Column(Integer)
    CLPA_REG = Column(DateTime, server_default=text("(getdate())"))
    CLPA_REGBY = Column(Integer, server_default=text("((1))"))


class COMPARISON(Base):
    __tablename__ = "COMPARISON"
    __table_args__ = {"schema": "dbo"}

    COM_ID = Column(Integer, primary_key=True)
    COM_NAME_DE = Column(Unicode(120), index=True)
    COM_NAME_EN = Column(Unicode(120))
    COM_COMMENT = Column(Unicode(500))
    COM_REG = Column(DateTime)
    COM_REGBY = Column(Integer)
    COM_UPDATE = Column(DateTime)
    COM_UPDATEBY = Column(Integer)


class COMPARISONELEMENT(Base):
    __tablename__ = "COMPARISON_ELEMENTS"
    __table_args__ = {"schema": "dbo"}

    COME_ID = Column(Integer, primary_key=True)
    COM_ID = Column(Integer)
    COME_NUMBER = Column(Integer)
    COME_TEXT_DE = Column(Unicode(500))
    COME_TEXT_EN = Column(Unicode(500))
    COME_TEXT_FR = Column(Unicode(500))


class CONFIG(Base):
    __tablename__ = "CONFIG"
    __table_args__ = {"schema": "dbo"}

    C_ID = Column(Integer, primary_key=True)
    P_ID = Column(Integer, index=True)
    E_ID = Column(Integer, index=True)
    CD_ID = Column(Integer)
    C_NAME_DE = Column(Unicode(120), index=True)
    C_NAME_EN = Column(Unicode(120))
    C_NAME_FR = Column(Unicode(120))
    BEGR_ID = Column(Integer, index=True)
    C_COMMENT = Column(Unicode(500))
    C_DATE_START = Column(DateTime)
    C_DATE_END = Column(DateTime)
    C_MASTER = Column(BIT, index=True)
    C_REG = Column(DateTime)
    C_REGBY = Column(Integer)
    C_UPDATE = Column(DateTime)
    C_UPDATEBY = Column(Integer)
    SC_ID = Column(
        Unicode(50), nullable=False, server_default=text("(N'000.000')")
    )
    ZM_OBJECT = Column(Unicode(5), server_default=text("((400))"))
    KOT_ID = Column(Integer, nullable=False, server_default=text("((24))"))
    CLP_ID = Column(Integer)
    HR_NEW_ID = Column(
        Integer, nullable=False, server_default=text("((101010100))")
    )
    HRC_ID = Column(Integer, nullable=False, server_default=text("((1))"))
    HRP_ID = Column(Integer, nullable=False, server_default=text("((1))"))


class CONFIGBASE(Base):
    __tablename__ = "CONFIG_BASE"
    __table_args__ = {"schema": "dbo"}

    CB_ID = Column(Integer, primary_key=True)
    C_ID = Column(Integer, index=True)
    B_ID = Column(Integer, index=True)
    CB_CONDITION = Column(Unicode(800))
    CB_MODULE_CALCULATION = Column(Integer, index=True)
    CB_MODULE_TEST = Column(Integer)
    CB_COMMENT = Column(Unicode(500))
    CT_ID = Column(Integer, index=True)
    CB_DISPO_MODULE = Column(BIT, nullable=False, server_default=text("((1))"))


class CONFIGBASECALC(Base):
    __tablename__ = "CONFIG_BASE_CALC"
    __table_args__ = {"schema": "dbo"}

    CBC_ID = Column(Integer, primary_key=True)
    C_ID = Column(Integer, index=True)
    CB_ID = Column(Integer, index=True)
    CBC_TIME_HOURS = Column(Float(53))
    CBC_TIME_DAYS = Column(Float(53))
    CBC_DELTA_START = Column(Float(53))
    CBC_COSTS = Column(DECIMAL(18, 2), server_default=text("((0))"))
    CBC_TASK = Column(Unicode(500))
    CBC_COMMENT = Column(Unicode(500))
    CBC_RATE = Column(DECIMAL(18, 2))
    CBC_PRICE = Column(DECIMAL(18, 2), server_default=text("((1))"))
    CBC_FACTOR = Column(Float(53), server_default=text("((1))"))
    WST_ID = Column(Integer)
    SO_NUMBER = Column(Integer)
    DMC_ID = Column(Integer)
    CBC_TRAVEL = Column(DECIMAL(18, 2), server_default=text("((0))"))
    GP_POSITION = Column(Integer, server_default=text("((1000))"))
    PP_ID = Column(Integer)
    ZM_ID = Column(Unicode(50))
    TEMP_NO_MATERIAL = Column(
        BIT, nullable=False, server_default=text("((0))")
    )
    ST_ID = Column(Integer, nullable=False, server_default=text("((1))"))


class CONFIGBASEGOAL(Base):
    __tablename__ = "CONFIG_BASE_GOAL"
    __table_args__ = {"schema": "dbo"}

    CBG_ID = Column(Integer, primary_key=True)
    C_ID = Column(Integer, index=True)
    CB_ID = Column(Integer, index=True)
    G_ID = Column(Integer)


class CONFIGBASELINE(Base):
    __tablename__ = "CONFIG_BASE_LINE"
    __table_args__ = {"schema": "dbo"}

    CBL_ID = Column(Integer, primary_key=True)
    CB_ID = Column(Integer, index=True)
    C_ID = Column(Integer, index=True)
    DI_ID = Column(Integer)
    WST_ID = Column(Integer)
    CBL_ORDER = Column(Integer)


class CONFIGBASEPROOF(Base):
    __tablename__ = "CONFIG_BASE_PROOF"
    __table_args__ = {"schema": "dbo"}

    CBP_ID = Column(Integer, primary_key=True)
    C_ID = Column(Integer, index=True)
    CB_ID = Column(Integer, index=True)
    CBP_SHORT = Column(Unicode(20))
    CPB_TEXT_DE = Column(Unicode(1000))
    CPB_TEXT_EN = Column(Unicode(1000))
    CPB_TEXT_FR = Column(Unicode(1000))
    TOP_ID = Column(Integer, server_default=text("((1))"))


class CONFIGBASETEST(Base):
    __tablename__ = "CONFIG_BASE_TEST"
    __table_args__ = {"schema": "dbo"}

    CBT_ID = Column(Integer, primary_key=True)
    C_ID = Column(Integer, index=True)
    CB_ID = Column(Integer, index=True)
    CBT_SHORT = Column(Unicode(20))
    CPT_TEXT_DE = Column(Unicode(1000))
    CPT_TEXT_EN = Column(Unicode(1000))
    CPT_TEXT_FR = Column(Unicode(1000))
    TOT_ID = Column(Integer, server_default=text("((1))"))


class CONFIGGOAL(Base):
    __tablename__ = "CONFIG_GOAL"
    __table_args__ = {"schema": "dbo"}

    CG_ID = Column(Integer, primary_key=True)
    C_ID = Column(Integer, index=True)
    G_ID = Column(Integer, index=True)
    CG_COMMENT = Column(Unicode(500))
    CG_NUMBER = Column(Integer)


class CONFIGPACKAGE(Base):
    __tablename__ = "CONFIG_PACKAGE"
    __table_args__ = {"schema": "dbo"}

    CP_ID = Column(Integer, primary_key=True, index=True)
    C_ID = Column(Integer, index=True)
    CP_ORDER = Column(Integer, server_default=text("((1))"))
    CP_NAME_DE = Column(Unicode(150))
    CP_NAME_EN = Column(Unicode(150))
    CP_NAME_FR = Column(Unicode(150))
    CP_COMMENT = Column(Unicode(800))
    CP_PRICE = Column(DECIMAL(18, 2), server_default=text("((0))"))
    CP_REG = Column(DateTime, server_default=text("(getutcdate())"))
    CP_REGBY = Column(Integer, server_default=text("((1))"))
    CP_UPDATE = Column(DateTime)
    CP_UPDATEBY = Column(Integer)
    CP_STATUS = Column(Integer, nullable=False, server_default=text("((0))"))
    CP_CLEARDATE = Column(DateTime)
    CP_CLEARBY = Column(Integer)
    CP_LICENCE = Column(
        DECIMAL(18, 2), nullable=False, server_default=text("((0))")
    )
    ZM_PRODUCT = Column(Unicode(5), server_default=text("(N'S18')"))
    PT_ID = Column(
        Integer, nullable=False, index=True, server_default=text("((1))")
    )
    CP_TESTSAMPLES = Column(
        Integer, nullable=False, server_default=text("((0))")
    )
    CP_IS_TEMPLATE = Column(BIT, nullable=False, server_default=text("((0))"))
    CP_TEMPLATE_ID = Column(Integer)


class CONFIGPACKAGEELEMENT(Base):
    __tablename__ = "CONFIG_PACKAGE_ELEMENTS"
    __table_args__ = {"schema": "dbo"}

    CPE_ID = Column(Integer, primary_key=True, index=True)
    CP_ID = Column(Integer, index=True)
    C_ID = Column(Integer)
    G_ID = Column(Integer, index=True)


class CONFIGPACKAGESERVICELEVEL(Base):
    __tablename__ = "CONFIG_PACKAGE_SERVICELEVEL"
    __table_args__ = {"schema": "dbo"}

    CPSL_ID = Column(Integer, primary_key=True)
    SL_ID = Column(Integer)
    CP_ID = Column(Integer, index=True)


class CONFIGSPECIALITEM(Base):
    __tablename__ = "CONFIG_SPECIALITEMS"
    __table_args__ = {"schema": "dbo"}

    CSPI_ID = Column(Integer, primary_key=True)
    CSPI_HEADER_PROOF = Column(Integer)
    CSPI_HEADER_TEST = Column(Integer)
    CSPI_HEADER_GOAL = Column(Integer)
    CSPI_HEADER_PRODUCT = Column(Integer)


class CUSTOMLIST(Base):
    __tablename__ = "CUSTOM_LIST"
    __table_args__ = {"schema": "dbo"}

    CUL_ID = Column(Integer, primary_key=True)
    CUL_NAME_DE = Column(Unicode(256))
    CUL_NAME_EN = Column(Unicode(256))
    CUL_REG = Column(DateTime, server_default=text("(getdate())"))
    CUL_REGBY = Column(Integer)
    CUL_UPDATE = Column(DateTime)
    CUL_UPDATEBY = Column(Integer)


class CUSTOMLISTELEMENT(Base):
    __tablename__ = "CUSTOM_LIST_ELEMENT"
    __table_args__ = {"schema": "dbo"}

    CULE_ID = Column(Integer, primary_key=True)
    CUL_ID = Column(Integer)
    CULE_NAME_DE = Column(Unicode(512))
    CULE_NAME_EN = Column(Unicode(512))
    CULE_INDENT = Column(Integer)
    CULE_ORDER = Column(Integer)
    CULE_REG = Column(DateTime, server_default=text("(getdate())"))
    CULE_REGBY = Column(Integer)
    CULE_UPDATE = Column(DateTime)
    CULE_UPDATEBY = Column(Integer)
    CULE_STYLE = Column(Integer, nullable=False, server_default=text("((0))"))
    CULE_TESTBASE = Column(
        Integer, nullable=False, server_default=text("((0))")
    )
    CULE_MODULBASE = Column(
        Integer, nullable=False, server_default=text("((0))")
    )
    CULE_DEF_COMMENT_DE = Column(Unicode(2048))
    CULE_DEF_COMMENT_EN = Column(Unicode(2048))
    DI_ID = Column(Integer)
    CULE_MARKETABILITY = Column(
        BIT, nullable=False, server_default=text("((0))")
    )
    CULE_NUMBER = Column(Unicode(10))
    CULE_ID_MAP_LIDL = Column(Integer)


t_DEADLINE_ACTION = Table(
    "DEADLINE_ACTION",
    metadata,
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("P_PRODUCT", Unicode(255)),
    Column("P_MODEL", Unicode(255)),
    Column("Termin", Unicode(30)),
    Column("Vortermin", Unicode(30)),
    Column("ACT_INFO", Unicode(512)),
    Column("Projektmanager", Unicode(111)),
    Column("Bearbeiter", Unicode(111)),
    Column("ACT_DATE", DateTime),
    Column("ACT_PREDATE", DateTime),
    Column("P_PROJECTMANAGER", Integer),
    Column("ST_ID", Integer),
    Column("PROJECTMANAGER_TEAM", Integer, nullable=False),
    Column("BEARBEITER_TEAM", Integer),
    schema="dbo",
)


t_DEADLINE_ACTION_FINISHED = Table(
    "DEADLINE_ACTION_FINISHED",
    metadata,
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("P_PRODUCT", Unicode(255)),
    Column("P_MODEL", Unicode(255)),
    Column("Termin", Unicode(30)),
    Column("Vortermin", Unicode(30)),
    Column("ACT_INFO", Unicode(512)),
    Column("Projektmanager", Unicode(111)),
    Column("Bearbeiter", Unicode(111)),
    Column("ACT_DATE", DateTime),
    Column("ACT_PREDATE", DateTime),
    Column("P_PROJECTMANAGER", Integer),
    Column("ST_ID", Integer),
    Column("PROJECTMANAGER_TEAM", Integer, nullable=False),
    Column("BEARBEITER_TEAM", Integer),
    Column("ACT_READY", SMALLDATETIME),
    Column("ACT_PREDATEINFO", Unicode(255)),
    schema="dbo",
)


t_DEADLINE_PROJECT = Table(
    "DEADLINE_PROJECT",
    metadata,
    Column("P_ID", Integer),
    Column("P_PRODUCT", Unicode(255)),
    Column("P_MODEL", Unicode(255)),
    Column("Termin", Unicode(30)),
    Column("Vortermin", Unicode(30)),
    Column("P_ORDERTEXT", Unicode(2048)),
    Column("Projektmanager", Unicode(111)),
    Column("Bearbeiter", Unicode(111)),
    Column("AVIS", Unicode(69)),
    Column("P_DEADLINE", DateTime),
    Column("P_PREDATE", DateTime),
    Column("P_STATUS", Integer),
    Column("P_PROJECTMANAGER", Integer),
    Column("P_HANDLEDBY", Integer),
    Column("P_PROJECTMANAGER_TEAM", Integer),
    Column("P_HANDLEDBY_TEAM", Integer),
    Column("P_TS_RECEIPT_ADVISED", BIT),
    Column("PROJECTMANAGER_TEAM", Integer, nullable=False),
    Column("BEARBEITER_TEAM", Integer),
    Column("P_EXPECTED_TS_RECEIPT", DateTime),
    Column("P_PROJECTINFO", Unicode(4000)),
    schema="dbo",
)


t_DEADLINE_SUBORDERS = Table(
    "DEADLINE_SUBORDERS",
    metadata,
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("P_PRODUCT", Unicode(255)),
    Column("P_MODEL", Unicode(255)),
    Column("Termin", Unicode(30)),
    Column("Vortermin", Unicode(30)),
    Column("SO_TASK", Unicode(512)),
    Column("Projektmanager", Unicode(111)),
    Column("Bearbeiter", Unicode(111)),
    Column("SO_DEADLINE", DateTime),
    Column("SO_PREDATE", DateTime),
    Column("P_STATUS", Integer),
    Column("P_PROJECTMANAGER", Integer),
    Column("ST_ID", Integer),
    Column("PROJECTMANAGER_TEAM", Integer, nullable=False),
    Column("BEARBEITER_TEAM", Integer),
    Column("SO_DISABLED", BIT),
    Column("SO_COMMENT", Unicode(2000)),
    schema="dbo",
)


t_DEADLINE_TASK = Table(
    "DEADLINE_TASK",
    metadata,
    Column("P_ALIAS", Unicode(6), nullable=False),
    Column("SO_ALIAS", String(1, "Latin1_General_CI_AS"), nullable=False),
    Column("TA_REL_ID", Integer),
    Column("NAME_DE", Unicode(255)),
    Column("NAME_EN", Unicode(255)),
    Column("TA_DEADLINE", Date),
    Column("TA_DATE", DateTime),
    Column("TA_TEXT_EN", Unicode(2048)),
    Column("ERSTELLER", Unicode(117)),
    Column("BEARBEITER", Unicode(115)),
    Column("TA_FROM", Integer),
    Column("TA_TO", Integer),
    Column("TA_TYPE", Integer, nullable=False),
    Column("BEARBEITER_TEAM", Integer, nullable=False),
    Column("ERSTELLER_TEAM", Integer, nullable=False),
    Column("TA_COMMENT", Unicode(2048)),
    Column("TA_READY", DateTime),
    schema="dbo",
)


class DEFAULTITEMCALC(Base):
    __tablename__ = "DEFAULT_ITEM_CALC"
    __table_args__ = {"schema": "dbo"}

    DICA_ID = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, index=True)
    DICA_PRICE = Column(MONEY)
    PL_ID = Column(Integer)
    DICA_REG = Column(DateTime, server_default=text("(getdate())"))
    DICA_REGBY = Column(Integer, server_default=text("((1))"))
    DICA_UPDATE = Column(DateTime)
    DICA_UPDATEBY = Column(Integer)


class DEFAULTITEMCLEARING(Base):
    __tablename__ = "DEFAULT_ITEM_CLEARING"
    __table_args__ = {"schema": "dbo"}

    DIC_ID = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, index=True)
    DI_VERSION = Column(Integer)
    CL_ID = Column(Integer)
    ST_ID = Column(Integer)
    DIC_DATE = Column(DateTime)


class DEFAULTITEMCOMPARISON(Base):
    __tablename__ = "DEFAULT_ITEM_COMPARISON"
    __table_args__ = {"schema": "dbo"}

    DICO_ID = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, index=True)
    DICO_ORDER = Column(Integer)
    DICO_TEXT_DE = Column(Unicode(500))
    DICO_TEXT_EN = Column(Unicode(500))
    DICO_TEXT_FR = Column(Unicode(500))
    DICO_REG = Column(DateTime)
    DICO_REGBY = Column(Integer)
    DICO_UPDATE = Column(DateTime)
    DICO_UPDATEBY = Column(Integer)
    DIT_ID = Column(Integer)


class DEFAULTITEMCRITERION(Base):
    __tablename__ = "DEFAULT_ITEM_CRITERIA"
    __table_args__ = {"schema": "dbo"}

    DICR_ID = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, index=True)
    DICR_NUMBER = Column(Integer)
    DICR_CASE = Column(Unicode(2000))
    DICR_RESULT_DEFAULT = Column(Unicode(50))
    DICR_RESULT_NUL = Column(Unicode(50))
    DICR_RESULT_PRO = Column(Unicode(50))
    DICR_RESULT_SER = Column(Unicode(50))
    DICR_COMMENT = Column(Unicode(1000))
    DICR_STATUS = Column(Unicode(120))
    DICR_REG = Column(DateTime)
    DICR_REGBY = Column(Integer)
    DICR_UPDATE = Column(DateTime)
    DICR_UPDATEBY = Column(Integer)


class DEFAULTITEMLINK(Base):
    __tablename__ = "DEFAULT_ITEM_LINK"
    __table_args__ = {"schema": "dbo"}

    DIL_ID = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, index=True)
    DIL_TEXT_DE = Column(Unicode(1024))
    DIL_TEXT_EN = Column(Unicode(1024))
    DIL_TEXT_FR = Column(Unicode(1024))
    DIL_URL = Column(Unicode(512))
    DIL_UPDATE = Column(DateTime, server_default=text("(getdate())"))
    DIL_UPDATEBY = Column(Integer)


class DEFAULTITEMTABLE(Base):
    __tablename__ = "DEFAULT_ITEM_TABLE"
    __table_args__ = {"schema": "dbo"}

    DIT_ID = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, index=True)
    DIT_NUMBER = Column(Integer)
    DIT_NAME_DE = Column(Unicode(255))
    DIT_NAME_EN = Column(Unicode(255))
    DIT_NAME_FR = Column(Unicode(255))
    DIT_LIMIT = Column(Unicode(255))
    DIT_REG = Column(DateTime, server_default=text("(getdate())"))
    DIT_REGBY = Column(Integer)
    DIT_UPDATE = Column(DateTime)
    DIT_UPDATEBY = Column(Integer)


class DEFAULTITEMTESTLEVEL(Base):
    __tablename__ = "DEFAULT_ITEM_TESTLEVEL"
    __table_args__ = {"schema": "dbo"}

    DITL_ID = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, index=True)
    TLEV_ID = Column(Integer)


class DEFAULTMODULANNEX(Base):
    __tablename__ = "DEFAULT_MODUL_ANNEX"
    __table_args__ = {"schema": "dbo"}

    DMAX_ID = Column(Integer, primary_key=True)
    DM_ID = Column(Integer)
    DMAX_NAME_DE = Column(Unicode(500))
    DMAX_NAME_EN = Column(Unicode(500))
    DMAX_NAME_FR = Column(Unicode(500))
    DMAX_FILENAME = Column(Unicode(255))
    DMAX_CHECKSUM = Column(Unicode(32))
    DMAX_DATA = Column(LargeBinary)
    AT_ID = Column(Integer, nullable=False, server_default=text("((1))"))
    DI_ID = Column(Integer)


class DEFAULTMODULLINK(Base):
    __tablename__ = "DEFAULT_MODUL_LINK"
    __table_args__ = {"schema": "dbo"}

    DML_ID = Column(Integer, primary_key=True)
    DM_ID = Column(Integer, index=True)
    DML_TEXT_DE = Column(Unicode(1024))
    DML_TEXT_EN = Column(Unicode(1024))
    DML_TEXT_FR = Column(Unicode(1024))
    DML_URL = Column(Unicode(512))
    DML_UPDATE = Column(DateTime, server_default=text("(getdate())"))
    DML_UPDATEBY = Column(Integer)


class DEFAULTMODULUPDATE(Base):
    __tablename__ = "DEFAULT_MODUL_UPDATE"
    __table_args__ = {"schema": "dbo"}

    DMU_ID = Column(Integer, primary_key=True)
    DM_ID = Column(Integer, index=True)
    DMU_UPDATE = Column(
        DateTime, nullable=False, server_default=text("(getdate())")
    )
    DMU_UPDATEBY = Column(Integer, index=True)


class EDOC(Base):
    __tablename__ = "EDOC"
    __table_args__ = {"schema": "dbo"}

    E_ID = Column(Integer, primary_key=True)
    E_VERSION = Column(Integer)
    E_NAME = Column(Unicode(255), index=True)
    HEAD_ID = Column(Integer, server_default=text("(6)"))
    E_YN_SYMBOL = Column(BIT, server_default=text("((1))"))
    E_REG = Column(DateTime)
    E_REGBY = Column(Integer)
    E_UPDATE = Column(DateTime)
    E_UPDATEBY = Column(Integer)
    E_REMINDER = Column(Integer)
    NP_ID = Column(Integer)
    E_ANNEX = Column(Unicode(4000))
    E_TABLE = Column(Unicode(4000))


class EDOCOFFICECOUNT(Base):
    __tablename__ = "EDOCOFFICE_COUNT"
    __table_args__ = {"schema": "dbo"}

    EOFF_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer, index=True)
    EOFF_REG = Column(DateTime, server_default=text("(getutcdate())"))


class EDOCRESULT(Base):
    __tablename__ = "EDOCRESULT"
    __table_args__ = {"schema": "dbo"}

    ER_ID = Column(Integer, primary_key=True)
    ER_NAME_DE = Column(Unicode(50))
    ER_NAME_EN = Column(Unicode(50))
    ER_NAME_FR = Column(Unicode(50))
    ER_SYMBOL_1 = Column(Unicode(5))
    ER_SYMBOL_2 = Column(Unicode(5))
    ER_IS_NUMERIC = Column(BIT)
    ER_VALUE = Column(DECIMAL(18, 2))
    ER_TOOLTIP_DE = Column(Unicode(255))
    ER_TOOLTIP_EN = Column(Unicode(255))
    ER_TOOLTIP_FR = Column(Unicode(255))
    ER_DESCRIPTION_DE = Column(Unicode(255))
    ER_DESCRIPTION_EN = Column(Unicode(255))
    ER_DESCRIPTION_FR = Column(Unicode(255))
    ER_IS_MODULRESULT = Column(Integer)
    ER_REG = Column(DateTime)
    ER_REGBY = Column(Integer)
    ER_UPDATE = Column(DateTime)
    ER_UPDATEBY = Column(Integer)
    ER_SHOW_IN_PROOF = Column(BIT, server_default=text("((0))"))
    ER_VALUE_YN = Column(Integer, server_default=text("((0))"))


class EDOCUSER(Base):
    __tablename__ = "EDOCUSER"
    __table_args__ = {"schema": "dbo"}

    EU_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer, index=True)
    ERO_ID = Column(Integer)
    EU_REG = Column(DateTime, server_default=text("(getdate())"))
    EU_REGBY = Column(Integer, server_default=text("((1))"))
    EU_UPDATE = Column(DateTime)
    EU_UPDATEBY = Column(Integer)
    EU_SHOW_USERSTATUS = Column(
        BIT, nullable=False, server_default=text("((0))")
    )


class EDOCUSERROLE(Base):
    __tablename__ = "EDOCUSERROLE"
    __table_args__ = {"schema": "dbo"}

    ERO_ID = Column(Integer, primary_key=True)
    ERO_NAME_DE = Column(Unicode(50))
    ERO_NAME_EN = Column(Unicode(50))
    ERO_TEXT_DE = Column(Unicode(1000))
    ERO_TEXT_EN = Column(Unicode(1000))
    ERO_LEVEL = Column(Integer)


class EDOCCOUNT(Base):
    __tablename__ = "EDOC_COUNT"
    __table_args__ = {"schema": "dbo"}

    EC_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer, index=True)
    EC_COUNT = Column(Integer)


class EDOCITEMSTATISTIC(Base):
    __tablename__ = "EDOC_ITEM_STATISTIC"
    __table_args__ = {"schema": "dbo"}

    EIS_ID = Column(Integer, primary_key=True)
    E_ID = Column(Integer, index=True)
    DM_ID = Column(Integer, index=True)
    DI_ID = Column(Integer, index=True)
    PRP_ID = Column(Integer)
    EMI_ID = Column(Integer, index=True)
    HRP_ID = Column(Integer, index=True)
    EIS_VALUE = Column(Numeric(28, 8))
    EIS_REG = Column(DateTime, server_default=text("(getdate())"))
    EIS_REGBY = Column(Integer)
    EIS_UPDATE = Column(DateTime)
    EIS_UPDATEBY = Column(Integer)


class EDOCMODUL(Base):
    __tablename__ = "EDOC_MODUL"
    __table_args__ = {"schema": "dbo"}

    EM_ID = Column(Integer, primary_key=True)
    E_ID = Column(Integer, index=True)
    DM_ID = Column(Integer, index=True)
    DM_VERSION = Column(Integer)
    EM_NAME = Column(Unicode(255))
    EM_LETTER = Column(Unicode(10))
    EM_NUMBER = Column(Integer)
    SO_NUMBER = Column(Integer)
    EM_OFFLINE_BY = Column(Integer)
    EM_OFFLINE_SINCE = Column(DateTime)
    EM_REG = Column(DateTime, server_default=text("(getdate())"))
    EM_REGBY = Column(Integer)
    EM_UPDATE = Column(DateTime)
    EM_UPDATEBY = Column(Integer)
    EM_FILTER_LEVEL = Column(Unicode(100))
    EM_FILTER_PARAM = Column(Unicode(512))
    EM_FILTER_ITEMS = Column(Unicode(2048))


class EDOCMODULDELETED(Base):
    __tablename__ = "EDOC_MODUL_DELETED"
    __table_args__ = {"schema": "dbo"}

    EMD_ID = Column(Integer, primary_key=True)
    E_ID = Column(Integer)
    DM_ID = Column(Integer)
    EMD_NAME = Column(Unicode(255))
    EMD_DELETED = Column(
        DateTime, nullable=False, server_default=text("(getdate())")
    )
    EM_DELETED_BY = Column(Integer)


class EDOCMODULITEM(Base):
    __tablename__ = "EDOC_MODUL_ITEM"
    __table_args__ = {"schema": "dbo"}

    EMI_ID = Column(Integer, primary_key=True)
    EMI_VERSION = Column(Integer)
    EMI_NUMBER = Column(Integer)
    E_ID = Column(Integer, index=True)
    EM_ID = Column(Integer, index=True)
    DM_ID = Column(Integer)
    DI_ID = Column(Integer, index=True)
    DI_VERSION = Column(Integer)
    EMI_REQUIREMENT_DE = Column(Unicode(1500))
    EMI_REQUIREMENT_EN = Column(Unicode(1500))
    EMI_REQUIREMENT_FR = Column(Unicode(1500))
    EMI_INDENT = Column(Integer)
    WST_ID = Column(Integer)
    EMI_NORM = Column(Unicode(80))
    PSI_ID = Column(Integer)
    EMI_TIME = Column(DECIMAL(18, 0))
    EMI_COST = Column(DECIMAL(18, 2))
    EMI_TIME_MIN = Column(DECIMAL(18, 2))
    TPER_ID = Column(Integer)
    EMI_KENNWERT = Column(Unicode(60))
    EMI_TITLE = Column(BIT)
    EMI_KEYNOTE = Column(BIT)
    EMI_MEASURE = Column(BIT)
    EMI_ADD = Column(BIT)
    EMI_REG = Column(DateTime)
    EMI_REGBY = Column(Integer)
    EMI_UPDATE = Column(DateTime)
    EMI_UPDATEBY = Column(Integer)
    EMI_MAINFEATURE = Column(BIT, server_default=text("((0))"))
    ST_ID = Column(Integer, nullable=False, server_default=text("((1))"))
    NL_ID = Column(Integer, nullable=False, server_default=text("((1))"))


class EDOCMODULITEMCOMPARISON(Base):
    __tablename__ = "EDOC_MODUL_ITEM_COMPARISON"
    __table_args__ = {"schema": "dbo"}

    EMIC_ID = Column(Integer, primary_key=True)
    EMI_ID = Column(Integer, index=True)
    EM_ID = Column(Integer, index=True)
    EMIC_ORDER = Column(Integer, server_default=text("(1)"))
    EMIC_TEXT_DE = Column(Unicode(500))
    EMIC_TEXT_EN = Column(Unicode(500))
    EMIC_TEXT_FR = Column(Unicode(500))
    EMIC_REG = Column(DateTime)
    EMIC_REGBY = Column(Integer)
    EMIC_UPDATE = Column(DateTime)
    EMIC_UPDATEBY = Column(Integer)


class EDOCMODULITEMCOMPARISONPHASE(Base):
    __tablename__ = "EDOC_MODUL_ITEM_COMPARISON_PHASE"
    __table_args__ = {"schema": "dbo"}

    EMICP_ID = Column(Integer, primary_key=True)
    EMIC_ID = Column(Integer, index=True)
    EMI_ID = Column(Integer, index=True)
    PRP_ID = Column(Integer)
    EMICP_TEXT_DE = Column(Unicode(500))
    EMICP_TEXT_EN = Column(Unicode(500))
    EMICP_TEXT_FR = Column(Unicode(500))
    ER_ID = Column(Integer, server_default=text("(1)"))
    ER_UPDATE = Column(DateTime)
    ER_UPDATEBY = Column(Integer)


class EDOCMODULITEMPHASE(Base):
    __tablename__ = "EDOC_MODUL_ITEM_PHASE"
    __table_args__ = {"schema": "dbo"}

    EMIP_ID = Column(Integer, primary_key=True)
    EM_ID = Column(Integer, index=True)
    EMI_ID = Column(Integer, index=True)
    PRP_ID = Column(Integer, index=True)
    EMIP_RESULT_DE = Column(Unicode(2048))
    EMIP_RESULT_EN = Column(Unicode(2048))
    EMIP_RESULT_FR = Column(Unicode(2048))
    EMIP_COMMENT = Column(Unicode(500))
    EMIP_READY = Column(BIT)
    ER_ID = Column(Integer, index=True)
    EMIP_HANDLEDBY = Column(Integer, server_default=text("((1))"))
    EMIP_HINT = Column(BIT)
    EMIP_REG = Column(DateTime)
    EMIP_REGBY = Column(Integer)
    EMIP_UPDATE = Column(DateTime)
    EMIP_UPDATEBY = Column(Integer)
    WST_ID = Column(Integer, server_default=text("((1))"))
    SO_NUMBER = Column(Integer)
    ST_ID = Column(Integer, nullable=False, server_default=text("((1))"))
    EMIP_IS_COPY = Column(BIT, nullable=False, server_default=text("((0))"))


class EDOCMODULITEMPHASEANNEX(Base):
    __tablename__ = "EDOC_MODUL_ITEM_PHASE_ANNEX"
    __table_args__ = {"schema": "dbo"}

    EMIPA_ID = Column(Integer, primary_key=True)
    EMIP_ID = Column(Integer, index=True)
    EMIPA_NAME_DE = Column(Unicode(500))
    EMIPA_NAME_EN = Column(Unicode(500))
    EMIPA_NAME_FR = Column(Unicode(500))
    EMIPA_FILENAME = Column(Unicode(255))
    EMIPA_CHECKSUM = Column(Unicode(32))
    EMIPA_DATA = Column(IMAGE)
    EMIPA_UPLOAD = Column(DateTime)
    EMIPA_UPLOAD_BY = Column(Integer)


class EDOCMODULITEMPHASEPICTURE(Base):
    __tablename__ = "EDOC_MODUL_ITEM_PHASE_PICTURE"
    __table_args__ = {"schema": "dbo"}

    EMIPP_ID = Column(Integer, primary_key=True)
    EMIP_ID = Column(Integer, index=True)
    EMIPP_NUMBER = Column(Integer)
    EMIPP_TEXT_DE = Column(Unicode(500))
    EMIPP_TEXT_EN = Column(Unicode(500))
    EMIPP_TEXT_FR = Column(Unicode(500))
    EMIPP_FILENAME = Column(Unicode(255))
    EMIPP_CHECKSUM = Column(Unicode(32))
    EMIPP_WIDTH = Column(Integer)
    EMIPP_HEIGHT = Column(Integer)
    EMIPP_DATA = Column(IMAGE)


class EDOCMODULITEMPHASESTORIX(Base):
    __tablename__ = "EDOC_MODUL_ITEM_PHASE_STORIX"
    __table_args__ = {"schema": "dbo"}

    EMIPS_ID = Column(Integer, primary_key=True)
    EMIP_ID = Column(Integer, index=True)
    LG_ID = Column(Integer)
    LGEL_NR = Column(Integer)


class EDOCMODULITEMPHASETABLE(Base):
    __tablename__ = "EDOC_MODUL_ITEM_PHASE_TABLE"
    __table_args__ = {"schema": "dbo"}

    EMIPT_ID = Column(Integer, primary_key=True)
    EMIP_ID = Column(Integer, index=True)
    EMIPT_NUMBER = Column(Integer)
    EMIPT_NAME_DE = Column(Unicode(255))
    EMIPT_NAME_EN = Column(Unicode(255))
    EMIPT_NAME_FR = Column(Unicode(255))
    EMIPT_VALUE = Column(Unicode(255))
    EMIPT_LIMIT = Column(Unicode(255))
    DIT_ID = Column(Integer)


class EDOCMODULITEMPICTURE(Base):
    __tablename__ = "EDOC_MODUL_ITEM_PICTURE"
    __table_args__ = {"schema": "dbo"}

    EMIPC_ID = Column(Integer, primary_key=True)
    EMI_ID = Column(Integer, index=True)
    EM_ID = Column(Integer, index=True)
    EMIPC_NUMBER = Column(Integer)
    EMIPC_TEXT_DE = Column(Unicode(500))
    EMIPC_TEXT_EN = Column(Unicode(500))
    EMIPC_TEXT_FR = Column(Unicode(500))
    EMIPC_FILENAME = Column(Unicode(255))
    EMIPC_CHECKSUM = Column(Unicode(32))
    EMIPC_WIDTH = Column(Integer)
    EMIPC_HEIGHT = Column(Integer)
    EMIPC_DATA = Column(IMAGE)


class EDOCMODULPHASE(Base):
    __tablename__ = "EDOC_MODUL_PHASE"
    __table_args__ = {"schema": "dbo"}

    EMP_ID = Column(Integer, primary_key=True)
    E_ID = Column(Integer, index=True)
    EM_ID = Column(Integer, index=True)
    PRP_ID = Column(Integer, index=True)
    EMP_SUMMARY_DE = Column(Unicode)
    EMP_SUMMARY_EN = Column(Unicode)
    EMP_SUMMARY_FR = Column(Unicode)
    EMP_COMMENT_DE = Column(Unicode(4000))
    EMP_COMMENT_EN = Column(Unicode(4000))
    EMP_COMMENT_FR = Column(Unicode(4000))
    ER_ID = Column(Integer)
    EMP_VALUE = Column(DECIMAL(18, 3))
    SO_NUMBER = Column(Integer)
    EMP_WITH_ADD = Column(BIT, server_default=text("((0))"))


class EDOCPHASE(Base):
    __tablename__ = "EDOC_PHASE"
    __table_args__ = {"schema": "dbo"}

    EP_ID = Column(Integer, primary_key=True)
    E_ID = Column(Integer, index=True)
    PRP_ID = Column(Integer, index=True)
    P_ID = Column(Integer, index=True)
    SO_NUMBER = Column(Integer, nullable=False, server_default=text("((0))"))
    EP_TEXT_DE = Column(Unicode(500))
    EP_TEXT_EN = Column(Unicode(500))
    EP_TEXT_FR = Column(Unicode(500))
    ER_ID = Column(Integer)
    EP_PHASE_ORDER = Column(Integer)
    EP_SAP = Column(Unicode(20))
    EP_CUSTOMER_RESULT = Column(Integer, server_default=text("((1))"))
    EP_CUSTOMER_VALUE = Column(DECIMAL(18, 3))
    EP_CUSTOMER_COMMENT_DE = Column(Unicode)
    EP_CUSTOMER_COMMENT_EN = Column(Unicode)
    EP_CUSTOMER_COMMENT_FR = Column(Unicode)
    EP_MARKETABILITY_RESULT = Column(Integer, server_default=text("((1))"))
    EP_MARKETABILITY_VALUE = Column(DECIMAL(18, 3))
    EP_MARKETABILITY_COMMENT_DE = Column(Unicode)
    EP_MARKETABILITY_COMMENT_EN = Column(Unicode)
    EP_MARKETABILITY_COMMENT_FR = Column(Unicode)
    EP_USABILITY_RESULT = Column(Integer, server_default=text("((1))"))
    EP_USABILITY_VALUE = Column(DECIMAL(18, 3))
    EP_USABILITY_COMMENT_DE = Column(Unicode)
    EP_USABILITY_COMMENT_EN = Column(Unicode)
    EP_USABILITY_COMMENT_FR = Column(Unicode)
    EP_PHASEALIAS = Column(Unicode(100))


class EDOCSETTING(Base):
    __tablename__ = "EDOC_SETTINGS"
    __table_args__ = {"schema": "dbo"}

    ES_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer, index=True)
    ES_PHASEPROTECTION = Column(BIT, server_default=text("((1))"))
    ES_SHOW_BROWSER = Column(BIT, server_default=text("((1))"))
    ES_ZOOM = Column(Integer, server_default=text("((100))"))
    ES_BORDER = Column(Integer, server_default=text("((40))"))
    ES_JUMP_NEXT = Column(BIT, server_default=text("((1))"))
    ES_RESULT_TYPE = Column(
        Integer, nullable=False, server_default=text("((0))")
    )
    ES_STYLE = Column(Integer, nullable=False, server_default=text("((3))"))
    ES_CACHE = Column(BIT, nullable=False, server_default=text("((0))"))
    ES_REPORT_INCLUDE_STANDARD = Column(
        Integer, nullable=False, server_default=text("((0))")
    )
    ES_REMOVE_EMPTY_HEADERS = Column(
        BIT, nullable=False, server_default=text("((1))")
    )
    ES_LOAD_SELECTION_ST_ID = Column(
        Integer, nullable=False, server_default=text("((0))")
    )


class EDOCTABLE(Base):
    __tablename__ = "EDOC_TABLE"
    __table_args__ = {"schema": "dbo"}

    ET_ID = Column(Integer, primary_key=True)
    E_ID = Column(Integer)
    ET_NUMBER = Column(Integer)
    ET_NAME_DE = Column(Unicode(500))
    ET_NAME_EN = Column(Unicode(500))
    ET_VALUE_DE = Column(Unicode(1024))
    ET_VALUE_EN = Column(Unicode(1024))
    ET_DATE = Column(Unicode(500))
    ET_REG = Column(
        DateTime, nullable=False, server_default=text("(getdate())")
    )
    ET_REGBY = Column(Integer)
    ET_UPDATE = Column(DateTime)
    ET_UPDATEBY = Column(Integer)


t_EDOC_USAGE = Table(
    "EDOC_USAGE",
    metadata,
    Column("ST_ID", Integer, nullable=False),
    Column("ST_SURNAME", Unicode(60), nullable=False),
    Column("ST_FORENAME", Unicode(50)),
    Column("EC_COUNT", Integer),
    schema="dbo",
)


class FILESERVER(Base):
    __tablename__ = "FILESERVER"
    __table_args__ = {"schema": "dbo"}

    FS_ID = Column(Integer, primary_key=True)
    FS_SHORT = Column(Unicode(5))
    FS_LONG = Column(Unicode(255))
    FS_PATH = Column(Unicode(255))
    FS_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    FS_REG = Column(
        DateTime, nullable=False, server_default=text("(getdate())")
    )
    FS_REGBY = Column(Integer, nullable=False, server_default=text("((133))"))
    FS_UPDATE = Column(DateTime)
    FS_UPDATEBY = Column(Integer)


class GMACOUNTRY(Base):
    __tablename__ = "GMA_COUNTRY"
    __table_args__ = {"schema": "dbo"}

    GMAC_ID = Column(Integer, primary_key=True)
    HRC_ID = Column(Integer)


class GMAPRODUCT(Base):
    __tablename__ = "GMA_PRODUCT"
    __table_args__ = {"schema": "dbo"}

    GMAP_ID = Column(Integer, primary_key=True)
    HRP_ID = Column(Integer)


class GOAL(Base):
    __tablename__ = "GOAL"
    __table_args__ = {"schema": "dbo"}

    G_ID = Column(Integer, primary_key=True)
    GT_ID = Column(Integer, index=True, server_default=text("((1))"))
    G_TEXT_DE = Column(Unicode(255))
    G_TEXT_EN = Column(Unicode(255))
    G_TEXT_FR = Column(Unicode(255))
    G_SHORT = Column(Unicode(10))
    G_VALUE = Column(Unicode(255))
    G_WEIGHTING = Column(Unicode(255))
    G_COMMENT = Column(Unicode(500))
    G_REG = Column(DateTime, server_default=text("(getutcdate())"))
    G_REGBY = Column(Integer, server_default=text("((1))"))
    G_UPDATE = Column(DateTime)
    G_UPDATEBY = Column(Integer)
    GP_POSITION = Column(Integer, server_default=text("((1000))"))
    ZM_PRODUCT = Column(Unicode(5))
    ZM_OBJECT = Column(Unicode(5))
    ZM_LOCATION = Column(Unicode(5))
    ZM_SUBLOCATION = Column(Unicode(5))
    G_POSITION = Column(Integer)
    TPER_ID = Column(Integer, nullable=False, server_default=text("((0))"))
    GR_ID = Column(
        Integer, nullable=False, index=True, server_default=text("((1))")
    )
    NL_ID = Column(Integer, nullable=False, server_default=text("((1))"))


class GOALPOSITION(Base):
    __tablename__ = "GOAL_POSITION"
    __table_args__ = {"schema": "dbo"}

    GP_ID = Column(Integer, primary_key=True)
    GP_POSITION = Column(Integer)
    GP_TEXT_DE = Column(Unicode(255))
    GP_TEXT_EN = Column(Unicode(255))
    GP_TEXT_FR = Column(Unicode(255))
    ZP_ID = Column(Unicode(3), server_default=text("(N'S18')"))
    ZO_ID = Column(Unicode(3), server_default=text("((400))"))
    ZP_LOCATION = Column(Unicode(2), server_default=text("((0))"))


class GOALRANGE(Base):
    __tablename__ = "GOAL_RANGE"
    __table_args__ = {"schema": "dbo"}

    GR_ID = Column(Integer, primary_key=True)
    GR_SHORT = Column(Unicode(10))
    GR_NAME_DE = Column(Unicode(100))
    GR_NAME_EN = Column(Unicode(100))
    GR_REG = Column(DateTime, server_default=text("(getdate())"))
    GR_REGBY = Column(Integer, server_default=text("((1))"))
    GR_ORDER = Column(Integer)


class GOALTYPE(Base):
    __tablename__ = "GOAL_TYPE"
    __table_args__ = {"schema": "dbo"}

    GT_ID = Column(Integer, primary_key=True)
    GT_SHORT = Column(Unicode(10))
    GT_NAME_DE = Column(Unicode(90))
    GT_NAME_EN = Column(Unicode(90))
    GT_NAME_FR = Column(Unicode(90))
    GT_SYMBOL_NUMBER = Column(Integer)
    GT_REG = Column(DateTime)
    GT_REGBY = Column(Integer)
    DI_ID = Column(Integer)
    GT_ORDER = Column(Integer)
    GT_COLOR_BG_HEX = Column(Unicode(6), server_default=text("(N'FFFFFF')"))
    GT_COLOR_FG_HEX = Column(Unicode(6), server_default=text("(N'000000')"))
    GT_COMMENT = Column(Unicode(255))


class HEADER(Base):
    __tablename__ = "HEADER"
    __table_args__ = {"schema": "dbo"}

    HEAD_ID = Column(Integer, primary_key=True)
    HEAD_ACTIVE = Column(BIT, server_default=text("(1)"))
    HEAD_FILENAME = Column(Unicode(255))
    HEAD_NAME = Column(Unicode(120))
    HEAD_DATA = Column(IMAGE)
    HEAD_REG = Column(DateTime)
    HEAD_REGBY = Column(Integer)
    HEAD_UPDATE = Column(DateTime)
    HEAD_UPDATEBY = Column(Integer)
    HEAD_DEFAULT_PROTOCOL = Column(BIT, server_default=text("((0))"))
    HEAD_DEFAULT_REPORT = Column(BIT, server_default=text("((0))"))
    HEAD_NAME_EN = Column(Unicode(120))


class HISTORY(Base):
    __tablename__ = "HISTORY"
    __table_args__ = {"schema": "dbo"}

    HIST_ID = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, index=True)
    DI_VERSION = Column(Integer)
    HIST_REQUIREMENT_DE = Column(Unicode(1500))
    HIST_REQUIREMENT_EN = Column(Unicode(1500))
    HIST_REQUIREMENT_FR = Column(Unicode(1500))
    HIST_REG = Column(DateTime)
    HIST_REGBY = Column(Integer)
    HIST_KEYNOTE = Column(BIT, nullable=False, server_default=text("((0))"))
    HIST_MAINFEATURE = Column(
        BIT, nullable=False, server_default=text("((0))")
    )
    HIST_ADD = Column(BIT, nullable=False, server_default=text("((0))"))


class HRCOUNTRY(Base):
    __tablename__ = "HR_COUNTRY"
    __table_args__ = {"schema": "dbo"}

    HRC_ID = Column(Integer, primary_key=True)
    HRC_LEFT = Column(Integer, index=True)
    HRC_RIGHT = Column(Integer, index=True)
    HRC_INDENT = Column(Integer)
    HRC_NAME_DE = Column(Unicode(255), index=True)
    HRC_NAME_EN = Column(Unicode(255), index=True)
    HRC_NAME_FR = Column(Unicode(255))
    HRC_UPDATE = Column(DateTime, server_default=text("(getdate())"))
    HRC_UPDATEBY = Column(Integer, server_default=text("((1))"))


class HRCOUNTRYHISTORY(Base):
    __tablename__ = "HR_COUNTRY_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HHRC_ID = Column(Integer, primary_key=True)
    HHRC_DATE = Column(DateTime, server_default=text("(getdate())"))
    HRC_ID = Column(Integer, nullable=False)
    HRC_LEFT = Column(Integer)
    HRC_RIGHT = Column(Integer)
    HRC_INDENT = Column(Integer)
    HRC_NAME_DE = Column(Unicode(255))
    HRC_NAME_EN = Column(Unicode(255))
    HRC_NAME_FR = Column(Unicode(255))
    HRC_UPDATE = Column(DateTime)
    HRC_UPDATEBY = Column(Integer)


class HRDEFAULT(Base):
    __tablename__ = "HR_DEFAULT"
    __table_args__ = {"schema": "dbo"}

    HRD_ID = Column(Integer, primary_key=True)
    HRD_TYPE = Column(Integer, server_default=text("((0))"))
    HRD_NAME_DE = Column(Unicode(255))
    HRD_NAME_EN = Column(Unicode(255))
    HRD_NAME_FR = Column(Unicode(255), server_default=text("((1))"))
    HRD_SELECTED = Column(BIT)


class HRPRODUCT(Base):
    __tablename__ = "HR_PRODUCT"
    __table_args__ = {"schema": "dbo"}

    HRP_ID = Column(Integer, primary_key=True)
    HRP_LEFT = Column(Integer, index=True)
    HRP_RIGHT = Column(Integer, index=True)
    HRP_INDENT = Column(Integer)
    HRP_NAME_DE = Column(Unicode(255), index=True)
    HRP_NAME_EN = Column(Unicode(255), index=True)
    HRP_NAME_FR = Column(Unicode(255))
    HRP_UPDATE = Column(DateTime, server_default=text("(getdate())"))
    HRP_UPDATEBY = Column(Integer, server_default=text("((1))"))


class HRPRODUCTHISTORY(Base):
    __tablename__ = "HR_PRODUCT_HISTORY"
    __table_args__ = {"schema": "dbo"}

    HHRP_ID = Column(Integer, primary_key=True)
    HHRP_DATE = Column(DateTime, server_default=text("(getdate())"))
    HRP_ID = Column(Integer, nullable=False)
    HRP_LEFT = Column(Integer)
    HRP_RIGHT = Column(Integer)
    HRP_INDENT = Column(Integer)
    HRP_NAME_DE = Column(Unicode(255))
    HRP_NAME_EN = Column(Unicode(255))
    HRP_NAME_FR = Column(Unicode(255))
    HRP_UPDATE = Column(DateTime)
    HRP_UPDATEBY = Column(Integer)
    HHRP_ELEMENT = Column(Integer)


class IMAGEFILE(Base):
    __tablename__ = "IMAGEFILES"
    __table_args__ = {"schema": "dbo"}

    IM_ID = Column(Integer, primary_key=True)
    IM_NAME = Column(Unicode(255))
    IM_DATA = Column(IMAGE)
    IM_MD5 = Column(Unicode(32))


class INTERNALFILE(Base):
    __tablename__ = "INTERNAL_FILES"
    __table_args__ = {"schema": "dbo"}

    IF_ID = Column(Integer, primary_key=True)
    IF_CLEARINGFILE = Column(IMAGE)
    IF_CLEARINGFILE_NAME = Column(Unicode(50))


t_KRITERIEN_ERSTELLT = Table(
    "KRITERIEN_ERSTELLT",
    metadata,
    Column("Jahr", Integer),
    Column("Woche", Integer),
    Column("Team", Unicode(20)),
    Column("Summe", BigInteger),
    schema="dbo",
)


t_KRITERIEN_GEAENDERT = Table(
    "KRITERIEN_GEAENDERT",
    metadata,
    Column("Jahr", Integer),
    Column("Woche", Integer),
    Column("Team", Unicode(20)),
    Column("Summe", BigInteger),
    schema="dbo",
)


class MODULEXE(Base):
    __tablename__ = "MODULEXE"
    __table_args__ = {"schema": "dbo"}

    MEXE_ID = Column(Integer, primary_key=True)
    DM_ID = Column(Integer)
    ST_ID = Column(Integer, index=True)
    MEXE_REG = Column(
        DateTime, index=True, server_default=text("(getutcdate())")
    )


class MODULHISTORY(Base):
    __tablename__ = "MODUL_HISTORY"
    __table_args__ = {"schema": "dbo"}

    MH_ID = Column(Integer, primary_key=True)
    MH_COMMENT = Column(Unicode(1000))
    MH_DOCUMENT_NAME = Column(Unicode(255))
    MH_DOCUMENT = Column(IMAGE)
    MH_CLEAR_DOCUMENT_NAME = Column(Unicode(255))
    MH_CLEAR_DOCUMENT = Column(IMAGE)
    DM_ID = Column(Integer, index=True)
    DM_VERSION = Column(Integer, server_default=text("((1))"))
    DM_NAME = Column(Unicode(255))
    DM_LETTER = Column(Unicode(10))
    CL_ID = Column(Integer, server_default=text("((1))"))
    DM_CLEAR_BY = Column(Integer)
    DM_CLEAR_DATE = Column(DateTime)
    MH_REG = Column(DateTime, server_default=text("(getutcdate())"))
    MH_REGBY = Column(Integer, server_default=text("((1))"))
    MH_UPDATE = Column(DateTime)
    MH_UPDATEBY = Column(Integer)
    DM_TESTBASE_DE = Column(Unicode(500))
    DM_TESTBASE_EN = Column(Unicode(500))
    DM_TESTBASE_FR = Column(Unicode(500))
    DM_IS_CUSTOMER = Column(BIT, server_default=text("((0))"))
    DM_IS_MARKETABILITY = Column(BIT, server_default=text("((0))"))
    DM_IS_USABILITY = Column(BIT, server_default=text("((0))"))
    CT_ID = Column(Integer, server_default=text("((1))"))
    DM_SCOPE_DE = Column(Unicode(500))
    DM_SCOPE_EN = Column(Unicode(500))
    DM_SCOPE_FR = Column(Unicode(500))
    DM_CLEAR_BY_VT = Column(Integer)
    DM_CLEAR_DATE_VT = Column(DateTime)
    DM_CREATED_FOR = Column(Integer, server_default=text("((1))"))
    DM_CREATED_FOR_DATE = Column(DateTime)
    DM_REVISION = Column(Unicode(60))


class MODULHISTORYITEM(Base):
    __tablename__ = "MODUL_HISTORY_ITEM"
    __table_args__ = {"schema": "dbo"}

    MHI_ID = Column(Integer, primary_key=True)
    MH_ID = Column(Integer, index=True)
    DI_ID = Column(Integer)
    DI_VERSION = Column(Integer)
    DI_REQUIREMENT_DE = Column(Unicode(1500))
    DI_REQUIREMENT_EN = Column(Unicode(1500))
    DI_REQUIREMENT_FR = Column(Unicode(1500))
    DMI_ID = Column(Integer)
    DMI_NUMBER = Column(Integer, server_default=text("((1))"))
    DMI_INDENT = Column(Integer, server_default=text("((0))"))
    DMI_TITLE = Column(BIT, server_default=text("((0))"))


t_MODUL_PARAMETER = Table(
    "MODUL_PARAMETER",
    metadata,
    Column("MP_ID", Integer, nullable=False, index=True),
    Column("DM_ID", Integer, index=True),
    Column("MP_PARAMETER_DE", Unicode(255), index=True),
    Column("MP_PARAMETER_EN", Unicode(255), index=True),
    Column(
        "MP_REG", DateTime, nullable=False, server_default=text("(getdate())")
    ),
    Column("MP_REGBY", Integer),
    Column("MP_UPDATE", DateTime),
    Column("MP_UPDATEBY", Integer),
    schema="dbo",
)


class NAV(Base):
    __tablename__ = "NAV"
    __table_args__ = {"schema": "dbo"}

    N_ID = Column(Integer, primary_key=True)
    N_TEMPLATE = Column(Integer)
    N_NAME_DE = Column(Unicode(120), index=True)
    N_NAME_EN = Column(Unicode(120), index=True)
    BEGR_ID = Column(Integer, index=True)
    N_COMMENT_DE = Column(Unicode(500))
    N_COMMENT_EN = Column(Unicode(500))
    N_DURATION = Column(Integer)
    N_MASTER = Column(BIT, index=True)
    HR_NEW_ID = Column(
        Integer,
        nullable=False,
        index=True,
        server_default=text("((101010100))"),
    )
    HRC_ID = Column(
        Integer, nullable=False, index=True, server_default=text("((1))")
    )
    HRP_ID = Column(
        Integer, nullable=False, index=True, server_default=text("((1))")
    )
    ZM_OBJECT = Column(Unicode(5), server_default=text("((400))"))
    KOT_ID = Column(Integer, nullable=False, server_default=text("((24))"))
    N_REG = Column(DateTime)
    N_REGBY = Column(Integer)
    N_UPDATE = Column(DateTime)
    N_UPDATEBY = Column(Integer)


class NAVDOMAIN(Base):
    __tablename__ = "NAVDOMAIN"
    __table_args__ = {"schema": "dbo"}

    ND_ID = Column(Integer, primary_key=True)
    ND_SHORT = Column(Unicode(10))
    ND_NAME_DE = Column(Unicode(100))
    ND_NAME_EN = Column(Unicode(100))
    ND_REG = Column(DateTime, server_default=text("(getdate())"))
    ND_REGBY = Column(Integer, server_default=text("((1))"))
    ND_ORDER = Column(Integer)
    ND_ORDER_EXPORT = Column(
        Integer, nullable=False, server_default=text("((50))")
    )
    ND_ORDER_PLAN_DEFAULT = Column(
        Integer, nullable=False, server_default=text("((1000))")
    )


class NAVLEVEL(Base):
    __tablename__ = "NAVLEVEL"
    __table_args__ = {"schema": "dbo"}

    NL_ID = Column(Integer, primary_key=True)
    NL_LEVEL = Column(Integer)
    NL_NAME_DE = Column(Unicode(30))
    NL_NAME_EN = Column(Unicode(30))


class NAVPOSITION(Base):
    __tablename__ = "NAVPOSITION"
    __table_args__ = {"schema": "dbo"}

    NPOS_ID = Column(Integer, primary_key=True)
    NPOS_POSITION = Column(Integer)
    NPOS_TEXT_DE = Column(Unicode(2048))
    NPOS_TEXT_EN = Column(Unicode(2048))
    NPOS_REG = Column(DateTime, server_default=text("(getdate())"))
    NPOS_REGBY = Column(Integer, server_default=text("((1))"))
    NPOS_UPDATE = Column(DateTime)
    NPOS_UPDATEBY = Column(Integer)


class NAVPROOF(Base):
    __tablename__ = "NAVPROOF"
    __table_args__ = {"schema": "dbo"}

    NPR_ID = Column(Integer, primary_key=True)
    NPR_NAME_DE = Column(Unicode(1000))
    NPR_NAME_EN = Column(Unicode(1000))
    NPR_SHOWBASE = Column(Integer, server_default=text("((0))"))
    NPR_REG = Column(DateTime)
    NPR_REGBY = Column(Integer)
    NPR_UPDATE = Column(DateTime)
    NPR_UPDATEBY = Column(Integer)


class NAVCOUNTMODULEEXPORT(Base):
    __tablename__ = "NAV_COUNT_MODULEEXPORT"
    __table_args__ = {"schema": "dbo"}

    NCM_ID = Column(Integer, primary_key=True)
    DM_ID = Column(Integer, index=True)
    NCM_TYPE = Column(Integer)
    NCM_REG = Column(
        DateTime, index=True, server_default=text("(getutcdate())")
    )
    NCM_REGBY = Column(Integer)


class NAVCOUNTTESTPLAN(Base):
    __tablename__ = "NAV_COUNT_TESTPLAN"
    __table_args__ = {"schema": "dbo"}

    NCT_ID = Column(Integer, primary_key=True)
    N_ID = Column(Integer)
    NP_ID = Column(Integer)
    NCT_NAME = Column(Unicode(255))
    NCT_TYPE = Column(Integer, server_default=text("((1))"))
    NCT_REG = Column(DateTime, server_default=text("(getutcdate())"))
    NCT_REGBY = Column(Integer)


class NAVEDOC(Base):
    __tablename__ = "NAV_EDOC"
    __table_args__ = {"schema": "dbo"}

    NE_ID = Column(Integer, primary_key=True)
    NE_NAME = Column(Unicode(255), nullable=False)
    HEAD_ID = Column(Integer, server_default=text("((1))"))
    NE_RANDOM = Column(Integer)
    ST_ID = Column(Integer, server_default=text("((1))"))
    P_ID = Column(Integer)


class NAVEDOCMODULE(Base):
    __tablename__ = "NAV_EDOC_MODULE"
    __table_args__ = {"schema": "dbo"}

    NEM_ID = Column(Integer, primary_key=True)
    NE_RANDOM = Column(Integer)
    DM_ID = Column(Integer)
    ST_ID = Column(Integer)
    NE_NUMBER = Column(Integer)


class NAVEDOCMODULEITEM(Base):
    __tablename__ = "NAV_EDOC_MODULE_ITEM"
    __table_args__ = {"schema": "dbo"}

    NEMI_ID = Column(Integer, primary_key=True)
    NE_RANDOM = Column(Integer)
    DM_ID = Column(Integer)
    DI_ID = Column(Integer)
    NEMI_INDENT = Column(Integer, server_default=text("((0))"))
    DMI_ID = Column(Integer)
    NE_NUMBER = Column(Integer)


class NAVPACK(Base):
    __tablename__ = "NAV_PACK"
    __table_args__ = {"schema": "dbo"}

    NP_ID = Column(Integer, primary_key=True)
    N_ID = Column(Integer, index=True)
    NP_NAME_DE = Column(Unicode(150))
    NP_NAME_EN = Column(Unicode(150))
    NP_COMMENT_DE = Column(Unicode(800))
    NP_COMMENT_EN = Column(Unicode(800))
    CL_ID = Column(Integer, nullable=False, server_default=text("((1))"))
    NP_CLEARDATE = Column(DateTime)
    NP_CLEARBY = Column(Integer)
    ZM_PRODUCT = Column(Unicode(5), server_default=text("(N'T10')"))
    PT_ID = Column(
        Integer, nullable=False, index=True, server_default=text("((1))")
    )
    NP_TESTSAMPLES = Column(
        Integer, nullable=False, server_default=text("((0))")
    )
    NP_IS_TEMPLATE = Column(BIT, nullable=False, server_default=text("((0))"))
    NP_TEMPLATE_ID = Column(Integer)
    NP_REG = Column(DateTime, server_default=text("(getutcdate())"))
    NP_REGBY = Column(Integer, server_default=text("((1))"))
    NP_UPDATE = Column(DateTime)
    NP_UPDATEBY = Column(Integer)
    PN_ID = Column(Integer, nullable=False, server_default=text("((1))"))


class NAVPACKCUSTOM(Base):
    __tablename__ = "NAV_PACK_CUSTOM"
    __table_args__ = {"schema": "dbo"}

    NPCU_ID = Column(Integer, primary_key=True)
    NP_ID = Column(Integer, index=True)
    CUL_ID = Column(Integer)
    CUR_ID = Column(Unicode(10))
    NPCU_TESTSAMPLES = Column(Unicode(512))
    NPCU_TESTSAMPLES_TEXT_DE = Column(Unicode(1024))
    NPCU_TESTSAMPLES_TEXT_EN = Column(Unicode(1024))
    NPCU_TESTSAMPLE_COUNT = Column(Integer)
    NPCU_HINT_DE = Column(Unicode(2048))
    NPCU_HINT_EN = Column(Unicode(2048))
    NPCU_DURATION_DE = Column(Unicode(1024))
    NPCU_DURATION_EN = Column(Unicode(1024))
    P_ID = Column(Integer)
    NPCU_REG = Column(
        DateTime, nullable=False, server_default=text("(getdate())")
    )
    NPCU_REGBY = Column(Integer)
    NPCU_UPDATE = Column(DateTime)
    NPCU_UPDATEBY = Column(Integer)
    NPCU_TEMPLATE = Column(BIT, nullable=False, server_default=text("((0))"))
    NPCU_TEMPLATE_NAME = Column(Unicode(256))


class NAVPACKCUSTOMELEMENT(Base):
    __tablename__ = "NAV_PACK_CUSTOM_ELEMENTS"
    __table_args__ = {"schema": "dbo"}

    NPCUE_ID = Column(Integer, primary_key=True)
    NPCU_ID = Column(Integer)
    NP_ID = Column(Integer, index=True)
    CUL_ID = Column(Integer)
    CULE_ID = Column(Integer, index=True)
    NPCUE_APPLICABLE = Column(
        BIT, nullable=False, server_default=text("((0))")
    )
    NPCUE_PRICE = Column(DECIMAL(18, 2))
    NPCUE_PRICE_EXTERN = Column(DECIMAL(18, 2), server_default=text("((0))"))
    NPCUE_LAB = Column(Unicode(256))
    NPCUE_COMMENT_DE = Column(Unicode(2048))
    NPCUE_COMMENT_EN = Column(Unicode(2048))
    NPCUE_LABTEST = Column(BIT, nullable=False, server_default=text("((0))"))
    NPCUE_SPOTTEST = Column(BIT, nullable=False, server_default=text("((0))"))
    NPCUE_DOCUCHECK = Column(BIT, nullable=False, server_default=text("((0))"))
    NPCUE_REFERENCE = Column(Integer)
    NPCUE_TESTSAMPLES = Column(Integer)
    NPCUE_REG = Column(
        DateTime, nullable=False, server_default=text("(getdate())")
    )
    NPCUE_REGBY = Column(Integer)
    NPCUE_UPDATE = Column(DateTime)
    NPCUE_UPDATEBY = Column(Integer)


class NAVPACKDELETED(Base):
    __tablename__ = "NAV_PACK_DELETED"
    __table_args__ = {"schema": "dbo"}

    NPD_ID = Column(Integer, primary_key=True)
    NP_ID = Column(Integer)
    NPD_NAME_DE = Column(Unicode(150))
    NPD_NAME_EN = Column(Unicode(150))
    NPD_DELETED = Column(DateTime, server_default=text("(getutcdate())"))
    NPD_DELETEDBY = Column(Integer)


class NAVPACKELEMENT(Base):
    __tablename__ = "NAV_PACK_ELEMENT"
    __table_args__ = {"schema": "dbo"}

    NPE_ID = Column(Integer, primary_key=True)
    NP_ID = Column(Integer, index=True)
    DM_ID = Column(Integer, index=True)
    NL_ID = Column(Integer, index=True)
    ZM_LOCATION = Column(Unicode(5))
    NPE_CREATE = Column(BIT, server_default=text("((1))"))
    CT_ID = Column(Integer, server_default=text("((1))"))
    NPE_REG = Column(DateTime, server_default=text("(getutcdate())"))
    NPE_REGBY = Column(Integer, server_default=text("((1))"))
    NPE_UPDATE = Column(DateTime)
    NPE_UPDATEBY = Column(Integer)
    NPE_CREATE_SO = Column(BIT, nullable=False, server_default=text("((1))"))


class NAVPACKELEMENTCALC(Base):
    __tablename__ = "NAV_PACK_ELEMENT_CALC"
    __table_args__ = {"schema": "dbo"}

    NPEC_ID = Column(Integer, primary_key=True)
    NPE_ID = Column(Integer, index=True)
    ST_ID = Column(Integer, nullable=False, server_default=text("((1))"))
    NPEC_DELTA_START = Column(Float(53))
    NPEC_TIME_DAYS = Column(Float(53))
    NPEC_TIME_HOURS = Column(Float(53))
    NPEC_RATE = Column(DECIMAL(18, 2))
    NPEC_COSTS = Column(DECIMAL(18, 2), server_default=text("((0))"))
    NPEC_TRAVEL = Column(DECIMAL(18, 2), server_default=text("((0))"))
    NPEC_FACTOR = Column(Float(53), server_default=text("((1))"))
    NPEC_PRICE = Column(DECIMAL(18, 2), server_default=text("((1))"))
    NPEC_COMMENT = Column(Unicode(500))
    NPEC_TASK = Column(Unicode(500))
    ZM_ID = Column(Unicode(50))
    NPOS_ID = Column(Integer, server_default=text("((1))"))
    NPEC_REG = Column(DateTime, server_default=text("(getutcdate())"))
    NPEC_REGBY = Column(Integer, server_default=text("((1))"))
    NPEC_UPDATE = Column(DateTime)
    NPEC_UPDATEBY = Column(Integer)
    CBC_ID = Column(Integer)
    NPEC_COSTS_EXTERNAL = Column(DECIMAL(18, 2), server_default=text("((0))"))
    NPEC_COSTS_OLD = Column(DECIMAL(18, 2), server_default=text("((0))"))
    NPEC_COSTS_EXTERNAL_OLD = Column(
        DECIMAL(18, 2), server_default=text("((0))")
    )


class NAVPACKELEMENTFILTER(Base):
    __tablename__ = "NAV_PACK_ELEMENT_FILTER"
    __table_args__ = {"schema": "dbo"}

    NPEF_ID = Column(Integer, primary_key=True)
    NPE_ID = Column(Integer)
    DMI_ID = Column(Integer)
    NPEF_REG = Column(DateTime, server_default=text("(getutcdate())"))
    NPEF_REGBY = Column(Integer, server_default=text("((1))"))


class NAVPACKELEMENTPROOF(Base):
    __tablename__ = "NAV_PACK_ELEMENT_PROOF"
    __table_args__ = {"schema": "dbo"}

    NPEP_ID = Column(Integer, primary_key=True)
    NPE_ID = Column(Integer, index=True)
    NPEP_TYPE = Column(Integer, server_default=text("((0))"))
    NPR_ID = Column(Integer, index=True, server_default=text("((1))"))
    NPEP_TEXT_DE = Column(Unicode(255), server_default=text("(N'')"))
    NPEP_TEXT_EN = Column(Unicode(255), server_default=text("(N'')"))
    NPEP_REG = Column(DateTime)
    NPEP_REGBY = Column(Integer)
    NPEP_UPDATE = Column(DateTime)
    NPEP_UPDATEBY = Column(Integer)


class NAVPACKSERVICECLAS(Base):
    __tablename__ = "NAV_PACK_SERVICECLASS"
    __table_args__ = {"schema": "dbo"}

    NPS_ID = Column(Integer, primary_key=True)
    NP_ID = Column(Integer, index=True)
    SCL_ID = Column(Integer)


class NAVSAVE(Base):
    __tablename__ = "NAV_SAVE"
    __table_args__ = {"schema": "dbo"}

    NS_ID = Column(Integer, primary_key=True)
    NS_COMMENT = Column(Unicode(512))
    N_ID = Column(Integer, index=True)
    P_ID = Column(Integer, index=True)
    E_ID = Column(Integer, index=True)
    NS_NAME_DE = Column(Unicode(256))
    NS_NAME_EN = Column(Unicode(256))
    NS_CRM = Column(Unicode(256))
    NS_TYPE = Column(
        Integer, nullable=False, index=True, server_default=text("((1))")
    )
    NS_REG = Column(DateTime, server_default=text("(getdate())"))
    NS_REGBY = Column(Integer, index=True)


class NAVSAVECALC(Base):
    __tablename__ = "NAV_SAVE_CALC"
    __table_args__ = {"schema": "dbo"}

    NSC_ID = Column(Integer, primary_key=True)
    NS_ID = Column(Integer, index=True)
    NPEC_ID = Column(Integer, index=True)
    NSC_TIME_HOURS = Column(Float(53))
    NSC_TIME_DAYS = Column(Float(53))
    NSC_DELTA_START = Column(Float(53))
    NSC_COSTS = Column(DECIMAL(18, 2))
    NSC_TASK = Column(Unicode(500))
    NSC_COMMENT = Column(Unicode(500))
    NSC_RATE = Column(DECIMAL(18, 2))
    NSC_PRICE = Column(DECIMAL(18, 2))
    NSC_FACTOR = Column(Float(53))
    NSC_TRAVEL = Column(DECIMAL(18, 2))
    NPOS_ID = Column(Integer)
    ZM_ID = Column(Unicode(50))
    ST_ID = Column(Integer, nullable=False, server_default=text("((1))"))
    NSC_COSTS_EXTERNAL = Column(DECIMAL(18, 2), server_default=text("((0))"))


class NAVSAVESELECTION(Base):
    __tablename__ = "NAV_SAVE_SELECTION"
    __table_args__ = {"schema": "dbo"}

    NSS_ID = Column(Integer, primary_key=True)
    NS_ID = Column(Integer, index=True)
    NP_ID = Column(Integer, index=True)


class PACKAGECAT(Base):
    __tablename__ = "PACKAGE_CAT"
    __table_args__ = {"schema": "dbo"}

    PC_ID = Column(Integer, primary_key=True)
    PC_NAME_DE = Column(Unicode(50))
    PC_NAME_EN = Column(Unicode(50))
    PC_REG = Column(DateTime, server_default=text("(getdate())"))
    PC_REG_BY = Column(Integer, server_default=text("((1))"))


class PACKAGENAME(Base):
    __tablename__ = "PACKAGE_NAME"
    __table_args__ = {"schema": "dbo"}

    PN_ID = Column(Integer, primary_key=True)
    PN_NAME_DE = Column(Unicode(255))
    PN_NAME_EN = Column(Unicode(255))
    PN_REG = Column(DateTime, server_default=text("(getdate())"))
    PN_REG_BY = Column(Integer, server_default=text("((1))"))
    PN_UPDATE = Column(DateTime)
    PN_UPDATE_BY = Column(Integer)


class PACKAGETYPE(Base):
    __tablename__ = "PACKAGE_TYPE"
    __table_args__ = {"schema": "dbo"}

    PT_ID = Column(Integer, primary_key=True)
    PT_NAME_DE = Column(Unicode(255))
    PT_NAME_EN = Column(Unicode(255))
    PT_REG = Column(DateTime, server_default=text("(getdate())"))
    PT_REG_BY = Column(Integer, server_default=text("((1))"))
    PC_ID = Column(Integer, nullable=False, server_default=text("((1))"))


t_PL = Table(
    "PL",
    metadata,
    Column("DI_COSTITEM", Unicode(255)),
    Column("DI_TYPE", Unicode(255)),
    Column("DI_NAME_EN", Unicode(255)),
    Column("CUR_GER", Float(53)),
    Column("CUR_IND", Float(53)),
    Column("CUR_HK", Float(53)),
    Column("CUR_GCN", Float(53)),
    Column("CUR_BGD", Float(53)),
    Column("CUR_VNM", Float(53)),
    Column("CUR_VNM_1000", Float(53)),
    schema="dbo",
)


t_PREISLISTE_LABOR_2019 = Table(
    "PREISLISTE_LABOR_2019",
    metadata,
    Column("SubItem", Unicode(255)),
    Column("Type", Unicode(255)),
    Column("TestGroup", Unicode(255)),
    Column("GER_EUR", MONEY),
    Column("GCN_CNY", MONEY),
    Column("HK_HKD", MONEY),
    Column("IND_INR", MONEY),
    Column("VNM_VND", MONEY),
    Column("BGD_BDT", MONEY),
    schema="dbo",
)


class PRICELIST(Base):
    __tablename__ = "PRICELIST"
    __table_args__ = {"schema": "dbo"}

    PL_ID = Column(Integer, primary_key=True)
    PL_SHORT = Column(Unicode(10))
    PL_NAME_DE = Column(Unicode(100))
    PL_NAME_EN = Column(Unicode(100))
    CUR_ID = Column(NCHAR(3))
    PL_ORDER = Column(Integer, server_default=text("((1))"))
    PL_REG = Column(DateTime, server_default=text("(getdate())"))
    PL_REGBY = Column(Integer, server_default=text("((1))"))
    PL_TYPE = Column(Integer, nullable=False, server_default=text("((0))"))
    PL_FACTOR_CC = Column(
        DECIMAL(18, 5), nullable=False, server_default=text("((1))")
    )
    PL_FACTOR_PROFIT = Column(
        DECIMAL(18, 5), nullable=False, server_default=text("((1))")
    )
    PL_UPDATE = Column(DateTime)
    PL_UPDATEBY = Column(Integer)


class PRICELISTCURRENCY(Base):
    __tablename__ = "PRICELIST_CURRENCY"
    __table_args__ = {"schema": "dbo"}

    PLC_ID = Column(Integer, primary_key=True)
    CUR_ID = Column(NCHAR(3), nullable=False)


class PRICELISTROLE(Base):
    __tablename__ = "PRICELIST_ROLE"
    __table_args__ = {"schema": "dbo"}

    PLR_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer, nullable=False)


class PSI(Base):
    __tablename__ = "PSI"
    __table_args__ = {"schema": "dbo"}

    PSI_ID = Column(Integer, primary_key=True)
    PSI_LEVEL = Column(Integer)
    PSI_NAME_DE = Column(Unicode(50))
    PSI_NAME_EN = Column(Unicode(50))


class PSINFOCOUNT(Base):
    __tablename__ = "PSINFO_COUNT"
    __table_args__ = {"schema": "dbo"}

    PSIC_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer, index=True)
    PSIC_REG = Column(DateTime, server_default=text("(getutcdate())"))


class PSINFOSTAFF(Base):
    __tablename__ = "PSINFO_STAFF"
    __table_args__ = {"schema": "dbo"}

    PSS_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer)


class REGISTERPOSITION(Base):
    __tablename__ = "REGISTERPOSITION"
    __table_args__ = {"schema": "dbo"}

    REGP_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer)
    REGP_POSITION_RIGHT = Column(BIT)
    REGP_REGISTER = Column(Integer)
    REG_NUMBER = Column(Integer)


class RELEVANCE(Base):
    __tablename__ = "RELEVANCE"
    __table_args__ = {"schema": "dbo"}

    REL_ID = Column(Integer, primary_key=True)
    REL_TEXT_DE = Column(Unicode(255))
    REL_TEXT_EN = Column(Unicode(255))
    REL_TEXT_FR = Column(Unicode(255))
    REL_REG = Column(DateTime, server_default=text("(getdate())"))
    REL_REGBY = Column(Integer)
    REL_UPDATE = Column(DateTime)
    REL_UPDATEBY = Column(Integer)


class REPORTCOMMENT(Base):
    __tablename__ = "REPORTCOMMENT"
    __table_args__ = {"schema": "dbo"}

    RC_ID = Column(Integer, primary_key=True)
    TPT_ID = Column(Integer)
    RC_TEXT_DE = Column(Unicode(1000))
    RC_TEXT_EN = Column(Unicode(1000))
    RC_TEXT_FR = Column(Unicode(1000))


t_SCCT_MODULE = Table(
    "SCCT_MODULE",
    metadata,
    Column("DM_ID", Integer, nullable=False),
    Column("DM_NAME", Unicode(255)),
    Column("DM_NAME_EN", Unicode(255)),
    schema="dbo",
)


class SERVICECLAS(Base):
    __tablename__ = "SERVICECLASS"
    __table_args__ = {"schema": "dbo"}

    SCL_ID = Column(Integer, primary_key=True)
    SCL_LEVEL = Column(Integer)
    SCL_REMARK_DE = Column(Unicode(500))
    SCL_REMARK_EN = Column(Unicode(500))
    SCL_REG = Column(DateTime, server_default=text("(getdate())"))
    SCL_REGBY = Column(Integer, server_default=text("((1))"))
    SCL_UPDATE = Column(DateTime)
    SCL_UPDATEBY = Column(Integer)


class SERVICELEVEL(Base):
    __tablename__ = "SERVICELEVEL"
    __table_args__ = {"schema": "dbo"}

    SL_ID = Column(Integer, primary_key=True)
    SL_LEVEL = Column(Integer)
    SL_REMARK_DE = Column(Unicode(500))
    SL_REMARK_EN = Column(Unicode(500))
    SL_REG = Column(DateTime, server_default=text("(getdate())"))
    SL_REG_BY = Column(Integer, server_default=text("((1))"))
    SL_UPDATE = Column(DateTime)
    SL_UPDATE_BY = Column(Integer)


class SIGN(Base):
    __tablename__ = "SIGN"
    __table_args__ = {"schema": "dbo"}

    SIGN_ID = Column(Integer, primary_key=True, index=True)
    ST_ID = Column(Integer, index=True)
    SIGN_PW = Column(Unicode(50), server_default=text("((12345678))"))
    SIGN_REMEMBER = Column(BIT, server_default=text("((1))"))
    SIGN_PICTURE = Column(IMAGE)
    SIGN_REG = Column(DateTime, server_default=text("(getdate())"))
    SIGN_REGBY = Column(Integer, server_default=text("((133))"))
    SIGN_AUTOCLOSE = Column(BIT, nullable=False, server_default=text("((1))"))
    SIGN_PREFIX = Column(Unicode(100))
    SIGN_OPEN_PDF = Column(BIT, nullable=False, server_default=text("((0))"))
    SIGN_HASH = Column(Unicode(512))


class SIGNADMIN(Base):
    __tablename__ = "SIGN_ADMIN"
    __table_args__ = {"schema": "dbo"}

    SIGA_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer)
    SIGA_ROLE = Column(Integer)
    SIGN_REG = Column(DateTime, server_default=text("(getdate())"))
    SIGN_REGBY = Column(Integer)


class SIGNUSE(Base):
    __tablename__ = "SIGN_USE"
    __table_args__ = {"schema": "dbo"}

    SIGU_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer, index=True)
    SIGU_PDF = Column(IMAGE)
    SIGU_FILENAME = Column(Unicode(500))
    SIGU_ERROR = Column(BIT)
    SIGU_MD5 = Column(Unicode(255))
    SIGU_FILESIZE = Column(BigInteger)
    SIGU_REG = Column(DateTime, index=True, server_default=text("(getdate())"))
    SIGU_RESERVED_BY = Column(Integer)
    SIGU_RESERVED_DATE = Column(DateTime)
    SIGU_USED = Column(BIT, nullable=False, server_default=text("((1))"))
    SIGU_TEMP = Column(Unicode(30))


class STATISTICITEM(Base):
    __tablename__ = "STATISTIC_ITEM"
    __table_args__ = {"schema": "dbo"}

    STAI_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer)
    DI_ID = Column(Integer)
    STAT_ID = Column(Integer)
    STAI_REG = Column(DateTime, server_default=text("(getutcdate())"))


class STATISTICMODULE(Base):
    __tablename__ = "STATISTIC_MODULE"
    __table_args__ = {"schema": "dbo"}

    STAM_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer)
    DM_ID = Column(Integer)
    STAT_ID = Column(Integer)
    STAM_REG = Column(DateTime, server_default=text("(getutcdate())"))


class STATISTICTYPE(Base):
    __tablename__ = "STATISTIC_TYPE"
    __table_args__ = {"schema": "dbo"}

    STAT_ID = Column(Integer, primary_key=True)
    STAT_NAME_DE = Column(Unicode(256))
    STAT_NAME_EN = Column(Unicode(256))
    STAT_REG = Column(DateTime, server_default=text("(getutcdate())"))
    STAT_TYPE = Column(Integer, nullable=False, server_default=text("((0))"))


class SBUSINESSLINE(Base):
    __tablename__ = "S_BUSINESSLINE"
    __table_args__ = {"schema": "dbo"}

    S_BL_ID = Column(Integer, primary_key=True)
    S_BL_NAME = Column(Unicode(255))
    S_BL_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_BL_REG = Column(DateTime, server_default=text("(getdate())"))
    S_BL_REGBY = Column(Integer, server_default=text("((1))"))
    S_BL_UPDATE = Column(DateTime)
    S_BL_UPDATEBY = Column(Integer)


class SBUSINESSLINEREGION(Base):
    __tablename__ = "S_BUSINESSLINE_REGION"
    __table_args__ = {"schema": "dbo"}

    S_BLR_ID = Column(Integer, primary_key=True)
    S_BL_ID = Column(Integer)
    S_BLR_NAME = Column(Unicode(255))
    S_BLR_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_BLR_REG = Column(DateTime, server_default=text("(getdate())"))
    S_BLR_REGBY = Column(Integer, server_default=text("((1))"))
    S_BLR_UPDATE = Column(DateTime)
    S_BLR_UPDATEBY = Column(Integer)


class SBUSINESSLINEREGIONTEAM(Base):
    __tablename__ = "S_BUSINESSLINE_REGION_TEAM"
    __table_args__ = {"schema": "dbo"}

    S_BLRT_ID = Column(Integer, primary_key=True)
    S_BLR_ID = Column(Integer)
    S_BLRT_NAME = Column(Unicode(255))
    S_BLRT_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_BLRT_REG = Column(DateTime, server_default=text("(getdate())"))
    S_BLRT_REGBY = Column(Integer, server_default=text("((1))"))
    S_BLRT_UPDATE = Column(DateTime)
    S_BLRT_UPDATEBY = Column(Integer)


class SCUSTOMER(Base):
    __tablename__ = "S_CUSTOMER"
    __table_args__ = {"schema": "dbo"}

    S_CU_ID = Column(Integer, primary_key=True)
    S_CU_NAME = Column(Unicode(255))
    S_CU_COUNTRY = Column(Unicode(3))
    S_CU_STREET = Column(Unicode(100))
    S_CU_CITY = Column(Unicode(100))
    S_CU_ZIPCODE = Column(Unicode(100))
    S_CU_FAX = Column(Unicode(100))
    S_CU_PHONE = Column(Unicode(100))
    S_CU_EMAIL = Column(Unicode(100))
    S_CU_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_CU_REG = Column(DateTime, server_default=text("(getdate())"))
    S_CU_REGBY = Column(Integer, server_default=text("((1))"))
    S_CU_UPDATE = Column(DateTime)
    S_CU_UPDATEBY = Column(Integer)


class SDEFAULTCONTRACT(Base):
    __tablename__ = "S_DEFAULT_CONTRACT"
    __table_args__ = {"schema": "dbo"}

    S_DC_ID = Column(Integer, primary_key=True)
    S_DC_NAME_EN = Column(Unicode(255))
    S_DC_ORDER = Column(Integer)
    S_DC_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_DC_REG = Column(DateTime, server_default=text("(getdate())"))
    S_DC_REGBY = Column(Integer, server_default=text("((1))"))
    S_DC_UPDATE = Column(DateTime)
    S_DC_UPDATEBY = Column(Integer)


class SDEFAULTCONTRACTELEMENT(Base):
    __tablename__ = "S_DEFAULT_CONTRACT_ELEMENTS"
    __table_args__ = {"schema": "dbo"}

    S_DCE_ID = Column(Integer, primary_key=True)
    S_DC_ID = Column(Integer)
    S_DCE_NAME_EN = Column(Unicode(255))
    S_DCE_ORDER = Column(Integer)
    S_DCE_SHOW_NA = Column(BIT)
    S_DCE_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_DCE_REG = Column(DateTime, server_default=text("(getdate())"))
    S_DCE_REGBY = Column(Integer, server_default=text("((1))"))
    S_DCE_UPDATE = Column(DateTime)
    S_DCE_UPDATEBY = Column(Integer)


class SDEFAULTPRODUCTDETAIL(Base):
    __tablename__ = "S_DEFAULT_PRODUCTDETAILS"
    __table_args__ = {"schema": "dbo"}

    S_DPD_ID = Column(Integer, primary_key=True)
    S_PS_ID = Column(Integer)
    S_DPD_NAME_EN = Column(Unicode(255))
    S_DPD_FAMILYGROUP = Column(BIT, server_default=text("((0))"))
    S_DPD_ORDER = Column(Integer)
    S_DPD_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_DPD_REG = Column(DateTime, server_default=text("(getdate())"))
    S_DPD_REGBY = Column(Integer)
    S_DPD_UPDATE = Column(DateTime)
    S_DPD_UPDATEBY = Column(Integer)


class SDEFAULTSERVICE(Base):
    __tablename__ = "S_DEFAULT_SERVICE"
    __table_args__ = {"schema": "dbo"}

    S_DS_ID = Column(Integer, primary_key=True)
    S_DS_NAME = Column(Unicode(256))
    S_TM_ID = Column(Integer)
    S_D_ID = Column(Integer)
    S_DS_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_DS_REG = Column(DateTime, server_default=text("(getdate())"))
    S_DS_REGBY = Column(Integer, server_default=text("((1))"))
    S_DS_UPDATE = Column(DateTime)
    S_DS_UPDATEBY = Column(Integer)


class SDOMAIN(Base):
    __tablename__ = "S_DOMAIN"
    __table_args__ = {"schema": "dbo"}

    S_D_ID = Column(Integer, primary_key=True)
    S_D_NAME = Column(Unicode(255))
    S_D_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_D_REG = Column(DateTime, server_default=text("(getdate())"))
    S_D_REGBY = Column(Integer, server_default=text("((1))"))
    S_D_UPDATE = Column(DateTime)
    S_D_UPDATEBY = Column(Integer)


class SFEATURENAME(Base):
    __tablename__ = "S_FEATURENAME"
    __table_args__ = {"schema": "dbo"}

    S_FN_ID = Column(Integer, primary_key=True)
    S_FN_NAME_EN = Column(Unicode(512))
    S_FN_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_FN_REG = Column(DateTime, server_default=text("(getdate())"))
    S_FN_REGBY = Column(Integer, server_default=text("((1))"))
    S_FN_UPDATE = Column(DateTime)
    S_FN_UPDATEBY = Column(Integer)


t_S_FEATURENAMES_IMPORT = Table(
    "S_FEATURENAMES_IMPORT",
    metadata,
    Column("S_FN_NAME_EN", Unicode(255)),
    schema="dbo",
)


t_S_FEATURES_IMPORT = Table(
    "S_FEATURES_IMPORT",
    metadata,
    Column("S_FN_NAME_EN", Unicode(255)),
    Column("S_FN_INFO_PRICE", Unicode(255)),
    Column("S_FN_PRICE", DECIMAL(18, 2)),
    Column("S_SM_ID", Integer),
    Column("S_FN_ID", Integer),
    schema="dbo",
)


class SPRODUCT(Base):
    __tablename__ = "S_PRODUCT"
    __table_args__ = {"schema": "dbo"}

    S_P_ID = Column(Integer, primary_key=True)
    S_BL_ID = Column(Integer, index=True)
    S_P_NAME_EN = Column(Unicode(255), index=True)
    S_P_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_P_REG = Column(DateTime, server_default=text("(getdate())"))
    S_P_REGBY = Column(Integer, server_default=text("((1))"))
    S_P_UPDATE = Column(DateTime)
    S_P_UPDATEBY = Column(Integer)


class SPRODUCTSUB(Base):
    __tablename__ = "S_PRODUCTSUB"
    __table_args__ = {"schema": "dbo"}

    S_PS_ID = Column(Integer, primary_key=True)
    S_P_ID = Column(Integer, index=True)
    S_PS_NAME_EN = Column(Unicode(255), index=True)
    S_PS_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_PS_REG = Column(DateTime, server_default=text("(getdate())"))
    S_PS_REGBY = Column(Integer, server_default=text("((1))"))
    S_PS_UPDATE = Column(DateTime)
    S_PS_UPDATEBY = Column(Integer)


class SPRODUCTSUBSPECIFIC(Base):
    __tablename__ = "S_PRODUCTSUBSPECIFIC"
    __table_args__ = {"schema": "dbo"}

    S_PSS_ID = Column(Integer, primary_key=True)
    S_PS_ID = Column(Integer, index=True)
    S_PSS_NAME_EN = Column(Unicode(255), index=True)
    S_PSS_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_PSS_REG = Column(DateTime, server_default=text("(getdate())"))
    S_PSS_REGBY = Column(Integer, server_default=text("((1))"))
    S_PSS_UPDATE = Column(DateTime)
    S_PSS_UPDATEBY = Column(Integer)


class SQUOTATION(Base):
    __tablename__ = "S_QUOTATION"
    __table_args__ = {"schema": "dbo"}

    S_Q_ID = Column(Integer, primary_key=True)
    CU_ID = Column(Integer, nullable=False, server_default=text("((1))"))
    S_CU_ID = Column(Integer, nullable=False, server_default=text("((1))"))
    S_Q_SALESMANAGER = Column(Integer)
    S_Q_PRICE = Column(DECIMAL(18, 2))
    S_Q_DISCOUNT = Column(DECIMAL(18, 2))
    S_Q_COMMENT_EN = Column(Unicode(1024))
    S_Q_TASKHOLDER = Column(
        Integer, nullable=False, server_default=text("((1))")
    )
    S_S_ID = Column(Integer, server_default=text("((1))"))
    S_PSS_ID = Column(Integer)
    S_Q_CR_POSITIVE = Column(
        Integer, nullable=False, server_default=text("((0))")
    )
    S_Q_CR_POSITIVE_USER = Column(Integer)
    S_Q_CR_POSITIVE_DATE = Column(DateTime)
    S_Q_CR_POSITIVE_COMMENT = Column(Unicode(512))
    S_Q_CR_SPECIAL = Column(
        Integer, nullable=False, server_default=text("((0))")
    )
    S_Q_CR_SPECIAL_USER = Column(Integer)
    S_Q_CR_SPECIAL_DATE = Column(DateTime)
    S_Q_CR_SPECIAL_COMMENT = Column(Unicode(512))
    S_Q_ATTACHEMENT = Column(IMAGE)
    S_Q_ATTACHEMENT_NAME = Column(Unicode(512))
    S_Q_QUOTATION = Column(IMAGE)
    S_Q_QUOTATION_NAME = Column(Unicode(512))
    S_Q_REG = Column(DateTime, server_default=text("(getdate())"))
    S_Q_REGBY = Column(Integer, server_default=text("((1))"))
    S_Q_UPDATE = Column(DateTime)
    S_Q_UPDATEBY = Column(Integer)


class SQUOTATIONCONTRACT(Base):
    __tablename__ = "S_QUOTATION_CONTRACT"
    __table_args__ = {"schema": "dbo"}

    S_QC_ID = Column(Integer, primary_key=True)
    S_Q_ID = Column(Integer)
    S_DCE_ID = Column(Integer)
    S_QC_COMMENT = Column(Unicode(512))
    S_QC_RESULT = Column(Integer)
    S_QC_REG = Column(DateTime, server_default=text("(getdate())"))
    S_QC_REGBY = Column(Integer, server_default=text("((1))"))
    S_QC_UPDATE = Column(DateTime)
    S_QC_UPDATEBY = Column(Integer)


class SQUOTATIONFEATURE(Base):
    __tablename__ = "S_QUOTATION_FEATURES"
    __table_args__ = {"schema": "dbo"}

    S_QF_ID = Column(Integer, primary_key=True)
    S_Q_ID = Column(Integer)
    S_SMF_ID = Column(Integer)
    S_QF_UNITS = Column(Integer)
    S_QF_PRICE = Column(DECIMAL(18, 2))
    S_QF_DISCOUNTPRICE = Column(DECIMAL(18, 2))
    S_QF_COMMENT_EN = Column(Unicode(1024))
    S_QF_REG = Column(DateTime, server_default=text("(getdate())"))
    S_QF_REGBY = Column(Integer, server_default=text("((1))"))
    S_QF_UPDATE = Column(DateTime)
    S_QF_UPDATEBY = Column(Integer)


class SQUOTATIONPRODUCTDETAIL(Base):
    __tablename__ = "S_QUOTATION_PRODUCTDETAILS"
    __table_args__ = {"schema": "dbo"}

    S_QP_ID = Column(Integer, primary_key=True)
    S_Q_ID = Column(Integer)
    S_PS_ID = Column(Integer)
    S_QP_FAMILY = Column(Integer)
    S_QP_ORDER = Column(Integer)
    S_QP_REG = Column(DateTime, server_default=text("(getdate())"))
    S_QP_REGBY = Column(Integer, server_default=text("((1))"))
    S_QP_UPDATE = Column(DateTime)
    S_QP_UPDATEBY = Column(Integer)


class SQUOTATIONPRODUCTDETAILSELEMENT(Base):
    __tablename__ = "S_QUOTATION_PRODUCTDETAILS_ELEMENTS"
    __table_args__ = {"schema": "dbo"}

    S_QPE_ID = Column(Integer, primary_key=True)
    S_QP_ID = Column(Integer)
    S_DPD_ID = Column(Integer)
    S_QPE_VALUE = Column(Unicode(1024))
    S_QPE_REG = Column(DateTime, server_default=text("(getdate())"))
    S_QPE_REGBY = Column(Integer, server_default=text("((1))"))
    S_QPE_UPDATE = Column(DateTime)
    S_QPE_UPDATEBY = Column(Integer)


class SQUOTATIONSERVICE(Base):
    __tablename__ = "S_QUOTATION_SERVICES"
    __table_args__ = {"schema": "dbo"}

    S_QS_ID = Column(Integer, primary_key=True)
    S_Q_ID = Column(Integer)
    S_SME_ID = Column(Integer)
    S_QS_UNITS = Column(Integer)
    S_QS_PRICE = Column(DECIMAL(18, 2))
    S_QS_DISCOUNTPRICE = Column(DECIMAL(18, 2))
    S_QS_COMMENT_EN = Column(Unicode(1024))
    S_QS_REG = Column(DateTime, server_default=text("(getdate())"))
    S_QS_REGBY = Column(Integer, server_default=text("((1))"))
    S_QS_UPDATE = Column(DateTime)
    S_QS_UPDATEBY = Column(Integer)


class SREGION(Base):
    __tablename__ = "S_REGION"
    __table_args__ = {"schema": "dbo"}

    S_R_ID = Column(Integer, primary_key=True)
    S_R_NAME = Column(Unicode(255))
    S_R_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_R_REG = Column(DateTime, server_default=text("(getdate())"))
    S_R_REGBY = Column(Integer, server_default=text("((1))"))
    S_R_UPDATE = Column(DateTime)
    S_R_UPDATEBY = Column(Integer)


class SREGIONCOUNTRY(Base):
    __tablename__ = "S_REGION_COUNTRY"
    __table_args__ = {"schema": "dbo"}

    S_RC_ID = Column(Integer, primary_key=True)
    S_R_ID = Column(Integer, nullable=False, server_default=text("((1))"))
    S_RC_NAME = Column(Unicode(255))
    S_RC_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_RC_REG = Column(DateTime, server_default=text("(getdate())"))
    S_RC_REGBY = Column(Integer, server_default=text("((1))"))
    S_RC_UPDATE = Column(DateTime)
    S_RC_UPDATEBY = Column(Integer)


class SSERVICEMATRIX(Base):
    __tablename__ = "S_SERVICEMATRIX"
    __table_args__ = {"schema": "dbo"}

    S_SM_ID = Column(Integer, primary_key=True)
    S_DS_ID = Column(Integer)
    S_PSS_ID = Column(Integer)
    S_RC_ID = Column(Integer)
    S_SM_STANDARD = Column(Unicode(512))
    S_SM_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_SM_REG = Column(DateTime, server_default=text("(getdate())"))
    S_SM_REGBY = Column(Integer, server_default=text("((1))"))
    S_SM_UPDATE = Column(DateTime)
    S_SM_UPDATEBY = Column(Integer)


class SSERVICEMATRIXELEMENT(Base):
    __tablename__ = "S_SERVICEMATRIX_ELEMENTS"
    __table_args__ = {"schema": "dbo"}

    S_SME_ID = Column(Integer, primary_key=True)
    S_SM_ID = Column(Integer, index=True)
    S_SN_ID = Column(Integer)
    S_SME_PRICE = Column(DECIMAL(18, 2), server_default=text("((0))"))
    S_SME_PRICECHECK = Column(
        BIT, nullable=False, server_default=text("((0))")
    )
    S_SME_FIXPRICE = Column(BIT, nullable=False, server_default=text("((0))"))
    S_SME_INFO = Column(Unicode(2048))
    S_SME_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_SME_REG = Column(DateTime, server_default=text("(getdate())"))
    S_SME_REGBY = Column(Integer, server_default=text("((1))"))
    S_SME_UPDATE = Column(DateTime)
    S_SME_UPDATEBY = Column(Integer)


class SSERVICEMATRIXFEATURE(Base):
    __tablename__ = "S_SERVICEMATRIX_FEATURES"
    __table_args__ = {"schema": "dbo"}

    S_SMF_ID = Column(Integer, primary_key=True)
    S_SM_ID = Column(Integer)
    S_FN_ID = Column(Integer)
    S_SMF_PRICE = Column(DECIMAL(18, 2), server_default=text("((0))"))
    S_SMF_PRICECHECK = Column(
        BIT, nullable=False, server_default=text("((0))")
    )
    S_SMF_FIXPRICE = Column(BIT, nullable=False, server_default=text("((0))"))
    S_SMF_INFO = Column(Unicode(2048))
    S_SMF_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_SMF_REG = Column(DateTime, server_default=text("(getdate())"))
    S_SMF_REGBY = Column(Integer, server_default=text("((1))"))
    S_SMF_UPDATE = Column(DateTime)
    S_SMF_UPDATEBY = Column(Integer)


class SSERVICENAME(Base):
    __tablename__ = "S_SERVICENAME"
    __table_args__ = {"schema": "dbo"}

    S_SN_ID = Column(Integer, primary_key=True)
    S_SN_NAME_EN = Column(Unicode(255))
    S_SN_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_SN_REG = Column(DateTime, server_default=text("(getdate())"))
    S_SN_REGBY = Column(Integer, server_default=text("((1))"))
    S_SN_UPDATE = Column(DateTime)
    S_SN_UPDATEBY = Column(Integer)


class SSTATU(Base):
    __tablename__ = "S_STATUS"
    __table_args__ = {"schema": "dbo"}

    S_S_ID = Column(Integer, primary_key=True)
    S_S_NAME_EN = Column(Unicode(255))
    S_S_REG = Column(DateTime, server_default=text("(getdate())"))
    S_S_REGBY = Column(Integer, server_default=text("((1))"))
    S_S_UPDATE = Column(DateTime)
    S_S_UPDATEBY = Column(Integer)


class STASK(Base):
    __tablename__ = "S_TASK"
    __table_args__ = {"schema": "dbo"}

    S_T_ID = Column(Integer, primary_key=True)
    S_Q_ID = Column(Integer)
    S_S_ID = Column(Integer)
    S_T_TASK_FOR = Column(Integer)
    S_T_COMMENT = Column(Unicode(2048))
    S_T_DELTA_TIME = Column(
        BigInteger, nullable=False, server_default=text("((0))")
    )
    S_T_REG = Column(DateTime, server_default=text("(getdate())"))
    S_T_REGBY = Column(Integer, server_default=text("((1))"))
    S_T_UPDATE = Column(DateTime)
    S_T_UPDATEBY = Column(Integer)


class STESTMARK(Base):
    __tablename__ = "S_TESTMARK"
    __table_args__ = {"schema": "dbo"}

    S_TM_ID = Column(Integer, primary_key=True)
    S_TM_NAME = Column(Unicode(255))
    S_TM_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_TM_REG = Column(DateTime, server_default=text("(getdate())"))
    S_TM_REGBY = Column(Integer, server_default=text("((1))"))
    S_TM_UPDATE = Column(DateTime)
    S_TM_UPDATEBY = Column(Integer)


class SUSERSSCCT(Base):
    __tablename__ = "S_USERS_SCCT"
    __table_args__ = {"schema": "dbo"}

    S_U_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer, index=True)
    S_BLRT_ID = Column(Integer, index=True)
    S_U_TYPE = Column(Integer, server_default=text("((0))"))
    S_UR_ID = Column(Integer)
    S_UA_ID = Column(Integer, nullable=False, server_default=text("((1))"))
    S_P_ID = Column(
        Integer, nullable=False, index=True, server_default=text("((1))")
    )
    S_U_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))
    S_U_REG = Column(DateTime, server_default=text("(getutcdate())"))
    S_U_REGBY = Column(Integer, server_default=text("((1))"))
    S_U_UPDATE = Column(DateTime)
    S_U_UPDATEBY = Column(Integer)


class SUSERAUTHORIZATION(Base):
    __tablename__ = "S_USER_AUTHORIZATION"
    __table_args__ = {"schema": "dbo"}

    S_UA_ID = Column(Integer, primary_key=True)
    S_UA_NAME_EN = Column(Unicode(90))
    S_UA_REG = Column(DateTime, server_default=text("(getutcdate())"))
    S_UA_REGBY = Column(Integer, server_default=text("((1))"))
    S_UA_UPDATE = Column(DateTime)
    S_UA_UPDATEBY = Column(Integer)


class SUSERROLE(Base):
    __tablename__ = "S_USER_ROLE"
    __table_args__ = {"schema": "dbo"}

    S_UR_ID = Column(Integer, primary_key=True)
    S_UR_DISCOUNT = Column(DECIMAL(18, 2))
    S_UR_NAME_EN = Column(Unicode(90))
    S_UR_REG = Column(DateTime, server_default=text("(getutcdate())"))
    S_UR_REGBY = Column(Integer, server_default=text("((1))"))
    S_UR_UPDATE = Column(DateTime)
    S_UR_UPDATEBY = Column(Integer)


class TASK(Base):
    __tablename__ = "TASK"
    __table_args__ = {"schema": "dbo"}

    TA_ID = Column(Integer, primary_key=True)
    TA_REL_ID = Column(Integer)
    TA_TEXT_EN = Column(Unicode(2048))
    TA_COMMENT = Column(Unicode(2048))
    TA_FROM = Column(Integer, index=True)
    TA_TO = Column(Integer, index=True)
    TA_DATE = Column(DateTime, server_default=text("(getdate())"))
    TA_DEADLINE = Column(Date)
    TA_READY = Column(DateTime)
    TA_CHECK = Column(DateTime)
    TA_DELETED = Column(BIT, nullable=False, server_default=text("((0))"))
    TA_UPDATE = Column(DateTime)
    TA_UPDATE_BY = Column(Integer)
    TA_READY_BY = Column(Integer)
    TA_CHECK_BY = Column(Integer)
    TA_TYPE = Column(Integer, nullable=False, server_default=text("((0))"))


class TEMPDEFAULTITEM(Base):
    __tablename__ = "TEMP_DEFAULT_ITEM"
    __table_args__ = {"schema": "dbo"}

    TDI_ID = Column(Integer, primary_key=True)
    TDI_RANDOM = Column(Unicode(50))
    TDI_NUMBER = Column(Integer)
    TDI_NAME_DE = Column(Unicode(100))
    TDI_NAME_EN = Column(Unicode(100))
    TDI_REQUIREMENT_DE = Column(Unicode(1000))
    TDI_REQUIREMENT_EN = Column(Unicode(1000))
    TDI_REQUIREMENT_FR = Column(Unicode(1000))
    TDI_HIDE_COL1 = Column(BIT, nullable=False)
    TDI_TITLE = Column(BIT)
    TDI_INDENT = Column(Integer)
    TDI_SUBCLAUSE = Column(Unicode(512))
    TDI_REG = Column(DateTime, server_default=text("(getdate())"))
    TDI_REGBY = Column(Integer)


class TEMPNAVPACKAGE(Base):
    __tablename__ = "TEMP_NAV_PACKAGE"
    __table_args__ = {"schema": "dbo"}

    TNP_ID = Column(Integer, primary_key=True)
    TNP_RANDOM = Column(Unicode(50))
    NP_ID = Column(Integer)
    TNP_REG = Column(DateTime, server_default=text("(getdate())"))
    TNP_REGBY = Column(Integer)


class TEMPNAVPACKAGEELEMENT(Base):
    __tablename__ = "TEMP_NAV_PACKAGE_ELEMENT"
    __table_args__ = {"schema": "dbo"}

    TNPE_ID = Column(Integer, primary_key=True)
    TNPE_RANDOM = Column(Unicode(20))
    NPE_ID = Column(Integer)
    TNPE_REG = Column(DateTime, server_default=text("(getdate())"))
    TNPE_REGBY = Column(Integer)


class TESTLEVEL(Base):
    __tablename__ = "TESTLEVEL"
    __table_args__ = {"schema": "dbo"}

    TLEV_ID = Column(Integer, primary_key=True)
    TLEV_ACTIVE = Column(BIT)
    TPT_ID = Column(Integer)
    TLEV_NAME_DE = Column(Unicode(90))
    TLEV_NAME_EN = Column(CHAR(10, "Latin1_General_CI_AS"))
    TLEV_SHORT = Column(Unicode(12))
    TLEV_NUMBER = Column(Integer)
    TLEV_REG = Column(DateTime)
    TLEV_REGBY = Column(Integer)
    TLEV_UPDATE = Column(DateTime)
    TLEV_UPDATEBY = Column(Integer)


class TESTPERSON(Base):
    __tablename__ = "TESTPERSON"
    __table_args__ = {"schema": "dbo"}

    TPER_ID = Column(Integer, primary_key=True)
    TPER_LEVEL = Column(Integer)
    TPER_NAME_DE = Column(Unicode(30))
    TPER_NAME_EN = Column(Unicode(30))


t_TEST_RESULT = Table(
    "TEST_RESULT",
    metadata,
    Column("Total", BigInteger),
    Column("DI_ID", Integer),
    Column("Passed", Integer),
    Column("Failed", Integer),
    schema="dbo",
)


class TEXTELEMENT(Base):
    __tablename__ = "TEXTELEMENT"
    __table_args__ = {"schema": "dbo"}

    TE_ID = Column(Integer, primary_key=True)
    TE_TEXT_DE = Column(Unicode(1000))
    TE_TEXT_EN = Column(Unicode(1000))
    TE_TEXT_FR = Column(Unicode(1000))
    TT_ID = Column(Integer)
    TE_REG = Column(DateTime)
    TE_REGBY = Column(Integer)
    TE_UPDATE = Column(DateTime)
    TE_UPDATEBY = Column(Integer)


class TEXTELEMENTTYPE(Base):
    __tablename__ = "TEXTELEMENT_TYPE"
    __table_args__ = {"schema": "dbo"}

    TT_ID = Column(Integer, primary_key=True)
    TT_NAME_DE = Column(Unicode(20))
    TT_NAME_EN = Column(Unicode(20))
    TT_SHOW_OWN = Column(BIT)


class TEXTHELP(Base):
    __tablename__ = "TEXTHELP"
    __table_args__ = {"schema": "dbo"}

    TH_ID = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, index=True)
    THT_ID = Column(Integer)
    TH_TEXT_DE = Column(Unicode(1000))
    TH_TEXT_EN = Column(Unicode(1000))
    TH_TEXT_FR = Column(Unicode(1000))
    TH_REG = Column(DateTime)
    TH_REGBY = Column(Integer)
    TH_UPDATE = Column(DateTime)
    TH_UPDATEBY = Column(Integer)


class TEXTHELPTYPE(Base):
    __tablename__ = "TEXTHELP_TYPE"
    __table_args__ = {"schema": "dbo"}

    THT_ID = Column(Integer, primary_key=True)
    THT_NAME_DE = Column(Unicode(20))
    THT_NAME_EN = Column(Unicode(20))


class TRANSEDOC(Base):
    __tablename__ = "TRANSEDOC"
    __table_args__ = {"schema": "dbo"}

    TE_ID = Column(Integer, primary_key=True)
    TE_NAME = Column(Unicode(50))
    HEAD_ID = Column(Integer)
    TE_YN_SYMBOL = Column(BIT, nullable=False, server_default=text("(1)"))
    E_ID = Column(Integer, index=True)


class TRANSEDOCMODULE(Base):
    __tablename__ = "TRANSEDOC_MODULE"
    __table_args__ = {"schema": "dbo"}

    TEM_ID = Column(Integer, primary_key=True)
    TE_ID = Column(Integer, nullable=False, index=True)
    TEM_NUMBER = Column(Integer, nullable=False)
    DM_ID = Column(Integer, nullable=False)
    TEM_NAME = Column(Unicode(100))


class TRANSEDOCMODULEPHASE(Base):
    __tablename__ = "TRANSEDOC_MODULE_PHASE"
    __table_args__ = {"schema": "dbo"}

    TEMP_ID = Column(Integer, primary_key=True)
    TEM_ID = Column(Integer, nullable=False)
    TE_ID = Column(Integer, nullable=False)
    TEP_ID = Column(Integer, nullable=False)
    ST_ID = Column(Integer, nullable=False, server_default=text("(1)"))
    SO_NUMBER = Column(Integer)


class TRANSEDOCPHASE(Base):
    __tablename__ = "TRANSEDOC_PHASE"
    __table_args__ = {"schema": "dbo"}

    TEP_ID = Column(Integer, primary_key=True)
    TE_ID = Column(Integer, nullable=False, index=True)
    PRP_ID = Column(Integer, nullable=False)
    TEP_PHASE_ORDER = Column(Integer, nullable=False)
    P_ID = Column(Integer)
    TEP_SAP = Column(Unicode(20))


class TYPEOFPROOF(Base):
    __tablename__ = "TYPE_OF_PROOF"
    __table_args__ = {"schema": "dbo"}

    TOP_ID = Column(Integer, primary_key=True)
    TOP_SHORT = Column(Unicode(15))
    TOP_NAME_DE = Column(Unicode(1000))
    TOP_NAME_EN = Column(Unicode(1000))
    TOP_NAME_FR = Column(Unicode(1000))
    GT_ID = Column(Integer)
    TOP_REG = Column(DateTime)
    TOP_REGBY = Column(Integer)
    TOP_UPDATE = Column(DateTime)
    TOP_UPDATEBY = Column(Integer)
    DI_ID = Column(Integer, server_default=text("((1))"))
    TOP_TYPE = Column(Integer, server_default=text("((0))"))
    TOP_SHOWBASE = Column(BIT, server_default=text("((0))"))


class TYPEOFTEST(Base):
    __tablename__ = "TYPE_OF_TEST"
    __table_args__ = {"schema": "dbo"}

    TOT_ID = Column(Integer, primary_key=True)
    TOT_SHORT = Column(Unicode(15))
    TOT_NAME_DE = Column(Unicode(1000))
    TOT_NAME_EN = Column(Unicode(1000))
    TOT_NAME_FR = Column(Unicode(1000))
    GT_ID = Column(Integer)
    TOT_REG = Column(DateTime)
    TOT_REGBY = Column(Integer)
    TOT_UPDATE = Column(DateTime)
    TOT_UPDATEBY = Column(Integer)
    DI_ID = Column(Integer, server_default=text("((1))"))
    TOT_TYPE = Column(Integer, server_default=text("((0))"))
    TOT_SHOWBASE = Column(BIT, server_default=text("((0))"))


t_VERIFICATION_DOCUMENT = Table(
    "VERIFICATION_DOCUMENT",
    metadata,
    Column("VD_ID", Integer, nullable=False),
    Column("VD_TYPE", Integer),
    Column("VD_NAME_DE", Unicode(500)),
    Column("VD_NAME_EN", Unicode(500)),
    Column("VD_NAME_FR", Unicode(500)),
    Column("VD_ORDER", Integer),
    Column("TOP_ID", Integer, nullable=False, server_default=text("((1))")),
    schema="dbo",
)


t_VTEST_DEFAULT_ITEM = Table(
    "VTEST_DEFAULT_ITEM",
    metadata,
    Column("DI_ID", Integer, nullable=False),
    Column("DI_NAME", Unicode(100)),
    Column("DI_REQUIREMENT_DE", Unicode(1000)),
    Column("DI_REQUIREMENT_EN", Unicode(1000)),
    Column("DI_NORM", Unicode(80)),
    Column("STARS", Integer),
    Column("DI_INFO", Unicode(1500)),
    Column("TP_ID", Integer),
    Column("DI_UPDATE", DateTime),
    Column("LAST_UPDATE_BY", Unicode(111)),
    Column("KENNWERTE_DE", Unicode),
    Column("KENNWERTE_EN", Unicode),
    Column("HRC_NAME_DE", Unicode(255)),
    Column("HRC_NAME_EN", Unicode(255)),
    Column("HRP_NAME_DE", Unicode(255)),
    Column("HRP_NAME_EN", Unicode(255)),
    Column("CL_NAME_DE", Unicode(100)),
    Column("CL_NAME_EN", Unicode(100)),
    Column("PFAD_PRODUKT_DE", Unicode),
    Column("PFAD_PRODUKT_EN", Unicode),
    Column("PFAD_LAND_DE", Unicode),
    Column("PFAD_LAND_EN", Unicode),
    schema="dbo",
)


t_VTEST_DEFAULT_ITEM_ANNEX = Table(
    "VTEST_DEFAULT_ITEM_ANNEX",
    metadata,
    Column("DIAX_ID", Integer, nullable=False),
    Column("DI_ID", Integer),
    Column("DIAX_NAME_DE", Unicode(500)),
    Column("DIAX_NAME_EN", Unicode(500)),
    Column("DIAX_NAME_FR", Unicode(500)),
    Column("DIAX_FILENAME", Unicode(255)),
    Column("DIAX_CHECKSUM", Unicode(32)),
    Column("DIAX_DATA", IMAGE),
    schema="dbo",
)


t_VTEST_DEFAULT_ITEM_LINK = Table(
    "VTEST_DEFAULT_ITEM_LINK",
    metadata,
    Column("DIL_ID", Integer, nullable=False),
    Column("DI_ID", Integer),
    Column("DIL_TEXT_DE", Unicode(1024)),
    Column("DIL_TEXT_EN", Unicode(1024)),
    Column("DIL_URL", Unicode(512)),
    schema="dbo",
)


t_V_ALDI_MAIN = Table(
    "V_ALDI_MAIN",
    metadata,
    Column("ALDI_ID", Integer, nullable=False),
    Column("ALDI_MESSAGE_CREATION_DATE", DateTime),
    Column("ALRT_ID", Integer, nullable=False),
    Column("ALRT_NAME", Unicode(100)),
    Column("ALDI_REQUESTID", Integer),
    Column("ALMT_ID", Integer, nullable=False),
    Column("ALMT_NAME", Unicode(100)),
    Column("regby", Unicode(111)),
    Column("ALDI_RESPONSEID", Integer),
    Column("ALDI_INVESTIGATION_NUMBER", Unicode(255)),
    Column("ALDI_INVESTIGATION_ID", Unicode(255)),
    Column("ALDI_INVESTIGATIONPLAN_ID", Unicode(255)),
    Column("ALDI_NEEDED_RESPONSE_DATE", DateTime),
    Column("ALDI_SUPPLIER", Unicode(255)),
    Column("ALDI_PRODUCT", Unicode(255)),
    Column("ALDI_PRODUCTVARIETY", Unicode(255)),
    Column("ALDI_INVESTIGATION_RANGE", Unicode(255)),
    Column("ALDI_INVESTIGATION_THEME", Unicode(255)),
    Column("ALDI_TOTAL_PRICE", Float(53)),
    Column("ALDI_TOTAL_PRICE_UNIT", Unicode(3)),
    Column("ALDI_SAMPLE_AMOUNT", Float(53)),
    Column("ALSU_ID", Integer),
    Column("ALSU_NAME", Unicode(100)),
    Column("ALDI_REMARK", Unicode(800)),
    Column("ALDI_REGDATE", DateTime),
    Column("ALDI_REGBY", Integer),
    Column("P_ID", Integer),
    Column("ALS_ID", Integer, nullable=False),
    Column("ALS_NAME_DE", Unicode(100)),
    schema="dbo",
)


t_V_ANALYZER_52WEEKS = Table(
    "V_ANALYZER_52WEEKS",
    metadata,
    Column("KW", String(33, "Latin1_General_CI_AS")),
    Column("AGENT", Unicode(111)),
    Column("C", DECIMAL(38, 2)),
    Column("NC", DECIMAL(38, 2)),
    Column("Region", Unicode(20)),
    Column("HR_NEW_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_ANALYZER_ACC_NV = Table(
    "V_ANALYZER_ACC_NV",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_NV_KST = Table(
    "V_ANALYZER_ACC_NV_KST",
    metadata,
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_NV_KST_PRODUKTIV = Table(
    "V_ANALYZER_ACC_NV_KST_PRODUKTIV",
    metadata,
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_NV_KST_PRODUKTIV_ASIA = Table(
    "V_ANALYZER_ACC_NV_KST_PRODUKTIV_ASIA",
    metadata,
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_NV_KST_UNPRODUKTIV = Table(
    "V_ANALYZER_ACC_NV_KST_UNPRODUKTIV",
    metadata,
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_NV_KST_UNPRODUKTIV_ASIA = Table(
    "V_ANALYZER_ACC_NV_KST_UNPRODUKTIV_ASIA",
    metadata,
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_NV_PRODUKTIV = Table(
    "V_ANALYZER_ACC_NV_PRODUKTIV",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_NV_PRODUKTIV_ASIA = Table(
    "V_ANALYZER_ACC_NV_PRODUKTIV_ASIA",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_NV_ST = Table(
    "V_ANALYZER_ACC_NV_ST",
    metadata,
    Column("Mitarbeiter", Unicode(111)),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_NV_UNPRODUKTIV = Table(
    "V_ANALYZER_ACC_NV_UNPRODUKTIV",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_NV_UNPRODUKTIV_ASIA = Table(
    "V_ANALYZER_ACC_NV_UNPRODUKTIV_ASIA",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_V = Table(
    "V_ANALYZER_ACC_V",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_V_ASIA = Table(
    "V_ANALYZER_ACC_V_ASIA",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_V_KST = Table(
    "V_ANALYZER_ACC_V_KST",
    metadata,
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_V_KST_ASIA = Table(
    "V_ANALYZER_ACC_V_KST_ASIA",
    metadata,
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_V_KST_MONEY = Table(
    "V_ANALYZER_ACC_V_KST_MONEY",
    metadata,
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("CLEARABLE_EFFORT", MONEY),
    Column("NON_CLEARABLE_EFFORT", MONEY),
    schema="dbo",
)


t_V_ANALYZER_ACC_V_MONEY = Table(
    "V_ANALYZER_ACC_V_MONEY",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("CLEARABLE_EFFORT", MONEY),
    Column("NON_CLEARABLE_EFFORT", MONEY),
    schema="dbo",
)


t_V_ANALYZER_ACC_V_MONEY_ASIA = Table(
    "V_ANALYZER_ACC_V_MONEY_ASIA",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("CLEARABLE_EFFORT", MONEY),
    Column("NON_CLEARABLE_EFFORT", MONEY),
    schema="dbo",
)


t_V_ANALYZER_ACC_V_ST = Table(
    "V_ANALYZER_ACC_V_ST",
    metadata,
    Column("Mitarbeiter", Unicode(111)),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_V_ST_HJ = Table(
    "V_ANALYZER_ACC_V_ST_HJ",
    metadata,
    Column("Mitarbeiter", Unicode(111)),
    Column("Halbjahr", Unicode(8)),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_V_ST_HJ_PIVOT = Table(
    "V_ANALYZER_ACC_V_ST_HJ_PIVOT",
    metadata,
    Column("Name", Unicode(111)),
    Column("2008-1HJ", DECIMAL(38, 2)),
    Column("2008-2HJ", DECIMAL(38, 2)),
    Column("2009-1HJ", DECIMAL(38, 2)),
    Column("2009-2HJ", DECIMAL(38, 2)),
    Column("2010-1HJ", DECIMAL(38, 2)),
    Column("2010-2HJ", DECIMAL(38, 2)),
    Column("2011-1HJ", DECIMAL(38, 2)),
    Column("2011-2HJ", DECIMAL(38, 2)),
    Column("2012-1HJ", DECIMAL(38, 2)),
    Column("2012-2HJ", DECIMAL(38, 2)),
    Column("2013-1HJ", DECIMAL(38, 2)),
    Column("2013-2HJ", DECIMAL(38, 2)),
    Column("SUMME", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_ACC_V_WEEK = Table(
    "V_ANALYZER_ACC_V_WEEK",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Stunden", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_COUNT_PROJECTS = Table(
    "V_ANALYZER_COUNT_PROJECTS",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Anzahl_Projekte", BigInteger),
    Column("Anzahl_UA", BigInteger),
    schema="dbo",
)


t_V_ANALYZER_COUNT_PROJECTS_ASIA = Table(
    "V_ANALYZER_COUNT_PROJECTS_ASIA",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Anzahl_Projekte", BigInteger),
    Column("Anzahl_UA", BigInteger),
    schema="dbo",
)


t_V_ANALYZER_COUNT_PROJECTS_KST = Table(
    "V_ANALYZER_COUNT_PROJECTS_KST",
    metadata,
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Anzahl_Projekte", BigInteger),
    Column("Anzahl_UA", BigInteger),
    schema="dbo",
)


t_V_ANALYZER_COUNT_PROJECTS_KST_ASIA = Table(
    "V_ANALYZER_COUNT_PROJECTS_KST_ASIA",
    metadata,
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("Anzahl_Projekte", BigInteger),
    Column("Anzahl_UA", BigInteger),
    schema="dbo",
)


t_V_ANALYZER_COUNT_SUBORDERS = Table(
    "V_ANALYZER_COUNT_SUBORDERS",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("Anzahl_UA", BigInteger),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("HR_SHORT", Unicode(20)),
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    schema="dbo",
)


t_V_ANALYZER_COUNT_SUBORDERS_ASIA = Table(
    "V_ANALYZER_COUNT_SUBORDERS_ASIA",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("Anzahl_UA", BigInteger),
    Column("Monat", Integer),
    Column("Jahr", Integer),
    Column("HR_SHORT", Unicode(20)),
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    schema="dbo",
)


t_V_ANALYZER_DELAY_CHECK = Table(
    "V_ANALYZER_DELAY_CHECK",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("UA", Integer, nullable=False),
    Column("DatumCHECK", DateTime),
    Column("Termin", DateTime),
    Column("Delta", Integer),
    Column("Jahr", Integer),
    Column("Monat", Integer),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Zeit0", Integer, nullable=False),
    Column("Zeit3", Integer, nullable=False),
    Column("Zeit7", Integer, nullable=False),
    Column("Zeit30", Integer, nullable=False),
    Column("Zeit100", Integer, nullable=False),
    Column("P_HANDLEDBY", Integer),
    Column("P_HANDLEDBY_TEAM", Integer, nullable=False),
    schema="dbo",
)


t_V_ANALYZER_DELAY_CHECK_DEPARTMENT = Table(
    "V_ANALYZER_DELAY_CHECK_DEPARTMENT",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("UA", Integer, nullable=False),
    Column("DatumCHECK", DateTime),
    Column("Termin", DateTime),
    Column("Delta", Integer),
    Column("Jahr", Integer),
    Column("Monat", Integer),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Zeit0", Integer, nullable=False),
    Column("Zeit3", Integer, nullable=False),
    Column("Zeit7", Integer, nullable=False),
    Column("Zeit30", Integer, nullable=False),
    Column("Zeit100", Integer, nullable=False),
    Column("P_HANDLEDBY", Integer),
    Column("KOT_ID", Integer),
    Column("Abteilung", Unicode(20)),
    Column("Abteilung_HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("Region", Unicode(20)),
    Column("P_CUSTOMER_A", Integer),
    Column("P_CUSTOMER_B", Integer),
    schema="dbo",
)


t_V_ANALYZER_DELAY_CHECK_P = Table(
    "V_ANALYZER_DELAY_CHECK_P",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("UA", Integer, nullable=False),
    Column("DatumCHECK", DateTime),
    Column("Termin", DateTime),
    Column("Delta", Integer),
    Column("Jahr", Integer),
    Column("Monat", Integer),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Zeit0", Integer, nullable=False),
    Column("Zeit3", Integer, nullable=False),
    Column("Zeit7", Integer, nullable=False),
    Column("Zeit30", Integer, nullable=False),
    Column("Zeit100", Integer, nullable=False),
    Column("P_HANDLEDBY", Integer),
    Column("P_HANDLEDBY_TEAM", Integer, nullable=False),
    Column("KOT_ID", Integer),
    Column("Region", Unicode(20)),
    Column("Anzahl", BigInteger),
    schema="dbo",
)


t_V_ANALYZER_DELAY_CHECK_P_ASIA = Table(
    "V_ANALYZER_DELAY_CHECK_P_ASIA",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("UA", Integer, nullable=False),
    Column("DatumCHECK", DateTime),
    Column("Termin", DateTime),
    Column("Delta", Integer),
    Column("Jahr", Integer),
    Column("Monat", Integer),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Zeit0", Integer, nullable=False),
    Column("Zeit3", Integer, nullable=False),
    Column("Zeit7", Integer, nullable=False),
    Column("Zeit30", Integer, nullable=False),
    Column("Zeit100", Integer, nullable=False),
    Column("P_HANDLEDBY", Integer),
    Column("P_HANDLEDBY_TEAM", Integer, nullable=False),
    Column("KOT_ID", Integer),
    schema="dbo",
)


t_V_ANALYZER_DELAY_CHECK_UA = Table(
    "V_ANALYZER_DELAY_CHECK_UA",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("UA", Integer, nullable=False),
    Column("DatumCHECK", DateTime),
    Column("Termin", DateTime),
    Column("Delta", Integer),
    Column("Jahr", Integer),
    Column("Monat", Integer),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Zeit0", Integer, nullable=False),
    Column("Zeit3", Integer, nullable=False),
    Column("Zeit7", Integer, nullable=False),
    Column("Zeit30", Integer, nullable=False),
    Column("Zeit100", Integer, nullable=False),
    Column("P_HANDLEDBY", Integer),
    Column("P_HANDLEDBY_TEAM", Integer, nullable=False),
    Column("KOT_ID", Integer),
    Column("Region", Unicode(20)),
    Column("Anzahl", BigInteger),
    schema="dbo",
)


t_V_ANALYZER_DELAY_CHECK_UA_ASIA = Table(
    "V_ANALYZER_DELAY_CHECK_UA_ASIA",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("UA", Integer, nullable=False),
    Column("DatumCHECK", DateTime),
    Column("Termin", DateTime),
    Column("Delta", Integer),
    Column("Jahr", Integer),
    Column("Monat", Integer),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Zeit0", Integer, nullable=False),
    Column("Zeit3", Integer, nullable=False),
    Column("Zeit7", Integer, nullable=False),
    Column("Zeit30", Integer, nullable=False),
    Column("Zeit100", Integer, nullable=False),
    Column("P_HANDLEDBY", Integer),
    Column("P_HANDLEDBY_TEAM", Integer, nullable=False),
    Column("KOT_ID", Integer),
    schema="dbo",
)


t_V_ANALYZER_DELAY_DEADLINE = Table(
    "V_ANALYZER_DELAY_DEADLINE",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("UA", Integer, nullable=False),
    Column("DatumREADY", DateTime),
    Column("Termin", DateTime),
    Column("Delta", Integer),
    Column("Jahr", Integer),
    Column("Monat", Integer),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Zeit0", Integer, nullable=False),
    Column("Zeit3", Integer, nullable=False),
    Column("Zeit7", Integer, nullable=False),
    Column("Zeit30", Integer, nullable=False),
    Column("Zeit100", Integer, nullable=False),
    Column("P_HANDLEDBY", Integer),
    Column("HR_SHORT", Unicode(20)),
    Column("P_HANDLEDBY_TEAM", Integer, nullable=False),
    Column("Region", Unicode(20)),
    Column("KOT_ID", Integer),
    Column("Abteilung", Unicode(20)),
    Column("Abteilung_HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("P_CUSTOMER_A", Integer),
    Column("P_CUSTOMER_B", Integer),
    schema="dbo",
)


t_V_ANALYZER_DELAY_READY = Table(
    "V_ANALYZER_DELAY_READY",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("UA", Integer, nullable=False),
    Column("DatumREADY", DateTime),
    Column("Termin", DateTime),
    Column("Delta", Integer),
    Column("Jahr", Integer),
    Column("Monat", Integer),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Zeit0", Integer, nullable=False),
    Column("Zeit3", Integer, nullable=False),
    Column("Zeit7", Integer, nullable=False),
    Column("Zeit30", Integer, nullable=False),
    Column("Zeit100", Integer, nullable=False),
    Column("P_HANDLEDBY", Integer),
    Column("P_HANDLEDBY_TEAM", Integer, nullable=False),
    Column("Region", Unicode(20)),
    schema="dbo",
)


t_V_ANALYZER_DELAY_READY_ASIA = Table(
    "V_ANALYZER_DELAY_READY_ASIA",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("UA", Integer, nullable=False),
    Column("DatumREADY", DateTime),
    Column("Termin", DateTime),
    Column("Delta", Integer),
    Column("Jahr", Integer),
    Column("Monat", Integer),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Zeit0", Integer, nullable=False),
    Column("Zeit3", Integer, nullable=False),
    Column("Zeit7", Integer, nullable=False),
    Column("Zeit30", Integer, nullable=False),
    Column("Zeit100", Integer, nullable=False),
    Column("P_HANDLEDBY", Integer),
    Column("P_HANDLEDBY_TEAM", Integer, nullable=False),
    schema="dbo",
)


t_V_ANALYZER_DELAY_READY_P = Table(
    "V_ANALYZER_DELAY_READY_P",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("UA", Integer, nullable=False),
    Column("DatumREADY", DateTime),
    Column("Termin", DateTime),
    Column("Delta", Integer),
    Column("Jahr", Integer),
    Column("Monat", Integer),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Zeit0", Integer, nullable=False),
    Column("Zeit3", Integer, nullable=False),
    Column("Zeit7", Integer, nullable=False),
    Column("Zeit30", Integer, nullable=False),
    Column("Zeit100", Integer, nullable=False),
    Column("P_HANDLEDBY", Integer),
    Column("P_HANDLEDBY_TEAM", Integer, nullable=False),
    Column("KOT_ID", Integer),
    Column("Region", Unicode(20)),
    Column("Anzahl", BigInteger),
    schema="dbo",
)


t_V_ANALYZER_DELAY_READY_P_ASIA = Table(
    "V_ANALYZER_DELAY_READY_P_ASIA",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("UA", Integer, nullable=False),
    Column("DatumREADY", DateTime),
    Column("Termin", DateTime),
    Column("Delta", Integer),
    Column("Jahr", Integer),
    Column("Monat", Integer),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Zeit0", Integer, nullable=False),
    Column("Zeit3", Integer, nullable=False),
    Column("Zeit7", Integer, nullable=False),
    Column("Zeit30", Integer, nullable=False),
    Column("Zeit100", Integer, nullable=False),
    Column("P_HANDLEDBY", Integer),
    Column("P_HANDLEDBY_TEAM", Integer, nullable=False),
    Column("KOT_ID", Integer),
    schema="dbo",
)


t_V_ANALYZER_DELAY_READY_UA = Table(
    "V_ANALYZER_DELAY_READY_UA",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("UA", Integer, nullable=False),
    Column("DatumREADY", DateTime),
    Column("Termin", DateTime),
    Column("Delta", Integer),
    Column("Jahr", Integer),
    Column("Monat", Integer),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Zeit0", Integer, nullable=False),
    Column("Zeit3", Integer, nullable=False),
    Column("Zeit7", Integer, nullable=False),
    Column("Zeit30", Integer, nullable=False),
    Column("Zeit100", Integer, nullable=False),
    Column("P_HANDLEDBY", Integer),
    Column("P_HANDLEDBY_TEAM", Integer, nullable=False),
    Column("KOT_ID", Integer),
    Column("Region", Unicode(20)),
    Column("Anzahl", BigInteger),
    schema="dbo",
)


t_V_ANALYZER_DELAY_READY_UA_ASIA = Table(
    "V_ANALYZER_DELAY_READY_UA_ASIA",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("UA", Integer, nullable=False),
    Column("DatumREADY", DateTime),
    Column("Termin", DateTime),
    Column("Delta", Integer),
    Column("Jahr", Integer),
    Column("Monat", Integer),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("Zeit0", Integer, nullable=False),
    Column("Zeit3", Integer, nullable=False),
    Column("Zeit7", Integer, nullable=False),
    Column("Zeit30", Integer, nullable=False),
    Column("Zeit100", Integer, nullable=False),
    Column("P_HANDLEDBY", Integer),
    Column("P_HANDLEDBY_TEAM", Integer, nullable=False),
    Column("KOT_ID", Integer),
    schema="dbo",
)


t_V_ANALYZER_FORECAST = Table(
    "V_ANALYZER_FORECAST",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("SO_FORECAST", DECIMAL(18, 2)),
    Column("SO_DEADLINE", DateTime),
    Column("MyStatus", Integer, nullable=False),
    Column("ST_ID", Integer),
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_NEW_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_ANALYZER_FORECAST_12WEEKS = Table(
    "V_ANALYZER_FORECAST_12WEEKS",
    metadata,
    Column("Team", Unicode(10)),
    Column("KW", Integer),
    Column("sumFC", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_FORECAST_12WEEKS_AVIS = Table(
    "V_ANALYZER_FORECAST_12WEEKS_AVIS",
    metadata,
    Column("Team", Unicode(20)),
    Column("KW", Integer),
    Column("sumFC", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_FORECAST_12WEEKS_ONLY_WAIT = Table(
    "V_ANALYZER_FORECAST_12WEEKS_ONLY_WAIT",
    metadata,
    Column("Team", Unicode(10)),
    Column("KW", Integer),
    Column("sumFC", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_FORECAST_12WEEKS_WITH_WAIT = Table(
    "V_ANALYZER_FORECAST_12WEEKS_WITH_WAIT",
    metadata,
    Column("Team", Unicode(10)),
    Column("KW", Integer),
    Column("sumFC", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_ANALYZER_FORECAST_ASIA = Table(
    "V_ANALYZER_FORECAST_ASIA",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("SO_FORECAST", DECIMAL(18, 2)),
    Column("SO_DEADLINE", DateTime),
    Column("MyStatus", Integer, nullable=False),
    Column("ST_ID", Integer),
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_NEW_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_ANALYZER_MATERIAL = Table(
    "V_ANALYZER_MATERIAL",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("ZM_ID", String(18, "SQL_Latin1_General_CP1_CI_AS")),
    schema="dbo",
)


t_V_ANALYZER_P = Table(
    "V_ANALYZER_P",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("P_PRODUCT", Unicode(255), nullable=False),
    Column("P_MODEL", Unicode(255), nullable=False),
    Column("ACTION_QUOTESENT", DateTime),
    Column("P_AUDIT_DATE", DateTime),
    Column("ACTION_AUDITPLAN", DateTime),
    Column("AUDIT_ONSITE", DateTime),
    Column("ACTION_REPORTSENT", DateTime),
    Column("STARTDATE", DateTime),
    Column("ACTION_PROOFDOCUMENTS", DateTime),
    Column("TESTSAMPLE", DateTime),
    Column("STORIX", DateTime),
    Column("PROJECTCOORDINATION", DateTime),
    Column("CATEGORY_ID", Integer, nullable=False),
    Column("NAME", Unicode(256), nullable=False),
    Column("CATEGORY_PARENT_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_ANALYZER_PIPE = Table(
    "V_ANALYZER_PIPE",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("P_PRODUCT", Unicode(255), nullable=False),
    Column("P_MODEL", Unicode(255), nullable=False),
    Column("TEAM_HR_SHORT", Unicode(20)),
    Column("TEAM_HR_NEW_ID", Integer, nullable=False),
    Column("DEPARTMENT_HR_SHORT", Unicode(20)),
    Column("DEPARTMENT_HR_NEW_ID", Integer, nullable=False),
    Column("WC_HR_SHORT", Unicode(20)),
    Column("WC_HR_NEW_ID", Integer, nullable=False),
    Column("BRANCH_HR_SHORT", Unicode(20)),
    Column("BRANCH_HR_NEW_ID", Integer, nullable=False),
    Column("REGION_HR_SHORT", Unicode(20)),
    Column("REGION_HR_NEW_ID", Integer, nullable=False),
    Column("P_DATE_ORDER", DateTime),
    Column("YEAR_ORDER", Integer),
    Column("MONTH_ORDER", Integer),
    Column("WEEK_ORDER", Integer),
    Column("QUARTER_ORDER", Unicode(62)),
    Column("HY_ORDER", Unicode(34)),
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("P_DATE_DONE", DateTime),
    Column("ACTION_TEST_STARTED", DateTime),
    Column("DELTA_ORDER_STARTED", Integer),
    Column("P_DATE_READY", DateTime),
    Column("CU_ID", Integer, nullable=False),
    Column("CU_NAME", Unicode(165), nullable=False),
    Column("P_DATE_CHECK", DateTime),
    Column("DELTA_READY_TO_CHECK", Integer),
    Column("YEAR_READY", Integer),
    Column("MONTH_READY", Integer),
    Column("WEEK_READY", Integer),
    Column("QUARTER_READY", Unicode(62)),
    Column("HY_READY", Unicode(34)),
    Column("DELTA_CHECK_TO_DONE", Integer),
    Column("YEAR_CHECK", Integer),
    Column("MONTH_CHECK", Integer),
    Column("WEEK_CHECK", Integer),
    Column("QUARTER_CHECK", Unicode(62)),
    Column("HY_CHECK", Unicode(34)),
    Column("YEAR_TEST_STARTED", Integer),
    Column("MONTH_TEST_STARTED", Integer),
    Column("WEEK_TEST_STARTED", Integer),
    Column("QUARTER_TEST_STARTED", Unicode(62)),
    Column("HY_TEST_STARTED", Unicode(34)),
    Column("DELTA_TEST_STARTED_TO_FINISHED", Integer),
    Column("ACTION_TEST_FINISHED", DateTime),
    Column("ACTION_LAST_REPORT", DateTime),
    Column("YEAR_ACTION_TEST_FINISHED", Integer),
    Column("MONTH_ACTION_TEST_FINISHED", Integer),
    Column("WEEK_ACTION_TEST_FINISHED", Integer),
    Column("QUARTER_ACTION_TEST_FINISHED", Unicode(62)),
    Column("HY_ACTION_TEST_FINISHED", Unicode(34)),
    Column("DELTA_TEST_FINISHED_TO_READY", Integer),
    Column("DELTA_TEST_FINISHED_TO_LAST_REPORT", Integer),
    Column("P_REGDATE", DateTime),
    Column("YEAR_REG", Integer),
    Column("MONTH_REG", Integer),
    Column("WEEK_REG", Integer),
    Column("QUARTER_REG", Unicode(62)),
    Column("HY_REG", Unicode(34)),
    Column("DELTA_REG_STARTED", Integer),
    Column("ACTION_LAST_REPORT_ALL", DateTime),
    Column("DELTA_REG_LAST_REPORT_ALL", Integer),
    Column("DELTA_CHECK_LAST_REPORT_ALL", Integer),
    Column("PROJECTMANAGER", Unicode(111)),
    Column("HANDLEDBY", Unicode(111)),
    Column("MATERIAL", String(18, "SQL_Latin1_General_CP1_CI_AS")),
    Column("P_DEADLINE", DateTime),
    Column("DELR_ID", Integer),
    Column("DELR_NAME_EN", Unicode(256)),
    Column("CATEGORY_ID", Integer, nullable=False),
    Column("CATEGORY_NAME", Unicode(256), nullable=False),
    Column("CATEGORY_ID_PARENT", Integer, nullable=False),
    Column("CATEGORY_NAME_PARENT", Unicode(256), nullable=False),
    schema="dbo",
)


t_V_ANALYZER_PIPE_CUSTOMER = Table(
    "V_ANALYZER_PIPE_CUSTOMER",
    metadata,
    Column("CU_ID", Integer, nullable=False),
    Column("CU_NAME", Unicode(165), nullable=False),
    Column("REGION_HR_NEW_ID", Integer, nullable=False),
    Column("REGION_HR_SHORT", Unicode(20)),
    Column("Anzahl", BigInteger),
    schema="dbo",
)


t_V_ANALYZER_PIPE_II = Table(
    "V_ANALYZER_PIPE_II",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("P_PRODUCT", Unicode(255), nullable=False),
    Column("P_MODEL", Unicode(255), nullable=False),
    Column("TEAM_HR_SHORT", Unicode(20)),
    Column("TEAM_HR_NEW_ID", Integer, nullable=False),
    Column("DEPARTMENT_HR_SHORT", Unicode(20)),
    Column("DEPARTMENT_HR_NEW_ID", Integer, nullable=False),
    Column("WC_HR_SHORT", Unicode(20)),
    Column("WC_HR_NEW_ID", Integer, nullable=False),
    Column("BRANCH_HR_SHORT", Unicode(20)),
    Column("BRANCH_HR_NEW_ID", Integer, nullable=False),
    Column("REGION_HR_SHORT", Unicode(20)),
    Column("REGION_HR_NEW_ID", Integer, nullable=False),
    Column("P_DATE_ORDER", DateTime),
    Column("YEAR_ORDER", Integer),
    Column("MONTH_ORDER", Integer),
    Column("WEEK_ORDER", Integer),
    Column("QUARTER_ORDER", Unicode(62)),
    Column("HY_ORDER", Unicode(34)),
    Column("CU_ID", Integer, nullable=False),
    Column("CU_NAME", Unicode(165), nullable=False),
    Column("MATERIAL", String(18, "SQL_Latin1_General_CP1_CI_AS")),
    Column("PROJECTMANAGER", Unicode(111)),
    Column("HANDLEDBY", Unicode(111)),
    Column("ACTION_QUOTESENT", DateTime),
    Column("P_AUDIT_DATE", DateTime),
    Column("DELTA_AUDIT_QUOTESENT", Integer),
    Column("QUOTESENT_OK", Unicode(6), nullable=False),
    Column("GESETZT", Integer, nullable=False),
    Column("DELTA_AUDIT_GETDATE", Integer),
    Column("CAT_QUOTESENT", Unicode(14), nullable=False),
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("P_REGDATE", DateTime),
    Column("P_DATE_READY", DateTime),
    Column("P_PROJECTMANAGER", Integer),
    Column("P_DATE_CHECK", DateTime),
    Column("ACTION_AUDITPLAN", DateTime),
    Column("DELTA_AUDIT_AUDITPLAN", Integer),
    Column("CAT_AUDITPLAN", Unicode(14), nullable=False),
    Column("AUDIT_ONSITE", DateTime),
    Column("CATEGORY_ID", Integer, nullable=False),
    Column("CATEGORY_NAME", Unicode(256), nullable=False),
    Column("CATEGORY_PARENT_ID", Integer, nullable=False),
    Column("CATEGORY_PARENT_NAME", Unicode(256), nullable=False),
    schema="dbo",
)


t_V_ANALYZER_PIPE_III = Table(
    "V_ANALYZER_PIPE_III",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("P_PRODUCT", Unicode(255), nullable=False),
    Column("P_MODEL", Unicode(255), nullable=False),
    Column("TEAM_HR_SHORT", Unicode(20)),
    Column("TEAM_HR_NEW_ID", Integer, nullable=False),
    Column("DEPARTMENT_HR_SHORT", Unicode(20)),
    Column("DEPARTMENT_HR_NEW_ID", Integer, nullable=False),
    Column("WC_HR_SHORT", Unicode(20)),
    Column("WC_HR_NEW_ID", Integer, nullable=False),
    Column("BRANCH_HR_SHORT", Unicode(20)),
    Column("BRANCH_HR_NEW_ID", Integer, nullable=False),
    Column("REGION_HR_SHORT", Unicode(20)),
    Column("REGION_HR_NEW_ID", Integer, nullable=False),
    Column("CU_ID", Integer, nullable=False),
    Column("CU_NAME", Unicode(165), nullable=False),
    Column("MATERIAL", String(18, "SQL_Latin1_General_CP1_CI_AS")),
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("P_REGDATE", DateTime),
    Column("P_DATE_READY", DateTime),
    Column("P_PROJECTMANAGER", Integer),
    Column("P_DATE_CHECK", DateTime),
    Column("P_DATE_ORDER", DateTime),
    Column("YEAR_ORDER", Integer),
    Column("MONTH_ORDER", Integer),
    Column("WEEK_ORDER", Integer),
    Column("QUARTER_ORDER", Unicode(62)),
    Column("HY_ORDER", Unicode(34)),
    Column("PROJECTMANAGER", Unicode(111)),
    Column("HANDLEDBY", Unicode(111)),
    Column("P_AUDIT_DATE", DateTime),
    Column("DELTA_QUOTESENT_AUDITDATE", Integer),
    Column(
        "CAT_QUOTESENT", String(13, "Latin1_General_CI_AS"), nullable=False
    ),
    Column("ACTION_AUDITPLAN", DateTime),
    Column("DELTA_AUDITPLAN_AUDITDATE", Integer),
    Column(
        "CAT_AUDITPLAN", String(13, "Latin1_General_CI_AS"), nullable=False
    ),
    Column("STARTDATE", DateTime),
    Column("ACTION_QUOTESENT", DateTime),
    Column("DELTA_STARTDATE_QUOTESENT", Integer),
    Column(
        "CAT_STARTDATE_QUOTESENT",
        String(13, "Latin1_General_CI_AS"),
        nullable=False,
    ),
    Column("AUDIT_ONSITE", DateTime),
    Column("ACTION_REPORTSENT", DateTime),
    Column("DELTA_AUDITONSITE_REPORTSENT", Integer),
    Column(
        "CAT_REPORTSENT", String(13, "Latin1_General_CI_AS"), nullable=False
    ),
    Column("STORIX", DateTime),
    Column("ACTION_PROOFDOCUMENTS", DateTime),
    Column("DELTA_PROOFDOCUMENTS_STORIX", Integer),
    Column(
        "CAT_PROOFDOCUMENTS",
        String(13, "Latin1_General_CI_AS"),
        nullable=False,
    ),
    Column("PROJECTCOORDINATION", DateTime),
    Column("DELTA_STORIX_PROJECTCOORDINATION", Integer),
    Column(
        "CAT_PROJECTCOORDINATION",
        String(13, "Latin1_General_CI_AS"),
        nullable=False,
    ),
    Column("CATEGORY_ID", Integer, nullable=False),
    Column("CATEGORY_NAME", Unicode(256), nullable=False),
    Column("CATEGORY_ID_PARENT", Integer, nullable=False),
    Column("CATEGORY_NAME_PARENT", Unicode(256), nullable=False),
    schema="dbo",
)


t_V_ANALYZER_PIPE_II_AUDIT_ONSIDE = Table(
    "V_ANALYZER_PIPE_II_AUDIT_ONSIDE",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("AUDIT_ONSITE", DateTime),
    schema="dbo",
)


t_V_ANALYZER_PIPE_SO = Table(
    "V_ANALYZER_PIPE_SO",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("SO_NUMBER", Integer, nullable=False),
    Column("P_PRODUCT", Unicode(255), nullable=False),
    Column("P_MODEL", Unicode(255), nullable=False),
    Column("CU_ID", Integer, nullable=False),
    Column("CU_NAME", Unicode(165), nullable=False),
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("ST_ID_TEAM", Integer),
    Column("TEAM_HR_SHORT", Unicode(20)),
    Column("TEAM_HR_NEW_ID", Integer, nullable=False),
    Column("DEPARTMENT_HR_SHORT", Unicode(20)),
    Column("DEPARTMENT_HR_NEW_ID", Integer, nullable=False),
    Column("WC_HR_SHORT", Unicode(20)),
    Column("WC_HR_NEW_ID", Integer, nullable=False),
    Column("BRANCH_HR_SHORT", Unicode(20)),
    Column("BRANCH_HR_NEW_ID", Integer, nullable=False),
    Column("REGION_HR_SHORT", Unicode(20)),
    Column("REGION_HR_NEW_ID", Integer, nullable=False),
    Column("SO_DISABLED", BIT, nullable=False),
    Column("SO_WAIT", BIT),
    Column("P_ACTION", BIT),
    Column("SO_DATE_READY", DateTime),
    Column("SO_DATE_CHECK", DateTime),
    Column("YEAR_READY", Integer),
    Column("MONTH_READY", Integer),
    Column("WEEK_READY", Integer),
    Column("QUARTER_READY", Unicode(62)),
    Column("HY_READY", Unicode(34)),
    Column("ACTION_TEST_STARTED", DateTime),
    Column("ACTION_TEST_FINISHED", DateTime),
    Column("YEAR_TEST_STARTED", Integer),
    Column("MONTH_TEST_STARTED", Integer),
    Column("WEEK_TEST_STARTED", Integer),
    Column("QUARTER_TEST_STARTED", Unicode(62)),
    Column("HY_TEST_STARTED", Unicode(34)),
    Column("YEAR_ACTION_TEST_FINISHED", Integer),
    Column("MONTH_ACTION_TEST_FINISHED", Integer),
    Column("WEEK_ACTION_TEST_FINISHED", Integer),
    Column("QUARTER_ACTION_TEST_FINISHED", Unicode(62)),
    Column("HY_ACTION_TEST_FINISHED", Unicode(34)),
    Column("DELTA_READY_TO_CHECK", Integer),
    Column("DELTA_TEST_FINISHED_TO_READY", Integer),
    Column("DELTA_TEST_STARTED_TO_FINISHED", Integer),
    Column("P_DATE_DONE", DateTime),
    Column("PROJECTMANAGER", Unicode(111)),
    Column("HANDLEDBY", Unicode(111)),
    Column("MATERIAL", String(18, "SQL_Latin1_General_CP1_CI_AS")),
    Column("P_REGDATE", DateTime),
    Column("SO_DEADLINE", DateTime),
    Column("ACTION_REPORT_SEND", DateTime),
    Column("DELTA_REG_TO_REPORT", Integer),
    Column("YEAR_REG", Integer),
    Column("MONTH_REG", Integer),
    Column("WEEK_REG", Integer),
    Column("QUARTER_REG", Unicode(62)),
    Column("HY_REG", Unicode(34)),
    Column("DELTA_REG_TO_TEST_STARTED", Integer),
    Column("DELR_ID", Integer),
    Column("DELR_NAME_EN", Unicode(256)),
    Column("CATEGORY_ID", Integer, nullable=False),
    Column("CATEGORY_NAME", Unicode(256), nullable=False),
    Column("CATEGORY_ID_PARENT", Integer, nullable=False),
    Column("CATEGORY_NAME_PARENT", Unicode(256), nullable=False),
    schema="dbo",
)


t_V_ANALYZER_P_DURATION = Table(
    "V_ANALYZER_P_DURATION",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("ACTION_QUOTESENT", DateTime),
    Column("P_AUDIT_DATE", DateTime),
    Column("DELTA_QUOTESENT_AUDITDATE", Integer),
    Column("ACTION_AUDITPLAN", DateTime),
    Column("DELTA_AUDITPLAN_AUDITDATE", Integer),
    Column("DELTA_AUDITPLAN_AUDITDATE_WD", Integer),
    Column("AUDIT_ONSITE", DateTime),
    Column("ACTION_REPORTSENT", DateTime),
    Column("DELTA_AUDITONSITE_REPORTSENT", Integer),
    Column("STARTDATE", DateTime),
    Column("DELTA_STARTDATE_QUOTESENT", Integer),
    Column("STORIX", DateTime),
    Column("ACTION_PROOFDOCUMENTS", DateTime),
    Column("DELTA_PROOFDOCUMENTS_STORIX", Integer),
    Column("PROJECTCOORDINATION", DateTime),
    Column("DELTA_STORIX_PROJECTCOORDINATION", Integer),
    schema="dbo",
)


t_V_ANALYZER_SKPI = Table(
    "V_ANALYZER_SKPI",
    metadata,
    Column("CU_NAME", Unicode(165), nullable=False),
    Column("P_ID", Integer, nullable=False),
    Column("P_PRODUCT", Unicode(255)),
    Column("SO_NUMBER", Integer, nullable=False),
    Column("IS_KPI", String(1, "Latin1_General_CI_AS"), nullable=False),
    Column("S_KPI_NUMBER", Integer),
    Column("SO_PREDATE", DateTime),
    Column("FirstAccounting", DateTime),
    Column("SO_DEADLINE", DateTime),
    Column("SO_DATE_READY", DateTime),
    Column("P_AUDIT_DATE", DateTime),
    Column("P_ZARA_NUMBER", Unicode(10)),
    Column("SO_MODEL", Unicode(255)),
    Column("SO_TASK", Unicode(1024)),
    Column("TEAM", Unicode(20)),
    Column("DEPARTMENT", Unicode(20)),
    Column("WC", Unicode(20)),
    Column("BRANCH", Unicode(20)),
    Column("REGION", Unicode(20)),
    Column("TEAM_HR_NEW_ID", Integer, nullable=False),
    Column("DEPARTMENT_HR_NEW_ID", Integer, nullable=False),
    Column("WC_HR_NEW_ID", Integer, nullable=False),
    Column("BRANCH_HR_NEW_ID", Integer, nullable=False),
    Column("REGION__HR_NEW_ID", Integer, nullable=False),
    Column("P_DATE_ORDER", DateTime),
    schema="dbo",
)


t_V_ANALYZER_SKPI_RESULT = Table(
    "V_ANALYZER_SKPI_RESULT",
    metadata,
    Column("CU_NAME", Unicode(165), nullable=False),
    Column("P_ZARA_NUMBER", Unicode(10)),
    Column("P_ID", Integer, nullable=False),
    Column("P_PRODUCT", Unicode(255)),
    Column("SO_TASK", Unicode(1024)),
    Column("SO_NUMBER", Integer, nullable=False),
    Column("IS_KPI", String(1, "Latin1_General_CI_AS"), nullable=False),
    Column("S_KPI_NUMBER", Integer),
    Column("SO_PREDATE", DateTime),
    Column("FirstAccounting", DateTime),
    Column("SO_DEADLINE", DateTime),
    Column("SO_DATE_READY", DateTime),
    Column("P_AUDIT_DATE", DateTime),
    Column("PUNCT_PERFORMANCE", Integer),
    Column("PUNCT_COMPLETE", Integer),
    Column("SCHEDULE_REVIEW", Integer),
    Column("TEAM", Unicode(20)),
    Column("DEPARTMENT", Unicode(20)),
    Column("WC", Unicode(20)),
    Column("BRANCH", Unicode(20)),
    Column("REGION", Unicode(20)),
    Column("TEAM_HR_NEW_ID", Integer, nullable=False),
    Column("DEPARTMENT_HR_NEW_ID", Integer, nullable=False),
    Column("WC_HR_NEW_ID", Integer, nullable=False),
    Column("BRANCH_HR_NEW_ID", Integer, nullable=False),
    Column("P_DATE_ORDER", DateTime),
    Column("REGION__HR_NEW_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_ANALYZER_USAGE = Table(
    "V_ANALYZER_USAGE",
    metadata,
    Column("ST_SURNAME", Unicode(60), nullable=False),
    Column("ST_FORENAME", Unicode(50)),
    Column("ST_ID", Integer),
    Column("AS_ROLE", Integer),
    Column("Anzahl", Integer),
    Column("AS_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_ANALYZER_USAGE_TEAM = Table(
    "V_ANALYZER_USAGE_TEAM",
    metadata,
    Column("ST_SURNAME", Unicode(60), nullable=False),
    Column("ST_FORENAME", Unicode(50)),
    Column("ST_ID", Integer),
    Column("AS_ROLE", Integer),
    Column("Anzahl", Integer),
    Column("AS_ID", Integer, nullable=False),
    Column("AST_ID", Integer, nullable=False),
    Column("HR_NEW_ID", Integer),
    Column("HR_SHORT", Unicode(20)),
    schema="dbo",
)


t_V_ANA_FC_AGENT = Table(
    "V_ANA_FC_AGENT",
    metadata,
    Column("Datum", String(33, "Latin1_General_CI_AS")),
    Column("Mitarbeiter", Unicode(111)),
    Column("SO_FORECAST", DECIMAL(18, 2)),
    Column("SO_DEADLINE", DateTime),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("Region", Unicode(20)),
    Column("ST_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_ANA_FORECAST = Table(
    "V_ANA_FORECAST",
    metadata,
    Column("HR_SHORT", Unicode(20)),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("SO_FORECAST", DECIMAL(18, 2)),
    Column("SO_DEADLINE", DateTime),
    Column("MyStatus", Integer, nullable=False),
    Column("ST_ID", Integer),
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("Land", Unicode(20)),
    Column("Region", Unicode(20)),
    schema="dbo",
)


t_V_ANA_HIERARCHY = Table(
    "V_ANA_HIERARCHY",
    metadata,
    Column("HR_TYPE", Unicode(50)),
    Column("TEAM_HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("TEAM_HR_SHORT", Unicode(20)),
    Column("TEAM_HR_NEW_ID", Integer, nullable=False),
    Column("DEPARTMENT_HR_SHORT", Unicode(20)),
    Column("WC_HR_SHORT", Unicode(20)),
    Column("BRANCH_HR_SHORT", Unicode(20)),
    Column("REGION_HR_SHORT", Unicode(20)),
    Column("REGION_HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("REGION_HR_NEW_ID", Integer, nullable=False),
    Column("BRANCH_HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("BRANCH_HR_NEW_ID", Integer, nullable=False),
    Column("WC_HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("WC_HR_NEW_ID", Integer, nullable=False),
    Column("DEPARTMENT_HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("DEPARTMENT_HR_NEW_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_ANA_HIERARCHY_DEP = Table(
    "V_ANA_HIERARCHY_DEP",
    metadata,
    Column("DEPARTMENT_HR_SHORT", Unicode(20)),
    Column("WC_HR_SHORT", Unicode(20)),
    Column("BRANCH_HR_SHORT", Unicode(20)),
    Column("REGION_HR_SHORT", Unicode(20)),
    Column("REGION_HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("REGION_HR_NEW_ID", Integer, nullable=False),
    Column("BRANCH_HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("BRANCH_HR_NEW_ID", Integer, nullable=False),
    Column("WC_HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("WC_HR_NEW_ID", Integer, nullable=False),
    Column("DEPARTMENT_HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("DEPARTMENT_HR_NEW_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_CLEARPASS_CONFIG_BASE = Table(
    "V_CLEARPASS_CONFIG_BASE",
    metadata,
    Column("CB_ID", Integer, nullable=False),
    Column("GT_ID", Integer, nullable=False),
    Column("GT_NAME_DE", Unicode(90)),
    Column("GT_NAME_EN", Unicode(90)),
    Column("B_NAME_DE", Unicode(512)),
    Column("B_NAME_EN", Unicode(512)),
    Column("DM_ID", Integer),
    Column("DM_NAME", Unicode(255)),
    Column("TPT_NAME_DE", Unicode(256)),
    Column("CL_NAME_DE", Unicode(100)),
    Column("DM_TESTBASE_DE", Unicode(500)),
    Column("DM_TESTBASE_EN", Unicode(500)),
    Column("MyClearBy", Unicode(111)),
    Column("DM_CLEAR_DATE", DateTime),
    Column("MyRegBy", Unicode(111)),
    Column("DM_REG", DateTime),
    Column("MyUpdateBy", Unicode(111)),
    Column("DM_UPDATE", DateTime),
    Column("C_ID", Integer),
    schema="dbo",
)


t_V_CONFIG = Table(
    "V_CONFIG",
    metadata,
    Column("C_ID", Integer),
    Column("CB_ID", Integer, nullable=False),
    Column("CT_ID", Integer),
    Column("DM_NAME", Unicode(255)),
    Column("DM_ID", Integer),
    Column("B_ID", Integer),
    Column("B_NAME_DE", Unicode(120)),
    Column("TP_ID", Integer),
    schema="dbo",
)


t_V_CONFIG_BASE_FOR_PSEX = Table(
    "V_CONFIG_BASE_FOR_PSEX",
    metadata,
    Column("CBC_ID", Integer, nullable=False),
    Column("C_ID", Integer),
    Column("CB_ID", Integer),
    Column("CBC_TIME_HOURS", Float(53)),
    Column("CBC_TIME_DAYS", Float(53)),
    Column("CBC_DELTA_START", Float(53)),
    Column("CBC_COSTS", DECIMAL(18, 2)),
    Column("CBC_TASK", Unicode(500)),
    Column("CBC_COMMENT", Unicode(500)),
    Column("CBC_RATE", DECIMAL(18, 2)),
    Column("CBC_PRICE", DECIMAL(18, 2)),
    Column("CBC_FACTOR", Float(53)),
    Column("WST_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("DMC_ID", Integer),
    Column("CBC_TRAVEL", DECIMAL(18, 2)),
    Column("ST_ID", Integer),
    Column("WST_SHORT", Unicode(20)),
    Column("CB_MODULE_CALCULATION", Integer),
    Column("DM_ID", Integer),
    Column("TP_ID", Integer),
    Column("GP_POSITION", Integer),
    Column("PP_ID", Integer),
    schema="dbo",
)


t_V_CONFIG_CALC_MATERIAL = Table(
    "V_CONFIG_CALC_MATERIAL",
    metadata,
    Column("C_ID", Integer, nullable=False),
    Column("C_NAME_DE", Unicode(120)),
    Column("G_TEXT_DE", Unicode(255)),
    Column("CBC_TASK", Unicode(500)),
    Column("ZM_PRODUCT", Unicode(5)),
    Column("ProductPaket", Unicode(5)),
    Column("ObjectAusConfig", Unicode(5)),
    Column("ZM_OBJECT", Unicode(5)),
    Column("ZM_SUBLOCATION", Unicode(5)),
    Column("SubLocationAusTeam", Unicode(5), nullable=False),
    Column("PRODUCT_NEU", Unicode(5)),
    Column("OBJECT_NEU", Unicode(5)),
    Column("ZM_LOCATION", Unicode(5)),
    Column("SUBLOCATION_NEU", Unicode(5)),
    Column("ZM_ORGINAL", Unicode(50)),
    Column("ZM_NEU", Unicode(23)),
    Column("WST_SHORT", Unicode(20)),
    Column("CBC_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_CONFIG_FOR_PSEX = Table(
    "V_CONFIG_FOR_PSEX",
    metadata,
    Column("C_ID", Integer),
    Column("CB_ID", Integer, nullable=False),
    Column("CT_ID", Integer),
    Column("DM_NAME", Unicode(255)),
    Column("DM_ID", Integer),
    Column("B_ID", Integer),
    Column("B_NAME_DE", Unicode(120)),
    Column("TP_ID", Integer),
    schema="dbo",
)


t_V_CONFIG_GOAL_ONE = Table(
    "V_CONFIG_GOAL_ONE",
    metadata,
    Column("C_ID", Integer),
    Column("CB_ID", Integer, nullable=False),
    Column("CBG_ID", Integer),
    schema="dbo",
)


t_V_CONFIG_NAV = Table(
    "V_CONFIG_NAV",
    metadata,
    Column("C_ID", Integer),
    Column("CB_ID", Integer, nullable=False),
    Column("CB_CONDITION", Unicode(800)),
    Column("CB_COMMENT", Unicode(500)),
    Column("CT_ID", Integer),
    Column("CB_DISPO_MODULE", BIT, nullable=False),
    Column("G_ID", Integer),
    Column("G_TEXT_DE", Unicode(255)),
    Column("G_TEXT_EN", Unicode(255)),
    Column("B_ID", Integer, nullable=False),
    Column("B_NAME_DE", Unicode(512)),
    Column("B_NAME_EN", Unicode(512)),
    Column("DI_ID", Integer),
    Column("DI_REQUIREMENT_DE", Unicode(1000)),
    Column("DI_REQUIREMENT_EN", Unicode(1000)),
    Column("BT_ID", Integer, nullable=False),
    Column("BT_NAME_DE", Unicode(50)),
    Column("BT_NAME_EN", Unicode(50)),
    Column("GT_ID", Integer, nullable=False),
    Column("GT_NAME_DE", Unicode(90)),
    Column("GT_NAME_EN", Unicode(90)),
    Column("DM_ID", Integer),
    Column("DM_NAME", Unicode(255)),
    Column("DM_NAME_EN", Unicode(255)),
    Column("DM_TESTBASE_DE", Unicode(500)),
    Column("DM_TESTBASE_EN", Unicode(500)),
    Column("TPT_ID", Integer),
    Column("TPT_NAME_DE", Unicode(256)),
    Column("TPT_NAME_EN", Unicode(256)),
    Column("CBC_TIME_HOURS", Float(53)),
    Column("CBC_TIME_DAYS", Float(53)),
    Column("CBC_DELTA_START", Float(53)),
    Column("CBC_COSTS", DECIMAL(18, 2)),
    Column("CBC_TASK", Unicode(500)),
    Column("CBC_COMMENT", Unicode(500)),
    Column("CBC_RATE", DECIMAL(18, 2)),
    Column("CBC_PRICE", DECIMAL(18, 2)),
    Column("CBC_FACTOR", Float(53)),
    Column("WST_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("DMC_ID", Integer),
    Column("CBC_TRAVEL", DECIMAL(18, 2)),
    Column("GP_POSITION", Integer),
    Column("PP_ID", Integer),
    Column("ZM_ID", Unicode(50)),
    Column("GP_TEXT_DE", Unicode(255)),
    Column("GP_TEXT_EN", Unicode(255)),
    Column("ZP_ID", Unicode(3)),
    Column("ZO_ID", Unicode(3)),
    Column("ZP_LOCATION", Unicode(2)),
    schema="dbo",
)


t_V_CONFIG_NAV_SERVICEDETAILS = Table(
    "V_CONFIG_NAV_SERVICEDETAILS",
    metadata,
    Column("C_ID", Integer),
    Column("GR_SHORT", Unicode(10)),
    Column("GR_NAME_DE", Unicode(100)),
    Column("GR_NAME_EN", Unicode(100)),
    Column("TPER_ID", Integer, nullable=False),
    Column("TPER_LEVEL", Integer),
    Column("TPER_NAME_DE", Unicode(30)),
    Column("TPER_NAME_EN", Unicode(30)),
    Column("PC_ID", Integer, nullable=False),
    Column("PC_NAME_DE", Unicode(50)),
    Column("PC_NAME_EN", Unicode(50)),
    Column("DM_ID", Integer, nullable=False),
    Column("DM_NAME", Unicode(255)),
    Column("DM_NAME_EN", Unicode(255)),
    Column("CL_NAME_DE", Unicode(100)),
    Column("CL_NAME_EN", Unicode(100)),
    Column("QUELLE_DE", Unicode),
    Column("QUELLE_EN", Unicode),
    Column("PROZEDUR_DE", Unicode),
    Column("PROZEDUR_EN", Unicode),
    Column("CP_ID", Integer, nullable=False),
    Column("CP_NAME_DE", Unicode(150)),
    Column("CP_NAME_EN", Unicode(150)),
    Column("Class", Unicode),
    Column("MyStatus", Unicode(1), nullable=False),
    Column("PT_ID", Integer, nullable=False),
    Column("PT_NAME_DE", Unicode(255)),
    Column("PT_NAME_EN", Unicode(255)),
    Column("G_ID", Integer),
    Column("G_TEXT_DE", Unicode(255)),
    Column("G_TEXT_EN", Unicode(255)),
    Column("G_SHORT", Unicode(10)),
    Column("GT_NAME_DE", Unicode(90)),
    Column("GT_SHORT", Unicode(10)),
    Column("GR_ORDER", Integer),
    Column("CB_ID", Integer, nullable=False),
    Column("TP", Integer),
    schema="dbo",
)


t_V_CONFIG_PACKAGE_SUM = Table(
    "V_CONFIG_PACKAGE_SUM",
    metadata,
    Column("C_ID", Integer),
    Column("CP_ID", Integer, nullable=False),
    Column("HK", Float(53)),
    Column("VK", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_CONFIG_POSITION = Table(
    "V_CONFIG_POSITION",
    metadata,
    Column("C_ID", Integer),
    Column("CB_ID", Integer, nullable=False),
    Column("GP_POSITION", Integer),
    Column("GP_TEXT_DE", Unicode(255)),
    Column("G_ID", Integer, nullable=False),
    Column("GP_TEXT_EN", Unicode(255)),
    schema="dbo",
)


t_V_CONFIG_PROOF = Table(
    "V_CONFIG_PROOF",
    metadata,
    Column("C_ID", Integer),
    Column("CP_ID", Integer),
    Column("Nachweis_EN", Unicode(1016)),
    Column("Nachweis_DE", Unicode(1019)),
    schema="dbo",
)


t_V_CONFIG_TEMPLATE = Table(
    "V_CONFIG_TEMPLATE",
    metadata,
    Column("CBC_ID", Integer, nullable=False),
    Column("C_ID", Integer),
    Column("CB_ID", Integer),
    Column("CBC_TIME_HOURS", Float(53)),
    Column("CBC_TIME_DAYS", Float(53)),
    Column("CBC_DELTA_START", Float(53)),
    Column("CBC_COSTS", DECIMAL(18, 2)),
    Column("CBC_TASK", Unicode(500)),
    Column("CBC_COMMENT", Unicode(500)),
    Column("CBC_RATE", DECIMAL(18, 2)),
    Column("CBC_PRICE", DECIMAL(18, 2)),
    Column("CBC_FACTOR", Float(53)),
    Column("WST_ID", Integer),
    Column("SO_NUMBER", Integer),
    Column("DMC_ID", Integer),
    Column("CBC_TRAVEL", DECIMAL(18, 2)),
    Column("ST_ID", Integer),
    Column("WST_SHORT", Unicode(20)),
    Column("CB_MODULE_CALCULATION", Integer),
    Column("GP_POSITION", Integer),
    Column("PP_ID", Integer),
    Column("TP_ID", Integer),
    Column("ZM_ID", Unicode(50)),
    schema="dbo",
)


t_V_CONFIG_TESTLEVEL = Table(
    "V_CONFIG_TESTLEVEL",
    metadata,
    Column("C_ID", Integer),
    Column("CP_ID", Integer, nullable=False),
    Column("GR_ID", Integer, nullable=False),
    Column("GR_SHORT", Unicode(10)),
    Column("TPER_ID", Integer, nullable=False),
    Column("TPER_LEVEL", Integer),
    Column("TPER_NAME_DE", Unicode(30)),
    Column("TPER_NAME_EN", Unicode(30)),
    Column("PC_ID", Integer, nullable=False),
    Column("PC_NAME_DE", Unicode(50)),
    Column("PC_NAME_EN", Unicode(50)),
    Column("CP_PRICE", DECIMAL(18, 2)),
    Column("CP_LICENCE", DECIMAL(18, 2), nullable=False),
    Column("PT_NAME_DE", Unicode(255)),
    Column("PT_NAME_EN", Unicode(255)),
    Column("GR_ORDER", Integer),
    schema="dbo",
)


t_V_DEFAULT_MODUL_NO_ATTRIBUTES = Table(
    "V_DEFAULT_MODUL_NO_ATTRIBUTES",
    metadata,
    Column("DM_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_DEPARTMENT_CURRENCY = Table(
    "V_DEPARTMENT_CURRENCY",
    metadata,
    Column("CUR_ID", NCHAR(3), nullable=False),
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("LS_BASE_CURRENCY", Unicode(3)),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("HR_SHORT", Unicode(20)),
    Column("CUR_SHORT", NCHAR(3), nullable=False),
    Column("CUR_NAME", Unicode(256), nullable=False),
    Column("CUR_SIGN", Unicode(4), nullable=False),
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
    Column("SHOW_UPLOAD", Integer, nullable=False),
    Column("EMI_TITLE", BIT),
    Column("EMIP_ID", Integer, nullable=False),
    Column("P_ID", Integer),
    Column("EM_OFFLINE_BY", Integer),
    Column("E_ID", Integer, nullable=False),
    Column("EMI_NUMBER", Integer),
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


t_V_EDOC_CATEGORY_RESULT = Table(
    "V_EDOC_CATEGORY_RESULT",
    metadata,
    Column("E_ID", Integer, nullable=False),
    Column("ND_ID", Integer, nullable=False),
    Column("PRP_ID", Integer),
    Column("ER_ID", Integer),
    Column("CULE_NAME_DE", Unicode(512)),
    Column("CULE_NUMBER", Unicode(10)),
    Column("CULE_ID", Integer, nullable=False),
    Column("ER_VALUE", DECIMAL(18, 2)),
    Column("HAUPTNOTE", Integer, nullable=False),
    Column("NEBENNOTE", Integer, nullable=False),
    Column("WertHAUPTNOTE", DECIMAL(18, 2)),
    Column("WertNEBENNOTE", DECIMAL(18, 2)),
    Column("ER_VALUE_YN", Integer),
    schema="dbo",
)


t_V_EDOC_CATEGORY_RESULT_YN = Table(
    "V_EDOC_CATEGORY_RESULT_YN",
    metadata,
    Column("E_ID", Integer, nullable=False),
    Column("ND_ID", Integer, nullable=False),
    Column("PRP_ID", Integer),
    Column("ER_ID", Integer),
    Column("CULE_NAME_DE", Unicode(512)),
    Column("CULE_NUMBER", Unicode(10)),
    Column("CULE_ID", Integer, nullable=False),
    Column("ER_VALUE", DECIMAL(18, 2)),
    Column("ER_VALUE_YN", Integer),
    Column("PHASE", Unicode(256)),
    Column("P_ID", Integer, nullable=False),
    Column("P_PRODUCT", Unicode(255)),
    Column("P_MODEL", Unicode(255)),
    Column("P_DATE_APPOINTMENT", DateTime),
    Column("P_DATE_READY", DateTime),
    Column("BATCH_NUMBER", Unicode(16)),
    Column("P_TOKEN", Unicode(60)),
    Column("P_IAN", Unicode(256)),
    Column("EP_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_EDOC_CATEGORY_TOTAL_RESULT = Table(
    "V_EDOC_CATEGORY_TOTAL_RESULT",
    metadata,
    Column("E_ID", Integer),
    Column("PHASE", Unicode(256)),
    Column("P_ID", Integer),
    Column("P_PRODUCT", Unicode(255)),
    Column("P_MODEL", Unicode(255)),
    Column("BATCH_NUMBER", Unicode(16)),
    Column("P_IAN", Unicode(256)),
    Column("P_DATE_READY", DateTime),
    Column("Auftragsdatum", Unicode(30)),
    Column("1", Unicode(3)),
    Column("1.1", Unicode(3)),
    Column("1.2", Unicode(3)),
    Column("2", Unicode(3)),
    Column("2.1", Unicode(3)),
    Column("3", Unicode(3)),
    Column("3.1", Unicode(3)),
    Column("3.2", Unicode(3)),
    Column("3.3", Unicode(3)),
    Column("3.4", Unicode(3)),
    Column("4", Unicode(3)),
    Column("4.1", Unicode(3)),
    Column("4.2", Unicode(3)),
    Column("5", Unicode(1), nullable=False),
    Column("5.1 PERF", Unicode(10)),
    Column("5.1 INSTR", Unicode(10)),
    Column("5.2", Unicode(3)),
    Column("5.3", Unicode(3)),
    Column("5.4", Unicode(3)),
    Column("6", Unicode(3)),
    Column("6.1", Unicode(3)),
    Column("6.2", Unicode(3)),
    Column("7", Unicode(3)),
    Column("7.1", Unicode(3)),
    Column("7.2", Unicode(3)),
    Column("8", Unicode(3)),
    Column("8.1", Unicode(3)),
    Column("8.2", Unicode(3)),
    Column("9", Unicode(3)),
    Column("9.1", Unicode(3)),
    Column("9.2", Unicode(3)),
    Column("10", Unicode(3)),
    Column("10.1", Unicode(3)),
    Column("10.2", Unicode(3)),
    Column("11", Unicode(3)),
    Column("11.1", Unicode(3)),
    Column("11.2", Unicode(3)),
    Column("11.3", Unicode(3)),
    schema="dbo",
)


t_V_EDOC_MODUL_ITEM_HANDLEDBY = Table(
    "V_EDOC_MODUL_ITEM_HANDLEDBY",
    metadata,
    Column("E_ID", Integer),
    Column("EM_ID", Integer),
    Column("DM_ID", Integer),
    Column("Bearbeiter", Unicode(111)),
    schema="dbo",
)


t_V_EDOC_SUBORDERS = Table(
    "V_EDOC_SUBORDERS",
    metadata,
    Column("E_ID", Integer),
    Column("P_ID", Integer),
    Column("SO_NUMBER", Integer, nullable=False),
    Column("MyProject", Unicode(65)),
    schema="dbo",
)


t_V_EVAL_MODULE = Table(
    "V_EVAL_MODULE",
    metadata,
    Column("DM_ID", Integer, nullable=False),
    Column("DM_NAME_DE", Unicode(255)),
    Column("DM_NAME_EN", Unicode(255)),
    Column("PRODUCT_PATH_DE", Unicode),
    Column("PRODUCT_PATH_EN", Unicode),
    Column("COUNTRY_PATH_DE", Unicode),
    Column("COUNTRY_PATH_EN", Unicode),
    Column("HRP_ID", Integer, nullable=False),
    Column("HRC_ID", Integer, nullable=False),
    Column("TPT_ID", Integer),
    Column("CL_NAME_DE", Unicode(100)),
    Column("CL_NAME_EN", Unicode(100)),
    Column("ND_SHORT", Unicode(10)),
    Column("ND_ID", Integer, nullable=False),
    Column("BASE_PROCEDURE_DE", Unicode),
    Column("BASE_PROCEDURE_EN", Unicode),
    schema="dbo",
)


t_V_EVAL_MODULE_ANNEX = Table(
    "V_EVAL_MODULE_ANNEX",
    metadata,
    Column("DMAX_ID", Integer, nullable=False),
    Column("DM_ID", Integer, nullable=False),
    Column("DMAX_NAME_DE", Unicode(500)),
    Column("DMAX_NAME_EN", Unicode(500)),
    Column("DMAX_FILENAME", Unicode(255)),
    Column("DMAX_DATA", LargeBinary),
    schema="dbo",
)


t_V_FLOWCHART = Table(
    "V_FLOWCHART",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("SO_NUMBER", Integer, nullable=False),
    Column("ST_ID", Integer),
    Column("MyName", Unicode(111)),
    Column("MyAufgabe", Unicode(512)),
    Column("MyStatus", String(14, "Latin1_General_CI_AS"), nullable=False),
    Column("STARTTERMIN", DateTime),
    Column("SO_DEADLINE", DateTime),
    Column("SO_HOURS", DECIMAL(18, 6)),
    Column("SO_DATE_READY", DateTime),
    Column("SO_DATE_CHECK", DateTime),
    Column("P_DATE_DONE", DateTime),
    Column("MyWait", Integer, nullable=False),
    Column("SO_CONFIRMED_DATE", DateTime),
    schema="dbo",
)


t_V_GMA = Table(
    "V_GMA",
    metadata,
    Column("DI_ID", Integer, nullable=False),
    Column("HRC_NAME_EN", Unicode(255)),
    Column("HRC_ID", Integer),
    Column("HRP_NAME_EN", Unicode(255)),
    Column("CL_NAME_EN", Unicode(100)),
    Column("HRP_ID", Integer),
    Column("CATEGORY", Unicode),
    Column("CL_ID", Integer),
    Column("DI_REQUIREMENT_EN", Unicode(1000)),
    Column("MyURL", Unicode(512)),
    Column("MyURLTEXT", Unicode(1024)),
    Column("DI_UPDATE", DateTime),
    schema="dbo",
)


t_V_GMA_COMPLETE = Table(
    "V_GMA_COMPLETE",
    metadata,
    Column("HRC_NAME_EN", Unicode(255)),
    Column("HRP_NAME_EN", Unicode(255)),
    Column("CATEGORY", Unicode),
    Column("CL_NAME_EN", Unicode(100)),
    Column("DI_REQUIREMENT_EN", Unicode(1000)),
    Column("MyURL", Unicode(512)),
    Column("MyURLTEXT", Unicode(1024)),
    schema="dbo",
)


t_V_GMA_CROSS = Table(
    "V_GMA_CROSS",
    metadata,
    Column("HRC_NAME_EN", Unicode(255)),
    Column("HRP_NAME_EN", Unicode(255)),
    Column("HRC_ID", Integer),
    Column("HRP_ID", Integer),
    schema="dbo",
)


t_V_GMA_DEFAULT_ITEM = Table(
    "V_GMA_DEFAULT_ITEM",
    metadata,
    Column("DI_ID", Integer, nullable=False),
    Column("HRC_NAME_EN", Unicode(255)),
    Column("HRC_ID", Integer),
    Column("HRP_NAME_EN", Unicode(255)),
    Column("HRP_ID", Integer),
    Column("CL_NAME_EN", Unicode(100)),
    Column("CL_ID", Integer),
    Column("DI_REQUIREMENT_EN", Unicode(1000)),
    schema="dbo",
)


t_V_GUILLOTINE_MAIN = Table(
    "V_GUILLOTINE_MAIN",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("SO_NUMBER", Integer, nullable=False),
    Column("P_PRODUCT", Unicode(255), nullable=False),
    Column("P_MODEL", Unicode(255), nullable=False),
    Column("TEAM_BEARBEITER", Unicode(20)),
    Column("PM_EINGANG", DateTime),
    Column("PM_EINGANG_LABOR", DateTime),
    Column("SO_DATE_READY", DateTime),
    Column("SO_DATE_CHECK", DateTime),
    Column("SO_DEADLINE", DateTime),
    Column("P_DEADLINE", DateTime),
    Column("BERICHT_VERSCHICKT", DateTime),
    Column("P_DATE_DONE", DateTime),
    Column("HR_NEW_ID_BEARBEITER", Integer, nullable=False),
    Column("PROJEKTMANAGER_TEAM", Unicode(20)),
    Column("HR_NEW_ID_PROJEKTMANAGER", Integer, nullable=False),
    Column("P_ACTION", BIT),
    Column("SO_WAIT", BIT),
    Column("KUNDE", Unicode(165)),
    Column("HERSTELLER", Unicode(165)),
    Column("PM_EINGANG_TIME", DateTime),
    Column("P_STATUS", Integer),
    Column("P_PROJECTMANAGER", Integer),
    Column("ST_ID", Integer, nullable=False),
    Column("BEARBEITER", Unicode(111)),
    Column("PROJEKTLEITER", Unicode(111)),
    Column("SO_COMMENT", Unicode(2000)),
    Column("DELTA_P_DEADLINE", Integer),
    Column("DELTA_SO_DEADLINE", Integer),
    Column("DELTA_STOCK_REPORT", Integer),
    schema="dbo",
)


t_V_HR_COUNTRY = Table(
    "V_HR_COUNTRY",
    metadata,
    Column("HRC_ID", Integer, nullable=False),
    Column("HRC_LEFT", Integer),
    Column("HRC_RIGHT", Integer),
    Column("HRC_INDENT", Integer),
    Column("HRC_NAME_DE", Unicode(255)),
    Column("HRC_NAME_EN", Unicode(255)),
    Column("HRC_NAME_FR", Unicode(255)),
    Column("Unterkategorien", Integer),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_COUNTRY_CONFIG = Table(
    "V_HR_COUNTRY_CONFIG",
    metadata,
    Column("HRC_ID", Integer, nullable=False),
    Column("HRC_LEFT", Integer),
    Column("HRC_RIGHT", Integer),
    Column("HRC_INDENT", Integer),
    Column("HRC_NAME_DE", Unicode(255)),
    Column("HRC_NAME_EN", Unicode(255)),
    Column("HRC_NAME_FR", Unicode(255)),
    Column("Unterkategorien", Integer),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_COUNTRY_COUNT = Table(
    "V_HR_COUNTRY_COUNT",
    metadata,
    Column("HRC_ID", Integer, nullable=False),
    Column("ItemsInSub", Integer),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_COUNTRY_COUNT_CONFIG = Table(
    "V_HR_COUNTRY_COUNT_CONFIG",
    metadata,
    Column("HRC_ID", Integer, nullable=False),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_COUNTRY_COUNT_INFOMODULE = Table(
    "V_HR_COUNTRY_COUNT_INFOMODULE",
    metadata,
    Column("HRC_ID", Integer, nullable=False),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_COUNTRY_COUNT_ITEMS = Table(
    "V_HR_COUNTRY_COUNT_ITEMS",
    metadata,
    Column("HRC_ID", Integer, nullable=False),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_COUNTRY_COUNT_MODULE = Table(
    "V_HR_COUNTRY_COUNT_MODULE",
    metadata,
    Column("HRC_ID", Integer, nullable=False),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_COUNTRY_COUNT_NAV = Table(
    "V_HR_COUNTRY_COUNT_NAV",
    metadata,
    Column("HRC_ID", Integer, nullable=False),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_COUNTRY_INFOMODULE = Table(
    "V_HR_COUNTRY_INFOMODULE",
    metadata,
    Column("HRC_ID", Integer, nullable=False),
    Column("HRC_LEFT", Integer),
    Column("HRC_RIGHT", Integer),
    Column("HRC_INDENT", Integer),
    Column("HRC_NAME_DE", Unicode(255)),
    Column("HRC_NAME_EN", Unicode(255)),
    Column("HRC_NAME_FR", Unicode(255)),
    Column("Unterkategorien", Integer),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_COUNTRY_ITEMS = Table(
    "V_HR_COUNTRY_ITEMS",
    metadata,
    Column("HRC_ID", Integer, nullable=False),
    Column("HRC_LEFT", Integer),
    Column("HRC_RIGHT", Integer),
    Column("HRC_INDENT", Integer),
    Column("HRC_NAME_DE", Unicode(255)),
    Column("HRC_NAME_EN", Unicode(255)),
    Column("HRC_NAME_FR", Unicode(255)),
    Column("Unterkategorien", Integer),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_COUNTRY_MODULE = Table(
    "V_HR_COUNTRY_MODULE",
    metadata,
    Column("HRC_ID", Integer, nullable=False),
    Column("HRC_LEFT", Integer),
    Column("HRC_RIGHT", Integer),
    Column("HRC_INDENT", Integer),
    Column("HRC_NAME_DE", Unicode(255)),
    Column("HRC_NAME_EN", Unicode(255)),
    Column("HRC_NAME_FR", Unicode(255)),
    Column("Unterkategorien", Integer),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_COUNTRY_NAV = Table(
    "V_HR_COUNTRY_NAV",
    metadata,
    Column("HRC_ID", Integer, nullable=False),
    Column("HRC_LEFT", Integer),
    Column("HRC_RIGHT", Integer),
    Column("HRC_INDENT", Integer),
    Column("HRC_NAME_DE", Unicode(255)),
    Column("HRC_NAME_EN", Unicode(255)),
    Column("HRC_NAME_FR", Unicode(255)),
    Column("Unterkategorien", Integer),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_COUNTRY_SUB_IDS = Table(
    "V_HR_COUNTRY_SUB_IDS",
    metadata,
    Column("HRC_ID", Integer, nullable=False),
    Column("HRC_ID_CONTENT", Integer, nullable=False),
    schema="dbo",
)


t_V_HR_PRODUCT = Table(
    "V_HR_PRODUCT",
    metadata,
    Column("HRP_ID", Integer, nullable=False),
    Column("HRP_LEFT", Integer),
    Column("HRP_RIGHT", Integer),
    Column("HRP_INDENT", Integer),
    Column("HRP_NAME_DE", Unicode(255)),
    Column("HRP_NAME_EN", Unicode(255)),
    Column("HRP_NAME_FR", Unicode(255)),
    Column("Unterkategorien", Integer),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_PRODUCT_CONFIG = Table(
    "V_HR_PRODUCT_CONFIG",
    metadata,
    Column("HRP_ID", Integer, nullable=False),
    Column("HRP_LEFT", Integer),
    Column("HRP_RIGHT", Integer),
    Column("HRP_INDENT", Integer),
    Column("HRP_NAME_DE", Unicode(255)),
    Column("HRP_NAME_EN", Unicode(255)),
    Column("HRP_NAME_FR", Unicode(255)),
    Column("Unterkategorien", Integer),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_PRODUCT_COUNT = Table(
    "V_HR_PRODUCT_COUNT",
    metadata,
    Column("HRP_ID", Integer, nullable=False),
    Column("ItemsInSub", Integer),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_PRODUCT_COUNT_CONFIG = Table(
    "V_HR_PRODUCT_COUNT_CONFIG",
    metadata,
    Column("HRP_ID", Integer, nullable=False),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_PRODUCT_COUNT_INFOMODULE = Table(
    "V_HR_PRODUCT_COUNT_INFOMODULE",
    metadata,
    Column("HRP_ID", Integer, nullable=False),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_PRODUCT_COUNT_ITEMS = Table(
    "V_HR_PRODUCT_COUNT_ITEMS",
    metadata,
    Column("HRP_ID", Integer, nullable=False),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_PRODUCT_COUNT_MODULE = Table(
    "V_HR_PRODUCT_COUNT_MODULE",
    metadata,
    Column("HRP_ID", Integer, nullable=False),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_PRODUCT_COUNT_MODULE_MASTER = Table(
    "V_HR_PRODUCT_COUNT_MODULE_MASTER",
    metadata,
    Column("HRP_ID", Integer, nullable=False),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_PRODUCT_COUNT_NAV = Table(
    "V_HR_PRODUCT_COUNT_NAV",
    metadata,
    Column("HRP_ID", Integer, nullable=False),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_PRODUCT_COUNT_NAV_MASTER = Table(
    "V_HR_PRODUCT_COUNT_NAV_MASTER",
    metadata,
    Column("HRP_ID", Integer, nullable=False),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_PRODUCT_INFOMODULE = Table(
    "V_HR_PRODUCT_INFOMODULE",
    metadata,
    Column("HRP_ID", Integer, nullable=False),
    Column("HRP_LEFT", Integer),
    Column("HRP_RIGHT", Integer),
    Column("HRP_INDENT", Integer),
    Column("HRP_NAME_DE", Unicode(255)),
    Column("HRP_NAME_EN", Unicode(255)),
    Column("HRP_NAME_FR", Unicode(255)),
    Column("Unterkategorien", Integer),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_PRODUCT_ITEMS = Table(
    "V_HR_PRODUCT_ITEMS",
    metadata,
    Column("HRP_ID", Integer, nullable=False),
    Column("HRP_LEFT", Integer),
    Column("HRP_RIGHT", Integer),
    Column("HRP_INDENT", Integer),
    Column("HRP_NAME_DE", Unicode(255)),
    Column("HRP_NAME_EN", Unicode(255)),
    Column("HRP_NAME_FR", Unicode(255)),
    Column("Unterkategorien", Integer),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_PRODUCT_MODULE = Table(
    "V_HR_PRODUCT_MODULE",
    metadata,
    Column("HRP_ID", Integer, nullable=False),
    Column("HRP_LEFT", Integer),
    Column("HRP_RIGHT", Integer),
    Column("HRP_INDENT", Integer),
    Column("HRP_NAME_DE", Unicode(255)),
    Column("HRP_NAME_EN", Unicode(255)),
    Column("HRP_NAME_FR", Unicode(255)),
    Column("Unterkategorien", Integer),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_PRODUCT_NAV = Table(
    "V_HR_PRODUCT_NAV",
    metadata,
    Column("HRP_ID", Integer, nullable=False),
    Column("HRP_LEFT", Integer),
    Column("HRP_RIGHT", Integer),
    Column("HRP_INDENT", Integer),
    Column("HRP_NAME_DE", Unicode(255)),
    Column("HRP_NAME_EN", Unicode(255)),
    Column("HRP_NAME_FR", Unicode(255)),
    Column("Unterkategorien", Integer),
    Column("ItemsInSub", BigInteger),
    Column("ItemsDirect", BigInteger),
    schema="dbo",
)


t_V_HR_PRODUCT_SUB_IDS = Table(
    "V_HR_PRODUCT_SUB_IDS",
    metadata,
    Column("HRP_ID", Integer, nullable=False),
    Column("HRP_ID_CONTENT", Integer, nullable=False),
    schema="dbo",
)


t_V_INFOMODULE = Table(
    "V_INFOMODULE",
    metadata,
    Column("DM_ID", Integer, nullable=False),
    Column("HRC_ID", Integer, nullable=False),
    Column("HRP_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_INFO_ATTRIBUTES = Table(
    "V_INFO_ATTRIBUTES",
    metadata,
    Column("C_ID", Integer),
    Column("ATT_ID", Integer),
    Column("ATT_TYPE", Integer),
    schema="dbo",
)


t_V_NAVIGATOR_FORECAST = Table(
    "V_NAVIGATOR_FORECAST",
    metadata,
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("SO_FORECAST", DECIMAL(18, 2)),
    Column("SO_DEADLINE", DateTime),
    Column("MyStatus", Integer, nullable=False),
    Column("ST_ID", Integer),
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("HR_SHORT", Unicode(20)),
    schema="dbo",
)


t_V_NAV_CRITICAL_ITEMS = Table(
    "V_NAV_CRITICAL_ITEMS",
    metadata,
    Column("N_ID", Integer),
    Column("NP_ID", Integer, nullable=False),
    Column("NP_NAME_DE", Unicode(150)),
    Column("NP_NAME_EN", Unicode(150)),
    Column("DI_ID", Integer, nullable=False),
    Column("DI_NAME", Unicode(100)),
    Column("DI_NAME_EN", Unicode(100)),
    Column("schlecht", Integer),
    Column("gut", Integer),
    Column("neutral", Integer),
    Column("sonstige", Integer),
    schema="dbo",
)


t_V_NAV_CUSTOM_MODULE = Table(
    "V_NAV_CUSTOM_MODULE",
    metadata,
    Column("CULE_ID", Integer, nullable=False),
    Column("NP_ID", Integer),
    Column("DM_ID", Integer, nullable=False),
    Column("DM_NAME", Unicode(255)),
    Column("DM_NAME_EN", Unicode(255)),
    Column("MyItems", BigInteger),
    Column("ND_SHORT", Unicode(10)),
    Column("NAME_DE", Unicode(788)),
    Column("NAME_EN", Unicode(788)),
    schema="dbo",
)


t_V_NAV_ISPROJECTNAV = Table(
    "V_NAV_ISPROJECTNAV",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("NAVIGATE", Integer, nullable=False),
    schema="dbo",
)


t_V_NAV_ITEM_STATISTIC = Table(
    "V_NAV_ITEM_STATISTIC",
    metadata,
    Column("N_ID", Integer),
    Column("NP_ID", Integer, nullable=False),
    Column("NP_NAME_DE", Unicode(150)),
    Column("Positiv", Integer),
    Column("Mittel", Integer),
    Column("Negativ", Integer),
    Column("Sonstige", Integer),
    Column("Gesamt", BigInteger),
    Column("DI_NAME", Unicode(100)),
    Column("NP_NAME_EN", Unicode(150)),
    Column("DI_NAME_EN", Unicode(100)),
    Column("DI_ID", Integer, nullable=False),
    Column("DM_ID", Integer),
    Column("DM_NAME", Unicode(255)),
    Column("DM_NAME_EN", Unicode(255)),
    schema="dbo",
)


t_V_NAV_ITEM_STATISTIC2 = Table(
    "V_NAV_ITEM_STATISTIC2",
    metadata,
    Column("N_ID", Integer),
    Column("NP_ID", Integer, nullable=False),
    Column("NP_NAME_DE", Unicode(150)),
    Column("Positiv", Integer),
    Column("Mittel", Integer),
    Column("Negativ", Integer),
    Column("Gesamt", BigInteger),
    Column("DI_NAME", Unicode(100)),
    Column("NP_NAME_EN", Unicode(150)),
    Column("DI_NAME_EN", Unicode(100)),
    Column("DI_ID", Integer, nullable=False),
    Column("DM_ID", Integer),
    Column("DM_NAME", Unicode(255)),
    Column("DM_NAME_EN", Unicode(255)),
    schema="dbo",
)


t_V_NAV_PROOF = Table(
    "V_NAV_PROOF",
    metadata,
    Column("C_ID", Integer),
    Column("CP_ID", Integer),
    Column("Nachweis_EN", Unicode(1016)),
    Column("Nachweis_DE", Unicode(1019)),
    schema="dbo",
)


t_V_NAV_SEARCH = Table(
    "V_NAV_SEARCH",
    metadata,
    Column("N_NAME_DE", Unicode(120)),
    Column("N_NAME_EN", Unicode(120)),
    Column("HRP_ID", Integer, nullable=False),
    Column("HRC_ID", Integer, nullable=False),
    Column("N_ID", Integer, nullable=False),
    Column("P_ID", Integer, nullable=False),
    Column("P_PRODUCT", Unicode(255)),
    Column("P_MODEL", Unicode(255)),
    Column("P_IAN", Unicode(256)),
    Column("E_ID", Integer),
    Column("NP_ID", Integer),
    schema="dbo",
)


t_V_NAV_SERVICEDETAILS = Table(
    "V_NAV_SERVICEDETAILS",
    metadata,
    Column("N_ID", Integer),
    Column("NP_ID", Integer, nullable=False),
    Column("ND_SHORT", Unicode(10)),
    Column("ND_NAME_DE", Unicode(100)),
    Column("ND_NAME_EN", Unicode(100)),
    Column("NL_LEVEL", Integer),
    Column("PC_ID", Integer, nullable=False),
    Column("DM_ID", Integer, nullable=False),
    Column("DM_NAME", Unicode(255)),
    Column("DM_NAME_EN", Unicode(255)),
    Column("CL_NAME_DE", Unicode(100)),
    Column("CL_NAME_EN", Unicode(100)),
    Column("SOURCE_DE", Unicode),
    Column("PROCEDURE_DE", Unicode),
    Column("SOURCE_EN", Unicode),
    Column("PROCEDURE_EN", Unicode),
    Column("ND_ORDER", Integer),
    Column("NP_NAME_DE", Unicode(150)),
    Column("NP_NAME_EN", Unicode(150)),
    Column("TP", Integer),
    Column("PROCEDURE_DE_DOC", Unicode),
    Column("PROCEDURE_EN_DOC", Unicode),
    Column("DOW", Unicode),
    schema="dbo",
)


t_V_NAV_SERVICEMATRIX = Table(
    "V_NAV_SERVICEMATRIX",
    metadata,
    Column("N_ID", Integer, nullable=False),
    Column("NP_ID", Integer, nullable=False),
    Column("ND_SHORT", Unicode(10)),
    Column("NL_LEVEL", Integer),
    Column("PC_ID", Integer, nullable=False),
    Column("ND_ORDER", Integer),
    schema="dbo",
)


t_V_PROJECTLIST_PROOF = Table(
    "V_PROJECTLIST_PROOF",
    metadata,
    Column("PFP_ID", Integer, nullable=False),
    Column("PF_ID", Integer),
    Column("P_ID", Integer),
    Column("PC_ID", Integer),
    Column("P_PRODUCT", Unicode(255), nullable=False),
    Column("P_MODEL", Unicode(255), nullable=False),
    Column("PFP_REG", DateTime),
    Column("P_FOLDER", Unicode(255)),
    Column("PFP_REGBY", Unicode(90)),
    Column("P_DATE_CHECK", DateTime),
    schema="dbo",
)


t_V_PSEX_ACCOUNTING = Table(
    "V_PSEX_ACCOUNTING",
    metadata,
    Column("ACO_ID", Integer, nullable=False),
    Column("P_ID", Integer, nullable=False),
    Column("SO_NUMBER", Integer),
    Column("ACO_POS", Unicode(10)),
    Column("ACOT_ID", Integer, nullable=False),
    Column("ST_ID", Integer),
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("ACO_DATE", DateTime),
    Column("ZP_ID", Unicode(3)),
    Column("ZO_ID", Unicode(3)),
    Column("ZP_LOCATION", Unicode(2)),
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
    Column("ACO_DISABLED", BIT, nullable=False),
    Column("ACO_POSTINGSTATUS", String(12, "SQL_Latin1_General_CP1_CI_AS")),
    Column("ZM_ID", String(18, "SQL_Latin1_General_CP1_CI_AS")),
    Column("ACO_MEASURE", String(3, "SQL_Latin1_General_CP1_CI_AS")),
    Column("ACO_RATE_BASECUR", MONEY),
    Column("ACO_SPENDS_BASECUR", MONEY),
    Column("ACO_TOTAL_BASECUR", MONEY),
    Column("ACO_IS_LEGACY", BIT, nullable=False),
    Column("ACTUAL_HOURS", DECIMAL(5, 2)),
    Column("TRAVELS", DECIMAL(8, 2)),
    Column("EXTERNALS", DECIMAL(8, 2)),
    Column("INVOICE_LOCK", BIT),
    Column("SYSTEM_MESSAGE", String(512, "SQL_Latin1_General_CP1_CI_AS")),
    Column("ACO_IDOC_FILE", String(50, "SQL_Latin1_General_CP1_CI_AS")),
    Column("REJECT_MESSAGE", Unicode(512)),
    Column("ACO_REGBY_TEAM", Integer),
    Column("ACO_UPDATEBY_TEAM", Integer),
    Column("ST_ID_TEAM", Integer),
    Column("AL_ID", Integer),
    Column("IDOC_ID", Integer),
    Column("ST_ID_SAPOK", Integer),
    Column("NONCLEARABLE", BIT),
    Column("INVOICE_TEXT", String(512, "SQL_Latin1_General_CP1_CI_AS")),
    schema="dbo",
)


t_V_PSEX_ACCOUNTTYPE = Table(
    "V_PSEX_ACCOUNTTYPE",
    metadata,
    Column("ACOT_ID", Integer, nullable=False),
    Column("ACOT_NAME_DE", Unicode(256), nullable=False),
    Column("ACOT_NAME_EN", Unicode(256), nullable=False),
    Column("ACOT_NAME_FR", Unicode(256), nullable=False),
    schema="dbo",
)


t_V_PSEX_ACTION = Table(
    "V_PSEX_ACTION",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("SO_NUMBER", Integer),
    Column("ACT_NUMBER", Integer, nullable=False),
    Column("ACT_DATE", DateTime),
    Column("ACT_NEWDATE", DateTime),
    Column("ST_ID", Integer),
    Column("ACTT_ID", Integer),
    Column("ACT_INFO", Unicode(512)),
    Column("ACT_FILE", Unicode(255)),
    Column("ACT_READY", SMALLDATETIME),
    Column("ACT_INTERNAL", BIT, nullable=False),
    Column("ACT_PREDATE", DateTime),
    Column("ACT_REMINDER", BIT, nullable=False),
    Column("ACT_PREDATEINFO", Unicode(255)),
    Column("ACT_REGBY", Integer),
    Column("ACT_REGDATE", DateTime),
    Column("ACT_UPDATEBY", Integer),
    Column("ACT_UPDATE", DateTime),
    Column("REPORT_SENT", BIT, nullable=False),
    schema="dbo",
)


t_V_PSEX_ACTION_TYPE = Table(
    "V_PSEX_ACTION_TYPE",
    metadata,
    Column("ACTT_ID", Integer, nullable=False),
    Column("ACTT_NAME_DE", Unicode(256), nullable=False),
    Column("ACTT_NAME_EN", Unicode(256), nullable=False),
    Column("ACTT_NAME_FR", Unicode(256), nullable=False),
    schema="dbo",
)


t_V_PSEX_BEGRIFF = Table(
    "V_PSEX_BEGRIFF",
    metadata,
    Column("BEGR_ID", Integer, nullable=False),
    Column("BEGR_BAUNR", Unicode(255)),
    Column("BEGRIFF_DE", Unicode(255)),
    Column("BEGRIFF_EN", Unicode(255)),
    schema="dbo",
)


t_V_PSEX_CATEGORY = Table(
    "V_PSEX_CATEGORY",
    metadata,
    Column("ID", Integer, nullable=False),
    Column("NAME", Unicode(256), nullable=False),
    Column("ZM_ID", String(18, "SQL_Latin1_General_CP1_CI_AS")),
    Column("CU_ID", Integer),
    Column("KOB_ID", Integer),
    Column("DEFAULT_PRICE", DECIMAL(18, 2)),
    Column("DEFAULT_SALES_RATE", DECIMAL(18, 2)),
    Column("DEFAULT_SPENDS", DECIMAL(18, 2)),
    Column("DEFAULT_EXTERNALS", DECIMAL(18, 2)),
    Column("DEFAULT_SUBORDERS", DECIMAL(18, 2)),
    Column("DEFAULT_LICENSES", DECIMAL(18, 2)),
    Column("DEFAULT_TRAVELS", DECIMAL(18, 2)),
    Column("DEFAULT_CORRECTION_FACTOR", DECIMAL(18, 2)),
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("IS_FOR_AUDIT_PROJECTS", BIT, nullable=False),
    Column("IS_DEFAULT_FOR_NEW_PROJECTS", BIT, nullable=False),
    Column("PARENT", Integer),
    Column("SORT", Integer),
    Column("DISABLED", DateTime),
    Column("CREATED", DateTime, nullable=False),
    Column("CREATED_BY", Integer, nullable=False),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    schema="dbo",
)


t_V_PSEX_CATEGORY_WORKING_CLUSTER = Table(
    "V_PSEX_CATEGORY_WORKING_CLUSTER",
    metadata,
    Column("ID", Integer, nullable=False),
    Column("CATEGORY_ID", Integer, nullable=False),
    Column("WORKING_CLUSTER_ID", UNIQUEIDENTIFIER),
    Column("DISABLED", BIT, nullable=False),
    Column("CREATED", DateTime, nullable=False),
    Column("CREATED_BY", Integer, nullable=False),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    schema="dbo",
)


t_V_PSEX_CATEGORY_WORKING_CLUSTER_DEPARTMENT = Table(
    "V_PSEX_CATEGORY_WORKING_CLUSTER_DEPARTMENT",
    metadata,
    Column("ID", Integer, nullable=False),
    Column("CATEGORY_WORKING_CLUSTER_ID", Integer, nullable=False),
    Column("DEPARTMENT_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("DISABLED", BIT, nullable=False),
    Column("CREATED", DateTime, nullable=False),
    Column("CREATED_BY", Integer, nullable=False),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    schema="dbo",
)


t_V_PSEX_CURRENCY = Table(
    "V_PSEX_CURRENCY",
    metadata,
    Column("CUR_ID", NCHAR(3), nullable=False),
    Column("CUR_SHORT", NCHAR(3), nullable=False),
    Column("CUR_NAME", Unicode(256), nullable=False),
    Column("CUR_SIGN", Unicode(4), nullable=False),
    Column("CREATED", DateTime, nullable=False),
    Column("CREATED_BY", Integer, nullable=False),
    Column("UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    Column("CUR_DECIMAL_PLACES", Integer, nullable=False),
    Column("RUN_ID", Integer),
    schema="dbo",
)


t_V_PSEX_CURRENCY_RATE = Table(
    "V_PSEX_CURRENCY_RATE",
    metadata,
    Column("CUR_FROM", NCHAR(3), nullable=False),
    Column("CUR_TO", NCHAR(3), nullable=False),
    Column("VALID_FROM", Date, nullable=False),
    Column("VALUE", DECIMAL(18, 5), nullable=False),
    Column("INSERTED", DateTime, nullable=False),
    Column("UPDATED", DateTime, nullable=False),
    Column("RUN_ID", Integer),
    schema="dbo",
)

t_V_PSEX_CUSTOMER_CONTACT = Table(
    "V_PSEX_CUSTOMER_CONTACT",
    metadata,
    Column("CUC_ID", Integer, nullable=False),
    Column("CU_ID", Integer, nullable=False),
    Column("CUC_FORENAME", Unicode(35)),
    Column("CUC_SURNAME", Unicode(35)),
    Column("CUC_PHONE", Unicode(50)),
    Column("CUC_FAX", Unicode(50)),
    Column("CUC_MOBILE", Unicode(50)),
    Column("CUC_MAIL", Unicode(255)),
    Column("CUC_SCOPE", Unicode(60)),
    schema="dbo",
)


t_V_PSEX_CUSTOMER_NATION = Table(
    "V_PSEX_CUSTOMER_NATION",
    metadata,
    Column("CN_ID", Integer, nullable=False),
    Column(
        "CN_NATION", String(1, "SQL_Latin1_General_CP1_CI_AS"), nullable=False
    ),
    Column("CN_DISPLAY_EN", Unicode(120)),
    Column("CN_DISPLAY_DE", Unicode(120)),
    Column("CN_DISPLAY_FR", Unicode(120)),
    schema="dbo",
)


t_V_PSEX_DELAYREASON = Table(
    "V_PSEX_DELAYREASON",
    metadata,
    Column("DELR_ID", Integer, nullable=False),
    Column("DELR_NAME_DE", Unicode(256), nullable=False),
    Column("DELR_NAME_EN", Unicode(256), nullable=False),
    Column("DELR_NAME_FR", Unicode(256), nullable=False),
    schema="dbo",
)


t_V_PSEX_EDOC_PSE = Table(
    "V_PSEX_EDOC_PSE",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("E_ID", Integer),
    schema="dbo",
)


t_V_PSEX_HIERARCHY = Table(
    "V_PSEX_HIERARCHY",
    metadata,
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_SHORT", Unicode(20)),
    Column("HR_TYPE", Unicode(50)),
    Column("HR_PARENT", UNIQUEIDENTIFIER),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("HR_LOCATION", Unicode(40)),
    Column("HR_PREFIX", Unicode(20)),
    Column("HR_ACTIVE", BIT, nullable=False),
    Column("HR_CURRENT", BIT),
    Column("HR_EMAIL", String(80, "SQL_Latin1_General_CP1_CI_AS")),
    Column("ST_ID", Integer),
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    schema="dbo",
)


t_V_PSEX_HIERARCHY_DEPARTMENT = Table(
    "V_PSEX_HIERARCHY_DEPARTMENT",
    metadata,
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_SHORT", Unicode(20)),
    Column("HR_TYPE", Unicode(50)),
    Column("HR_PARENT", UNIQUEIDENTIFIER),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("HR_LOCATION", Unicode(40)),
    Column("HR_PREFIX", Unicode(20)),
    schema="dbo",
)


t_V_PSEX_KIND_OF_BILL = Table(
    "V_PSEX_KIND_OF_BILL",
    metadata,
    Column("KOB_ID", Integer, nullable=False),
    Column("KOB_NAME_DE", Unicode(256), nullable=False),
    Column("KOB_NAME_EN", Unicode(256), nullable=False),
    Column("KOB_NAME_FR", Unicode(256), nullable=False),
    schema="dbo",
)


t_V_PSEX_KIND_OF_PRODUCT = Table(
    "V_PSEX_KIND_OF_PRODUCT",
    metadata,
    Column("KOP_ID", Integer, nullable=False),
    Column("KOP_NAME_DE", Unicode(256), nullable=False),
    Column("KOP_NAME_EN", Unicode(256), nullable=False),
    Column("KOP_NAME_FR", Unicode(256), nullable=False),
    schema="dbo",
)


t_V_PSEX_KIND_OF_TEST = Table(
    "V_PSEX_KIND_OF_TEST",
    metadata,
    Column("KOT_ID", Integer, nullable=False),
    Column("KOT_SHORT", Unicode(256), nullable=False),
    Column("KOT_NAME_DE", Unicode(256), nullable=False),
    Column("KOT_NAME_EN", Unicode(256), nullable=False),
    Column("KOT_NAME_FR", Unicode(256), nullable=False),
    Column("WORKING_CLUSTER", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_SHORT", Unicode(20)),
    schema="dbo",
)


t_V_PSEX_KST = Table(
    "V_PSEX_KST",
    metadata,
    Column(
        "CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS"), nullable=False
    ),
    Column("CC_BOOKINGAREA", Unicode(4)),
    Column("CC_TYPE", Integer),
    Column("KTEXT", Unicode(256)),
    Column("LTEXT", Unicode(256)),
    Column("CC_NAME", Unicode(16)),
    schema="dbo",
)


t_V_PSEX_KST_RATE = Table(
    "V_PSEX_KST_RATE",
    metadata,
    Column(
        "CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS"), nullable=False
    ),
    Column("CCR_PRODUCTIVE_RATE", DECIMAL(18, 2), nullable=False),
    Column("CCR_UNPRODUCTIVE_RATE", DECIMAL(18, 2), nullable=False),
    Column("CCR_INTERNAL_RATE", DECIMAL(18, 2), nullable=False),
    Column("CUR_ID", String(3, "SQL_Latin1_General_CP1_CI_AS")),
    Column("CCR_VALID_FROM", DateTime),
    Column("CCR_TRAVEL_RATE", DECIMAL(18, 2), nullable=False),
    schema="dbo",
)


t_V_PSEX_LOCATIONSERVER = Table(
    "V_PSEX_LOCATIONSERVER",
    metadata,
    Column("LS_ID", Integer, nullable=False),
    Column("LS_SERVERPATH", Unicode(255), nullable=False),
    Column("LS_REMARK", Unicode(255)),
    Column("LS_WEBSERVER", Unicode(255)),
    Column("LS_SAPSERVER", Integer),
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("LS_BASE_CURRENCY", Unicode(3)),
    schema="dbo",
)


t_V_PSEX_PM_PORTALRIGHTS = Table(
    "V_PSEX_PM_PORTALRIGHTS",
    metadata,
    Column("ID", BigInteger, nullable=False),
    Column("FullUserName", Unicode(256), nullable=False),
    Column("PORTAL_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_PSEX_PROCESS = Table(
    "V_PSEX_PROCESS",
    metadata,
    Column("PC_ID", Integer, nullable=False),
    Column("PC_PATH", Unicode(50)),
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
    Column("PC_CREATEDBY_TEAM", Integer),
    Column("PC_UPDATEBY_TEAM", Integer),
    Column("PC_REGDATE", DateTime),
    Column("PC_CREATEDBY", Integer),
    Column("PC_DISABLED", BIT, nullable=False),
    schema="dbo",
)


t_V_PSEX_PROCESSPHASE = Table(
    "V_PSEX_PROCESSPHASE",
    metadata,
    Column("PRP_ID", Integer, nullable=False),
    Column("PRP_NAME_DE", Unicode(256)),
    Column("PRP_NAME_EN", Unicode(256)),
    Column("PRP_NAME_FR", Unicode(256)),
    Column("PRP_SHORT_DE", Unicode(256)),
    Column("PRP_SHORT_EN", Unicode(256)),
    Column("PRP_SHORT_FR", Unicode(256)),
    Column("PRP_SORT", Integer, nullable=False),
    Column("PRP_SHOW_IN_PSEX", BIT, nullable=False),
    Column("PRP_EDOC_ACTIVE", BIT, nullable=False),
    Column("PRP_EDOC_NAME_DE", Unicode(256)),
    Column("PRP_EDOC_NAME_EN", Unicode(256)),
    Column("PRP_EDOC_SHORT_DE", Unicode(256)),
    Column("PRP_EDOC_SHORT_EN", Unicode(256)),
    Column("PRP_EDOC_SHORT_FR", Unicode(256)),
    Column("PRP_EDOC_NUMBER", Integer),
    Column("PRP_EDOC_IS_REFERENCE", BIT, nullable=False),
    Column("PRP_EDOC_IS_DEFAULT", BIT, nullable=False),
    Column("PRP_EDOC_NAME_FR", Unicode(256)),
    schema="dbo",
)


t_V_PSEX_PROCESSPHASE_L = Table(
    "V_PSEX_PROCESSPHASE_L",
    metadata,
    Column("PRP_ID", Integer, nullable=False),
    Column("PRP_EDOC_SHORT", Unicode(20)),
    Column("PRP_EDOC_NAME", Unicode(50)),
    Column("PRP_EDOC_NUMBER", Integer),
    Column("PRP_EDOC_IS_REFERENCE", BIT, nullable=False),
    Column("PRP_EDOC_IS_DEFAULT", BIT, nullable=False),
    Column("PRP_EDOC_ACTIVE", BIT, nullable=False),
    Column("Locale", Unicode(50)),
    schema="dbo",
)


t_V_PSEX_PROJECT = Table(
    "V_PSEX_PROJECT",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("P_FOLDER", Unicode(255)),
    Column("P_PRODUCT", Unicode(255)),
    Column("P_MODEL", Unicode(255)),
    Column("PC_ID", Integer),
    Column("P_DATE_DONE", DateTime),
    Column("P_PREDATE", DateTime),
    Column("P_DEADLINE", DateTime),
    Column("P_DATE_ORDER", DateTime),
    Column("MD_ID", Integer, nullable=False),
    Column("P_CUSTOMER_A", Integer),
    Column("P_CUSTOMER_B", Integer),
    Column("P_STATUS", Integer),
    Column("P_DATE_CHECK", DateTime),
    Column("P_CHECKBY", Integer),
    Column("TC_P_ID", Integer),
    Column("P_ORDERTEXT", Unicode(2048)),
    Column("P_PROJECTINFO", Unicode(4000)),
    Column("P_IS_QUOTATION", BIT, nullable=False),
    Column("P_ZARA_NUMBER", Unicode(10)),
    Column("P_NAME", Unicode(30)),
    Column("SC_ID", Unicode(7), nullable=False),
    Column("P_PROJECTMANAGER", Integer),
    Column("P_HANDLEDBY", Integer),
    Column("P_DATE_APPOINTMENT", DateTime),
    Column("P_DATE_READY", DateTime),
    Column("P_READYBY", Integer),
    Column("P_DATE_DISPO", DateTime),
    Column("P_DONEBY", Integer),
    Column("RES_ID", Integer),
    Column("P_DELAY", DECIMAL(18, 0)),
    Column("DELR_ID", Integer),
    Column("P_ACTION", BIT),
    Column("P_FORECAST", DECIMAL(18, 2)),
    Column("P_WC_ID", UNIQUEIDENTIFIER),
    Column("CC_ID", Unicode(10)),
    Column("P_CHECKBY_TEAM", Integer),
    Column("P_DONEBY_TEAM", Integer),
    Column("P_HANDLEDBY_TEAM", Integer),
    Column("P_PROJECTMANAGER_TEAM", Integer),
    Column("P_READYBY_TEAM", Integer),
    Column("P_REGBY_TEAM", Integer),
    Column("P_UPDATEBY_TEAM", Integer),
    Column("KOT_ID", Integer),
    Column("P_TS_RECEIPT_ADVISED", BIT, nullable=False),
    Column("P_ORDERSIZE", DECIMAL(18, 2)),
    Column("P_EXPECTED_TS_RECEIPT", DateTime),
    Column("P_PLANNED_ORDERSIZE", DECIMAL(18, 2)),
    Column("P_INTERN", BIT),
    Column("P_CUR_ID", NCHAR(3)),
    Column("P_CURRENCYRATE", DECIMAL(18, 0)),
    Column("P_REGBY", Integer),
    Column("P_REGDATE", DateTime),
    Column("SAP_QUOTATION_NUMBER", Unicode(10)),
    Column("P_PROJECTFOLDERCREATED", BIT, nullable=False),
    Column("BR_ID", UNIQUEIDENTIFIER),
    Column("P_TEAM_ID", UNIQUEIDENTIFIER),
    Column("P_AUDIT_DATE", DateTime),
    Column("P_PROCESSPHASE", Integer),
    Column("P_IAN", Unicode(256)),
    Column("P_TOKEN", Unicode(60)),
    Column("CATEGORY_ID", Integer, nullable=False),
    Column("E_ID", Integer),
    Column("P_CONTACT_CUC_ID", Integer),
    Column("P_REMARK", Unicode(1024)),
    Column("BATCH_NUMBER", Unicode(16)),
    Column("P_RETEST", Integer, nullable=False),
    Column("P_RETEST_OF", Integer),
    schema="dbo",
)


t_V_PSEX_PROJECT_POSITION = Table(
    "V_PSEX_PROJECT_POSITION",
    metadata,
    Column("PP_ID", Integer, nullable=False),
    Column("P_ID", Integer, nullable=False),
    Column("PP_IS_QUOTATION_POSITION", BIT),
    Column("PP_NUMBER", Integer, nullable=False),
    Column("PP_DISABLED", BIT, nullable=False),
    Column("PP_STATUS", Integer, nullable=False),
    Column("PP_STATUS_CHANGED_ON", DateTime),
    Column("PP_STATUS_CHANGED_BY", Integer),
    Column("PP_TEXT", Unicode(1024)),
    Column("PP_SALES_PRICE", DECIMAL(18, 2)),
    Column("ZM_ID", String(18, "SQL_Latin1_General_CP1_CI_AS")),
    Column("PP_TYPE", Integer, nullable=False),
    Column("PP_LAST_SAP_UPDATE", DateTime),
    Column("PP_CANCELLATION_FLAG", BIT, nullable=False),
    Column("PP_CREATED", DateTime, nullable=False),
    Column("PP_CREATED_BY", Integer, nullable=False),
    Column("PP_UPDATED", DateTime),
    Column("PP_UPDATED_BY", Integer),
    Column("PP_PREPAYMENT_PRICE", DECIMAL(18, 2), nullable=False),
    Column("PP_PRINTING_FLAG", Unicode(5)),
    Column("PP_SINGLE_PRICE", DECIMAL(18, 2), nullable=False),
    Column("PP_TARGET_COUNT", Integer, nullable=False),
    Column("PP_SP_FOREIGN", DECIMAL(18, 2)),
    Column("FROM_PS_CONFIG", BIT, nullable=False),
    Column("PP_UNIT", Unicode(3)),
    schema="dbo",
)


t_V_PSEX_PROKALKMODUL = Table(
    "V_PSEX_PROKALKMODUL",
    metadata,
    Column("PKM_ID", Integer, nullable=False),
    Column("P_ID", Integer, nullable=False),
    Column("KALM_ID", Integer),
    Column("KAL_ID", Integer),
    Column("PKM_TYP", Integer),
    Column("PKM_NAME", Unicode(256)),
    Column("PKM_IS_UA", BIT),
    Column("PKM_TAGE_UA", Integer),
    Column("TP_ID", Integer),
    Column("PKM_TESTDAUER", Integer),
    Column("PKM_EINHEITEN", DECIMAL(18, 2)),
    Column("PKM_SATZ", DECIMAL(18, 2)),
    Column("PKM_AUFWAND", DECIMAL(18, 2)),
    Column("PKM_FAKTOR", DECIMAL(18, 2)),
    Column("PKM_VK", DECIMAL(18, 2)),
    Column("PKM_AUFTRAGSTEXT", Unicode(500)),
    Column("PKM_KOMMENTAR", Unicode(500)),
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
    Column("PKM_DISABLED", BIT, nullable=False),
    Column("FROM_PS_CONFIG", BIT, nullable=False),
    schema="dbo",
)


t_V_PSEX_PROKALKUNTERMODUL = Table(
    "V_PSEX_PROKALKUNTERMODUL",
    metadata,
    Column("PKUM_ID", Integer, nullable=False),
    Column("PKM_ID", Integer, nullable=False),
    Column("P_ID", Integer, nullable=False),
    Column("SO_NUMBER", Integer),
    Column("PKUM_QUOTATION_POSITION", Integer),
    Column("PKUM_TESTING_POSITION", Integer),
    Column("ST_ID", Integer),
    Column("PKUM_NAME", Unicode(1024)),
    Column("PKUM_DAYS_TO_START", Integer, nullable=False),
    Column("PKUM_DURATION", Integer, nullable=False),
    Column("TP_ID", Integer),
    Column("PKUM_PLANNED_HOURS", DECIMAL(18, 2), nullable=False),
    Column("PKUM_PLANNED_EXPENSES", DECIMAL(18, 2), nullable=False),
    Column("PKUM_FACTOR", DECIMAL(18, 2), nullable=False),
    Column("PKUM_PLANNED_TRAVEL_COSTS", DECIMAL(18, 2), nullable=False),
    Column("PKUM_RECOMMENDED_PRICE", DECIMAL(18, 2), nullable=False),
    Column("PKUM_COMMENT", Unicode(2000)),
    Column("PKUM_ORDER_TEXT", Unicode(1024)),
    Column("PKUM_ADDITIONAL_TEXT", Unicode(1024)),
    Column("PKUM_SAP_TRANSFER", DateTime),
    Column("PKUM_SORT", Integer, nullable=False),
    Column("PKUM_DISABLED", BIT, nullable=False),
    Column("PKUM_CREATED", DateTime, nullable=False),
    Column("PKUM_CREATED_BY", Integer, nullable=False),
    Column("PKUM_UPDATED", DateTime),
    Column("PKUM_UPDATED_BY", Integer),
    Column("PKUM_SO_TRANSFER_PRICE", DECIMAL(18, 2), nullable=False),
    Column("PKUM_SP_PRICELIST", DECIMAL(18, 2), nullable=False),
    Column("PKUM_TRAVELTIME", DECIMAL(18, 2), nullable=False),
    Column("PKUM_SP_FOREIGN", DECIMAL(18, 10)),
    Column("ZM_ID", String(18, "SQL_Latin1_General_CP1_CI_AS")),
    Column("PKUM_BULKTEST", BIT),
    Column("PKUM_SP_PRICELIST_ORG", DECIMAL(18, 2), nullable=False),
    Column("PKUM_CANCELLED", BIT, nullable=False),
    Column("FROM_PS_CONFIG", BIT, nullable=False),
    schema="dbo",
)


t_V_PSEX_RESULT = Table(
    "V_PSEX_RESULT",
    metadata,
    Column("RES_ID", Integer, nullable=False),
    Column("RES_NAME_A", Unicode(70)),
    Column("RES_NAME_B", Unicode(70)),
    Column("UpdateDate", DateTime),
    Column("UpdateByID", Integer),
    Column("RES_UPDATE_TYPE", TINYINT),
    schema="dbo",
)


t_V_PSEX_STAFF = Table(
    "V_PSEX_STAFF",
    metadata,
    Column("ST_ID", Integer, nullable=False),
    Column("ST_SURNAME", Unicode(60), nullable=False),
    Column("ST_FORENAME", Unicode(50)),
    Column("ST_COSTID", Unicode(10)),
    Column("ST_ACTIVE", BIT, nullable=False),
    Column("ST_NUMBER", Unicode(8)),
    Column("ST_SHORT", Unicode(3)),
    Column("ST_PHONE", Unicode(40)),
    Column("ST_FAX", Unicode(40)),
    Column("ST_EMAIL", Unicode(80)),
    Column("ST_WINDOWSID", String(32, "SQL_Latin1_General_CP1_CI_AS")),
    Column("ST_TEAM", UNIQUEIDENTIFIER),
    Column("ST_TYPE", Integer, nullable=False),
    Column("ST_LOCATION", Unicode(50)),
    Column("ST_UNIT", Unicode(12)),
    Column("ST_SERVERID", Integer),
    Column("ST_HOURS_PER_DAY", Integer),
    Column(
        "ST_SKILLGROUP",
        String(8, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
    ),
    Column("ST_DOMAIN", String(32, "SQL_Latin1_General_CP1_CI_AS")),
    Column("ST_GENDER", Unicode(50)),
    schema="dbo",
)


t_V_PSEX_STAFFROLE = Table(
    "V_PSEX_STAFFROLE",
    metadata,
    Column("ST_ID", Integer, nullable=False),
    Column("RS_ID", Integer, nullable=False),
    Column("RS_ROLENAME", Unicode(25), nullable=False),
    schema="dbo",
)


t_V_PSEX_SUBORDERS = Table(
    "V_PSEX_SUBORDERS",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("SO_NUMBER", Integer, nullable=False),
    Column("SO_DISPOBY", Integer),
    Column("SO_CREATED", DateTime),
    Column("ST_ID", Integer),
    Column("SO_DEADLINE", DateTime),
    Column("SO_TASK", Unicode(1024)),
    Column("SO_HOURS", DECIMAL(18, 6)),
    Column("SO_ACC_HOURS", MONEY),
    Column("SO_COMMENT", Unicode(2000)),
    Column("SO_DATE_READY", DateTime),
    Column("SO_DATE_CHECK", DateTime),
    Column("RES_ID", Integer),
    Column("SO_PREDATE", DateTime),
    Column("SO_WAIT", BIT),
    Column("SO_REPORT", Unicode(255)),
    Column("SO_DISABLED", BIT, nullable=False),
    Column("SO_FORECAST", DECIMAL(18, 2)),
    Column("SO_INTERN", BIT),
    Column("ST_ID_TEAM", Integer),
    Column("SO_UPDATEBY_TEAM", Integer),
    Column("SO_REGBY_TEAM", Integer),
    Column("SO_READYBY_TEAM", Integer),
    Column("SO_DISPOBY_TEAM", Integer),
    Column("SO_CHECKBY_TEAM", Integer),
    Column("ORDER_POSITION", Unicode(6)),
    Column("ORDER_DATE", DateTime),
    Column("ORDER_SIGN", Unicode(35)),
    Column("SAP_NO", Unicode(10)),
    Column("SO_READYBY", Integer),
    Column("SO_RATE", MONEY),
    Column("SO_SPENDS", MONEY),
    Column("SO_POST_OUT_DATE", DateTime),
    Column("SO_CONFIRMED_DATE", DateTime),
    Column("ZM_ID", Unicode(18)),
    Column("SO_REMARK", Unicode(1024)),
    Column("SO_MODEL", Unicode(255)),
    Column("SO_SORT", Integer, nullable=False),
    Column("KPI", BIT, nullable=False),
    Column("S_KPI_NUMBER", Integer),
    Column("REPORT_SENT", DateTime),
    schema="dbo",
)


t_V_PSEX_TC_PROJECT = Table(
    "V_PSEX_TC_PROJECT",
    metadata,
    Column("P_ID", Integer, nullable=False),
    Column("P_CUSTOMER_A", Integer, nullable=False),
    Column("P_PRODUCT", Unicode(255), nullable=False),
    Column("P_DEADLINE", DateTime, nullable=False),
    Column("P_PROJECTINFO", Unicode(1024), nullable=False),
    Column("P_PREDATE", DateTime, nullable=False),
    Column("P_REGBY", Integer, nullable=False),
    Column("P_WC_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("P_PSOBJECT_TERM", Integer),
    Column("P_PSOBJECT_LANGUAGEID", Integer),
    Column("E_ID", Integer),
    Column("P_NUMBER_OF_TESTSAMPLES", Integer, nullable=False),
    Column("P_IS_QUOTATION", BIT, nullable=False),
    Column("P_PLANNED_ORDERSIZE", DECIMAL(18, 2), nullable=False),
    schema="dbo",
)


t_V_PSEX_TC_PROJECT_POSITION = Table(
    "V_PSEX_TC_PROJECT_POSITION",
    metadata,
    Column("PP_ID", Integer, nullable=False),
    Column("P_ID", Integer, nullable=False),
    Column("PP_NUMBER", Integer, nullable=False),
    Column("PP_TEXT", Unicode(1024)),
    Column("PP_SALES_PRICE", DECIMAL(18, 2)),
    Column("ZM_ID", String(18, "SQL_Latin1_General_CP1_CI_AS")),
    Column("PP_TYPE", Integer, nullable=False),
    schema="dbo",
)


t_V_PSEX_TC_PROKALKMODUL = Table(
    "V_PSEX_TC_PROKALKMODUL",
    metadata,
    Column("PKM_ID", Integer, nullable=False),
    Column("P_ID", Integer, nullable=False),
    Column("PKM_TYP", Integer, nullable=False),
    Column("PKM_NAME", Unicode(256), nullable=False),
    Column("PKM_REIHE", Integer, nullable=False),
    schema="dbo",
)


t_V_PSEX_TC_PROKALKUNTERMODUL = Table(
    "V_PSEX_TC_PROKALKUNTERMODUL",
    metadata,
    Column("PKUM_ID", Integer, nullable=False),
    Column("PKM_ID", Integer, nullable=False),
    Column("P_ID", Integer, nullable=False),
    Column("ST_ID", Integer, nullable=False),
    Column("PKUM_NAME", Unicode(256), nullable=False),
    Column("PKUM_DAYS_TO_START", Integer, nullable=False),
    Column("PKUM_DURATION", Integer, nullable=False),
    Column("TP_ID", Integer),
    Column("PKUM_PLANNED_HOURS", DECIMAL(18, 2), nullable=False),
    Column("PKUM_PLANNED_EXPENSES", DECIMAL(18, 2), nullable=False),
    Column("PKUM_FACTOR", DECIMAL(18, 2), nullable=False),
    Column("PKUM_PLANNED_TRAVEL_COSTS", DECIMAL(18, 2), nullable=False),
    Column("PKUM_RECOMMENDED_PRICE", DECIMAL(18, 2), nullable=False),
    Column("PKUM_COMMENT", Unicode(500), nullable=False),
    Column("PKUM_ORDER_TEXT", Unicode(500), nullable=False),
    Column("PKUM_SORT", Integer, nullable=False),
    Column("PP_ID", Integer),
    Column("ZM_ID", Unicode(18)),
    Column("PKUM_PLANNED_EXPENSES_EXTERNAL", DECIMAL(18, 2), nullable=False),
    schema="dbo",
)


t_V_PSEX_TC_VERIFICATION_DOCUMENT = Table(
    "V_PSEX_TC_VERIFICATION_DOCUMENT",
    metadata,
    Column("VD_ID", Integer, nullable=False),
    Column("P_ID", Integer, nullable=False),
    Column("VD_NAME", Unicode(1024), nullable=False),
    Column("VD_CATEGORY", Integer, nullable=False),
    Column("VD_SORT", Integer, nullable=False),
    schema="dbo",
)


t_V_PSEX_TEMPLATE = Table(
    "V_PSEX_TEMPLATE",
    metadata,
    Column("TP_ID", Integer, nullable=False),
    Column("MD_ID", Integer, nullable=False),
    Column("TPST_ID", Integer),
    Column("TPT_ID", Integer),
    Column("TPSC_ID", Integer),
    Column("TPF_ID", Integer),
    Column("TP_NAME_D", Unicode(255)),
    Column("TP_TIME_HOURS", Float(53)),
    Column("TP_TIME_DAYS", Float(53)),
    Column("TP_COSTS", DECIMAL(18, 2)),
    Column("TP_TESTPERSON_REQUIRED", BIT, nullable=False),
    Column("TP_NAME_E", Unicode(255)),
    Column("TP_NAME_F", Unicode(255)),
    Column("TP_COMMENT", Unicode(255)),
    Column("TP_VERSION", Integer),
    Column("TP_LANGUAGE", Unicode(255)),
    Column("TP_CLEARINGDATE", DateTime),
    Column("TP_CLEARINGBY", Integer),
    Column("TP_FILENAME", Unicode(255)),
    Column("TP_REGDATE", DateTime),
    Column("TP_REGBY", Integer),
    Column("TP_UPDATE", DateTime),
    Column("TP_UPDATEBY", Integer),
    Column("TP_ISGLOBAL", BIT),
    Column("TP_DISABLED", BIT, nullable=False),
    Column("TP_TRANSFER_STATUS", Unicode(50)),
    Column("TP_ORIGINATING_SERVERID", Integer),
    Column("TP_ROOT_TEMPLATE_ID", Integer),
    Column(
        "TP_FILE_EXPORTED",
        CHAR(1, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
    ),
    Column("TP_UTC", DateTime),
    Column("TP_WORKINGCLUSTER", UNIQUEIDENTIFIER),
    Column("DM_ID", Integer),
    Column("TP_OLD_TP", Integer),
    schema="dbo",
)


t_V_PSEX_TEMPLATE_DATA = Table(
    "V_PSEX_TEMPLATE_DATA",
    metadata,
    Column("TPD_ID", Integer, nullable=False),
    Column("TP_ID", Integer, nullable=False),
    Column("TPD_DATA", IMAGE, nullable=False),
    schema="dbo",
)


t_V_PSEX_TEMPLATE_FORMAT = Table(
    "V_PSEX_TEMPLATE_FORMAT",
    metadata,
    Column("TPF_ID", Integer, nullable=False),
    Column("TPF_NAME_DE", Unicode(256), nullable=False),
    Column("TPF_NAME_EN", Unicode(256), nullable=False),
    Column("TPF_NAME_FR", Unicode(256), nullable=False),
    Column("TPF_SHORT_DE", Unicode(256), nullable=False),
    Column("TPF_SHORT_EN", Unicode(256), nullable=False),
    Column("TPF_SHORT_FR", Unicode(256), nullable=False),
    schema="dbo",
)


t_V_PSEX_TEMPLATE_KEY = Table(
    "V_PSEX_TEMPLATE_KEY",
    metadata,
    Column("TPK_ID", Integer, nullable=False),
    Column("TP_ID", Integer),
    Column("TP_KEY", Unicode(255)),
    Column("TP_DISABLED", BIT, nullable=False),
    Column("TP_ROOT_TPK_ID", Integer),
    schema="dbo",
)


t_V_PSEX_TEMPLATE_PATH = Table(
    "V_PSEX_TEMPLATE_PATH",
    metadata,
    Column("TEMPLATEPATH", Unicode(779)),
    Column("TP_ID", Integer, nullable=False),
    Column("TP_ISGLOBAL", BIT),
    schema="dbo",
)


t_V_PSEX_TEMPLATE_SCOPE = Table(
    "V_PSEX_TEMPLATE_SCOPE",
    metadata,
    Column("TPSC_ID", Integer, nullable=False),
    Column("TPSC_NAME_DE", Unicode(256), nullable=False),
    Column("TPSC_NAME_EN", Unicode(256), nullable=False),
    Column("TPSC_NAME_FR", Unicode(256), nullable=False),
    Column("TPSC_SHORT_DE", Unicode(256), nullable=False),
    Column("TPSC_SHORT_EN", Unicode(256), nullable=False),
    Column("TPSC_SHORT_FR", Unicode(256), nullable=False),
    Column("TPSC_PATH", Unicode(256), nullable=False),
    schema="dbo",
)


t_V_PSEX_TEMPLATE_STATUS = Table(
    "V_PSEX_TEMPLATE_STATUS",
    metadata,
    Column("TPST_ID", Integer, nullable=False),
    Column("TPST_NAME_DE", Unicode(256), nullable=False),
    Column("TPST_NAME_EN", Unicode(256), nullable=False),
    Column("TPST_NAME_FR", Unicode(256), nullable=False),
    Column("TPST_SHORT_DE", Unicode(256), nullable=False),
    Column("TPST_SHORT_EN", Unicode(256), nullable=False),
    Column("TPST_SHORT_FR", Unicode(256), nullable=False),
    schema="dbo",
)


t_V_PSEX_TEMPLATE_TYPE = Table(
    "V_PSEX_TEMPLATE_TYPE",
    metadata,
    Column("TPT_ID", Integer, nullable=False),
    Column("TPT_NAME_DE", Unicode(256), nullable=False),
    Column("TPT_NAME_EN", Unicode(256), nullable=False),
    Column("TPT_NAME_FR", Unicode(256), nullable=False),
    Column("TPT_SHORT_DE", Unicode(256), nullable=False),
    Column("TPT_SHORT_EN", Unicode(256), nullable=False),
    Column("TPT_SHORT_FR", Unicode(256), nullable=False),
    Column("TPT_PATH", Unicode(256), nullable=False),
    Column("TPT_PREFIX", Unicode(256), nullable=False),
    Column("TPT_MODULETYPE", Unicode(256)),
    Column("TPT_SHOWINPROZESSFOLDER", BIT, nullable=False),
    Column("TPT_SHOWINTEMPLATEMANAGER", BIT, nullable=False),
    schema="dbo",
)


t_V_PSEX_TESTSAMPLE = Table(
    "V_PSEX_TESTSAMPLE",
    metadata,
    Column("TS_ID", Integer, nullable=False),
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
    Column("TS_DISABLED", BIT, nullable=False),
    Column("TS_UPDATEBY", Integer),
    Column("TS_UPDATE", DateTime),
    Column("TS_CREATEDBY", Integer),
    Column("TS_CREATED", DateTime),
    Column("TS_CREATEDBY_TEAM", Integer),
    Column("TS_UPDATEBY_TEAM", Integer),
    Column("AL_ID", Integer),
    schema="dbo",
)


t_V_PSEX_TESTSAMPLECHARACTERISTICS = Table(
    "V_PSEX_TESTSAMPLECHARACTERISTICS",
    metadata,
    Column("TC_ID", Integer, nullable=False),
    Column("TC_NAME", Unicode(2000)),
    Column("TC_VALUE", Unicode(2000)),
    Column("TS_ID", Integer, nullable=False),
    Column("TS_DISABLED", BIT, nullable=False),
    Column("TC_NUMBER", Integer, nullable=False),
    schema="dbo",
)


t_V_PSEX_TESTSAMPLEPICTURE = Table(
    "V_PSEX_TESTSAMPLEPICTURE",
    metadata,
    Column("TSP_ID", Integer, nullable=False),
    Column("TS_ID", Integer, nullable=False),
    Column("TS_FILE", Unicode(255), nullable=False),
    Column("TS_DESCRIPTION", Unicode(255)),
    Column("TS_DISABLED", BIT),
    Column("TSP_NUMBER", Integer),
    schema="dbo",
)


t_V_PSEX_WORKINGCLUSTER = Table(
    "V_PSEX_WORKINGCLUSTER",
    metadata,
    Column("ST_ID", Integer, nullable=False),
    Column("LS_SERVERPATH", Unicode(255), nullable=False),
    Column("LS_WEBSERVER", Unicode(255)),
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_SHORT", Unicode(20)),
    schema="dbo",
)


t_V_PSEX_WORKINGCLUSTERS_TO_ANONYMIZE = Table(
    "V_PSEX_WORKINGCLUSTERS_TO_ANONYMIZE",
    metadata,
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_LOCATION", Unicode(40)),
    Column("HR_SHORT", Unicode(20)),
    Column("HR_PREFIX", Unicode(20)),
    Column("HR_ACTIVE", BIT, nullable=False),
    Column("HR_TYPE", Unicode(50)),
    Column("HR_CURRENT", BIT),
    Column("HR_PARENT", UNIQUEIDENTIFIER),
    Column("HR_UPDATE_TYPE", TINYINT),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("CREATED", DateTime, nullable=False),
    Column("CREATED_BY", Integer, nullable=False),
    Column("HR_LAST_UPDATED", DateTime),
    Column("UPDATED_BY", Integer),
    Column("HR_EMAIL", String(80, "SQL_Latin1_General_CP1_CI_AS")),
    Column("ST_ID", Integer),
    Column("CC_ID", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    schema="dbo",
)


t_V_PSEX_ZARA_MATERIAL = Table(
    "V_PSEX_ZARA_MATERIAL",
    metadata,
    Column(
        "ZM_ID", String(18, "SQL_Latin1_General_CP1_CI_AS"), nullable=False
    ),
    Column("MD_ID", Integer, nullable=False),
    Column(
        "ZM_BOOKING_AREA",
        String(4, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
    ),
    Column("ACOT_ID", Integer, nullable=False),
    Column("ZM_PRODUCT", Unicode(5)),
    Column("ZM_OBJECT", Unicode(5)),
    Column("ZM_LOCATION", Unicode(5)),
    Column("ZM_SUBLOCATION", Unicode(4)),
    Column("SERVERID", Integer, nullable=False),
    Column("ZM_MATERIAL_GROUP", Unicode(9)),
    Column("CREATED", DateTime, nullable=False),
    Column("UPDATED", DateTime),
    Column("POSTABLE", BIT, nullable=False),
    Column("RUN_ID", Integer),
    Column("STATUS", String(2, "SQL_Latin1_General_CP1_CI_AS")),
    Column("STATUS_FROM", DateTime),
    Column("LVORM", BIT),
    Column("STAFF_POSTABLE", BIT, nullable=False),
    Column("DISABLED", DateTime),
    schema="dbo",
)


t_V_PSEX_ZARA_MATERIAL_CONDITIONS = Table(
    "V_PSEX_ZARA_MATERIAL_CONDITIONS",
    metadata,
    Column("ZMC_ID", Unicode(10)),
    Column(
        "ZM_ID", String(18, "SQL_Latin1_General_CP1_CI_AS"), nullable=False
    ),
    Column("ZMC_RATE", DECIMAL(18, 2)),
    Column("ZMC_UNIT", Unicode(3)),
    Column("SERVERID", Integer, nullable=False),
    Column(
        "ZARA_BOOKING_AREA",
        String(4, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
    ),
    Column("ZMC_FROM", DateTime),
    Column("ZMC_UNTIL", DateTime),
    Column("KPEIN", Unicode(50)),
    Column("KMEIN", Unicode(50)),
    Column("KNUMH", Unicode(45), nullable=False),
    Column("RUN_ID", Integer),
    schema="dbo",
)


t_V_PSEX_ZARA_MATERIAL_RATE = Table(
    "V_PSEX_ZARA_MATERIAL_RATE",
    metadata,
    Column("ZMC_ID", Unicode(10)),
    Column(
        "ZM_ID", String(18, "SQL_Latin1_General_CP1_CI_AS"), nullable=False
    ),
    Column("ZMC_RATE", DECIMAL(18, 2)),
    Column("ZMC_UNIT", Unicode(3)),
    Column("SERVERID", Integer, nullable=False),
    Column(
        "ZARA_BOOKING_AREA",
        String(4, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
    ),
    Column("ZMC_FROM", DateTime),
    Column("ZMC_UNTIL", DateTime),
    Column("KPEIN", Unicode(50)),
    Column("KMEIN", Unicode(50)),
    Column("KNUMH", Unicode(45), nullable=False),
    Column("RUN_ID", Integer),
    schema="dbo",
)


t_V_PSEX_ZLOCATION = Table(
    "V_PSEX_ZLOCATION",
    metadata,
    Column("ZM_LOCATION", Unicode(5), nullable=False),
    Column("ZM_LOCATION_NAME", Unicode(255)),
    Column("ZM_LOCATION_LANGUAGE", Unicode(2), nullable=False),
    schema="dbo",
)


t_V_PSEX_ZOBJECT = Table(
    "V_PSEX_ZOBJECT",
    metadata,
    Column("ZM_OBJECT", Unicode(5), nullable=False),
    Column("ZM_OBJECT_NAME", Unicode(255)),
    Column("ZM_OBJECT_LANGUAGE", Unicode(2), nullable=False),
    schema="dbo",
)


t_V_PSEX_ZPRODUCT = Table(
    "V_PSEX_ZPRODUCT",
    metadata,
    Column("ZM_PRODUCT", Unicode(5), nullable=False),
    Column("ZM_PROUDCT_NAME", Unicode(255)),
    Column("ZM_PRODUCT_LANGUAGE", Unicode(2), nullable=False),
    schema="dbo",
)


t_V_PSEX_ZPS_BEGRIFF = Table(
    "V_PSEX_ZPS_BEGRIFF",
    metadata,
    Column("BEGR_ID", Integer, nullable=False),
    Column("BEGR_BAUNR", Unicode(255)),
    Column("BEGR_EBENE", Integer),
    Column("BEGR_BAU0", Integer),
    Column("BEGR_BAU1", Integer),
    Column("BEGR_BAU2", Integer),
    Column("BEGR_BAU3", Integer),
    schema="dbo",
)


t_V_PSEX_ZPS_BEGRIFF_BEZ = Table(
    "V_PSEX_ZPS_BEGRIFF_BEZ",
    metadata,
    Column("BEBE_BEGR_ID", Integer, nullable=False),
    Column("BEBE_SP_ID", Integer, nullable=False),
    Column("BEBE_BEZ_EX", Unicode(255)),
    schema="dbo",
)


t_V_PSEX_ZSUBLOCATION = Table(
    "V_PSEX_ZSUBLOCATION",
    metadata,
    Column("ZM_SUBLOCATION", Unicode(4), nullable=False),
    Column("ZM_SUBLOCATION_NAME", Unicode(256), nullable=False),
    Column("ZM_SUBLOCATION_LANGUAGE", Unicode(2), nullable=False),
    schema="dbo",
)


t_V_PSEX_ZSUBLOCATION_TEAM = Table(
    "V_PSEX_ZSUBLOCATION_TEAM",
    metadata,
    Column("ID", NCHAR(10), nullable=False),
    Column("ZM_SUBLOCATION", Unicode(5), nullable=False),
    Column("HR_NEW_ID", Integer, nullable=False),
    Column("HR_ID", UNIQUEIDENTIFIER, nullable=False),
    Column("HR_SHORT", Unicode(20)),
    Column("ST_ID", Integer, nullable=False),
    Column("ST_SURNAME", Unicode(60), nullable=False),
    schema="dbo",
)


t_V_PSINFO_NO_ATTRIBUTES = Table(
    "V_PSINFO_NO_ATTRIBUTES",
    metadata,
    Column("DI_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_SCCT_CUSTOMER = Table(
    "V_SCCT_CUSTOMER",
    metadata,
    Column("DB", String(4, "Latin1_General_CI_AS"), nullable=False),
    Column("ID", Integer, nullable=False),
    Column("NAME", Unicode(255)),
    Column("COUNTRY", Unicode(3)),
    Column("STREET", Unicode(100)),
    Column("CITY", Unicode(100)),
    Column("ZIPCODE", Unicode(100)),
    Column("FAX", Unicode(100)),
    Column("PHONE", Unicode(100)),
    Column("MAIL", Unicode(100)),
    schema="dbo",
)


t_V_SCCT_SEARCH = Table(
    "V_SCCT_SEARCH",
    metadata,
    Column("S_Q_ID", Integer, nullable=False),
    Column("RegDate", Unicode(30)),
    Column("S_BL_NAME", Unicode(255)),
    Column("Salesmanager", Unicode(111)),
    Column("CU_NAME", Unicode(165), nullable=False),
    Column("S_PSS_NAME_EN", Unicode(255)),
    Column("S_Q_PRICE", DECIMAL(18, 2)),
    Column("S_Q_DISCOUNT", DECIMAL(18, 2)),
    Column("S_S_NAME_EN", Unicode(255)),
    Column("S_PSS_ID", Integer),
    Column("CU_ID", Integer, nullable=False),
    Column("S_S_ID", Integer),
    Column("S_CU_ID", Integer, nullable=False),
    Column("Customer", Unicode(255)),
    Column("S_CU_NAME", Unicode(255)),
    Column("S_BL_ID", Integer, nullable=False),
    Column("S_P_ID", Integer, nullable=False),
    Column("S_PS_ID", Integer, nullable=False),
    Column("Attachement", Integer, nullable=False),
    Column("S_Q_REG", DateTime),
    Column("S_Q_SALESMANAGER", Integer),
    Column("Pricecheck", Integer, nullable=False),
    schema="dbo",
)


t_V_SCCT_USER = Table(
    "V_SCCT_USER",
    metadata,
    Column("S_U_ID", Integer, nullable=False),
    Column("ST_SURNAME", Unicode(60), nullable=False),
    Column("ST_FORENAME", Unicode(50)),
    Column("S_BL_NAME", Unicode(255)),
    Column("S_BLR_NAME", Unicode(255)),
    Column("S_BLRT_NAME", Unicode(255)),
    Column("SalesOrLab", Unicode(5), nullable=False),
    Column("S_UR_NAME_EN", Unicode(90)),
    Column("S_P_NAME_EN", Unicode(255)),
    Column("S_UA_NAME_EN", Unicode(90)),
    Column("IsActive", Unicode(1), nullable=False),
    Column("ST_WINDOWSID", String(32, "SQL_Latin1_General_CP1_CI_AS")),
    Column("ST_ID", Integer),
    Column("S_BL_ID", Integer, nullable=False),
    Column("S_BLR_ID", Integer, nullable=False),
    Column("S_BLRT_ID", Integer),
    Column("S_UR_ID", Integer),
    Column("S_P_ID", Integer, nullable=False),
    Column("S_UA_ID", Integer, nullable=False),
    schema="dbo",
)


t_V_SERVICEMATRIX = Table(
    "V_SERVICEMATRIX",
    metadata,
    Column("C_ID", Integer),
    Column("CP_ID", Integer, nullable=False),
    Column("GR_SHORT", Unicode(10)),
    Column("TPER_LEVEL", Integer),
    Column("PC_ID", Integer, nullable=False),
    Column("GR_ORDER", Integer),
    schema="dbo",
)


t_V_STORIX_EMPFAENGER = Table(
    "V_STORIX_EMPFAENGER",
    metadata,
    Column("EMP_ID", Integer, nullable=False),
    Column("EMP_NAME", Unicode(60)),
    Column("EMP_ABTEILUNG", Unicode(60)),
    Column("EMP_EMAIL", Unicode(100)),
    Column("EMP_TELEFON", Unicode(50)),
    Column("EMP_FAX", Unicode(50)),
    Column("EMP_KURZZEICHEN", Unicode(10)),
    Column("BR_SHORT", Unicode(3)),
    Column("EMP_PW", Unicode(20)),
    Column("EMP_AKTIV", BIT, nullable=False),
    Column("EMP_IS_USER", BIT, nullable=False),
    Column("EMP_RECHTE", Integer),
    Column("EMP_IS_LAGER", BIT, nullable=False),
    Column("EMP_IS_ABTEILUNG", BIT, nullable=False),
    Column("EMP_LABELPRINTER_SMALL", Unicode(50)),
    Column("EMP_LABELPRINTER_LARGE", Unicode(50)),
    Column("EMP_MEINE_ABTEILUNGEN", Unicode(255)),
    Column("EMP_EMAILINFO1", Unicode(255)),
    Column("EMP_EMAILINFO2", Unicode(255)),
    Column("EMP_ROOTVERZEICHNIS", Unicode(255)),
    Column("EMP_MAXDATA", Integer),
    Column("EMP_BACKUP", BIT, nullable=False),
    Column("EMP_AUTOUPDATE", BIT, nullable=False),
    Column("EMP_COUNT", Integer),
    Column("ST_WINDOWS_ID", Unicode(20)),
    Column("DBZ_ID", Integer, nullable=False),
    Column("EMP_ALLOW_EXPORT", BIT, nullable=False),
    Column("EMP_REG", DateTime),
    Column("EMP_BARCODE", Unicode(10)),
    schema="dbo",
)


t_V_STORIX_LABOR = Table(
    "V_STORIX_LABOR",
    metadata,
    Column("LG_ID", Integer),
    Column("DATUM_AUS_LAGER", DateTime),
    schema="dbo",
)


t_V_STORIX_LABOREINGANG = Table(
    "V_STORIX_LABOREINGANG",
    metadata,
    Column("P_ID", Integer),
    Column("LABOREINGANG", DateTime),
    schema="dbo",
)


t_V_STORIX_LAGER = Table(
    "V_STORIX_LAGER",
    metadata,
    Column("LG_ID", Integer, nullable=False),
    Column("BR_SHORT", Unicode(3)),
    Column("LG_EINGANG", DateTime),
    Column("LG_KUNDE_NAME", Unicode(40)),
    Column("LG_KUNDE_STR", Unicode(40)),
    Column("LG_KUNDE_PLZ", Unicode(10)),
    Column("LG_KUNDE_ORT", Unicode(40)),
    Column("LG_KUNDE_LAND", Unicode(3)),
    Column("LG_ELEMENTE", Integer),
    Column("LG_BEMERKUNG", Unicode(4000)),
    Column("LG_EINGANGSART", Unicode(60)),
    Column("LG_PRODUKT", Unicode(255)),
    Column("LG_MODELL", Unicode(255)),
    Column("LG_ZOLL", BIT, nullable=False),
    Column("LG_ABT_BEMERKUNG", Unicode(255)),
    Column("LG_EMPF_ABT", Unicode(20)),
    Column("LG_EMPF_NAME", Unicode(60)),
    Column("LG_INFO", BIT, nullable=False),
    Column("LG_ERF_USER", Unicode(60)),
    Column("LG_ERF_DATUM", DateTime),
    Column("LG_AEND_USER", Unicode(60)),
    Column("LG_AEND_DATUM", DateTime),
    Column("LG_STATUS", BIT, nullable=False),
    Column("LG_MENGE", Unicode(60)),
    Column("LG_WARENLISTE", Unicode(4000)),
    Column("LG_RUECKVERSAND", Unicode(60)),
    Column("LG_MASTERPROJECT", Integer),
    Column("LG_PAKETNUMMERN", Unicode(255)),
    schema="dbo",
)


t_V_STORIX_LAGERELEMENT = Table(
    "V_STORIX_LAGERELEMENT",
    metadata,
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
    schema="dbo",
)


t_V_STORIX_LEGENDE = Table(
    "V_STORIX_LEGENDE",
    metadata,
    Column("LLG_ID", Integer, nullable=False),
    Column("LG_ID", Integer),
    Column("LGEL_NR", Integer),
    Column("LLG_NR", Integer),
    Column("LLG_DATUM", DateTime),
    Column("LLG_VON", Unicode(255)),
    Column("LLG_VON_ABT", Unicode(60)),
    Column("LLG_AN", Unicode(255)),
    Column("LLG_AN_ABT", Unicode(60)),
    Column("LLG_ORT", Unicode(60)),
    Column("LLG_BEMERKUNG", Unicode(255)),
    Column("LLG_ERF_USER", Unicode(60)),
    Column("LLG_ERF_DATUM", DateTime),
    Column("LLG_AEND_USER", Unicode(60)),
    Column("LLG_AEND_DATUM", DateTime),
    Column("BR_SHORT", Unicode(5)),
    Column("LLG_ORT_OLD", Unicode(60)),
    schema="dbo",
)


t_V_STORIX_WARENEINGANG = Table(
    "V_STORIX_WARENEINGANG",
    metadata,
    Column("P_ID", Integer),
    Column("WARENEINGANG", DateTime),
    schema="dbo",
)


t_V_TASKLIST = Table(
    "V_TASKLIST",
    metadata,
    Column("TA_ID", Integer, nullable=False),
    Column("MyType", Unicode(6), nullable=False),
    Column("TA_REL_ID", Integer),
    Column("TA_TEXT_EN", Unicode(2048)),
    Column("MyFrom", Unicode(111)),
    Column("MyTo", Unicode(111)),
    Column("TA_DEADLINE", Date),
    Column("TA_COMMENT", Unicode(2048)),
    Column("TA_DATE", DateTime),
    Column("TA_READY", DateTime),
    Column("TA_CHECK", DateTime),
    Column("MyBesitzer_ID", Integer),
    Column("MyBesitzer", Unicode(111)),
    Column("TA_FROM", Integer),
    Column("TA_TO", Integer),
    Column("TA_TYPE", Integer, nullable=False),
    schema="dbo",
)


t_V_TEAM_SUBLOCATION = Table(
    "V_TEAM_SUBLOCATION",
    metadata,
    Column("ST_ID", Integer, nullable=False),
    Column("ST_SURNAME", Unicode(60), nullable=False),
    Column("ST_TEAM", UNIQUEIDENTIFIER),
    Column("Sublocation", Unicode(6)),
    schema="dbo",
)


t_V_TEST_BAUSTEINZEITEN = Table(
    "V_TEST_BAUSTEINZEITEN",
    metadata,
    Column("TPT_NAME_DE", Unicode(256), nullable=False),
    Column("AnzahlModule", Integer),
    Column("GesamtPB", Integer),
    Column("GesamtStunden", Float(53)),
    Column("GesamtTage", Float(53)),
    Column("GesamtKosten", DECIMAL(38, 2)),
    Column("DurchschnittProPB", Float(53)),
    schema="dbo",
)


t_V_TEST_MODULSUMMEN = Table(
    "V_TEST_MODULSUMMEN",
    metadata,
    Column("DM_ID", Integer),
    Column("TPT_ID", Integer),
    Column("AnzahlPB", Integer),
    schema="dbo",
)


t_V_TEST_MODULSUMMEN_EINZELN = Table(
    "V_TEST_MODULSUMMEN_EINZELN",
    metadata,
    Column("DM_ID", Integer),
    Column("Stunden", Float(53)),
    Column("Tage", Float(53)),
    Column("Kosten", DECIMAL(38, 2)),
    schema="dbo",
)


t_V_TEST_MODULSUMMEN_GESAMT = Table(
    "V_TEST_MODULSUMMEN_GESAMT",
    metadata,
    Column("DM_ID", Integer),
    Column("TPT_ID", Integer),
    Column("AnzahlPB", Integer),
    Column("Stunden", Float(53)),
    Column("Tage", Float(53)),
    Column("Kosten", DECIMAL(38, 2)),
    Column("MinutenProPB", Float(53)),
    schema="dbo",
)


t_V_TOOLMANAGER_EDOC = Table(
    "V_TOOLMANAGER_EDOC",
    metadata,
    Column("P_ID", Integer),
    Column("P_ZARA_NUMBER", String(10, "SQL_Latin1_General_CP1_CI_AS")),
    Column("CU_NAME", Unicode(165)),
    Column("Projectmanager", Unicode(111)),
    Column("E_ID", Integer),
    Column("E_NAME", Unicode(255)),
    Column("EMIP_ID", Integer),
    Column("EMI_REQUIREMENT_DE", Unicode(1000)),
    Column("EMI_REQUIREMENT_EN", Unicode(1000)),
    Column("P_PROJECTMANAGER", Integer),
    Column("P_PRODUCT", Unicode(255)),
    Column("P_MODEL", Unicode(255)),
    Column("P_FOLDER", Unicode(255)),
    Column("P_ORDERTEXT", Unicode(2048)),
    schema="dbo",
)


t_V_TOOLMANAGER_VERWENDUNG = Table(
    "V_TOOLMANAGER_VERWENDUNG",
    metadata,
    Column("V_ID", Integer, nullable=False),
    Column("T_ID", Integer),
    Column("V_BEZEICHNUNG", Unicode(90)),
    Column("V_TYP", Unicode(90)),
    Column("V_SERIENNUMMER", Unicode(90)),
    Column("V_STATUS", Unicode(50)),
    Column("V_KLASSE", Unicode(50)),
    Column("V_KALIBRIERT_AM", DateTime),
    Column("V_KALIBRIERT_BIS", DateTime),
    Column("V_PSEX", Integer),
    Column("V_SAP", Unicode(20)),
    Column("V_PROJEKTLEITER", Unicode(60)),
    Column("V_AUFTRAGGEBER", Unicode(90)),
    Column("V_PRUEFBEGINN", DateTime),
    Column("V_BERICHTSDATUM", DateTime),
    Column("V_PROJEKTNAME", Unicode(500)),
    Column("V_PRUEFUNGSART", Unicode(255)),
    Column("V_REG", DateTime),
    Column("V_REGBY", Integer),
    Column("V_CALVIN", Unicode(20)),
    Column("V_BETRIEBSSTUNDEN", DECIMAL(16, 2), nullable=False),
    Column("TN_ID", Integer, nullable=False),
    Column("EMIP_ID", Integer),
    schema="dbo",
)


t_V_TOOL_BRANCH = Table(
    "V_TOOL_BRANCH",
    metadata,
    Column("BR_ID", Integer, nullable=False),
    Column("BR_NAME", Unicode(60)),
    Column("BR_PICTURE", Unicode(255)),
    Column("HR_ID", UNIQUEIDENTIFIER),
    Column("BR_ORT", Unicode(50)),
    Column("BR_PLZ", Unicode(20)),
    Column("BR_LAND", Unicode(10)),
    Column("BR_STRASSE", Unicode(50)),
    Column("BR_KENNUNG", Unicode(2)),
    Column("BR_CURRENCY", Unicode(10)),
    Column("BR_REGION", Unicode(10)),
    schema="dbo",
)


t_V_TOOL_COUNT = Table(
    "V_TOOL_COUNT",
    metadata,
    Column("TC_ID", Integer, nullable=False),
    Column("MIT_ID", Integer),
    Column("TC_REG", DateTime),
    Column("TC_VERSION", Unicode(50)),
    schema="dbo",
)


t_V_TOOL_MITARBEITER = Table(
    "V_TOOL_MITARBEITER",
    metadata,
    Column("MIT_ID", Integer, nullable=False),
    Column("MIT_NACHNAME", Unicode(50)),
    Column("MIT_VORNAME", Unicode(50)),
    Column("ST_WINDOWSID", Unicode(20)),
    Column("BR_ID", Integer),
    Column("ABT_ID", Integer),
    Column("ST_ID", Integer),
    Column("MIT_AKTIV", BIT, nullable=False),
    Column("MIT_IS_GERAETEWART", BIT, nullable=False),
    Column("MIT_IS_ADMIN", BIT, nullable=False),
    Column("MIT_TELEFON", Unicode(50)),
    Column("MIT_FAX", Unicode(50)),
    Column("MIT_EMAIL", Unicode(100)),
    Column("MIT_KURZ", Unicode(10)),
    Column("MIT_MAXDATA", Integer, nullable=False),
    Column("MIT_LABELPRINTER_SMALL", Unicode(50)),
    Column("MIT_LABELPRINTER_LARGE", Unicode(50)),
    Column("MIT_ROOTVERZEICHNIS", Unicode(255), nullable=False),
    Column("MIT_COUNT", Integer, nullable=False),
    Column("MIT_IS_ABTEILUNGSLEITER", BIT, nullable=False),
    Column("MIT_MONITOR_ANZAHL", Integer),
    Column("MIT_MONITOR_AUFLOESUNG", Unicode(50)),
    Column("MIT_REGDATE", DateTime),
    schema="dbo",
)


t_V_VERWENDUNG_NAVPACK = Table(
    "V_VERWENDUNG_NAVPACK",
    metadata,
    Column("Verwendung", BigInteger),
    Column("NP_ID", Integer, nullable=False),
    schema="dbo",
)


class WORKSTATION(Base):
    __tablename__ = "WORKSTATION"
    __table_args__ = {"schema": "dbo"}

    WST_ID = Column(Integer, primary_key=True)
    WST_NAME = Column(Unicode(60))
    WST_SHORT = Column(Unicode(20))
    WC_ID = Column(Integer)
    HR_ID = Column(UNIQUEIDENTIFIER)
    ST_ID = Column(Integer, server_default=text("((1))"))
    ZM_SUBLOCATION = Column(
        Unicode(5), nullable=False, server_default=text("(N'P001')")
    )
    WST_ACTIVE = Column(BIT, nullable=False, server_default=text("((1))"))


class XXXCHECKPROOF(Base):
    __tablename__ = "XXX_CHECK_PROOF"
    __table_args__ = {"schema": "dbo"}

    CPF_ID = Column(Integer, primary_key=True)
    CPF_KILLED = Column(BIT, server_default=text("((0))"))
    P_ID = Column(Integer)
    PF_ID = Column(Integer)
    CU_ID = Column(Integer)
    PF_NAME = Column(Unicode(255))
    PF_TYPENUMBER = Column(Unicode(255))
    PF_TESTBASE = Column(Unicode(500))
    PF_COMMENT_CU = Column(Unicode(800))
    PF_COMMENT_TUEV = Column(Unicode(800))
    ER_ID = Column(Integer, server_default=text("((1))"))
    PFS_ID = Column(Integer)
    TOP_ID = Column(Integer)
    PF_VALID_TO = Column(DateTime)
    PF_REG = Column(DateTime)
    PF_REG_BY = Column(Unicode(90))
    PF_UPDATE_BY_TUEV = Column(Integer)
    PF_UPDATE_TUEV = Column(DateTime)
    PF_UPDATE_BY_CU = Column(Unicode(90))
    PF_UPDATE_CU = Column(DateTime)
    CPF_REG = Column(DateTime, server_default=text("(getutcdate())"))
    CPF_REGBY = Column(Integer)


class XXXCHECKPROOFDOCUMENT(Base):
    __tablename__ = "XXX_CHECK_PROOF_DOCUMENTS"
    __table_args__ = {"schema": "dbo"}

    CPFD_ID = Column(Integer, primary_key=True)
    CPFD_KILLED = Column(BIT, server_default=text("((0))"))
    CPF_ID = Column(Integer)
    PFD_ID = Column(Integer)
    PF_ID = Column(Integer)
    PFS_ID = Column(Integer)
    PFD_LAB = Column(Unicode(255))
    PFD_UPLOAD = Column(DateTime)
    PFD_UPLOAD_BY = Column(Unicode(90))
    PFD_UPDATE_TUEV = Column(DateTime)
    PFD_UPDATE_TUEV_BY = Column(Integer)
    PFD_UPDATE_CU = Column(DateTime)
    PFD_UPDATE_CU_BY = Column(Unicode(90))
    CPFD_REG = Column(DateTime, server_default=text("(getutcdate())"))
    CPFD_REGBY = Column(Integer)


class XXXDEFAULTITEMWORKSTATION(Base):
    __tablename__ = "XXX_DEFAULT_ITEM_WORKSTATION"
    __table_args__ = {"schema": "dbo"}

    DIWST_ID = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, index=True)
    WST_ID = Column(Integer)
    HR_ID = Column(UNIQUEIDENTIFIER)


class XXXDEFAULTMODULITEMTESTLEVEL(Base):
    __tablename__ = "XXX_DEFAULT_MODUL_ITEM_TESTLEVEL"
    __table_args__ = {"schema": "dbo"}

    DMITL_ID = Column(Integer, primary_key=True)
    DMI_ID = Column(Integer, index=True)
    TLEV_ID = Column(Integer)


class XXXDEFAULTMODULITEMWORKSTATION(Base):
    __tablename__ = "XXX_DEFAULT_MODUL_ITEM_WORKSTATION"
    __table_args__ = {"schema": "dbo"}

    DMIWS = Column(Integer, primary_key=True)
    DMI_ID = Column(Integer, index=True)
    WST_ID = Column(Integer)
    HR_ID = Column(UNIQUEIDENTIFIER)


class XXXMODULBASE(Base):
    __tablename__ = "XXX_MODUL_BASE"
    __table_args__ = {"schema": "dbo"}

    MB_ID = Column(Integer, primary_key=True)
    DM_ID = Column(Integer, index=True)
    B_ID = Column(Integer, index=True)


class XXXNAVIGATOR(Base):
    __tablename__ = "XXX_NAVIGATOR"
    __table_args__ = {"schema": "dbo"}

    NAV_ID = Column(Integer, primary_key=True)
    NAV_COMMENT = Column(Unicode(512))
    C_ID = Column(Integer, index=True)
    P_ID = Column(Integer, index=True)
    NAV_REG = Column(DateTime, server_default=text("(getdate())"))
    NAV_REGBY = Column(Integer)
    NAV_NAME_DE = Column(Unicode(256))
    NAV_NAME_EN = Column(Unicode(256))
    NAV_CRM = Column(Unicode(256))
    NAV_TYPE = Column(
        Integer, nullable=False, index=True, server_default=text("((1))")
    )


class XXXNAVIGATORSELECTION(Base):
    __tablename__ = "XXX_NAVIGATOR_SELECTION"
    __table_args__ = {"schema": "dbo"}

    NAVS_ID = Column(Integer, primary_key=True)
    NAV_ID = Column(Integer, index=True)
    CP_ID = Column(Integer, index=True)


class XXXNAVCALCPERSONAL(Base):
    __tablename__ = "XXX_NAV_CALC_PERSONAL"
    __table_args__ = {"schema": "dbo"}

    NCP_ID = Column(Integer, primary_key=True)
    NAV_ID = Column(Integer, index=True)
    CBC_ID = Column(Integer, index=True)
    NCP_TIME_HOURS = Column(Float(53))
    NCP_TIME_DAYS = Column(Float(53))
    NCP_DELTA_START = Column(Float(53))
    NCP_COSTS = Column(DECIMAL(18, 2))
    NCP_TASK = Column(Unicode(500))
    NCP_COMMENT = Column(Unicode(500))
    NCP_RATE = Column(DECIMAL(18, 2))
    NCP_PRICE = Column(DECIMAL(18, 2))
    NCP_FACTOR = Column(Float(53))
    WST_ID = Column(Integer)
    NCP_TRAVEL = Column(DECIMAL(18, 2))
    GP_ID = Column(Integer)
    ZM_ID = Column(Unicode(50))
    ST_ID = Column(Integer, nullable=False, server_default=text("((1))"))


class XXXPLANNING(Base):
    __tablename__ = "XXX_PLANNING"
    __table_args__ = {"schema": "dbo"}

    PL_ID = Column(Integer, primary_key=True)
    PL_NAME = Column(Unicode(60))
    PL_INFO = Column(Unicode(500))
    PL_IS_MASTER = Column(BIT, server_default=text("(0)"))
    PL_REG = Column(DateTime)
    PL_REGBY = Column(Integer)
    PL_UPDATE = Column(DateTime)
    PL_UPDATEBY = Column(Integer)


class XXXPLANNINGBASE(Base):
    __tablename__ = "XXX_PLANNING_BASE"
    __table_args__ = {"schema": "dbo"}

    PLB_ID = Column(Integer, primary_key=True)
    PLB_NAME_DE = Column(Unicode(50))
    PLB_NAME_EN = Column(Unicode(50))
    DI_ID = Column(Integer)
    PLK_SHORT = Column(Unicode(10))
    PLB_REG = Column(DateTime, server_default=text("(getdate())"))
    PLB_REGBY = Column(Integer, server_default=text("(1)"))
    PLB_UPDATE = Column(DateTime)
    PLB_UPDATEBY = Column(Integer)


class XXXPLANNINGCOUNTRY(Base):
    __tablename__ = "XXX_PLANNING_COUNTRY"
    __table_args__ = {"schema": "dbo"}

    PLC_ID = Column(Integer, primary_key=True)
    PLC_SHORT = Column(Unicode(10))
    PLC_NAME_DE = Column(Unicode(50))
    PLC_NAME_EN = Column(Unicode(50))
    DI_ID = Column(Integer)
    PLC_REG = Column(DateTime, server_default=text("(getdate())"))
    PLC_REGBY = Column(Integer, server_default=text("(1)"))
    PLC_UPDATE = Column(DateTime)
    PLC_UPDATEBY = Column(Integer)


class XXXPLANNINGELEMENT(Base):
    __tablename__ = "XXX_PLANNING_ELEMENT"
    __table_args__ = {"schema": "dbo"}

    PLE_ID = Column(Integer, primary_key=True)
    PL_ID = Column(Integer)
    PLB_ID = Column(Integer)
    PLN_GS = Column(BIT, server_default=text("(0)"))
    PLN_TB = Column(BIT, server_default=text("(0)"))
    PLN_FST = Column(BIT, server_default=text("(0)"))
    PLN_PZ = Column(BIT, server_default=text("(0)"))
    PLN_PB = Column(BIT, server_default=text("(0)"))
    PLN_EE = Column(BIT, server_default=text("(0)"))
    PLN_CE = Column(BIT, server_default=text("(0)"))
    PLN_CDF = Column(BIT, server_default=text("(0)"))
    PLN_CB = Column(BIT, server_default=text("(0)"))
    PLE_PROOF_OTHER = Column(Unicode(500))
    PLP_TRF = Column(BIT, server_default=text("(0)"))
    PLP_PPP = Column(BIT, server_default=text("(0)"))
    PLP_MS = Column(BIT, server_default=text("(0)"))
    PLP_MA_I = Column(BIT, server_default=text("(0)"))
    PLP_EMC = Column(BIT, server_default=text("(0)"))
    PLP_ROHS = Column(BIT, server_default=text("(0)"))
    PLP_PAK = Column(BIT, server_default=text("(0)"))
    PLP_LFGB = Column(BIT, server_default=text("(0)"))
    PLP_MC = Column(BIT, server_default=text("(0)"))
    PLP_ADD = Column(Unicode(500))
    PLE_TEST_OTHER = Column(Unicode(500))
    PLE_NUMBER = Column(Integer, server_default=text("(0)"))
    PLE_COMMENT = Column(Unicode(500))
    PLE_REG = Column(DateTime)
    PLE_REGBY = Column(Integer)
    PLE_UPDATE = Column(DateTime)
    PLE_UPDATEBY = Column(Integer)


class XXXPLANNINGELEMENTCOUNTRY(Base):
    __tablename__ = "XXX_PLANNING_ELEMENT_COUNTRY"
    __table_args__ = {"schema": "dbo"}

    PLEC_ID = Column(Integer, primary_key=True)
    PL_ID = Column(Integer)
    PLC_ID = Column(Integer)
    PLEC_CDF = Column(BIT, server_default=text("(0)"))
    PLEC_CB = Column(BIT, server_default=text("(0)"))
    PLEC_PROOF_OTHER = Column(Unicode(500))
    PLEC_NDEV_TPS = Column(BIT, server_default=text("(0)"))
    PLEC_NDEV_COUNTRY = Column(BIT, server_default=text("(0)"))
    PLEC_FOOD = Column(BIT, server_default=text("(0)"))
    PLEC_TEST_OTHER = Column(Unicode(500))
    PLEC_REG = Column(DateTime)
    PLEC_REGBY = Column(Integer)
    PLEC_UPDATE = Column(DateTime)
    PLEC_UPDATEBY = Column(Integer)
    PLEC_NUMBER = Column(Integer, server_default=text("(0)"))


class XXXPLANNINGHEADER(Base):
    __tablename__ = "XXX_PLANNING_HEADER"
    __table_args__ = {"schema": "dbo"}

    PLH_ID = Column(Integer, primary_key=True)
    PLH_FILENAME = Column(Unicode(255))
    PLH_DATA = Column(IMAGE)


class XXXPLANNINGKIND(Base):
    __tablename__ = "XXX_PLANNING_KIND"
    __table_args__ = {"schema": "dbo"}

    PLK_ID = Column(Integer, primary_key=True)
    PLK_SHORT = Column(Unicode(20))
    PLK_NAME_DE = Column(Unicode(50))
    PLK_NAME_EN = Column(Unicode(50))


t_XXX_PLANNING_TYPE = Table(
    "XXX_PLANNING_TYPE",
    metadata,
    Column("PLT_KURZ", Unicode(20)),
    Column("PLT_ART", Integer),
    Column("PLT_TEXT_D", Unicode(500)),
    Column("PLT_TEXT_E", Unicode(500)),
    schema="dbo",
)


class XXXPROOF(Base):
    __tablename__ = "XXX_PROOF"
    __table_args__ = {"schema": "dbo"}

    PF_ID = Column(Integer, primary_key=True)
    PF_KILLED = Column(BIT, server_default=text("((0))"))
    CU_ID = Column(Integer)
    PF_NAME = Column(Unicode(255))
    PF_TYPENUMBER = Column(Unicode(255))
    PF_TESTBASE = Column(Unicode(500))
    PF_COMMENT_CU = Column(Unicode(800))
    PF_COMMENT_TUEV = Column(Unicode(800))
    ER_ID = Column(Integer, server_default=text("((1))"))
    PFS_ID = Column(Integer, server_default=text("((1))"))
    TOP_ID = Column(Integer, server_default=text("((1))"))
    PF_VALID_TO = Column(DateTime)
    PF_REG = Column(DateTime, server_default=text("(getutcdate())"))
    PF_REG_BY = Column(Unicode(90))
    PF_UPDATE_BY_TUEV = Column(Integer)
    PF_UPDATE_TUEV = Column(DateTime)
    PF_UPDATE_BY_CU = Column(Unicode(90))
    PF_UPDATE_CU = Column(DateTime)


class XXXPROOFDOCUMENT(Base):
    __tablename__ = "XXX_PROOF_DOCUMENTS"
    __table_args__ = {"schema": "dbo"}

    PFD_ID = Column(Integer, primary_key=True)
    PF_ID = Column(Integer)
    PFD_KILLED = Column(BIT, server_default=text("((0))"))
    PFS_ID = Column(Integer, server_default=text("((1))"))
    PFD_FILENAME = Column(Unicode(255))
    PFD_LAB = Column(Unicode(255))
    PFD_DATA = Column(IMAGE)
    PFD_UPLOAD = Column(DateTime, server_default=text("(getutcdate())"))
    PFD_UPLOAD_BY = Column(Unicode(90))
    PFD_UPDATE_TUEV = Column(DateTime)
    PFD_UPDATE_TUEV_BY = Column(Integer)
    PFD_UPDATE_CU = Column(DateTime)
    PFD_UPDATE_CU_BY = Column(Unicode(90))


class XXXPROOFEXCEL(Base):
    __tablename__ = "XXX_PROOF_EXCEL"
    __table_args__ = {"schema": "dbo"}

    PFE_ID = Column(Integer, primary_key=True)
    CU_ID = Column(Integer)
    PFE_COMMENT_CU = Column(Unicode(800))
    PFE_FILENAME = Column(Unicode(255))
    PFE_DATA = Column(IMAGE)
    PFE_CONVERTED = Column(BIT, server_default=text("((0))"))
    PFE_CONVERSION_BY = Column(Integer)
    PFE_CONVERSION_DATE = Column(DateTime)
    PFE_REG = Column(DateTime, server_default=text("(getutcdate())"))
    PFE_REGBY = Column(Unicode(90))


class XXXPROOFLAB(Base):
    __tablename__ = "XXX_PROOF_LAB"
    __table_args__ = {"schema": "dbo"}

    PFL_ID = Column(Integer, primary_key=True)
    PFL_NAME = Column(Unicode(200))


class XXXPROOFPROJECT(Base):
    __tablename__ = "XXX_PROOF_PROJECT"
    __table_args__ = {"schema": "dbo"}

    PFP_ID = Column(Integer, primary_key=True)
    PF_ID = Column(Integer)
    P_ID = Column(Integer)
    PFP_REG = Column(DateTime, server_default=text("(getutcdate())"))
    PFP_REGBY = Column(Unicode(90), server_default=text("((1))"))


class XXXPROOFSTATU(Base):
    __tablename__ = "XXX_PROOF_STATUS"
    __table_args__ = {"schema": "dbo"}

    PFS_ID = Column(Integer, primary_key=True)
    PFS_NAME_DE = Column(Unicode(50))
    PFS_NAME_EN = Column(Unicode(50))
    PFS_NAME_FR = Column(Unicode(50))


class XXXSIGNUSETEST(Base):
    __tablename__ = "XXX_SIGN_USE_TEST"
    __table_args__ = {"schema": "dbo"}

    SIGU_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer)
    SIGU_PDF = Column(IMAGE)
    SIGU_FILENAME = Column(Unicode(500))
    SIGU_ERROR = Column(BIT)
    SIGU_MD5 = Column(Unicode(255))
    SIGU_FILESIZE = Column(BigInteger)
    SIGU_REG = Column(DateTime, server_default=text("(getdate())"))
    SIGU_RESERVED_BY = Column(Integer)
    SIGU_RESERVED_DATE = Column(DateTime)
    SIGU_USED = Column(BIT, nullable=False, server_default=text("((1))"))
    SIGU_TEMP = Column(Unicode(20))


class XXXTEMP(Base):
    __tablename__ = "XXX_TEMP"
    __table_args__ = {"schema": "dbo"}

    TEMP_ID = Column(Integer, primary_key=True)
    TEMP_ID_MAIN = Column(Integer)
    TEMP_ID_SUB1 = Column(Integer)
    TEMP_ID_SUB2 = Column(Integer)
    TEMP_ID_SUB3 = Column(Integer)


class XXXTEMPORGINAL(Base):
    __tablename__ = "XXX_TEMP_ORGINAL"
    __table_args__ = {"schema": "dbo"}

    TEMPO_ID = Column(Integer, primary_key=True)
    TEMPO_PRODUKT = Column(Unicode(255))
    TEMPO_MILOMEX = Column(Unicode(50))
    TEMPO_MILOMEX_NR = Column(Unicode(50))
    TEMPO_ARTIKEL = Column(Unicode(50))
    TEMPO_LT = Column(DateTime)
    TEMPO_ZEILENNUMMER = Column(Integer)
    TEMPO_SC_ID = Column(String(50, "Latin1_General_CI_AS"))
    TEMPO_P_HANDLEDBY = Column(Integer)
    TEMPO_P_PROJECTMANAGER = Column(Integer)


t_XXX_TEMP_SUBCLAUSE_1 = Table(
    "XXX_TEMP_SUBCLAUSE_1",
    metadata,
    Column("ID", Integer),
    Column("SUBCLAUSE", Unicode(255)),
    Column("Testbasse Source", Unicode(255)),
    Column("Testbase Procedure", Unicode(255)),
    Column("Info", Unicode(255)),
    Column("Recheck", Unicode(255)),
    Column("Remark", Unicode(255)),
    schema="dbo",
)


t_XXX_TEMP_SUBCLAUSE_2 = Table(
    "XXX_TEMP_SUBCLAUSE_2",
    metadata,
    Column("ID", Integer),
    Column("SUBCLAUSE", Unicode(255)),
    Column("Testbasse Source", Unicode(255)),
    Column("Testbase Procedure", Unicode(255)),
    Column("Info", Unicode),
    Column("Recheck", Unicode(255)),
    Column("Remark", Unicode(255)),
    Column("Source & Procedure = 0", Unicode(255)),
    schema="dbo",
)


class ZSUBLOCATIONTEAM(Base):
    __tablename__ = "ZSUBLOCATION_TEAM"
    __table_args__ = {"schema": "dbo"}

    ID = Column(Integer, primary_key=True)
    ZM_SUBLOCATION = Column(Unicode(5), nullable=False)
    HR_NEW_ID = Column(
        Integer, nullable=False, server_default=text("((101010101))")
    )


t__TEST_01 = Table(
    "_TEST_01",
    metadata,
    Column("EM_ID", Integer, nullable=False),
    Column("E_ID", Integer),
    Column("DM_ID", Integer),
    Column("EMI_ID", Integer),
    Column("PRP_ID", Integer),
    Column("EMIP_RESULT_DE", Unicode(2048)),
    Column("EMI_NUMBER", Integer),
    Column("EMIP_ID", Integer, nullable=False),
    schema="dbo",
)


t__V_PRODUCT_HISTORY = Table(
    "_V_PRODUCT_HISTORY",
    metadata,
    Column("HHRP_ID", Integer, nullable=False),
    Column("HHRP_DATE", DateTime),
    Column("HRP_ID", Integer, nullable=False),
    Column("HRP_LEFT", Integer),
    Column("HRP_RIGHT", Integer),
    Column("HRP_INDENT", Integer),
    Column("HRP_NAME_DE", Unicode(255)),
    Column("HRP_NAME_EN", Unicode(255)),
    Column("HRP_NAME_FR", Unicode(255)),
    Column("HRP_UPDATE", DateTime),
    Column("HRP_UPDATEBY", Integer),
    schema="dbo",
)


class Dtproperty(Base):
    __tablename__ = "dtproperties"
    __table_args__ = {"schema": "dbo"}

    id = Column(Integer, primary_key=True, nullable=False)
    objectid = Column(Integer)
    property = Column(
        String(64, "Latin1_General_CI_AS"), primary_key=True, nullable=False
    )
    value = Column(String(255, "Latin1_General_CI_AS"))
    uvalue = Column(Unicode(255))
    lvalue = Column(IMAGE)
    version = Column(Integer, nullable=False, server_default=text("(0)"))


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


class EDOCMODULITEMATTRIBUTE(Base):
    __tablename__ = "EDOC_MODUL_ITEM_ATTRIBUTES"
    __table_args__ = {"schema": "dbo"}

    EMIAT_ID = Column(Integer, primary_key=True)
    EMI_ID = Column(Integer, index=True)
    EM_ID = Column(Integer, index=True)
    ATT_ID = Column(ForeignKey("dbo.ATTRIBUTES.ATT_ID"))

    ATTRIBUTE = relationship("ATTRIBUTE")


class XXXDEFAULTMODULITEMATTRIBUTE(Base):
    __tablename__ = "XXX_DEFAULT_MODUL_ITEM_ATTRIBUTES"
    __table_args__ = {"schema": "dbo"}

    DMIA_ID = Column(Integer, primary_key=True)
    DMI_ID = Column(Integer, index=True)
    ATT_ID = Column(
        ForeignKey("dbo.ATTRIBUTES.ATT_ID"), nullable=False, index=True
    )

    ATTRIBUTE = relationship("ATTRIBUTE")
