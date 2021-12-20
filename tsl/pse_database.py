"""Database connection and models for the PSE database."""
# pylint: disable=duplicate-code
from __future__ import annotations

import errno
import logging
import os
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator, List, Optional, cast
from winreg import HKEY_CURRENT_USER, KEY_READ, OpenKey, QueryValueEx

from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    LargeBinary,
    SmallInteger,
    Unicode,
)
from sqlalchemy.dialects.mssql import BIT, MONEY, TINYINT, UNIQUEIDENTIFIER
from sqlalchemy.orm import (
    Mapped,
    Session,
    declarative_base,
    load_only,
    relationship,
    sessionmaker,
)

from tsl.common_db import NullUnicode, create_db_engine
from tsl.variables import PATH
from tsl.vault import Vault

log = logging.getLogger("tsl.pse_database")  # pylint: disable=invalid-name

ENGINE = create_db_engine(Vault.Application.PSE)

Base = declarative_base()
Base.metadata.bind = ENGINE

AdminSession = sessionmaker(bind=ENGINE)  # pylint: disable=invalid-name

USER_ID: Optional[int] = None


# pylint: disable=global-statement
def _fetch_user_id() -> None:
    """Fetch and set the user id from the database."""
    global USER_ID
    with session_scope(False) as session:
        username = os.getlogin()
        log.debug("Getting database id for user %s", username)
        user = (
            session.query(Staff)
            .filter_by(ST_WINDOWSID=username)
            .options(load_only(Staff.ST_ID, Staff.ST_TEAM))
            .one()
        )
        USER_ID = user.ST_ID


def get_user_id() -> int:
    """Get the database id for the current user."""
    if USER_ID is None:
        _fetch_user_id()
    return cast(int, USER_ID)


@contextmanager
def session_scope(commit: bool = True) -> Iterator[Session]:
    """Provide a transactional scope around a series of operations."""
    session = AdminSession()
    try:
        session.expire_on_commit = False
        yield session
        if commit:
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


# pylint: disable=too-few-public-methods
class Process(Base):
    """Process table model."""

    __tablename__ = "PROCESS"

    PC_ID: Mapped[int] = Column(Integer, primary_key=True)
    PC_NAME: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )
    PC_IAN: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )
    PC_PATH: Mapped[str] = Column(
        NullUnicode(length=50), nullable=False, default=""
    )

    @property
    def process_archive(self) -> Path:
        """Return the full path to the process archive of the Process."""
        assert self.PC_PATH
        return PATH / "PSEX" / self.PC_PATH


class ProcessPhase(Base):
    """ProcessPhase table model."""

    __tablename__ = "PROCESSPHASE"

    PRP_ID: Mapped[int] = Column(Integer, primary_key=True)
    PRP_SHORT_DE: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )
    PRP_SHORT_EN: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )
    PRP_SHORT_FR: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )


