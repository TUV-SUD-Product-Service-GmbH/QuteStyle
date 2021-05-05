"""Database connection and models for the PSE database."""
import errno
import logging
import os
from winreg import OpenKey, HKEY_CURRENT_USER, KEY_READ, QueryValueEx
from contextlib import contextmanager
from typing import Iterator, Optional, List

from sqlalchemy import create_engine, Column, Integer, Unicode, Float, \
    ForeignKey, DateTime, Boolean, SmallInteger, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.pool import StaticPool

from tsl.common_db import NullUnicode
from tsl.variables import STD_DB_PATH, PATH

log = logging.getLogger("tsl.pse_database")  # pylint: disable=invalid-name

# pre pool ping will ensure, that connection is reestablished if not alive
# check_same_thread and poolclass are necessary so that unit test can use a
# in memory sqlite database across different threads.
ENGINE = create_engine(
    os.getenv("PSE_DB_PATH", STD_DB_PATH.format("PSExplorer")),
    connect_args={'check_same_thread': False}, poolclass=StaticPool,
    pool_pre_ping=True)

Base = declarative_base()
Base.metadata.bind = ENGINE

AdminSession = sessionmaker(bind=ENGINE)  # pylint: disable=invalid-name


@contextmanager
def session_scope(commit: bool = True) -> Iterator[Session]:
    """Provide a transactional scope around a series of operations."""
    session = AdminSession()
    try:
        session.expire_on_commit = False
        yield session
        if commit:
            session.commit()
    except:  # nopep8
        session.rollback()
        raise
    finally:
        session.close()


# pylint: disable=too-few-public-methods
class Process(Base):
    """Process table model."""

    __tablename__ = 'PROCESS'

    PC_ID = Column(Integer, primary_key=True, nullable=False)
    PC_NAME = Column(NullUnicode(length=256), nullable=False, default="")
    PC_IAN = Column(NullUnicode(length=256), nullable=False, default="")
    PC_PATH = Column(NullUnicode(length=50), nullable=False, default="")

    @property
    def process_archive(self) -> str:
        """Return the full path to the process archive of the Process"""
        return os.path.join(PATH, "PSEX", self.PC_PATH)


class ProcessPhase(Base):
    """ProcessPhase table model."""

    __tablename__ = 'PROCESSPHASE'

    PRP_ID = Column(Integer, primary_key=True, nullable=False)
    PRP_SHORT_DE = Column(NullUnicode(length=256), nullable=False, default="")
    PRP_SHORT_EN = Column(NullUnicode(length=256), nullable=False, default="")
    PRP_SHORT_FR = Column(NullUnicode(length=256), nullable=False, default="")


class Project(Base):
    """Project table model."""

    __tablename__ = 'PROJECT'

    P_ID = Column(Integer, primary_key=True, nullable=False)
    PC_ID = Column(Integer, ForeignKey('PROCESS.PC_ID'))
    P_IAN = Column(NullUnicode(length=256), nullable=False, default="")
    P_PRODUCT = Column(NullUnicode(length=256), nullable=False, default="")
    P_CONTACT = Column(NullUnicode(length=256), nullable=False, default="")
    P_CONTACT_CUC_ID = Column(Integer, ForeignKey('CUSTOMER_CONTACT.CUC_ID'))
    P_DEADLINE = Column(DateTime)
    P_ORDERSIZE = Column(Float)
    P_PROCESSPHASE = Column(Integer, ForeignKey('PROCESSPHASE.PRP_ID'))
    P_MODEL = Column(NullUnicode(length=256), nullable=False, default="")
    P_ZARA_NUMBER = Column(NullUnicode(length=11), nullable=False, default="")
    P_FOLDER = Column(NullUnicode(length=256), nullable=False, default="")
    DELR_ID = Column(Integer)
    P_WC_ID = Column(Unicode(length=36))
    P_NAME = Column(NullUnicode(length=31), nullable=False, default="")
    P_CUSTOMER_A = Column(Integer, ForeignKey('CUSTOMER.CU_ID'))
    P_CUSTOMER_B = Column(Integer, ForeignKey('CUSTOMER.CU_ID'))
    P_PROJECTMANAGER = Column(Integer, ForeignKey('STAFF.ST_ID'))
    P_TOKEN = Column(NullUnicode(length=61), nullable=False, default="")
    P_DATE_APPOINTMENT = Column(DateTime)
    P_EXPECTED_TS_RECEIPT = Column(DateTime)
    BATCH_NUMBER = Column(Unicode(length=16))

    customer_contact = relationship('CustomerContact')
    ordering_party = relationship('Customer', foreign_keys=[P_CUSTOMER_A])
    manufacturer = relationship('Customer', foreign_keys=[P_CUSTOMER_B])
    process = relationship('Process')
    phase = relationship('ProcessPhase')
    staff = relationship('Staff')

    @property
    def project_folder(self) -> str:
        """Return the full path to the project folder of the Project"""
        return os.path.join(PATH, self.P_FOLDER)


