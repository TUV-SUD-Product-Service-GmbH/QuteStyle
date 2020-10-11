"""
Database connection and models for the PSE database.

WARNING! Delete cascades do not work properly, when delete is executed on a
query. Always use session.delete()!

"""
import logging
import os
from contextlib import contextmanager
from datetime import datetime
from typing import List, Iterator

from sqlalchemy import create_engine, Column, Integer, Unicode, DateTime, \
    Boolean, Float, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.sql.schema import ForeignKey

from tsl.variables import STD_DB_PATH

log = logging.getLogger("tsl.edoc_database")  # pylint: disable=invalid-name

ENGINE = create_engine(os.getenv("EDOC_DB_PATH", STD_DB_PATH.format("EDOC")))

Base = declarative_base()
Base.metadata.bind = ENGINE

AdminSession = sessionmaker(bind=ENGINE)  # pylint: disable=invalid-name


# session fixture for use in with statement
@contextmanager
def session_scope() -> Iterator[Session]:
    """Provide a transactional scope around a series of operations."""
    session = AdminSession()
    try:
        session.expire_on_commit = False
        yield session
        session.commit()
    except:  # nopep8
        session.rollback()
        raise
    finally:
        session.close()


# pylint: disable=too-few-public-methods
class AppsCount(Base):
    """AppsCount table model."""

    __tablename__ = 'APPS_COUNT'

    APPSC_ID = Column(Integer, primary_key=True, nullable=False)
    ST_ID = Column(Integer)  # User Id
    APPST_ID = Column(Integer)  # App Id (as in APPS_TYPE)
    APPSC_REG = Column(DateTime)  # time of app call


class Staff(Base):
    """Staff table model."""

    __tablename__ = 'V_PSEX_STAFF'

    ST_ID = Column(Integer, primary_key=True, nullable=False)
    ST_SURNAME = Column(Unicode(length=60), nullable=False)
    ST_FORENAME = Column(Unicode(length=50))
    ST_COSTID = Column(Unicode(length=10))
    ST_ACTIVE = Column(Boolean, nullable=False)
    ST_NUMBER = Column(Unicode(length=8))
    ST_SHORT = Column(Unicode(length=3))
    ST_PHONE = Column(Unicode(length=40))
    ST_FAX = Column(Unicode(length=40))
    ST_EMAIL = Column(Unicode(length=80))
    ST_WINDOWSID = Column(Unicode(length=32))
    # the team is a UUID as follows: "319F6D8C-2094-40E9-A543-3975DE4B9A75"
    # in the MSSQL this is defined as UNIQUEIDENTIFIER. setting it as str since
    # we cannot use UNIQUEIDENTIFIER on sqlite
    ST_TEAM = Column(Unicode(length=36))
    ST_TYPE = Column(Integer, nullable=False)
    ST_LOCATION = Column(Unicode(length=50))
    ST_UNIT = Column(Unicode(length=12))
    ST_SERVERID = Column(Integer)
    ST_HOURS_PER_DAY = Column(Integer)
    ST_SKILLGROUP = Column(Unicode(length=8), nullable=False)
    ST_DOMAIN = Column(Unicode(length=32))
    ST_GENDER = Column(Unicode(length=50))


class Team(Base):
    """Staff table model."""

    __tablename__ = 'V_PSEX_HIERARCHY'

    HR_ID = Column(Integer, primary_key=True, nullable=False)
    HR_SHORT = Column(Unicode(length=21))


class PackageElement(Base):
    """Package element table model."""

    __tablename__ = "NAV_PACK_ELEMENT"

    NPE_ID = Column(Integer, primary_key=True, nullable=False)
    NP_ID = Column(Integer, ForeignKey('NAV_PACK.NP_ID', ondelete="CASCADE"))
    DM_ID = Column(Integer)
    NL_ID = Column(Integer)
    ZM_LOCATION = Column(Unicode(length=5))
    NPE_CREATE = Column(Boolean)
    CT_ID = Column(Integer)
    NPE_REG = Column(DateTime)
    NPE_REGBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    NPE_UPDATE = Column(DateTime)
    NPE_UPDATEBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    NPE_CREATE_SO = Column(Boolean, nullable=False)

    package = relationship("Package", back_populates="package_elements")
    package_calculations: List['PackageCalculation'] = \
        relationship('PackageCalculation', back_populates="package_element",
                     cascade="all, delete")
    proof_elements: List['ProofElement'] = \
        relationship("ProofElement", back_populates="package_element",
                     cascade="all, delete")