class Project(Base):
    """PROJECT table model."""

    __tablename__ = "PROJECT"

    P_ID: Mapped[int] = Column(Integer, primary_key=True)
    PC_ID = Column(Integer, ForeignKey("PROCESS.PC_ID"))
    P_IAN: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )
    P_PRODUCT: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )
    P_CONTACT: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )
    P_CONTACT_CUC_ID = Column(Integer, ForeignKey("CUSTOMER_CONTACT.CUC_ID"))
    P_DEADLINE = Column(DateTime)
    P_ORDERSIZE = Column(Float)
    P_PROCESSPHASE = Column(Integer, ForeignKey("PROCESSPHASE.PRP_ID"))
    P_MODEL: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )
    P_ZARA_NUMBER: Mapped[str] = Column(
        NullUnicode(length=11), nullable=False, default=""
    )
    P_FOLDER: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )
    DELR_ID = Column(Integer)
    P_WC_ID = Column(Unicode(length=36))
    P_NAME: Mapped[str] = Column(
        NullUnicode(length=31), nullable=False, default=""
    )
    P_CUSTOMER_A = Column(Integer, ForeignKey("CUSTOMER.CU_ID"))
    P_CUSTOMER_B = Column(Integer, ForeignKey("CUSTOMER.CU_ID"))
    P_PROJECTMANAGER = Column(Integer, ForeignKey("STAFF.ST_ID"))
    P_TOKEN: Mapped[str] = Column(
        NullUnicode(length=61), nullable=False, default=""
    )
    P_DATE_APPOINTMENT = Column(DateTime)
    P_EXPECTED_TS_RECEIPT = Column(DateTime)
    BATCH_NUMBER = Column(Unicode(length=16))
    P_DISABLED: Mapped[bool] = Column(BIT, nullable=False)
    P_REGBY: Mapped[int] = Column(
        Integer, ForeignKey("STAFF.ST_ID"), nullable=False, default=get_user_id
    )
    P_REGDATE: Mapped[datetime] = Column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    P_UPDATEBY = Column(Integer, ForeignKey("STAFF.ST_ID"))
    P_UPDATE = Column(DateTime)

    customer_contact: CustomerContact = relationship(
        "CustomerContact", uselist=False
    )
    ordering_party: Customer = relationship(
        "Customer", foreign_keys=[P_CUSTOMER_A], uselist=False
    )
    manufacturer: Customer = relationship(
        "Customer", foreign_keys=[P_CUSTOMER_B], uselist=False
    )
    process: Process = relationship("Process", uselist=False)
    phase: ProcessPhase = relationship("ProcessPhase", uselist=False)
    project_manager: Staff = relationship(
        "Staff", foreign_keys=[P_PROJECTMANAGER], uselist=False
    )
    created_by: Staff = relationship(
        "Staff", foreign_keys=[P_REGBY], uselist=False
    )
    update_by: Staff = relationship(
        "Staff", foreign_keys=[P_UPDATEBY], uselist=False
    )
    sub_orders: SubOrder = relationship(
        "SubOrder", back_populates="project", uselist=True
    )
    project_failure_rel: List[ProjectFailureRel] = relationship(
        "ProjectFailureRel", back_populates="project", uselist=True
    )

    @property
    def project_folder(self) -> Path:
        """Return the full path to the project folder of the Project."""
        assert self.P_FOLDER
        return PATH / self.P_FOLDER


class Customer(Base):
    """Customer table model."""

    __tablename__ = "CUSTOMER"

    CU_ID: Mapped[int] = Column(Integer, primary_key=True)
    MD_ID = Column(Integer)
    CU_NUMBER = Column(Unicode(length=10))
    CU_ACTIVE = Column(Boolean)
    CU_AUTHORIZATION = Column(Unicode(length=30))
    CU_SUPPLIER_NO = Column(Unicode(length=24))
    CU_CLASS = Column(Unicode(length=2))
    CU_ATTENDENT = Column(Unicode(length=40))
    CU_DATE = Column(DateTime)
    CU_UPDATE = Column(DateTime)
    CU_LOCKED = Column(Unicode(length=2))
    CU_BOOKING_AREA = Column(Unicode(length=4))
    CU_SERVERID = Column(Integer)
    CU_UPDATE_TYPE = Column(SmallInteger)
    CU_ISSUPPLIER = Column(Boolean)
    CU_LANGUAGE = Column(Unicode(length=2))
    CU_USER_STATE = Column(Unicode(length=5))
    CU_VBUND = Column(Unicode(length=40))
    CU_LOEKZ = Column(Unicode(length=1))
    RUN_ID = Column(Integer)
    CU_KTOKD = Column(Unicode(length=10))
    DEFAULT_CONTACT_PERSON = Column(Integer)
    IS_SURVEY_PARTICIPANT = Column(Boolean)
    SURVEY_REJECT_REASON = Column(Unicode(length=512))
    SEND_SURVEYS_TO_MANUFACTURER = Column(Boolean)
    TAX_ID_NUMBER = Column(Unicode(length=64))
    CU_MARK = Column(Unicode(length=256))
    CU_DISABLED_PSE = Column(DateTime)
    MDO_NUMBER = Column(Unicode(length=10))
    CREATED_BY = Column(Integer)
    UPDATED_BY = Column(Integer)
    DUNSNUMBER = Column(Unicode(length=10))
    EINVOICING_RELEVANCE = Column(Unicode(length=10))
    PRINT_OPTION = Column(Unicode(length=3))

    addresses: List["CustomerAddress"] = relationship(
        "CustomerAddress", back_populates="customer", uselist=True
    )


