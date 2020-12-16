"""Database connection and models for the PSE database."""
import errno
import logging
import os
from winreg import OpenKey, HKEY_CURRENT_USER, KEY_READ, QueryValueEx
from contextlib import contextmanager
from typing import Iterator, Optional

from sqlalchemy import create_engine, Column, Integer, Unicode, Float, \
    ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.pool import StaticPool

from tsl.variables import STD_DB_PATH

log = logging.getLogger("tsl.pse_database")  # pylint: disable=invalid-name

# pre pool ping will ensure, that connection is reestablished if not alive
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
    PC_NAME = Column(Unicode(length=256))
    PC_IAN = Column(Unicode(length=256))
    PC_PATH = Column(Unicode(length=50))


class ProcessPhase(Base):
    """ProcessPhase table model."""

    __tablename__ = 'PROCESSPHASE'

    PRP_ID = Column(Integer, primary_key=True, nullable=False)
    PRP_SHORT_DE = Column(Unicode(length=256))
    PRP_SHORT_EN = Column(Unicode(length=256))
    PRP_SHORT_FR = Column(Unicode(length=256))


class Project(Base):
    """Project table model."""

    __tablename__ = 'PROJECT'

    P_ID = Column(Integer, primary_key=True, nullable=False)
    PC_ID = Column(Integer, ForeignKey('PROCESS.PC_ID'))
    P_IAN = Column(Unicode(length=256))
    P_PRODUCT = Column(Unicode(length=256))
    P_CONTACT = Column(Unicode(length=256))
    P_CONTACT_CUC_ID = Column(Integer, ForeignKey('CUSTOMER_CONTACT.CUC_ID'))
    P_DEADLINE = Column(DateTime)
    P_ORDERSIZE = Column(Float)
    P_PROCESSPHASE = Column(Integer, ForeignKey('PROCESSPHASE.PRP_ID'))
    P_MODEL = Column(Unicode(length=256))
    P_ZARA_NUMBER = Column(Unicode(length=11))
    P_FOLDER = Column(Unicode(length=256))
    DELR_ID = Column(Integer)
    P_WC_ID = Column(Unicode(length=36))
    P_NAME = Column(Unicode(length=31))
    P_CUSTOMER_A = Column(Integer, ForeignKey('CUSTOMER_ADDRESS.CU_ID'))
    P_CUSTOMER_B = Column(Integer, ForeignKey('CUSTOMER_ADDRESS.CU_ID'))
    P_PROJECTMANAGER = Column(Integer, ForeignKey('STAFF.ST_ID'))
    P_TOKEN = Column(Unicode(length=61))
    P_DATE_APPOINTMENT = Column(DateTime)
    P_EXPECTED_TS_RECEIPT = Column(DateTime)
    BATCH_NUMBER = Column(Unicode(length=16))

    customer_contact = relationship('CustomerContact')
    ordering_party_address = relationship('CustomerAddress',
                                          foreign_keys=[P_CUSTOMER_A])
    manufacturer_address = relationship('CustomerAddress',
                                        foreign_keys=[P_CUSTOMER_B])
    process = relationship('Process')
    phase = relationship('ProcessPhase')
    staff = relationship('Staff')


class CustomerContact(Base):
    """CustomerContact table model."""

    __tablename__ = 'CUSTOMER_CONTACT'

    CUC_ID = Column(Integer, primary_key=True, nullable=False)
    CUC_FORENAME = Column(Unicode(length=51))
    CUC_SURNAME = Column(Unicode(length=36))
    ANRED = Column(Unicode(length=31))
    CUC_MAIL = Column(Unicode(length=256))


class CustomerAddress(Base):
    """CustomerAddress table model."""

    __tablename__ = 'CUSTOMER_ADDRESS'

    CA_ID = Column(Integer, primary_key=True, nullable=False)
    CU_ID = Column(Integer, nullable=False)
    CA_NAME = Column(Unicode(length=166), nullable=False)
    CA_STREET = Column(Unicode(length=101))
    CA_ZIPCODE = Column(Unicode(length=11))
    CA_CITY = Column(Unicode(length=41))


class Staff(Base):
    """Staff table model."""

    __tablename__ = 'STAFF'

    ST_ID = Column(Integer, primary_key=True, nullable=False)
    ST_SURNAME = Column(Unicode(length=61))
    ST_FORENAME = Column(Unicode(length=51))
    ST_PHONE = Column(Unicode(length=81))
    ST_FAX = Column(Unicode(length=81))
    ST_EMAIL = Column(Unicode(length=81))


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