class Package(Base):
    """Package table model."""

    __tablename__ = "NAV_PACK"

    NP_ID = Column(Integer, primary_key=True, nullable=False)
    N_ID = Column(Integer, ForeignKey('NAV.N_ID', ondelete="CASCADE"))
    NP_NAME_DE = Column(Unicode(length=150))
    NP_NAME_EN = Column(Unicode(length=150))
    NP_COMMENT_DE = Column(Unicode(length=800))
    NP_COMMENT_EN = Column(Unicode(length=800))
    CL_ID = Column(Integer, ForeignKey('CLEARING.CL_ID'), nullable=False)
    NP_CLEARDATE = Column(DateTime)
    NP_CLEARBY = Column(Integer)
    ZM_PRODUCT = Column(Unicode(length=5))
    PT_ID = Column(Integer, ForeignKey("PACKAGE_TYPE.PT_ID"), nullable=False)
    NP_TESTSAMPLES = Column(Integer, nullable=False)
    NP_IS_TEMPLATE = Column(Boolean, nullable=False)
    NP_TEMPLATE_ID = Column(Integer)
    NP_REG = Column(DateTime)
    NP_REGBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    NP_UPDATE = Column(DateTime)
    NP_UPDATEBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    PN_ID = Column(Integer, ForeignKey("PACKAGE_NAME.PN_ID"), nullable=False)

    clearing_state = relationship("Clearing")

    package_elements: List[PackageElement] = \
        relationship("PackageElement", back_populates="package",
                     cascade="all, delete")

    navigation = relationship("Navigation", back_populates="packages")

    service_classes: List['ServiceClass'] = \
        relationship("ServiceClass", back_populates="package",
                     cascade="all, delete")

    package_type = relationship("PackageType")

    package_name = relationship("PackageName")


class PackageCategory(Base):
    """Category of a Package (linked to the type)."""

    __tablename__ = 'PACKAGE_CAT'

    PC_ID = Column(Integer, primary_key=True)
    PC_NAME_DE = Column(Unicode(length=50))
    PC_NAME_EN = Column(Unicode(length=50))
    PC_REG = Column(DateTime)
    PC_REG_BY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))


class PackageType(Base):
    """Type of a Package."""

    __tablename__ = 'PACKAGE_TYPE'

    PT_ID = Column(Integer, primary_key=True)
    PT_NAME_DE = Column(Unicode(length=255))
    PT_NAME_EN = Column(Unicode(length=255))
    PT_REG = Column(DateTime)
    PT_REG_BY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    PC_ID = Column(Integer, ForeignKey('PACKAGE_CAT.PC_ID'))

    package_category = relationship("PackageCategory")


class PackageName(Base):
    """Name of a Package."""

    __tablename__ = "PACKAGE_NAME"

    PN_ID = Column(Integer, primary_key=True)
    PN_NAME_DE = Column(Unicode(length=255))
    PN_NAME_EN = Column(Unicode(length=255))
    PN_REG = Column(DateTime)
    PN_REG_BY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    PN_UPDATE = Column(DateTime)
    PN_UPDATE_BY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))


class Clearing(Base):
    """Clearing status definitions (i.e. 06-Freigegeben)."""

    __tablename__ = "CLEARING"

    CL_ID = Column(Integer, primary_key=True)
    CL_NAME_DE = Column(Unicode(length=100))
    CL_NAME_EN = Column(Unicode(length=100))
    CL_DESCRIPTION_DE = Column(Unicode(length=255))  # always NULL
    CL_DESCRIPTION_EN = Column(Unicode(length=255))  # always NULL
    CL_REG = Column(DateTime)
    CL_REGBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    CL_UPDATE = Column(DateTime)
    CL_UPDATEBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    TPST_ID = Column(Integer)  # not clear what this is


class PackageCalculation(Base):
    """Calculation data for a PackageElement."""

    __tablename__ = "NAV_PACK_ELEMENT_CALC"

    NPEC_ID = Column(Integer, primary_key=True, nullable=False)
    NPE_ID = Column(Integer, ForeignKey('NAV_PACK_ELEMENT.NPE_ID',
                                        ondelete="CASCADE"))
    ST_ID = Column(Integer, nullable=False)
    NPEC_DELTA_START = Column(Float)
    NPEC_TIME_DAYS = Column(Integer)
    NPEC_TIME_HOURS = Column(Float)
    NPEC_RATE = Column(Numeric(precision=18, scale=2))
    NPEC_COSTS = Column(Numeric(precision=18, scale=2))
    NPEC_TRAVEL = Column(Numeric(precision=18, scale=2))
    NPEC_FACTOR = Column(Float)
    NPEC_PRICE = Column(Numeric(precision=18, scale=2))
    NPEC_COMMENT = Column(Unicode(length=500))
    NPEC_TASK = Column(Unicode(length=500))
    ZM_ID = Column(Unicode(length=50))
    NPOS_ID = Column(Integer)
    NPEC_REG = Column(DateTime)
    NPEC_REGBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    NPEC_UPDATE = Column(DateTime)
    NPEC_UPDATEBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    CBC_ID = Column(Integer)
    NPEC_COSTS_EXTERNAL = Column(Numeric(precision=18, scale=2))
    NPEC_COSTS_OLD = Column(Numeric(precision=18, scale=2))
    NPEC_COSTS_EXTERNAL_OLD = Column(Numeric(precision=18, scale=2))

    package_element = relationship(PackageElement,
                                   back_populates="package_calculations")