class CustomerContact(Base):
    """CustomerContact table model."""

    __tablename__ = "CUSTOMER_CONTACT"

    CUC_ID: Mapped[int] = Column(Integer, primary_key=True)
    CUC_FORENAME: Mapped[str] = Column(
        NullUnicode(length=51), nullable=False, default=""
    )
    CUC_SURNAME: Mapped[str] = Column(
        NullUnicode(length=36), nullable=False, default=""
    )
    ANRED: Mapped[str] = Column(
        NullUnicode(length=31), nullable=False, default=""
    )
    CUC_MAIL: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )


class CustomerAddress(Base):
    """CustomerAddress table model."""

    __tablename__ = "CUSTOMER_ADDRESS"

    CA_ID: Mapped[int] = Column(Integer, primary_key=True)
    CU_ID: Mapped[int] = Column(
        Integer, ForeignKey("CUSTOMER.CU_ID"), nullable=False
    )
    CA_NAME: Mapped[str] = Column(
        NullUnicode(length=166), nullable=False, default=""
    )
    CA_STREET: Mapped[str] = Column(
        NullUnicode(length=101), nullable=False, default=""
    )
    CA_ZIPCODE: Mapped[str] = Column(
        NullUnicode(length=11), nullable=False, default=""
    )
    CA_CITY: Mapped[str] = Column(
        NullUnicode(length=41), nullable=False, default=""
    )

    customer: Customer = relationship(
        "Customer", back_populates="addresses", uselist=False
    )


class Staff(Base):
    """Staff table model."""

    __tablename__ = "STAFF"

    ST_ID: Mapped[int] = Column(Integer, primary_key=True)
    ST_SURNAME: Mapped[str] = Column(
        NullUnicode(length=61), nullable=False, default=""
    )
    ST_FORENAME: Mapped[str] = Column(
        NullUnicode(length=51), nullable=False, default=""
    )
    ST_PHONE: Mapped[str] = Column(
        NullUnicode(length=81), nullable=False, default=""
    )
    ST_FAX: Mapped[str] = Column(
        NullUnicode(length=81), nullable=False, default=""
    )
    ST_EMAIL: Mapped[str] = Column(
        NullUnicode(length=81), nullable=False, default=""
    )
    ST_TEAM = Column(Unicode(length=36))
    ST_WINDOWSID = Column(Unicode(32))
    ST_ACTIVE: Mapped[bool] = Column(BIT, nullable=False)
    ST_TYPE: Mapped[int] = Column(Integer, nullable=False)
    # ForeignKey('dbo.SKILLGROUP.SG_ID')
    ST_SKILLGROUP: Mapped[str] = Column(Unicode(8), nullable=False)


class TemplateData(Base):
    """TemplateData table model."""

    __tablename__ = "TEMPLATE_DATA"

    TPD_ID: Mapped[int] = Column(Integer, primary_key=True)
    TP_ID: Mapped[int] = Column(Integer, nullable=False)
    TPD_DATA = Column(LargeBinary)


