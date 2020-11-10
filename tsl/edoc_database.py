"""
Database connection and models for the PSE database.

WARNING! Delete cascades do not work properly, when delete is executed on a
query. Always use session.delete()!

"""
import logging
import operator
import os
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime
from typing import List, Iterator, Optional, Dict, cast

from sqlalchemy import create_engine, Column, Integer, Unicode, DateTime, \
    Boolean, Float, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session, Query
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
    HR_NEW_ID = Column(Integer, nullable=False)
    ST_ID = Column(Integer)


class TeamSublocation(Base):
    """Sublocation of a team."""

    __tablename__ = "V_TEAM_SUBLOCATION"

    ST_ID = Column(Integer, primary_key=True)
    ST_SURNAME = Column(Unicode(length=60), nullable=False)
    ST_TEAM = Column(Unicode(length=36))
    Sublocation = Column(Unicode(length=6))  # is always NULL as of 16.10.2020

    @property
    def name(self) -> Optional[str]:
        """Return the name of the team."""
        return self.ST_SURNAME


class PackageElement(Base):
    """Package element table model."""

    __tablename__ = "NAV_PACK_ELEMENT"

    NPE_ID = Column(Integer, primary_key=True, nullable=False)
    NP_ID = Column(Integer, ForeignKey('NAV_PACK.NP_ID', ondelete="CASCADE"))
    DM_ID = Column(Integer, ForeignKey('DEFAULT_MODUL.DM_ID'))
    NL_ID = Column(Integer, ForeignKey('NAVLEVEL.NL_ID'))
    ZM_LOCATION = Column(Unicode(length=5))
    NPE_CREATE = Column(Boolean)
    CT_ID = Column(Integer, ForeignKey('CALC_TYPE.CT_ID'))
    NPE_REG = Column(DateTime)
    NPE_REGBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    NPE_UPDATE = Column(DateTime)
    NPE_UPDATEBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    NPE_CREATE_SO = Column(Boolean, nullable=False)

    package = relationship("Package", back_populates="package_elements")
    package_calculations: List['PackageElementCalculation'] = \
        relationship('PackageElementCalculation',
                     back_populates="package_element", cascade="all, delete")
    proof_elements: List['ProofElement'] = \
        relationship("ProofElement", back_populates="package_element",
                     cascade="all, delete")

    default_module = relationship("DefaultModule")

    level = relationship("NavLevel")


class NavLevel(Base):
    """Level of a PackageElement."""

    __tablename__ = "NAVLEVEL"

    NL_ID = Column(Integer, primary_key=True, nullable=False)
    NL_LEVEL = Column(Integer, unique=True)
    NL_NAME_DE = Column(Unicode(length=30))
    NL_NAME_EN = Column(Unicode(length=30))


class CalculationType(Base):
    """Type of a calculation."""

    __tablename__ = "CALC_TYPE"

    CT_ID = Column(Integer, primary_key=True, nullable=False)
    CT_NAME = Column(Unicode(length=50))
    CT_ORDER = Column(Integer)
    CA_ID = Column(Integer)