class Customer(Base):
    """Customer table model."""

    __tablename__ = 'CUSTOMER'

    CU_ID = Column(Integer, primary_key=True)
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

    addresses: List['CustomerAddress'] = relationship(  # type: ignore
        'CustomerAddress', back_populates="customer")


class CustomerContact(Base):
    """CustomerContact table model."""

    __tablename__ = 'CUSTOMER_CONTACT'

    CUC_ID = Column(Integer, primary_key=True, nullable=False)
    CUC_FORENAME = Column(NullUnicode(length=51), nullable=False, default="")
    CUC_SURNAME = Column(NullUnicode(length=36), nullable=False, default="")
    ANRED = Column(NullUnicode(length=31), nullable=False, default="")
    CUC_MAIL = Column(NullUnicode(length=256), nullable=False, default="")


class CustomerAddress(Base):
    """CustomerAddress table model."""

    __tablename__ = 'CUSTOMER_ADDRESS'

    CA_ID = Column(Integer, primary_key=True, nullable=False)
    CU_ID = Column(Integer, ForeignKey('CUSTOMER.CU_ID'), nullable=False)
    CA_NAME = Column(NullUnicode(length=166), nullable=False, default="")
    CA_STREET = Column(NullUnicode(length=101), nullable=False, default="")
    CA_ZIPCODE = Column(NullUnicode(length=11), nullable=False, default="")
    CA_CITY = Column(NullUnicode(length=41), nullable=False, default="")

    customer = relationship('Customer', back_populates="addresses")


class Staff(Base):
    """Staff table model."""

    __tablename__ = 'STAFF'

    ST_ID = Column(Integer, primary_key=True, nullable=False)
    ST_SURNAME = Column(NullUnicode(length=61), nullable=False, default="")
    ST_FORENAME = Column(NullUnicode(length=51), nullable=False, default="")
    ST_PHONE = Column(NullUnicode(length=81), nullable=False, default="")
    ST_FAX = Column(NullUnicode(length=81), nullable=False, default="")
    ST_EMAIL = Column(NullUnicode(length=81), nullable=False, default="")


class TemplateData(Base):
    """TemplateData table model."""

    __tablename__ = 'TEMPLATE_DATA'

    TPD_ID = Column(Integer, primary_key=True, nullable=False)
    TP_ID = Column(Integer, nullable=False)
    TPD_DATA = Column(LargeBinary)


class Template(Base):
    """
    TemplateData table model.

    If the template represents an eDoc DefaultModule, the TP_FILENAME can be
    empty. In this case, the DM_ID must exist. Nevertheless it is possible
    to have a DM_ID and a TP_FILENAME at the same time.
    """

    __tablename__ = 'TEMPLATE'

    TP_ID = Column(Integer, primary_key=True, nullable=False)
    MD_ID = Column(Integer, nullable=False)
    TPST_ID = Column(Integer, nullable=False)
    TPT_ID = Column(Integer, ForeignKey('TEMPLATE_TYPE.TPT_ID'),
                    nullable=False)
    TPSC_ID = Column(Integer, ForeignKey('TEMPLATE_SCOPE.TPSC_ID'),
                     nullable=False)
    TPF_ID = Column(Integer, nullable=False)
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
    TP_DISABLED = Column(Boolean, nullable=False)
    TP_TRANSFER_STATUS = Column(Unicode(length=51))
    TP_ORIGINATING_SERVERID = Column(Integer)
    TP_ROOT_TEMPLATE_ID = Column(Integer)
    TP_UTC = Column(DateTime)
    TP_WORKINGCLUSTER = Column(Unicode(length=36))
    DM_ID = Column(Integer)
    TP_OLD_TP = Column(Integer)

    temp_scope = relationship('TemplateScope')
    temp_type = relationship('TemplateType')