class Template(Base):
    """
    TemplateData table model.

    If the template represents an eDoc DefaultModule, the TP_FILENAME can be
    empty. In this case, the DM_ID must exist. Nevertheless it is possible
    to have a DM_ID and a TP_FILENAME at the same time.
    """

    __tablename__ = "TEMPLATE"

    TP_ID: Mapped[int] = Column(Integer, primary_key=True)
    MD_ID: Mapped[int] = Column(Integer, nullable=False)
    TPST_ID: Mapped[int] = Column(Integer, nullable=False)
    TPT_ID: Mapped[int] = Column(
        Integer, ForeignKey("TEMPLATE_TYPE.TPT_ID"), nullable=False
    )
    TPSC_ID: Mapped[int] = Column(
        Integer, ForeignKey("TEMPLATE_SCOPE.TPSC_ID"), nullable=False
    )
    TPF_ID: Mapped[int] = Column(Integer, nullable=False)
    TP_NAME_D = Column(Unicode(length=256))
    TP_NAME_E = Column(Unicode(length=256))
    TP_TIME_HOURS = Column(Float)
    TP_TIME_DAYS = Column(Float)
    TP_TESTPERSON_REQUIRED = Column(Boolean)
    TP_COMMENT = Column(Unicode(length=256))
    TP_VERSION = Column(Integer)
    TP_LANGUAGE = Column(Unicode(length=256))
    TP_CLEARINGDATE = Column(DateTime)
    TP_CLEARINGBY = Column(Integer)
    TP_FILENAME = Column(Unicode(length=256))
    TP_REGDATE = Column(DateTime)
    TP_REGBY = Column(Integer)
    TP_UPDATE = Column(DateTime)
    TP_UPDATEBY = Column(Integer)
    TP_ISGLOBAL = Column(Boolean)
    TP_DISABLED: Mapped[bool] = Column(Boolean, nullable=False)
    TP_TRANSFER_STATUS = Column(Unicode(length=51))
    TP_ORIGINATING_SERVERID = Column(Integer)
    TP_ROOT_TEMPLATE_ID = Column(Integer)
    TP_UTC = Column(DateTime)
    TP_WORKINGCLUSTER = Column(Unicode(length=36))
    DM_ID = Column(Integer)
    TP_OLD_TP = Column(Integer)

    temp_scope: TemplateScope = relationship("TemplateScope", uselist=False)
    temp_type: TemplateType = relationship("TemplateType", uselist=False)


class TemplateScope(Base):
    """TemplateScope table model."""

    __tablename__ = "TEMPLATE_SCOPE"

    TPSC_ID: Mapped[int] = Column(Integer, primary_key=True, nullable=False)
    TPSC_NAME_DE: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPSC_NAME_EN: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPSC_NAME_FR: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPSC_SHORT_DE: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPSC_SHORT_EN: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPSC_SHORT_FR: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPSC_PATH: Mapped[str] = Column(Unicode(length=256), nullable=False)
    CREATED: Mapped[datetime] = Column(DateTime, nullable=False)
    CREATED_BY: Mapped[int] = Column(Integer, nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)


class TemplateStatus(Base):
    """TemplateStatus table model."""

    __tablename__ = "TEMPLATE_STATUS"

    TPST_ID: Mapped[int] = Column(Integer, primary_key=True)
    TPST_NAME_DE: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPST_NAME_EN: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPST_NAME_FR: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPST_SHORT_DE: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPST_SHORT_EN: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPST_SHORT_FR: Mapped[str] = Column(Unicode(length=256), nullable=False)
    CREATED: Mapped[datetime] = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)


class TemplateType(Base):
    """TemplateType table model."""

    __tablename__ = "TEMPLATE_TYPE"

    TPT_ID: Mapped[int] = Column(Integer, primary_key=True, nullable=False)
    TPT_NAME_DE: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_NAME_EN: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_NAME_FR: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_SHORT_DE: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_SHORT_EN: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_SHORT_FR: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_PATH: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_PREFIX: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_MODULETYPE: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_SHOWINPROZESSFOLDER: Mapped[bool] = Column(Boolean, nullable=False)
    TPT_SHOWINTEMPLATEMANAGER: Mapped[bool] = Column(Boolean, nullable=False)
    CREATED: Mapped[datetime] = Column(DateTime, nullable=False)
    CREATED_BY: Mapped[int] = Column(Integer, nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)
    TPT_INCLUDE_IN_TRADE_REPORT: Mapped[bool] = Column(Boolean, nullable=False)