class DefaultModule(Base):
    """Default module table model."""

    __tablename__ = "DEFAULT_MODUL"

    DM_ID = Column(Integer, primary_key=True, nullable=False)
    DM_VERSION = Column(Integer)
    DM_ACTIVE = Column(Boolean)
    DM_NAME = Column(Unicode(length=255))
    DM_LETTER = Column(Unicode(length=10))
    HEAD_ID = Column(Integer)
    TPT_ID = Column(Integer)
    TPSC_ID = Column(Integer)
    DM_IS_MASTER = Column(Boolean)
    DM_COMMENT = Column(Unicode(length=500))
    CL_ID = Column(Integer, ForeignKey('CLEARING.CL_ID'))
    DM_CLEAR_BY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    DM_CLEAR_DATE = Column(DateTime)
    DM_REGBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    DM_REG = Column(DateTime)
    DM_UPDATEBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    DM_UPDATE = Column(DateTime)
    DM_TESTBASE_DE = Column(Unicode(length=500))
    DM_TESTBASE_EN = Column(Unicode(length=500))
    DM_TESTBASE_FR = Column(Unicode(length=500))
    DM_IS_CUSTOMER = Column(Boolean)
    DM_IS_MARKETABILITY = Column(Boolean)
    DM_IS_USABILITY = Column(Boolean)
    CT_ID = Column(Integer, ForeignKey('CALC_TYPE.CT_ID'))
    DM_SCOPE_DE = Column(Unicode(length=500))
    DM_SCOPE_EN = Column(Unicode(length=500))
    DM_SCOPE_FR = Column(Unicode(length=500))
    DM_CLEAR_BY_VT = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    DM_CLEAR_DATE_VT = Column(DateTime)
    DM_CREATED_FOR = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    DM_CREATED_FOR_DATE = Column(DateTime)
    HRC_ID = Column(Integer, ForeignKey("HR_COUNTRY.HRC_ID"), nullable=False)
    HRP_ID = Column(Integer, ForeignKey("HR_PRODUCT.HRP_ID"), nullable=False)
    DM_IS_INFO = Column(Boolean)
    DM_SOURCE = Column(Integer)
    DM_PROCEDURE = Column(Integer)
    DM_COMMENT_DE = Column(Unicode(length=1024))
    DM_COMMENT_EN = Column(Unicode(length=1024))
    DM_COMMENT_FR = Column(Unicode(length=1024))
    DM_NAME_EN = Column(Unicode(length=255))
    ND_ID = Column(Integer, ForeignKey("NAVDOMAIN.ND_ID"))
    DM_ALIAS_DE = Column(Unicode(length=255))
    DM_ALIAS_EN = Column(Unicode(length=255))
    DM_PARENT = Column(Integer)
    DM_REVISION = Column(Unicode(length=60))

    nav_domain = relationship("NavDomain")


class NavDomain(Base):
    """Domain of a Navigation/Module."""

    __tablename__ = "NAVDOMAIN"

    ND_ID = Column(Integer, primary_key=True, nullable=False)
    ND_SHORT = Column(Unicode(length=10))
    ND_NAME_DE = Column(Unicode(length=100))
    ND_NAME_EN = Column(Unicode(length=100))
    ND_REG = Column(DateTime)
    ND_REGBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    ND_ORDER = Column(Integer)
    ND_ORDER_EXPORT = Column(Integer, nullable=False)
    ND_ORDER_PLAN_DEFAULT = Column(Integer, nullable=False)


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

    pe_quer: Query = relationship("PackageElement", lazy='dynamic')

    navigation = relationship("Navigation", back_populates="packages")

    service_classes: List['ServiceClass'] = \
        relationship("ServiceClass", back_populates="package",
                     cascade="all, delete")

    package_type = relationship("PackageType")

    package_name = relationship("PackageName")


class PackageCategory(Base):
    """Category of a Package (linked to the type)."""

    __tablename__ = 'PACKAGE_CAT'

    PC_ID = Column(Integer, primary_key=True, nullable=False)
    PC_NAME_DE = Column(Unicode(length=50))
    PC_NAME_EN = Column(Unicode(length=50))
    PC_REG = Column(DateTime)
    PC_REG_BY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))


class PackageType(Base):
    """Type of a Package."""

    __tablename__ = 'PACKAGE_TYPE'

    PT_ID = Column(Integer, primary_key=True, nullable=False)
    PT_NAME_DE = Column(Unicode(length=255))
    PT_NAME_EN = Column(Unicode(length=255))
    PT_REG = Column(DateTime)
    PT_REG_BY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    PC_ID = Column(Integer, ForeignKey('PACKAGE_CAT.PC_ID'))

    package_category = relationship("PackageCategory")


class PackageName(Base):
    """Name of a Package."""

    __tablename__ = "PACKAGE_NAME"

    PN_ID = Column(Integer, primary_key=True, nullable=False)
    PN_NAME_DE = Column(Unicode(length=255))
    PN_NAME_EN = Column(Unicode(length=255))
    PN_REG = Column(DateTime)
    PN_REG_BY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    PN_UPDATE = Column(DateTime)
    PN_UPDATE_BY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))


class Clearing(Base):
    """Clearing status definitions (i.e. 06-Freigegeben)."""

    __tablename__ = "CLEARING"

    CL_ID = Column(Integer, primary_key=True, nullable=False)
    CL_NAME_DE = Column(Unicode(length=100))
    CL_NAME_EN = Column(Unicode(length=100))
    CL_DESCRIPTION_DE = Column(Unicode(length=255))  # always NULL
    CL_DESCRIPTION_EN = Column(Unicode(length=255))  # always NULL
    CL_REG = Column(DateTime)
    CL_REGBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    CL_UPDATE = Column(DateTime)
    CL_UPDATEBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    TPST_ID = Column(Integer)  # not clear what this is