class TemplateScope(Base):
    """TemplateScope table model."""

    __tablename__ = 'TEMPLATE_SCOPE'

    TPSC_ID = Column(Integer, primary_key=True, nullable=False)
    TPSC_NAME_DE = Column(Unicode(length=256), nullable=False)
    TPSC_NAME_EN = Column(Unicode(length=256), nullable=False)
    TPSC_NAME_FR = Column(Unicode(length=256), nullable=False)
    TPSC_SHORT_DE = Column(Unicode(length=256), nullable=False)
    TPSC_SHORT_EN = Column(Unicode(length=256), nullable=False)
    TPSC_SHORT_FR = Column(Unicode(length=256), nullable=False)
    TPSC_PATH = Column(Unicode(length=256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)


class TemplateStatus(Base):
    """TemplateStatus table model."""

    __tablename__ = 'TEMPLATE_STATUS'

    TPST_ID = Column(Integer, primary_key=True, nullable=False)
    TPST_NAME_DE = Column(Unicode(length=256), nullable=False)
    TPST_NAME_EN = Column(Unicode(length=256), nullable=False)
    TPST_NAME_FR = Column(Unicode(length=256), nullable=False)
    TPST_SHORT_DE = Column(Unicode(length=256), nullable=False)
    TPST_SHORT_EN = Column(Unicode(length=256), nullable=False)
    TPST_SHORT_FR = Column(Unicode(length=256), nullable=False)
    CREATED = Column(DateTime, nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)


class TemplateType(Base):
    """TemplateType table model."""

    __tablename__ = 'TEMPLATE_TYPE'

    TPT_ID = Column(Integer, primary_key=True, nullable=False)
    TPT_NAME_DE = Column(Unicode(length=256), nullable=False)
    TPT_NAME_EN = Column(Unicode(length=256), nullable=False)
    TPT_NAME_FR = Column(Unicode(length=256), nullable=False)
    TPT_SHORT_DE = Column(Unicode(length=256), nullable=False)
    TPT_SHORT_EN = Column(Unicode(length=256), nullable=False)
    TPT_SHORT_FR = Column(Unicode(length=256), nullable=False)
    TPT_PATH = Column(Unicode(length=256), nullable=False)
    TPT_PREFIX = Column(Unicode(length=256), nullable=False)
    TPT_MODULETYPE = Column(Unicode(length=256), nullable=False)
    TPT_SHOWINPROZESSFOLDER = Column(Boolean, nullable=False)
    TPT_SHOWINTEMPLATEMANAGER = Column(Boolean, nullable=False)
    CREATED = Column(DateTime, nullable=False)
    CREATED_BY = Column(Integer, nullable=False)
    UPDATED = Column(DateTime)
    UPDATED_BY = Column(Integer)
    TPT_INCLUDE_IN_TRADE_REPORT = Column(Boolean, nullable=False)


def get_selected_psex_id() -> Optional[int]:
    """Get the id of the currently selected project in PSExplorer."""
    key = OpenKey(HKEY_CURRENT_USER, r"Software\TUV\PSExplorer", 0, KEY_READ)
    try:
        project_id = QueryValueEx(key, 'SelectedProjectId')[0]
        log.debug("Selected PSEX-ID is %s", project_id)
        return int(project_id) if project_id else None
    except OSError as error:
        if error.errno == errno.ENOENT:
            log.debug("Key does not exist.")
            return None
        raise
    finally:
        key.Close()