class SubOrder(Base):
    """SubOrder table model."""

    __tablename__ = "SUBORDERS"

    P_ID: Mapped[int] = Column(
        Integer, ForeignKey("PROJECT.P_ID"), primary_key=True
    )
    SO_NUMBER: Mapped[int] = Column(Integer, primary_key=True)
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
    SO_PREDATE_REMINDER: Mapped[bool] = Column(BIT, nullable=False)
    SO_PREDATE_INFO = Column(Unicode(255))
    SO_WAIT = Column(BIT)
    SO_REGBY = Column(Integer)
    SO_REGDATE = Column(DateTime)
    SO_UPDATEBY = Column(Integer)
    SO_UPDATE = Column(DateTime)
    SO_TRANSFERSTATUS = Column(Unicode(50))
    SO_DISABLED: Mapped[bool] = Column(BIT, nullable=False)
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
    SO_SORT: Mapped[int] = Column(Integer, nullable=False)
    SO_ADMINISTRATIVE: Mapped[bool] = Column(BIT, nullable=False)
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
    SO_CHECKBY_TEAM = Column(Integer, ForeignKey("HIERARCHY.HR_NEW_ID"))
    SO_DISPOBY_TEAM = Column(Integer, ForeignKey("HIERARCHY.HR_NEW_ID"))
    SO_READYBY_TEAM = Column(Integer, ForeignKey("HIERARCHY.HR_NEW_ID"))
    SO_REGBY_TEAM = Column(Integer, ForeignKey("HIERARCHY.HR_NEW_ID"))
    SO_UPDATEBY_TEAM = Column(Integer, ForeignKey("HIERARCHY.HR_NEW_ID"))
    ST_ID_TEAM = Column(Integer, ForeignKey("HIERARCHY.HR_NEW_ID"))
    AL_ID = Column(Integer, ForeignKey("ANONYMIZATION_LOG.AL_ID"))
    SO_PLANNED_MATERIAL = Column(DECIMAL(18, 2))
    SO_PLANNED_LICENSE = Column(DECIMAL(18, 2))
    BANF_REQUEST = Column(DateTime)
    BANF_ORDER = Column(DateTime)
    B2B: Mapped[bool] = Column(BIT, nullable=False)
    SO_REPORT_NUMBER = Column(Unicode(256))
    ZM_ID = Column(Unicode(18))
    SO_REMARK = Column(Unicode(1024))
    SO_POST_OUT_DATE = Column(DateTime)
    SO_CONFIRMED_DATE = Column(DateTime)
    LIMS_STATUS = Column(Unicode(16))
    LIMS_REMARK = Column(Unicode(256))
    SOC_ID = Column(Integer, ForeignKey("SUBORDER_CATEGORY.ID"))
    RFAE_ID = Column(Integer, ForeignKey("REASON_FOR_ADDITIONAL_EFFORT.ID"))
    FROM_STARLIMS: Mapped[bool] = Column(BIT, nullable=False)
    SO_COORDINATOR = Column(Integer)
    STARLIMS_DISTINCTIVE_FLAG = Column(Integer)
    DEADLINE_CALCULATION_WITHOUT_HOLIDAYS: Mapped[bool] = Column(
        BIT, nullable=False
    )
    SO_MODEL = Column(Unicode(255))
    TRANSFER_TO_STARLIMS = Column(DateTime)
    STARLIMS_PROJECT_NUMBER = Column(Unicode(25))
    URGENT: Mapped[bool] = Column(BIT, nullable=False)
    SO_POSTING_DONE_DATE = Column(DateTime)
    KPI: Mapped[bool] = Column(BIT, nullable=False)
    SO_DATE_READY_REASON = Column(Unicode(512))
    SO_DATE_READY_CHANGED = Column(DateTime)
    SO_DATE_CHECK_REASON = Column(Unicode(512))
    SO_DATE_CHECK_CHANGED = Column(DateTime)
    REPORT_SENT = Column(DateTime)
    S_KPI_NUMBER = Column(Integer)
    SO_TUV_CERT_EXISTS: Mapped[bool] = Column(BIT, nullable=False)
    SO_EXTERNAL_CERT_EXISTS: Mapped[bool] = Column(BIT, nullable=False)
    SO_CERT_COMMENT = Column(Unicode(512))

    anonymization_log: AnonymizationLog = relationship(
        "AnonymizationLog", uselist=False
    )
    project: Project = relationship(
        "Project", back_populates="sub_orders", uselist=False
    )
    reason_for_additional_effort: ReasonForAdditionalEffort = relationship(
        "ReasonForAdditionalEffort", uselist=False
    )
    suborder_category: SuborderCategory = relationship(
        "SuborderCategory", uselist=False
    )
    so_checkby_team: Hierarchy = relationship(
        "Hierarchy",
        primaryjoin="SubOrder.SO_CHECKBY_TEAM == Hierarchy.HR_NEW_ID",
        uselist=False,
    )
    so_dispoby_team: Hierarchy = relationship(
        "Hierarchy",
        primaryjoin="SubOrder.SO_DISPOBY_TEAM == Hierarchy.HR_NEW_ID",
        uselist=False,
    )
    so_dreadyby_team: Hierarchy = relationship(
        "Hierarchy",
        primaryjoin="SubOrder.SO_READYBY_TEAM == Hierarchy.HR_NEW_ID",
        uselist=False,
    )
    so_regby_team: Hierarchy = relationship(
        "Hierarchy",
        primaryjoin="SubOrder.SO_REGBY_TEAM == Hierarchy.HR_NEW_ID",
        uselist=False,
    )
    so_updateby_team: Hierarchy = relationship(
        "Hierarchy",
        primaryjoin="SubOrder.SO_UPDATEBY_TEAM == Hierarchy.HR_NEW_ID",
        uselist=False,
    )
    st_id_team: Hierarchy = relationship(
        "Hierarchy",
        primaryjoin="SubOrder.ST_ID_TEAM == Hierarchy.HR_NEW_ID",
        uselist=False,
    )