class PackageElementCalculation(Base):
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

    @property
    def team(self) -> TeamSublocation:
        """Return the team by ST_ID."""
        session = AdminSession.object_session(self)
        team = session.query(TeamSublocation).get(self.ST_ID)
        return cast(TeamSublocation, team)


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

    packages: Query = relationship("Package", lazy='dynamic')

    country = relationship("Country")
    product = relationship("Product")

    @property
    def lidl_phasen(self) -> List[Package]:
        """Return the LIDL phasen services."""
        # convert the name to a str since it could be None
        return [pack for pack in self.packages
                if "lidl" in str(pack.NP_NAME_DE).lower()
                and "phasen" in str(pack.NP_NAME_DE).lower()]

    # pylint: disable=too-many-locals
    def default_teams(self) -> Dict[str, int]:
        """
        Get the default teams used in the Navigation.

        Will return a dictionary with the DomainName as key and the team id
        as value.
        """
        team_counts: Dict[str, Dict[int, int]] = {
            "SAFE": defaultdict(int),
            "PERF": defaultdict(int),
            "PM": defaultdict(int)
        }

        session = Session.object_session(self)
        package_ids = [pack.NP_ID for pack in self.packages]
        pack_elements = session.query(PackageElement) \
            .filter(PackageElement.NP_ID.in_(package_ids)).all()
        default_module_ids = {pack_ele.NPE_ID: pack_ele.DM_ID
                              for pack_ele in pack_elements}
        default_modules = session.query(DefaultModule) \
            .filter(DefaultModule.DM_ID.in_(default_module_ids.values())).all()
        domain_ids = {mod.DM_ID: mod.ND_ID for mod in default_modules}
        domains = session.query(NavDomain) \
            .filter(NavDomain.ND_ID.in_(list(domain_ids.values()))).all()
        domain_names = {domain.ND_ID: domain.ND_SHORT for domain in domains}

        pack_ele_ids = [pack_ele.NPE_ID for pack_ele in pack_elements]
        calcs = session.query(PackageElementCalculation) \
            .filter(PackageElementCalculation.NPE_ID.in_(pack_ele_ids)).all()

        for calc in calcs:
            log.debug("Adding team id to dict: %s (calc: %s)", calc.ST_ID,
                      calc.NPEC_ID)
            mod_id = default_module_ids[calc.NPE_ID]
            if mod_id is None:
                log.warning("No module stored for PackageElement %s",
                            calc.NPE_ID)
                continue
            domain_id = domain_ids[mod_id]
            domain = domain_names[domain_id]
            if domain not in team_counts:
                continue
            team_counts[domain][calc.ST_ID] += 1
        teams = {
            "SAFE": -1,
            "PERF": -1,
            "PM": -1
        }
        for domain_name, counts in team_counts.items():
            try:
                team = max(counts.items(), key=operator.itemgetter(1))[0]
                log.debug("Returning team %s for domain %s", team, domain_name)
            except ValueError:
                log.debug("No teams were found for domain %s", domain_name)
                team = -1
            teams[domain_name] = team
        return teams
        # pylint: enable=too-many-locals

    def default_zara_product(self) -> str:
        """Calculate the default ZaraProduct."""
        log.debug("Calculation ZaraProduct for Navigation %s", self.N_ID)
        products: Dict[str, int] = defaultdict(int)
        for package in self.packages:
            products[package.ZM_PRODUCT] += 1

        if products["T10"] > products["T20"]:
            log.debug("ZaraProduct is T10")
            return "T10"
        log.debug("ZaraProduct is T20")
        return "T20"

    def calculations(self) -> List[PackageElementCalculation]:
        """Return all PackageElementCalculation."""
        session = Session.object_session(self)
        package_ids = [pack.NP_ID for pack in self.packages]
        pack_elements = session.query(PackageElement) \
            .filter(PackageElement.NP_ID.in_(package_ids)).all()
        pack_ele_ids = [pack_ele.NPE_ID for pack_ele in pack_elements]
        calcs = session.query(PackageElementCalculation) \
            .filter(PackageElementCalculation.NPE_ID.in_(pack_ele_ids)).all()
        return cast(List[PackageElementCalculation], calcs)


class Country(Base):
    """Countries."""

    __tablename__ = "HR_COUNTRY"

    HRC_ID = Column(Integer, primary_key=True, nullable=False)
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

    HRP_ID = Column(Integer, primary_key=True, nullable=False)
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
    SCL_ID = Column(Integer, ForeignKey('SERVICECLASS.SCL_ID'))

    package = relationship("Package", back_populates="service_classes")
    definition = relationship("ServiceClassDefinition")