class Navigation(Base):
    """Navigation table model."""

    __tablename__ = "NAV"

    N_ID = Column(Integer, primary_key=True, nullable=False)
    N_TEMPLATE = Column(Integer)
    N_NAME_DE = Column(Unicode(length=120))
    N_NAME_EN = Column(Unicode(length=120))
    BEGR_ID = Column(Integer)  # not clear what this is
    N_COMMENT_DE = Column(Unicode(length=500))
    N_COMMENT_EN = Column(Unicode(length=500))
    N_DURATION = Column(Integer)
    N_MASTER = Column(Boolean, nullable=False)
    HR_NEW_ID = Column(Integer, nullable=False)  # not clear what this is
    HRC_ID = Column(Integer, ForeignKey("HR_COUNTRY.HRC_ID"), nullable=False)
    HRP_ID = Column(Integer, ForeignKey("HR_PRODUCT.HRP_ID"), nullable=False)
    ZM_OBJECT = Column(Unicode(length=5))
    KOT_ID = Column(Integer, nullable=False)  # not clear what this is
    N_REG = Column(DateTime)
    N_REGBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    N_UPDATE = Column(DateTime)
    N_UPDATEBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))

    packages: List[Package] = relationship("Package", lazy='dynamic')

    country = relationship("Country")
    product = relationship("Product")


class Country(Base):
    """Countries."""

    __tablename__ = "HR_COUNTRY"

    HRC_ID = Column(Integer, primary_key=True)
    HRC_LEFT = Column(Integer)
    HRC_RIGHT = Column(Integer)
    HRC_INDENT = Column(Integer)
    HRC_NAME_DE = Column(Unicode(length=255))
    HRC_NAME_EN = Column(Unicode(length=255))
    HRC_NAME_FR = Column(Unicode(length=255))
    HRC_UPDATE = Column(DateTime)
    HRC_UPDATEBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))


class Product(Base):
    """Products."""

    __tablename__ = "HR_PRODUCT"

    HRP_ID = Column(Integer, primary_key=True)
    HRP_LEFT = Column(Integer)
    HRP_RIGHT = Column(Integer)
    HRP_INDENT = Column(Integer)
    HRP_NAME_DE = Column(Unicode(length=255))
    HRP_NAME_EN = Column(Unicode(length=255))
    HRP_NAME_FR = Column(Unicode(length=255))
    HRP_UPDATE = Column(DateTime)
    HRP_UPDATEBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))


class ServiceClass(Base):
    """Service Class of a Package."""

    __tablename__ = "NAV_PACK_SERVICECLASS"

    NPS_ID = Column(Integer, primary_key=True, nullable=False)
    NP_ID = Column(Integer, ForeignKey('NAV_PACK.NP_ID', ondelete="CASCADE"))
    SCL_ID = Column(Integer)

    package = relationship("Package", back_populates="service_classes")


class ProofElement(Base):
    """Proof Element of a Package."""

    __tablename__ = "NAV_PACK_ELEMENT_PROOF"

    NPEP_ID = Column(Integer, primary_key=True, nullable=False)
    NPE_ID = Column(Integer, ForeignKey('NAV_PACK_ELEMENT.NPE_ID',
                                        ondelete="CASCADE"))
    NPEP_TYPE = Column(Integer)
    NPR_ID = Column(Integer)
    NPEP_TEXT_DE = Column(Unicode(length=255))
    NPEP_TEXT_EN = Column(Unicode(length=255))
    NPEP_REG = Column(DateTime)
    NPEP_REGBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    NPEP_UPDATE = Column(DateTime)
    NPEP_UPDATEBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))

    package_element = relationship('PackageElement',
                                   back_populates="proof_elements")