class Hierarchy(Base):
    """Hierarchy table model."""

    __tablename__ = "HIERARCHY"

    HR_ID: Mapped[str] = Column(UNIQUEIDENTIFIER, primary_key=True)
    HR_LOCATION = Column(Unicode(40))
    HR_SHORT = Column(Unicode(20))
    HR_PREFIX = Column(Unicode(20))
    HR_ACTIVE: Mapped[bool] = Column(BIT, nullable=False)
    HR_TYPE = Column(Unicode(50))
    HR_CURRENT = Column(BIT)
    HR_PARENT = Column(UNIQUEIDENTIFIER)
    HR_UPDATE_TYPE = Column(TINYINT)
    HR_NEW_ID: Mapped[int] = Column(Integer, nullable=False, unique=True)
    HR_LEVEL: Mapped[int] = Column(Integer, nullable=False)
    HR_EMAIL = Column(Unicode(80))
    ST_ID = Column(Integer, ForeignKey("STAFF.ST_ID"))
    CC_ID = Column(Unicode(10), ForeignKey("KST.CC_ID"))
    POSTING_TARGET = Column(Unicode(4))
    COSTING_DATA_ORDER_SIZE = Column(DECIMAL(19, 4))
    CREATED: Mapped[datetime] = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, ForeignKey("STAFF.ST_ID"), nullable=False)
    HR_LAST_UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer, ForeignKey("STAFF.ST_ID"))
    IS_PLACEHOLDER: Mapped[bool] = Column(BIT, nullable=False)

    kst: Kst = relationship("Kst", uselist=False)
    created_by: Staff = relationship(
        "Staff",
        primaryjoin="Hierarchy.CREATED_BY == Staff.ST_ID",
        uselist=False,
    )
    st_id: Staff = relationship(
        "Staff", primaryjoin="Hierarchy.ST_ID == Staff.ST_ID", uselist=False
    )
    updated_by: Staff = relationship(
        "Staff",
        primaryjoin="Hierarchy.UPDATED_BY == Staff.ST_ID",
        uselist=False,
    )