class ServiceClassDefinition(Base):
    """Definitions for the service class."""

    __tablename__ = "SERVICECLASS"

    SCL_ID = Column(Integer, primary_key=True, nullable=False)
    SCL_LEVEL = Column(Integer)
    SCL_REMARK_DE = Column(Unicode(length=500))
    SCL_REMARK_EN = Column(Unicode(length=500))
    SCL_REG = Column(DateTime)
    SCL_REGBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))
    SCL_UPDATE = Column(DateTime)
    SCL_UPDATEBY = Column(Integer, ForeignKey('V_PSEX_STAFF.ST_ID'))


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


class ZaraObject(Base):
    """Zara Object table model."""

    __tablename__ = "V_PSEX_ZOBJECT"

    ZM_PRIMARY_FAKE = Column(Integer, primary_key=True)
    ZM_OBJECT = Column(Unicode(length=5))
    ZM_OBJECT_NAME = Column(Unicode(length=255))
    ZM_OBJECT_LANGUAGE = Column(Unicode(length=2))


class ZaraProduct(Base):
    """Zara Product table model."""

    __tablename__ = "V_PSEX_ZPRODUCT"

    ZM_PRIMARY_FAKE = Column(Integer, primary_key=True)
    ZM_PRODUCT = Column(Unicode(length=5))
    ZM_PROUDCT_NAME = Column(Unicode(length=255))
    ZM_PRODUCT_LANGUAGE = Column(Unicode(length=2))


# SCRIPTS
def insert_package_into_nav(nav_id: int, package_id: int, user_id: int,
                            session: Session, copy_pe: bool = True) -> int:
    """
    Insert a copy of the given package into the given navigation.

    Returns the id of the new package.

    If copy_pe is false, the PackageElements won't be copied along with the
    Package. This should be used if the PackageElements will be created
    otherwise (i.e. copied from the LIDL Phasen Service).

    Based on dbo.SP_NAV_INSERT_PACKAGE in dbo.EDOC.
    """
    log.debug("Inserting package %s into nav %s", package_id, nav_id)
    assert session.query(Navigation).get(nav_id)
    pack: Package = session.query(Package).get(package_id)
    assert pack

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
        NP_REG=datetime.now(),
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

    if copy_pe:
        for package_element in pack.package_elements:
            copy_package_element(new_pack.NP_ID, package_element, session,
                                 user_id)
    session.flush()
    return new_pack_id


def copy_package_element(new_pack_id: int, package_element: PackageElement,
                         session: Session, user_id: int) -> int:
    """Copy the PackageElement to the Package with the given id."""
    new_element = PackageElement(
        NP_ID=new_pack_id,
        DM_ID=package_element.DM_ID,
        NL_ID=package_element.NL_ID,
        ZM_LOCATION=package_element.ZM_LOCATION,
        CT_ID=package_element.CT_ID,
        NPE_CREATE=package_element.NPE_CREATE,
        NPE_CREATE_SO=package_element.NPE_CREATE_SO,
        NPE_REG=datetime.now(),
        NPE_REGBY=user_id
    )
    session.add(new_element)
    session.flush()
    for calculation in package_element.package_calculations:
        new_calc = PackageElementCalculation(
            NPE_ID=new_element.NPE_ID,
            ST_ID=calculation.ST_ID,
            NPEC_DELTA_START=calculation.NPEC_DELTA_START,
            NPEC_TIME_DAYS=calculation.NPEC_TIME_DAYS,
            NPEC_TIME_HOURS=calculation.NPEC_TIME_HOURS,
            NPEC_RATE=calculation.NPEC_RATE,
            NPEC_COSTS=calculation.NPEC_COSTS,
            NPEC_TRAVEL=calculation.NPEC_TRAVEL,
            NPEC_FACTOR=calculation.NPEC_FACTOR,
            NPEC_PRICE=calculation.NPEC_PRICE,
            NPEC_COMMENT=calculation.NPEC_COMMENT,
            NPEC_TASK=calculation.NPEC_TASK,
            ZM_ID=calculation.ZM_ID,
            NPOS_ID=calculation.NPOS_ID,
            NPEC_REG=datetime.now(),
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
            NPEP_REG=datetime.now(),
            NPEP_REGBY=user_id
        )
        session.add(new_proof)
    return new_element.NPE_ID