class Module(Base):
    """Module table model."""

    __tablename__ = "EDOC_MODUL"

    EM_ID = Column(Integer, primary_key=True, nullable=False)
    E_ID = Column(Integer)
    DM_ID = Column(Integer)
    DM_VERSION = Column(Integer)
    EM_NAME = Column(Unicode(length=255))
    EM_LETTER = Column(Unicode(length=10))
    EM_NUMBER = Column(Integer)
    SO_NUMBER = Column(Integer)
    EM_OFFLINE_BY = Column(Integer)
    EM_OFFLINE_SINCE = Column(DateTime)
    EM_REG = Column(DateTime)
    EM_REGBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    EM_UPDATE = Column(DateTime)
    EM_UPDATEBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    EM_FILTER_LEVEL = Column(Unicode(length=100))
    EM_FILTER_PARAM = Column(Unicode(length=512))
    EM_FILTER_ITEMS = Column(Unicode(length=2048))


# SCRIPTS
def insert_package_into_nav(nav_id: int, package_id: int, user_id: int,
                            session: AdminSession) -> int:
    """
    Insert a copy of the given package into the given navigation.

    Returns the id of the new package.

    Based on dbo.SP_NAV_INSERT_PACKAGE in dbo.EDOC.
    """
    log.debug("Inserting package %s into nav %s", package_id, nav_id)
    assert session.query(Navigation).get(nav_id)
    pack: Package = session.query(Package).get(package_id)
    assert pack

    now = datetime.now()
    new_pack = Package(
        N_ID=nav_id,
        NP_NAME_DE=pack.NP_NAME_DE,
        NP_NAME_EN=pack.NP_NAME_EN,
        NP_COMMENT_DE=pack.NP_COMMENT_DE,
        NP_COMMENT_EN=pack.NP_COMMENT_EN,
        CL_ID=pack.CL_ID,
        NP_CLEARDATE=pack.NP_CLEARDATE,
        NP_CLEARBY=pack.NP_CLEARBY,
        ZM_PRODUCT=pack.ZM_PRODUCT,
        PT_ID=pack.PT_ID,
        NP_TESTSAMPLES=pack.NP_TESTSAMPLES,
        NP_IS_TEMPLATE=False,
        NP_TEMPLATE_ID=pack.NP_ID,
        PN_ID=pack.PN_ID,
        NP_REG=now,
        NP_REGBY=user_id
    )
    session.add(new_pack)
    session.flush()

    new_pack_id = new_pack.NP_ID

    for service_class in pack.service_classes:
        new_class = ServiceClass(
            NP_ID=new_pack.NP_ID,
            SCL_ID=service_class.SCL_ID
        )
        session.add(new_class)

    for package_element in pack.package_elements:
        new_element = PackageElement(
            NP_ID=new_pack.NP_ID,
            DM_ID=package_element.DM_ID,
            NL_ID=package_element.NL_ID,
            ZM_LOCATION=package_element.ZM_LOCATION,
            CT_ID=package_element.CT_ID,
            NPE_CREATE=package_element.NPE_CREATE,
            NPE_CREATE_SO=package_element.NPE_CREATE_SO,
            NPE_REG=now,
            NPE_REGBY=user_id
        )
        session.add(new_element)
        session.flush()

        for calculaton in package_element.package_calculations:
            new_calc = PackageCalculation(
                NPE_ID=new_element.NPE_ID,
                ST_ID=calculaton.ST_ID,
                NPEC_DELTA_START=calculaton.NPEC_DELTA_START,
                NPEC_TIME_DAYS=calculaton.NPEC_TIME_DAYS,
                NPEC_TIME_HOURS=calculaton.NPEC_TIME_HOURS,
                NPEC_RATE=calculaton.NPEC_RATE,
                NPEC_COSTS=calculaton.NPEC_COSTS,
                NPEC_TRAVEL=calculaton.NPEC_TRAVEL,
                NPEC_FACTOR=calculaton.NPEC_FACTOR,
                NPEC_PRICE=calculaton.NPEC_PRICE,
                NPEC_COMMENT=calculaton.NPEC_COMMENT,
                NPEC_TASK=calculaton.NPEC_TASK,
                ZM_ID=calculaton.ZM_ID,
                NPOS_ID=calculaton.NPOS_ID,
                NPEC_REG=now,
                NPEC_REGBY=user_id
            )
            session.add(new_calc)

        for proof_element in package_element.proof_elements:
            new_proof = ProofElement(
                NPE_ID=new_element.NPE_ID,
                NPEP_TYPE=proof_element.NPEP_TYPE,
                NPR_ID=proof_element.NPR_ID,
                NPEP_TEXT_DE=proof_element.NPEP_TEXT_DE,
                NPEP_TEXT_EN=proof_element.NPEP_TEXT_EN,
                NPEP_REG=now,
                NPEP_REGBY=user_id
            )
            session.add(new_proof)
    session.flush()
    return new_pack_id