class Kst(Base):
    """Kst table model."""

    __tablename__ = "KST"

    CC_ID: Mapped[str] = Column(Unicode(10), primary_key=True)
    CC_NAME = Column(Unicode(16))
    CC_BOOKINGAREA = Column(Unicode(4))
    CC_TYPE = Column(Integer)
    CREATED: Mapped[datetime] = Column(DateTime, nullable=False)
    CREATED_BY: Mapped[int] = Column(
        Integer, ForeignKey("STAFF.ST_ID"), nullable=False
    )
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer, ForeignKey("STAFF.ST_ID"))
    CC_GLOBAL_PARTNER_MANDATORY: Mapped[bool] = Column(BIT, nullable=False)
    VALID_FROM = Column(DateTime)
    VALID_UNTIL = Column(DateTime)
    RUN_ID = Column(Integer)
    KTEXT = Column(Unicode(256))
    LTEXT = Column(Unicode(256))

    created_by: Staff = relationship(
        "Staff", primaryjoin="Kst.CREATED_BY == Staff.ST_ID", uselist=False
    )
    updated_by: Staff = relationship(
        "Staff", primaryjoin="Kst.UPDATED_BY == Staff.ST_ID", uselist=False
    )


class SuborderCategory(Base):
    """SuborderCategory table model."""

    __tablename__ = "SUBORDER_CATEGORY"

    ID: Mapped[int] = Column(Integer, primary_key=True)
    NAME_DE: Mapped[str] = Column(Unicode(256), nullable=False)
    NAME_EN: Mapped[str] = Column(Unicode(256), nullable=False)
    NAME_FR: Mapped[str] = Column(Unicode(256), nullable=False)
    CREATED: Mapped[datetime] = Column(DateTime, nullable=False)
    CREATED_BY: Mapped[int] = Column(
        Integer, ForeignKey("STAFF.ST_ID"), nullable=False
    )
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer, ForeignKey("STAFF.ST_ID"))

    created_by: Staff = relationship(
        "Staff",
        primaryjoin="SuborderCategory.CREATED_BY == Staff.ST_ID",
        uselist=False,
    )
    updated_by: Staff = relationship(
        "Staff",
        primaryjoin="SuborderCategory.UPDATED_BY == Staff.ST_ID",
        uselist=False,
    )


class AnonymizationLog(Base):
    """AnonymizationLog table model."""

    __tablename__ = "ANONYMIZATION_LOG"

    AL_ID: Mapped[int] = Column(Integer, primary_key=True)
    AL_DATE: Mapped[datetime] = Column(DateTime, nullable=False)
    AL_COUNT_ACCOUNTING: Mapped[int] = Column(Integer, nullable=False)
    AL_COUNT_CHANCES: Mapped[int] = Column(Integer, nullable=False)
    AL_COUNT_PROCESS: Mapped[int] = Column(Integer, nullable=False)
    AL_COUNT_PROCESSFOLDER: Mapped[int] = Column(Integer, nullable=False)
    AL_COUNT_PROJECT: Mapped[int] = Column(Integer, nullable=False)
    AL_COUNT_PROKALKMODUL: Mapped[int] = Column(Integer, nullable=False)
    AL_COUNT_SUBORDERS: Mapped[int] = Column(Integer, nullable=False)
    AL_COUNT_TESTSAMPLE: Mapped[int] = Column(Integer, nullable=False)
    AL_ERROR_ACCOUNTING: Mapped[int] = Column(Integer, nullable=False)
    AL_ERROR_CHANCES: Mapped[int] = Column(Integer, nullable=False)
    AL_ERROR_PROCESS: Mapped[int] = Column(Integer, nullable=False)
    AL_ERROR_PROCESSFOLDER: Mapped[int] = Column(Integer, nullable=False)
    AL_ERROR_PROJECT: Mapped[int] = Column(Integer, nullable=False)
    AL_ERROR_PROKALKMODUL: Mapped[int] = Column(Integer, nullable=False)
    AL_ERROR_SUBORDERS: Mapped[int] = Column(Integer, nullable=False)
    AL_ERROR_TESTSAMPLE: Mapped[int] = Column(Integer, nullable=False)


class ReasonForAdditionalEffort(Base):
    """ReasonForAdditionalEffort table model."""

    __tablename__ = "REASON_FOR_ADDITIONAL_EFFORT"

    ID: Mapped[int] = Column(Integer, primary_key=True)
    NAME_DE: Mapped[str] = Column(Unicode(256), nullable=False)
    NAME_EN: Mapped[str] = Column(Unicode(256), nullable=False)
    NAME_FR: Mapped[str] = Column(Unicode(256), nullable=False)
    CREATED: Mapped[datetime] = Column(DateTime, nullable=False)
    CREATED_BY: Mapped[int] = Column(
        Integer, ForeignKey("STAFF.ST_ID"), nullable=False
    )
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer, ForeignKey("STAFF.ST_ID"))

    created_by: Staff = relationship(
        "Staff",
        primaryjoin="ReasonForAdditionalEffort.CREATED_BY == Staff.ST_ID",
        uselist=False,
    )
    updated_by: Staff = relationship(
        "Staff",
        primaryjoin="ReasonForAdditionalEffort.UPDATED_BY == Staff.ST_ID",
        uselist=False,
    )


class ProjectFailureRel(Base):
    """ProjectFailureRel table model."""

    __tablename__ = "PROJECT_FAILURE_REL"

    ID: Mapped[int] = Column(Integer, primary_key=True)
    P_ID: Mapped[int] = Column(
        Integer, ForeignKey("PROJECT.P_ID"), nullable=False
    )
    SO_NUMBER = Column(Integer)
    FAIL_ID: Mapped[int] = Column(
        Integer, ForeignKey("FAILURE_MD.FAIL_ID"), nullable=False
    )

    failure_md: FailureMd = relationship("FailureMd")
    project: Project = relationship(
        "Project", back_populates="project_failure_rel"
    )


class FailureMd(Base):
    """FailureMd table model."""

    __tablename__ = "FAILURE_MD"

    FAIL_ID: Mapped[int] = Column(Integer, primary_key=True)
    MD_ID: Mapped[int] = Column(Integer, nullable=False)
    FAIL_KEY: Mapped[str] = Column(Unicode(16), nullable=False)
    FAIL_TEXT_EN = Column(Unicode(150))
    FAIL_TEXT_DE = Column(Unicode(150))
    FAIL_TEXT_FR = Column(Unicode(150))
    FAIL_EXAMPLE_EN = Column(Unicode(500))
    FAIL_EXAMPLE_DE = Column(Unicode(500))
    FAIL_EXAMPLE_FR = Column(Unicode(500))
    Created: Mapped[datetime] = Column(DateTime, nullable=False)
    CreatedBy = Column(Integer)
    Updated = Column(DateTime)
    UpdatedBy = Column(Integer)


def get_selected_psex_id() -> Optional[int]:
    """Get the id of the currently selected project in PSExplorer."""
    key = OpenKey(HKEY_CURRENT_USER, r"Software\TUV\PSExplorer", 0, KEY_READ)
    try:
        project_id = QueryValueEx(key, "SelectedProjectId")[0]
        log.debug("Selected PSEX-ID is %s", project_id)
        return int(project_id) if project_id else None
    except OSError as error:
        if error.errno == errno.ENOENT:
            log.debug("Key does not exist.")
            return None
        raise
    finally:
        key.Close()
