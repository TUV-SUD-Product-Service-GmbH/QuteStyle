"""
Database connection and models for the PSE database.

WARNING! Delete cascades do not work properly, when delete is executed on a
query. Always use session.delete()!

INFORMATION! We are using datetime.now as default/onupdate for reg and update
columns even if datetime.utcnow would be the correct choice to mimik Navigator
behaviour.

"""
# pylint: disable=too-many-lines
from __future__ import annotations
import logging
import os
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime
from enum import IntEnum
from typing import List, Iterator, Optional, Dict, cast

from sqlalchemy import create_engine, Column, Integer, Unicode, DateTime, \
    Boolean, Float, Numeric, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session, deferred, \
    validates
from sqlalchemy.sql.schema import ForeignKey

from tsl.common_db import NullUnicode
from tsl.variables import STD_DB_PATH, ClearingState

log = logging.getLogger("tsl.edoc_database")  # pylint: disable=invalid-name

# pre pool ping will ensure, that connection is reestablished if not alive
ENGINE = create_engine(os.getenv("EDOC_DB_PATH", STD_DB_PATH.format("EDOC")),
                       pool_pre_ping=True)

Base = declarative_base()
Base.metadata.bind = ENGINE

AdminSession = sessionmaker(bind=ENGINE)  # pylint: disable=invalid-name

USER_ID: Optional[int] = None


def get_user_id() -> int:
    """Get the database id for the current user."""
    global USER_ID  # pylint: disable=global-statement
    if USER_ID is None:
        with session_scope() as session:
            username = os.getlogin()
            log.debug("Getting database id for user %s", username)
            user = session.query(Staff).filter_by(ST_WINDOWSID=username).one()
            USER_ID = user.ST_ID
    return USER_ID


# session fixture for use in with statement
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
class AppsCount(Base):
    """AppsCount table model."""

    __tablename__ = "APPS_COUNT"

    APPSC_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer)  # User Id
    APPST_ID = Column(Integer)  # App Id (as in APPS_TYPE)
    APPSC_REG = Column(DateTime)  # time of app call


class Attribute(Base):
    """Attributes of a DefaultModul."""

    __tablename__ = "ATTRIBUTES"

    ATT_ID = Column(Integer, primary_key=True)
    ATT_SHORT = Column(Unicode(length=10))
    ATT_NAME_DE = Column(Unicode(length=60))
    ATT_NAME_EN = Column(Unicode(length=60))
    reg = Column("ATT_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "ATT_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("ATT_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "ATT_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    ATT_TYPE = Column(Integer, ForeignKey("ATTRIBUTES_TYPE.ATT_TYPE"))
    ATT_IS_FILTER = Column(Boolean, nullable=False)

    attribute_type = relationship("AttributeType")

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class AttributeType(Base):
    """Type of an Attribute."""

    __tablename__ = "ATTRIBUTES_TYPE"

    ATTT_ID = Column(Integer, primary_key=True)
    ATT_TYPE = Column(Integer)
    ATTT_NAME_DE = Column(Unicode(length=100))
    ATTT_NAME_EN = Column(Unicode(length=100))
    ATTT_NAME_FR = Column(Unicode(length=100))
    ATTT_ORDER = Column(Unicode(length=10))


class CalculationType(Base):
    """Type of a calculation."""

    __tablename__ = "CALC_TYPE"

    CT_ID = Column(Integer, primary_key=True)
    CT_NAME = Column(Unicode(length=50))
    CT_ORDER = Column(Integer)
    CA_ID = Column(Integer)


class Clearing(Base):
    """Clearing status definitions (i.e. 06-Freigegeben)."""

    __tablename__ = "CLEARING"

    CL_ID = Column(Integer, primary_key=True)
    # names are never null in the database
    CL_NAME_DE = Column(Unicode(length=100), nullable=False)
    CL_NAME_EN = Column(Unicode(length=100), nullable=False)
    CL_DESCRIPTION_DE = Column(Unicode(length=255))  # always NULL
    CL_DESCRIPTION_EN = Column(Unicode(length=255))  # always NULL
    reg = Column("CL_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "CL_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("CL_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "CL_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    TPST_ID = Column(Integer)  # not clear what this is

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])

    @property
    def final_state(self) -> bool:
        """Return if the Clearing is a final state."""
        return self.CL_NAME_DE in [
            "06 - Freigegeben",
            "09 - ohne Freigabeverfahren",
            "04 - validiert (ohne Freigabe)",
            "08 – gängige Praxis (nicht validiert)",
            "10 - TCC Status"
        ]

    @property
    def final_state(self) -> ClearingState:
        """Return if the Clearing is a final state."""
        if self.CL_NAME_DE in [
            "06 - Freigegeben",
            "09 - ohne Freigabeverfahren",
            "04 - validiert (ohne Freigabe)",
            "08 – gängige Praxis (nicht validiert)",
            "10 - TCC Status"
        ]:
            return ClearingState.Final
        elif self.CL_NAME_DE == "05 - Freigabeverfahren läuft":
            return ClearingState.Intermediate
        return ClearingState.NotFinal


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
    update = Column("HRC_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "HRC_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )

    update_user = relationship("Staff", foreign_keys=[update_by])


class CustomerAddress(Base):
    """CustomerAddress table model."""

    __tablename__ = "V_PSEX_CUSTOMER_ADDRESS"

    CU_ID = Column(Integer, primary_key=True, nullable=False)
    CA_NAME = Column(Unicode(length=166), nullable=False)
    CA_STREET = Column(Unicode(length=101))
    CA_ZIPCODE = Column(Unicode(length=11))
    CA_CITY = Column(Unicode(length=41))


class CustomerContact(Base):
    """CustomerContact table model."""

    __tablename__ = "V_PSEX_CUSTOMER_CONTACT"

    CUC_ID = Column(Integer, primary_key=True, nullable=False)
    CU_ID = Column(Integer, nullable=False)  # todo: add ForeignKey
    CUC_FORENAME = Column(Unicode(length=51))
    CUC_SURNAME = Column(Unicode(length=36))
    CUC_PHONE = Column(Unicode(length=50))
    CUC_MOBILE = Column(Unicode(length=50))
    CUC_FAX = Column(Unicode(length=50))
    CUC_MAIL = Column(Unicode(length=255))
    ANRED = Column(Unicode(length=31))


class DefaultItem(Base):
    """Default item (Prüfbaustein)."""

    __tablename__ = "DEFAULT_ITEM"

    DI_ID = Column(Integer, primary_key=True)
    DI_VERSION = Column(Integer)
    DI_NAME = Column(Unicode(length=100))
    TPT_ID = Column(Integer, ForeignKey("V_PSEX_TEMPLATE_TYPE.TPT_ID"))
    TPSC_ID = Column(Integer)  # todo: link ForeignKey
    DI_REQUIREMENT_DE = Column(Unicode(length=1500))
    DI_REQUIREMENT_EN = Column(Unicode(length=1500))
    DI_REQUIREMENT_FR = Column(Unicode(length=1500))
    DI_NORM = Column(Unicode(length=512))
    PSI_ID = Column(Integer)  # todo: link ForeignKey
    DI_TIME = Column(Numeric(precision=18, scale=2))
    DI_COST = Column(Numeric(precision=18, scale=2))
    DI_TIME_MIN = Column(Numeric(precision=18, scale=2))
    DI_INFO = Column(Unicode(length=4000))
    DI_INFO_CN = Column(Unicode(length=2048))
    TP_ID = Column(Integer)  # todo: link ForeignKey
    TPER_ID = Column(Integer)  # todo: link ForeignKey
    DI_KENNWERT = Column(Unicode(length=60))
    DI_PRUEFLEVEL = Column(Unicode(length=100))
    DI_TITLE = Column(Boolean)
    DI_KEYNOTE = Column(Boolean)
    CL_ID = Column(Integer, ForeignKey("CLEARING.CL_ID"))
    DI_CLEAR_BY = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    DI_CLEAR_DATE = Column(DateTime)
    reg = Column("DI_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "DI_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("DI_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "DI_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    DI_MAINFEATURE = Column(Boolean)
    DI_ADD = Column(Boolean)
    WST_ID = Column(Integer)
    DI_DELETED = Column(Boolean)
    HRC_ID = Column(Integer, ForeignKey("HR_COUNTRY.HRC_ID"), nullable=False)
    HRP_ID = Column(Integer, ForeignKey("HR_PRODUCT.HRP_ID"), nullable=False)
    DI_IS_INFO = Column(Boolean)
    DI_SOURCE = Column(Integer)
    DI_PROCEDURE = Column(Integer)
    DI_TESTSAMPLE_DE = Column(Unicode(length=1000))
    DI_TESTSAMPLE_EN = Column(Unicode(length=1000))
    DI_TESTSAMPLE_FR = Column(Unicode(length=1000))
    REL_ID = Column(Integer)
    DI_NAME_EN = Column(Unicode(length=100))
    DI_PARENT = Column(Integer)
    DI_OLD = Column(Numeric(precision=18, scale=2))
    DI_OWNER = Column(Integer)
    ST_ID = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    NL_ID = Column(Integer, ForeignKey("NAVLEVEL.NL_ID"))
    DI_PRICE_EUR = Column(Numeric(precision=18, scale=2))
    DI_COSTITEM = Column(Unicode(length=100))
    ND_ID = Column(Integer, ForeignKey("NAVDOMAIN.ND_ID"))
    DI_NORM_ALT = Column(Unicode(length=80))
    DI_HIDE_COL1 = Column(Boolean)
    DI_INSERT_STANDARD = Column(Boolean)
    DI_TESTCODE = Column(Unicode(length=512))
    DI_SECTION = Column(Unicode(length=512))
    DI_PROTECTED = Column(Boolean)

    clearing = relationship("Clearing")
    annexes = relationship("DefaultItemAnnex", back_populates="default_item")
    pictures = relationship("DefaultItemPicture",
                            back_populates="default_item")
    template_type = relationship("TemplateType")

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])
    level = relationship("NavLevel")
    attributes: List[DefaultItemAttribute] = \
        relationship("DefaultItemAttribute", back_populates="default_item")


class DefaultItemAnnex(Base):
    """Annex for a DefaultItem."""

    __tablename__ = "DEFAULT_ITEM_ANNEX"

    DIAX_ID = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, ForeignKey("DEFAULT_ITEM.DI_ID"))
    DIAX_NAME_DE = Column(Unicode(length=500))
    DIAX_NAME_EN = Column(Unicode(length=500))
    DIAX_NAME_FR = Column(Unicode(length=500))
    DIAX_FILENAME = Column(Unicode(length=255))
    DIAX_CHECKSUM = Column(Unicode(length=32))
    DIAX_DATA = Column(LargeBinary)
    DIAX_COPY = Column(Boolean)

    default_item = relationship("DefaultItem", back_populates="annexes",
                                lazy="joined")


class DefaultItemAttribute(Base):
    """Attribute of a DefaultItem."""

    __tablename__ = "DEFAULT_ITEM_ATTRIBUTES"

    DIA_ID = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, ForeignKey("DEFAULT_ITEM.DI_ID"), nullable=False)
    ATT_ID = Column(Integer, ForeignKey("ATTRIBUTES.ATT_ID"), nullable=False)

    default_item = relationship("DefaultItem", back_populates="attributes")
    attribute = relationship("Attribute")


class DefaultItemPicture(Base):
    """Picture for a DefaultItem."""

    __tablename__ = "DEFAULT_ITEM_PICTURE"

    DIP_ID = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, ForeignKey("DEFAULT_ITEM.DI_ID"))
    DIP_NUMBER = Column(Integer)
    DIP_TEXT_DE = Column(Unicode(length=500))
    DIP_TEXT_EN = Column(Unicode(length=500))
    DIP_TEXT_FR = Column(Unicode(length=500))
    DIP_FILENAME = Column(Unicode(length=255))
    DIP_CHECKSUM = Column(Unicode(length=32))
    DIP_WIDTH = Column(Integer)
    DIP_HEIGHT = Column(Integer)
    DIP_DATA = Column(LargeBinary)

    default_item = relationship("DefaultItem", back_populates="pictures",
                                lazy="joined")


class DefaultModule(Base):
    """Default module table model."""

    __tablename__ = "DEFAULT_MODUL"

    DM_ID = Column(Integer, primary_key=True)
    DM_VERSION = Column(Integer)
    DM_ACTIVE = Column(Boolean)
    DM_NAME = Column(Unicode(length=255), nullable=False)
    DM_LETTER = Column(Unicode(length=10))
    HEAD_ID = Column(Integer, ForeignKey("HEADER.HEAD_ID"))
    TPT_ID = Column(Integer, ForeignKey("V_PSEX_TEMPLATE_TYPE.TPT_ID"))
    TPSC_ID = Column(Integer)
    DM_IS_MASTER = Column(Boolean)
    DM_COMMENT = Column(Unicode(length=500))
    CL_ID = Column(Integer, ForeignKey("CLEARING.CL_ID"))
    DM_CLEAR_BY = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    DM_CLEAR_DATE = Column(DateTime)
    reg = Column("DM_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "DM_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("DM_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "DM_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    DM_TESTBASE_DE = Column(Unicode(length=500))
    DM_TESTBASE_EN = Column(Unicode(length=500))
    DM_TESTBASE_FR = Column(Unicode(length=500))
    DM_IS_CUSTOMER = Column(Boolean)
    DM_IS_MARKETABILITY = Column(Boolean)
    DM_IS_USABILITY = Column(Boolean)
    CT_ID = Column(Integer, ForeignKey("CALC_TYPE.CT_ID"))
    DM_SCOPE_DE = Column(Unicode(length=500))
    DM_SCOPE_EN = Column(Unicode(length=500))
    DM_SCOPE_FR = Column(Unicode(length=500))
    DM_CLEAR_BY_VT = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    DM_CLEAR_DATE_VT = Column(DateTime)
    DM_CREATED_FOR = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
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
    attributes = relationship("DefaultModuleAttribute",
                              back_populates="default_module")
    header = relationship("Header")
    items: List[DefaultModuleItem]\
        = relationship("DefaultModuleItem", back_populates="default_module")

    calculations: List[DefaultModuleCalc] = \
        relationship("DefaultModuleCalc", back_populates="default_module")
    template_type = relationship("TemplateType")
    links = relationship("DefaultModuleLink", back_populates="default_module")
    test_bases = relationship("DefaultModuleTestBase")

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])
    clearing = relationship("Clearing")


class DefaultModuleAttribute(Base):
    """Attribute of a DefaultModule."""

    __tablename__ = "DEFAULT_MODUL_ATTRIBUTES"

    DMA_ID = Column(Integer, primary_key=True)
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"), nullable=False)
    ATT_ID = Column(Integer, ForeignKey("ATTRIBUTES.ATT_ID"), nullable=False)

    default_module = relationship("DefaultModule", back_populates="attributes")
    attribute = relationship("Attribute")


class DefaultModuleTestBase(Base):
    """TestBase for a DefaultModule."""

    __tablename__ = "DEFAULT_MODUL_BASE"

    DMB_ID = Column(Integer, primary_key=True)
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"), nullable=False)
    B_ID = Column(Integer, ForeignKey("BASE.B_ID"), nullable=False)
    DMB_TYPE = Column(Integer, ForeignKey("BASE_TYPE.BT_ID"), nullable=False)

    test_base_type = relationship("TestBaseType")
    test_base = relationship("TestBase")
    default_module = relationship("DefaultModule", back_populates="test_bases")


class DefaultModuleCalc(Base):
    """Calculation for a DefaultModule."""

    __tablename__ = "DEFAULT_MODUL_CALC"

    DMC_ID = Column(Integer, primary_key=True)
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"))
    WST_ID = Column(Integer)  # todo: add foreign key
    DMC_TASK = Column(Unicode(length=500))
    DMC_TIME_HOURS = Column(Float, nullable=False)
    DMC_TIME_DAYS = Column(Float)
    DMC_COSTS = Column(Numeric(precision=18, scale=2))
    DMC_TRAVEL = Column(Numeric(precision=18, scale=2))
    DMC_COMMENT = Column(Unicode(length=500))
    ST_ID = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    DMC_COSTS_EXTERNAL = Column(Numeric(precision=18, scale=2))

    default_module = relationship("DefaultModule",
                                  back_populates="calculations")
    team = relationship("Staff")


class DefaultModuleItem(Base):
    """DefaultModuleItem (Link between DefaultModule and DefaultItem)."""

    __tablename__ = "DEFAULT_MODUL_ITEM"

    DMI_ID = Column(Integer, primary_key=True)
    # keys of DefaultItem and DefaultModule are nullable in database,
    # but the item isn't useful without
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"), nullable=False)
    DI_ID = Column(Integer, ForeignKey("DEFAULT_ITEM.DI_ID"), nullable=False)
    DMI_NUMBER = Column(Integer)
    # nullable in DB, but never NULL and also useless when NULL
    DMI_INDENT = Column(Integer, nullable=False)
    DMI_KENNWERT = Column(Unicode(length=255))
    DMI_PRUEFLEVEL = Column(Unicode(length=100))
    DMI_TITLE = Column(Boolean)
    reg = Column("DMI_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "DMI_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("DMI_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "DMI_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    WST_ID = Column(Integer)  # todo: Check if ForeignKey
    ST_ID = Column(Integer)  # todo: Check if Team of User
    DMI_FACTOR = Column(Numeric(precision=18, scale=2))
    DMI_PRICE = Column(Numeric(precision=18, scale=2))

    default_module = relationship("DefaultModule", back_populates="items")
    default_item = relationship("DefaultItem")

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class DefaultModuleLink(Base):
    """Link of a DefaultModule."""

    __tablename__ = "DEFAULT_MODUL_LINK"

    DML_ID = Column(Integer, primary_key=True)
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"))
    # the next four columns can never be NULL from eDOC
    DML_TEXT_DE = Column(Unicode(length=1024), nullable=False)
    DML_TEXT_EN = Column(Unicode(length=1024), nullable=False)
    DML_TEXT_FR = Column(Unicode(length=1024), nullable=False)
    DML_URL = Column(Unicode(length=512), nullable=False)
    update = Column("DML_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "DML_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )

    default_module = relationship("DefaultModule", back_populates="links")

    update_user = relationship("Staff", foreign_keys=[update_by])


class Edoc(Base):
    """eDOC model."""

    __tablename__ = "EDOC"

    E_ID = Column(Integer, primary_key=True)
    E_VERSION = Column(Integer, default=1)
    # E_NAME is nullable in database, but never actually NULL
    E_NAME = Column(Unicode(length=255), nullable=False)
    # default header is "Modulvorlage Standard" from HEADER table
    HEAD_ID = Column(Integer, ForeignKey("HEADER.HEAD_ID"), default=1)
    E_YN_SYMBOL = Column(Boolean, default=True)
    reg = Column("E_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "E_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("E_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "E_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    NP_ID = Column(Integer, ForeignKey("NAV_PACK.NP_ID"))

    package = relationship("Package")
    header = relationship("Header")
    phases: List["EdocPhase"] = relationship("EdocPhase",
                                             back_populates="edoc")
    modules: List["EdocModule"] = relationship("EdocModule",
                                               back_populates="edoc",
                                               order_by="EdocModule.EM_NUMBER")

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])
    items = relationship("EdocModuleItem", back_populates="edoc")


class EdocModuleItem(Base):
    """ModulItem in an eDOC protocol (Prüfbaustein)."""

    __tablename__ = "EDOC_MODUL_ITEM"

    EMI_ID = Column(Integer, primary_key=True)
    EMI_VERSION = Column(Integer)
    EMI_NUMBER = Column(Integer)
    E_ID = Column(Integer, ForeignKey("EDOC.E_ID"))
    EM_ID = Column(Integer, ForeignKey("EDOC_MODUL.EM_ID"))
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"))
    DI_ID = Column(Integer, ForeignKey("DEFAULT_ITEM.DI_ID"))
    DI_VERSION = Column(Integer)
    EMI_REQUIREMENT_DE = Column(NullUnicode(length=1500))
    EMI_REQUIREMENT_EN = Column(NullUnicode(length=1500))
    EMI_REQUIREMENT_FR = Column(NullUnicode(length=1500))
    # column is nullable in db, but actually never is. there are 6 items
    # without indent, but they are from 2009/2010
    EMI_INDENT = Column(Integer, nullable=False)
    WST_ID = Column(Integer)  # todo: add ForeignKey
    EMI_NORM = Column(Unicode(length=80))
    PSI_ID = Column(Integer)
    EMI_TIME = Column(Numeric(precision=18, scale=0))
    EMI_COST = Column(Numeric(precision=18, scale=2))
    EMI_TIME_MIN = Column(Numeric(precision=18, scale=2))
    TPER_ID = Column(Integer)
    EMI_KENNWERT = Column(Unicode(length=60))
    EMI_TITLE = Column(Boolean)
    EMI_KEYNOTE = Column(Boolean)
    EMI_MEASURE = Column(Boolean)
    EMI_ADD = Column(Boolean)
    reg = Column("EMI_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "EMI_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("EMI_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "EMI_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    EMI_MAINFEATURE = Column(Boolean)
    ST_ID = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    NL_ID = Column(Integer, ForeignKey("NAVLEVEL.NL_ID"))

    edoc = relationship("Edoc", back_populates="items")
    edoc_module = relationship("EdocModule", back_populates="items")
    default_module = relationship("DefaultModule")
    default_item = relationship("DefaultItem")
    nav_level = relationship("NavLevel")
    phase_results = relationship("EdocModuleItemPhase",
                                 back_populates="edoc_module_item")

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class EdocModuleItemComparison(Base):
    """Comparison table for EdocModuleItems."""

    __tablename__ = "EDOC_MODUL_ITEM_COMPARISON"

    EMIC_ID = Column(Integer, primary_key=True)
    EMI_ID = Column(Integer, ForeignKey("EDOC_MODUL_ITEM.EMI_ID"))
    EM_ID = Column(Integer, ForeignKey("EDOC_MODUL.EM_ID"))
    EMIC_ORDER = Column(Integer)
    EMIC_TEXT_DE = Column(Unicode(length=500))
    EMIC_TEXT_EN = Column(Unicode(length=500))
    EMIC_TEXT_FR = Column(Unicode(length=500))
    reg = Column("EMIC_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "EMIC_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("EMIC_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "EMIC_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class EdocModuleItemComparisonPhase(Base):
    """Comparison table for EdocModuleItems."""

    __tablename__ = "EDOC_MODUL_ITEM_COMPARISON_PHASE"

    EMICP_ID = Column(Integer, primary_key=True)
    EMIC_ID = Column(Integer, ForeignKey("EDOC_MODUL_ITEM_COMPARISON.EMIC_ID"))
    EMI_ID = Column(Integer, ForeignKey("EDOC_MODUL_ITEM.EMI_ID"))
    EM_ID = Column(Integer, ForeignKey("EDOC_MODUL.EM_ID"))
    PRP_ID = Column(Integer, ForeignKey("V_PSEX_PROCESSPHASE.PRP_ID"),
                    default=1)
    EMICP_TEXT_DE = Column(Unicode(length=500))
    EMICP_TEXT_EN = Column(Unicode(length=500))
    EMICP_TEXT_FR = Column(Unicode(length=500))
    ER_ID = Column(Integer, ForeignKey("EDOCRESULT.ER_ID"), default=1)
    update = Column("ER_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "ER_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )

    update_user = relationship("Staff", foreign_keys=[update_by])


class EdocModuleItemPhase(Base):
    """Phase result for an EdocModulItem."""

    __tablename__ = "EDOC_MODUL_ITEM_PHASE"

    EMIP_ID = Column(Integer, primary_key=True)
    EM_ID = Column(Integer, ForeignKey("EDOC_MODUL.EM_ID"))
    EMI_ID = Column(Integer, ForeignKey("EDOC_MODUL_ITEM.EMI_ID"))
    PRP_ID = Column(Integer, ForeignKey("V_PSEX_PROCESSPHASE.PRP_ID"))
    EMIP_RESULT_DE = Column(Unicode(length=2048), default="")
    EMIP_RESULT_EN = Column(Unicode(length=2048), default="")
    EMIP_RESULT_FR = Column(Unicode(length=2048), default="")
    EMIP_COMMENT = Column(Unicode(length=500), default="")
    EMIP_READY = Column(Boolean, default=False)
    ER_ID = Column(Integer, ForeignKey("EDOCRESULT.ER_ID"), default=1)
    EMIP_HANDLEDBY = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    EMIP_HINT = Column(Boolean, default=False)
    reg = Column("EMIP_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "EMIP_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("EMIP_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "EMIP_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    WST_ID = Column(Integer)  # todo: add ForeignKey
    SO_NUMBER = Column(Integer)
    ST_ID = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"), default=1)
    EMIP_IS_COPY = Column(Boolean, nullable=False, default=False)

    edoc_module = relationship("EdocModule")
    edoc_module_item = relationship("EdocModuleItem",
                                    back_populates="phase_results")
    phase = relationship("ProcessPhase")
    handleby = relationship("Staff", foreign_keys=[EMIP_HANDLEDBY])
    result = relationship("EdocResult")
    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class EdocModuleItemPhaseAnnex(Base):
    """Module for an annex of an eDOC phase."""

    __tablename__ = "EDOC_MODUL_ITEM_PHASE_ANNEX"

    EMIPA_ID = Column(Integer, primary_key=True)
    EMIP_ID = Column(Integer, ForeignKey("EDOC_MODUL_ITEM_PHASE.EMIP_ID"))
    EMIPA_NAME_DE = Column(Unicode(length=500))
    EMIPA_NAME_EN = Column(Unicode(length=500))
    EMIPA_NAME_FR = Column(Unicode(length=500))
    EMIPA_FILENAME = Column(Unicode(length=255))
    EMIPA_CHECKSUM = Column(Unicode(length=32))
    EMIPA_DATA = Column(LargeBinary)
    reg = Column("EMIPA_UPLOAD", DateTime, onupdate=datetime.now)
    reg_by = Column(
        "EMIPA_UPLOAD_BY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )

    edoc_module_item_phase = relationship("EdocModuleItemPhase")

    reg_user = relationship("Staff", foreign_keys=[reg_by])


class EdocModuleItemPicture(Base):
    """Picture for an EdocModuleItem."""

    __tablename__ = "EDOC_MODUL_ITEM_PICTURE"

    EMIPC_ID = Column(Integer, primary_key=True)
    EMI_ID = Column(Integer, ForeignKey("EDOC_MODUL_ITEM.EMI_ID"))
    EM_ID = Column(Integer, ForeignKey("EDOC_MODUL.EM_ID"))
    EMIPC_NUMBER = Column(Integer)
    EMIPC_TEXT_DE = Column(Unicode(length=500))
    EMIPC_TEXT_EN = Column(Unicode(length=500))
    EMIPC_TEXT_FR = Column(Unicode(length=500))
    EMIPC_FILENAME = Column(Unicode(length=255))
    EMIPC_CHECKSUM = Column(Unicode(length=32))
    EMIPC_WIDTH = Column(Integer)
    EMIPC_HEIGHT = Column(Integer)
    EMIPC_DATA = deferred(Column(LargeBinary))

    edoc_module_item = relationship("EdocModuleItem")
    edoc_module = relationship("EdocModule")


class EdocModulePhase(Base):
    """Phase for an EdocModule."""

    __tablename__ = "EDOC_MODUL_PHASE"

    EMP_ID = Column(Integer, primary_key=True)
    E_ID = Column(Integer, ForeignKey("EDOC.E_ID"))
    EM_ID = Column(Integer, ForeignKey("EDOC_MODUL.EM_ID"))
    # PRP_ID can't be null as this will surely break eDOC, it's nullable in
    # the DB tough
    PRP_ID = Column(Integer, ForeignKey("V_PSEX_PROCESSPHASE.PRP_ID"),
                    nullable=False)
    EMP_SUMMARY_DE = Column(Unicode)
    EMP_SUMMARY_EN = Column(Unicode)
    EMP_SUMMARY_FR = Column(Unicode)
    EMP_COMMENT_DE = Column(Unicode(length=4000))
    EMP_COMMENT_EN = Column(Unicode(length=4000))
    EMP_COMMENT_FR = Column(Unicode(length=4000))
    ER_ID = Column(Integer, ForeignKey("EDOCRESULT.ER_ID"))
    EMP_VALUE = Column(Numeric(precision=18, scale=3))
    SO_NUMBER = Column(Integer)
    EMP_WITH_ADD = Column(Boolean)

    edoc_module = relationship("EdocModule", back_populates="phases")


class EdocModule(Base):
    """Module table model."""

    __tablename__ = "EDOC_MODUL"

    EM_ID = Column(Integer, primary_key=True)
    E_ID = Column(Integer, ForeignKey("EDOC.E_ID"))
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"))
    DM_VERSION = Column(Integer)
    # there is no module in the db that is NULL, name can be empty tough
    EM_NAME = Column(Unicode(length=255), nullable=False)
    EM_LETTER = Column(Unicode(length=10))
    EM_NUMBER = Column(Integer)
    SO_NUMBER = Column(Integer)
    EM_OFFLINE_BY = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    EM_OFFLINE_SINCE = Column(DateTime)
    reg = Column("EM_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "EM_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("EM_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "EM_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    EM_FILTER_LEVEL = Column(Unicode(length=100))
    EM_FILTER_PARAM = Column(Unicode(length=512))
    EM_FILTER_ITEMS = Column(Unicode(length=2048))

    edoc = relationship("Edoc", back_populates="modules")
    default_module = relationship("DefaultModule")
    offline_by = relationship("Staff", foreign_keys=[EM_OFFLINE_BY])
    phases: List[EdocModulePhase] = relationship("EdocModulePhase",
                                                 back_populates="edoc_module")
    items = relationship("EdocModuleItem", back_populates="edoc_module")

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])

    @validates('EM_NAME', 'EM_LETTER', "EM_FILTER_LEVEL",  # type: ignore
               "EM_FILTER_PARAM", "EM_FILTER_ITEMS")
    def validate_str(self, key: str, value: str) -> str:
        """Validate and if necessary truncate a str value."""
        max_len = getattr(self.__class__, key).prop.columns[0].type.length
        if value and len(value) > max_len:
            log.warning("Truncating string by %s characters: %s",
                        len(value) - max_len, value)
            return value[:max_len]
        return value


class EdocPhase(Base):
    """eDOC phase model."""

    __tablename__ = "EDOC_PHASE"

    EP_ID = Column(Integer, primary_key=True)
    E_ID = Column(Integer, ForeignKey("EDOC.E_ID"))
    PRP_ID = Column(Integer, ForeignKey("V_PSEX_PROCESSPHASE.PRP_ID"),
                    default=1)
    P_ID = Column(Integer, ForeignKey("V_PSEX_PROJECT.P_ID"))
    SO_NUMBER = Column(Integer, nullable=False, default=0)
    EP_TEXT_DE = Column(Unicode(length=500), default="")
    EP_TEXT_EN = Column(Unicode(length=500), default="")
    EP_TEXT_FR = Column(Unicode(length=500), default="")
    ER_ID = Column(Integer, ForeignKey("EDOCRESULT.ER_ID"), default=1)
    EP_PHASE_ORDER = Column(Integer, default=1)
    EP_SAP = Column(Unicode(length=20), default="")
    EP_CUSTOMER_RESULT = Column(Integer)
    EP_CUSTOMER_VALUE = Column(Numeric(precision=18, scale=3))
    EP_CUSTOMER_COMMENT_DE = Column(Unicode)
    EP_CUSTOMER_COMMENT_EN = Column(Unicode)
    EP_CUSTOMER_COMMENT_FR = Column(Unicode)
    EP_MARKETABILITY_RESULT = Column(Integer, ForeignKey("EDOCRESULT.ER_ID"))
    EP_MARKETABILITY_VALUE = Column(Numeric(precision=18, scale=3))
    EP_MARKETABILITY_COMMENT_DE = Column(Unicode)
    EP_MARKETABILITY_COMMENT_EN = Column(Unicode)
    EP_MARKETABILITY_COMMENT_FR = Column(Unicode)
    EP_USABILITY_RESULT = Column(Integer, ForeignKey("EDOCRESULT.ER_ID"))
    EP_USABILITY_VALUE = Column(Numeric(precision=18, scale=3))
    EP_USABILITY_COMMENT_DE = Column(Unicode)
    EP_USABILITY_COMMENT_EN = Column(Unicode)
    EP_USABILITY_COMMENT_FR = Column(Unicode)
    EP_PHASEALIAS = Column(Unicode(length=100))

    edoc = relationship("Edoc", back_populates="phases")
    project = relationship("Project")
    result = relationship("EdocResult", foreign_keys=[ER_ID])
    usability_result = relationship("EdocResult",
                                    foreign_keys=[EP_USABILITY_RESULT])
    marketability_result = relationship("EdocResult",
                                        foreign_keys=[EP_MARKETABILITY_RESULT])
    process_phase = relationship("ProcessPhase")


class EdocResult(Base):
    """EdocResult model."""

    __tablename__ = "EDOCRESULT"

    ER_ID = Column(Integer, primary_key=True)
    ER_NAME_DE = Column(Unicode(length=50))
    ER_NAME_EN = Column(Unicode(length=50))
    ER_NAME_FR = Column(Unicode(length=50))
    ER_SYMBOL_1 = Column(Unicode(length=5))
    ER_SYMBOL_2 = Column(Unicode(length=5))
    ER_IS_NUMERIC = Column(Boolean)
    ER_VALUE = Column(Numeric(precision=18, scale=2))
    ER_TOOLTIP_DE = Column(Unicode(length=255))
    ER_TOOLTIP_EN = Column(Unicode(length=255))
    ER_TOOLTIP_FR = Column(Unicode(length=255))
    ER_DESCRIPTION_DE = Column(Unicode(length=255))
    ER_DESCRIPTION_EN = Column(Unicode(length=255))
    ER_DESCRIPTION_FR = Column(Unicode(length=255))
    ER_IS_MODULRESULT = Column(Integer)
    reg = Column("ER_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "ER_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("ER_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "ER_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    ER_SHOW_IN_PROOF = Column(Boolean)

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class Header(Base):
    """Header for a Module."""

    __tablename__ = "HEADER"

    HEAD_ID = Column(Integer, primary_key=True)
    HEAD_ACTIVE = Column(Boolean)
    HEAD_FILENAME = Column(Unicode(length=255))
    HEAD_NAME = Column(Unicode(length=120))
    HEAD_DATA = deferred(Column(LargeBinary))
    reg = Column("HEAD_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "HEAD_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("HEAD_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "HEAD_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    HEAD_DEFAULT_PROTOCOL = Column(Boolean)
    HEAD_DEFAULT_REPORT = Column(Boolean)
    HEAD_NAME_EN = Column(Unicode(length=120))

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class KindOfTest(Base):
    """Kind of test."""

    __tablename__ = "V_PSEX_KIND_OF_TEST"

    KOT_ID = Column(Integer, primary_key=True)
    KOT_NAME_DE = Column(Unicode(length=256))
    KOT_NAME_EN = Column(Unicode(length=256))
    KOT_NAME_FR = Column(Unicode(length=256))
    WORKING_CLUSTER = Column(Unicode(length=36))
    HR_SHORT = Column(Unicode(length=20))


class ModulParameter(Base):
    """ModuleParameter."""

    __tablename__ = "MODULE_PARAMETER"

    MP_ID = Column(Integer, primary_key=True)
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"))
    MP_PARAMETER_DE = Column(Unicode(length=256))
    MP_PARAMETER_EN = Column(Unicode(length=256))
    reg = Column("MP_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "MP_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("MP_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "MP_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class NavCountModuleExport(Base):
    """Count for module exports."""

    __tablename__ = "NAV_COUNT_MODULEEXPORT"

    NCM_ID = Column(Integer, primary_key=True)
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"))
    NCM_TYPE = Column(Integer)
    reg = Column("NCM_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "NCM_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )

    default_module = relationship("DefaultModule")

    reg_user = relationship("Staff", foreign_keys=[reg_by])


class NavDomain(Base):
    """Domain of a Navigation/Module."""

    __tablename__ = "NAVDOMAIN"

    ND_ID = Column(Integer, primary_key=True)
    # names are never null in the database
    ND_SHORT = Column(Unicode(length=10), nullable=False)
    ND_NAME_DE = Column(Unicode(length=100), nullable=False)
    ND_NAME_EN = Column(Unicode(length=100), nullable=False)
    reg = Column("ND_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "ND_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    ND_ORDER = Column(Integer)
    ND_ORDER_EXPORT = Column(Integer, nullable=False)
    ND_ORDER_PLAN_DEFAULT = Column(Integer, nullable=False)

    reg_user = relationship("Staff", foreign_keys=[reg_by])


class Navigation(Base):
    """Navigation table model."""

    __tablename__ = "NAV"

    N_ID = Column(Integer, primary_key=True)
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
    KOT_ID = Column(Integer, ForeignKey("V_PSEX_KIND_OF_TEST.KOT_ID"),
                    nullable=False)
    reg = Column("N_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "N_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("N_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "N_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )

    packages: List["Package"] = relationship("Package",
                                             back_populates="navigation")

    country = relationship("Country")
    product = relationship("Product")
    kind_of_test = relationship("KindOfTest")

    nav_saves = relationship("NavSave", back_populates="navigation")

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])

    @property
    def lidl_phasen(self) -> List['Package']:
        """Return the LIDL phasen services."""
        # convert the name to a str since it could be None
        return [pack for pack in cast(List[Package], self.packages)
                if "lidl" in str(pack.NP_NAME_DE).lower()
                and "phasen" in str(pack.NP_NAME_DE).lower()]

    def default_zara_product(self) -> str:
        """Calculate the default ZaraProduct."""
        log.debug("Calculation ZaraProduct for Navigation %s", self.N_ID)
        products: Dict[str, int] = defaultdict(int)
        for package in cast(List[Package], self.packages):
            assert package.ZM_PRODUCT
            products[package.ZM_PRODUCT] += 1

        if products["T10"] > products["T20"]:
            log.debug("ZaraProduct is T10")
            return "T10"
        log.debug("ZaraProduct is T20")
        return "T20"

    def calculations(self) -> List['PackageElementCalculation']:
        """Return all PackageElementCalculation."""
        calcs = Session.object_session(self).query(
            PackageElementCalculation
        ).join(
            PackageElement
        ).join(
            Package
        ).filter(
            Package.N_ID == self.N_ID
        ).all()
        return cast(List[PackageElementCalculation], calcs)


class NavEdoc(Base):
    """Edoc template model."""

    __tablename__ = "NAV_EDOC"

    NE_ID = Column(Integer, primary_key=True)
    NE_NAME = Column(Unicode(length=255), nullable=False)
    HEAD_ID = Column(Integer, ForeignKey("HEADER.HEAD_ID"), default=1)
    NE_RANDOM = Column(Integer, nullable=False)
    ST_ID = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"), nullable=False,
                   default=get_user_id)
    P_ID = Column(Integer, ForeignKey("V_PSEX_PROJECT.P_ID"))


class NavEdocModule(Base):
    """EdocModule template model."""

    __tablename__ = "NAV_EDOC_MODULE"

    NEM_ID = Column(Integer, primary_key=True)
    NE_RANDOM = Column(Integer, nullable=False)
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"), nullable=False)
    ST_ID = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"), nullable=False,
                   default=1)
    NE_NUMBER = Column(Integer)


class NavEdocModuleItem(Base):
    """EdocModuleItem template model."""

    __tablename__ = "NAV_EDOC_MODULE_ITEM"

    NEMI_ID = Column(Integer, primary_key=True)
    NE_RANDOM = Column(Integer, nullable=False)
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"), nullable=False)
    DI_ID = Column(Integer, ForeignKey("DEFAULT_ITEM.DI_ID"), nullable=False)
    NEMI_INDENT = Column(Integer, nullable=False, default=0)
    DMI_ID = Column(Integer, ForeignKey("DEFAULT_MODUL_ITEM.DMI_ID"),
                    nullable=False)
    NE_NUMBER = Column(Integer)


class NavLevel(Base):
    """Level of a PackageElement."""

    __tablename__ = "NAVLEVEL"

    NL_ID = Column(Integer, primary_key=True)
    NL_LEVEL = Column(Integer, unique=True, nullable=False)
    NL_NAME_DE = Column(Unicode(length=30), nullable=False)
    NL_NAME_EN = Column(Unicode(length=30), nullable=False)


class NavPosition(Base):
    """NavPosition (Rechnungsposition)."""

    __tablename__ = "NAVPOSITION"

    NPOS_ID = Column(Integer, primary_key=True)
    NPOS_POSITION = Column(Integer)
    NPOS_TEXT_DE = Column(Unicode(length=2048))
    NPOS_TEXT_EN = Column(Unicode(length=2048))
    reg = Column("EMIPAOS_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "EMIPAOS_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("EMIPAOS_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "EMIPAOS_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class NavSave(Base):
    """Navigation Save model (called Auswahl in Navigator)."""

    __tablename__ = "NAV_SAVE"

    NS_ID = Column(Integer, primary_key=True)
    NS_COMMENT = Column(Unicode(length=512))
    N_ID = Column(Integer, ForeignKey("NAV.N_ID", ondelete="CASCADE"))
    P_ID = Column(Integer, ForeignKey("V_PSEX_PROJECT.P_ID"))
    E_ID = Column(Integer, ForeignKey("EDOC.E_ID"))
    # the names could be null, but are never in the db.
    NS_NAME_DE = Column(Unicode(length=256), nullable=False)
    NS_NAME_EN = Column(Unicode(length=256), nullable=False)
    NS_CRM = Column(Unicode(length=256))
    NS_TYPE = Column(Integer, nullable=False)
    reg = Column("NS_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "NS_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )

    navigation = relationship("Navigation", back_populates="nav_saves")
    reg_user = relationship("Staff", foreign_keys=[reg_by])
    project = relationship("Project")

    save_calculations = relationship("NavSaveCalculation",
                                     back_populates="nav_save")
    selections: List[NavSaveSelection] = \
        relationship("NavSaveSelection", back_populates="nav_save")

    @property
    def nav_save_type(self) -> 'NavSaveType':
        """Return the NavSaveType for the NavSave object."""
        return NavSaveType(self.NS_TYPE)

    @nav_save_type.setter
    def nav_save_type(self, value: 'NavSaveType') -> None:
        """Set the NavSaveType for the NavSave object."""
        self.NS_TYPE = value.value  # pylint: disable=invalid-name


class NavSaveCalculation(Base):
    """Calculation data for a NavSave."""

    __tablename__ = "NAV_SAVE_CALC"

    NSC_ID = Column(Integer, primary_key=True)
    NS_ID = Column(Integer, ForeignKey("NAV_SAVE.NS_ID", ondelete="CASCADE"))
    NPEC_ID = Column(Integer, ForeignKey("NAV_PACK_ELEMENT_CALC.NPEC_ID"))
    NSC_TIME_HOURS = Column(Float)
    NSC_TIME_DAYS = Column(Integer)
    NSC_DELTA_START = Column(Float)
    NSC_COSTS = Column(Numeric(precision=18, scale=2))
    NSC_TASK = Column(Unicode(length=500))
    NSC_COMMENT = Column(Unicode(length=500))
    NSC_RATE = Column(Numeric(precision=18, scale=2))
    NSC_PRICE = Column(Numeric(precision=18, scale=2))
    NSC_FACTOR = Column(Float)
    NSC_TRAVEL = Column(Numeric(precision=18, scale=2))
    NPOS_ID = Column(Integer, ForeignKey("NAVPOSITION.NPOS_ID"))
    ZM_ID = Column(Unicode(length=50))
    ST_ID = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"), nullable=False)
    NSC_COSTS_EXTERNAL = Column(Numeric(precision=18, scale=2))

    nav_save = relationship("NavSave", back_populates="save_calculations")
    calculation = relationship("PackageElementCalculation")
    user = relationship("Staff")
    nav_position = relationship("NavPosition")


class NavSaveSelection(Base):
    """Selection for a NavSave."""

    __tablename__ = "NAV_SAVE_SELECTION"

    NSS_ID = Column(Integer, primary_key=True)
    NS_ID = Column(Integer, ForeignKey("NAV_SAVE.NS_ID"))
    NP_ID = Column(Integer, ForeignKey("NAV_PACK.NP_ID"))

    nav_save = relationship("NavSave", back_populates="selections")
    package = relationship("Package")


class NavSaveType(IntEnum):
    """Values for the different NavSaveTypes."""

    Manual = 1
    Project = 2
    Offer = 3
    Opportunity = 4


class Package(Base):
    """Package table model."""

    __tablename__ = "NAV_PACK"

    NP_ID = Column(Integer, primary_key=True)
    N_ID = Column(Integer, ForeignKey("NAV.N_ID", ondelete="CASCADE"))
    NP_NAME_DE = Column(NullUnicode(length=150), nullable=False)
    NP_NAME_EN = Column(Unicode(length=150))
    NP_COMMENT_DE = Column(Unicode(length=800))
    NP_COMMENT_EN = Column(Unicode(length=800))
    CL_ID = Column(Integer, ForeignKey("CLEARING.CL_ID"), nullable=False)
    NP_CLEARDATE = Column(DateTime)
    NP_CLEARBY = Column(Integer)
    ZM_PRODUCT = Column(Unicode(length=5))
    PT_ID = Column(Integer, ForeignKey("PACKAGE_TYPE.PT_ID"), nullable=False)
    NP_TESTSAMPLES = Column(Integer, nullable=False)
    NP_IS_TEMPLATE = Column(Boolean, nullable=False)
    NP_TEMPLATE_ID = Column(Integer)
    reg = Column("NP_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "NP_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("NP_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "NP_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    PN_ID = Column(Integer, ForeignKey("PACKAGE_NAME.PN_ID"), nullable=False)

    clearing_state = relationship("Clearing")

    package_elements: List["PackageElement"] = \
        relationship("PackageElement", back_populates="package",
                     cascade="all, delete")

    navigation = relationship("Navigation", back_populates="packages")

    service_classes: List["ServiceClass"] = \
        relationship("ServiceClass", back_populates="package",
                     cascade="all, delete")

    package_type = relationship("PackageType")

    package_name = relationship("PackageName")

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class PackageCategory(Base):
    """Category of a Package (linked to the type)."""

    __tablename__ = "PACKAGE_CAT"

    PC_ID = Column(Integer, primary_key=True)
    PC_NAME_DE = Column(Unicode(length=50))
    PC_NAME_EN = Column(Unicode(length=50))
    reg = Column("PC_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "PC_REG_BY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )

    reg_user = relationship("Staff", foreign_keys=[reg_by])


class PackageElement(Base):
    """Package element table model."""

    __tablename__ = "NAV_PACK_ELEMENT"

    NPE_ID = Column(Integer, primary_key=True)
    NP_ID = Column(Integer, ForeignKey("NAV_PACK.NP_ID", ondelete="CASCADE"))
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"))
    NL_ID = Column(Integer, ForeignKey("NAVLEVEL.NL_ID"))
    ZM_LOCATION = Column(Unicode(length=5))
    NPE_CREATE = Column(Boolean)
    CT_ID = Column(Integer, ForeignKey("CALC_TYPE.CT_ID"))
    reg = Column("NPE_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "NPE_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("NPE_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "NPE_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    NPE_CREATE_SO = Column(Boolean, nullable=False)

    package = relationship("Package", back_populates="package_elements")
    package_calculations: List["PackageElementCalculation"]\
        = relationship("PackageElementCalculation",
                       back_populates="package_element",
                       cascade="all, delete")
    proof_elements = relationship("ProofElement", cascade="all, delete",
                                  back_populates="package_element")

    default_module = relationship("DefaultModule")

    level = relationship("NavLevel")
    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])
    filters: List[PackageElementFilter] =\
        relationship("PackageElementFilter", back_populates="package_element")


class PackageElementCalculation(Base):
    """Calculation data for a PackageElement."""

    __tablename__ = "NAV_PACK_ELEMENT_CALC"

    NPEC_ID = Column(Integer, primary_key=True)
    NPE_ID = Column(Integer, ForeignKey("NAV_PACK_ELEMENT.NPE_ID",
                                        ondelete="CASCADE"))
    ST_ID = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
                   nullable=False)
    NPEC_DELTA_START = Column(Float)
    NPEC_TIME_DAYS = Column(Integer)
    NPEC_TIME_HOURS = Column(Float, nullable=False, default=0.0)
    NPEC_RATE = Column(Numeric(precision=18, scale=2))
    NPEC_COSTS = Column(Numeric(precision=18, scale=2))
    NPEC_TRAVEL = Column(Numeric(precision=18, scale=2),)
    NPEC_FACTOR = Column(Float)
    NPEC_PRICE = Column(Numeric(precision=18, scale=2))
    NPEC_COMMENT = Column(Unicode(length=500))
    NPEC_TASK = Column(NullUnicode(length=500))
    ZM_ID = Column(Unicode(length=50))
    NPOS_ID = Column(Integer, ForeignKey("NAVPOSITION.NPOS_ID"))
    reg = Column("NPEC_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "NPEC_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("NPEC_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "NPEC_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    CBC_ID = Column(Integer)
    NPEC_COSTS_EXTERNAL = Column(Numeric(precision=18, scale=2))
    NPEC_COSTS_OLD = Column(Numeric(precision=18, scale=2))
    NPEC_COSTS_EXTERNAL_OLD = Column(Numeric(precision=18, scale=2))

    package_element = relationship("PackageElement",
                                   back_populates="package_calculations")

    nav_position = relationship("NavPosition")

    team = relationship("Staff", foreign_keys=[ST_ID])
    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class PackageElementFilter(Base):
    """Filter for a PackageElement."""

    __tablename__ = "NAV_PACK_ELEMENT_FILTER"

    NPEF_ID = Column(Integer, primary_key=True)
    NPE_ID = Column(Integer, ForeignKey("NAV_PACK_ELEMENT.NPE_ID"),
                    nullable=False)
    DMI_ID = Column(Integer, ForeignKey("DEFAULT_MODUL_ITEM.DMI_ID"),
                    nullable=False)
    reg = Column("NPEF_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "NPEF_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )

    reg_user = relationship("Staff", foreign_keys=[reg_by])

    package_element = relationship("PackageElement", back_populates="filters")
    default_module_item = relationship("DefaultModuleItem")


class PackageName(Base):
    """Name of a Package."""

    __tablename__ = "PACKAGE_NAME"

    PN_ID = Column(Integer, primary_key=True)
    PN_NAME_DE = Column(Unicode(length=255))
    PN_NAME_EN = Column(Unicode(length=255))
    reg = Column("PN_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "PN_REG_BY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("PN_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "PN_UPDATE_BY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class PackageType(Base):
    """Type of a Package."""

    __tablename__ = "PACKAGE_TYPE"

    PT_ID = Column(Integer, primary_key=True)
    PT_NAME_DE = Column(Unicode(length=255))
    PT_NAME_EN = Column(Unicode(length=255))
    reg = Column("PT_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "PT_REG_BY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    PC_ID = Column(Integer, ForeignKey("PACKAGE_CAT.PC_ID"))

    package_category = relationship("PackageCategory")

    reg_user = relationship("Staff", foreign_keys=[reg_by])


class PriceList(Base):
    """Pricelist model."""

    __tablename__ = "PRICELIST"

    PL_ID = Column(Integer, primary_key=True)
    PL_SHORT = Column(Unicode(length=10))
    PL_NAME_DE = Column(Unicode(length=100))
    PL_NAME_EN = Column(Unicode(length=100))
    CUR_ID = Column(Unicode(length=3))
    PL_ORDER = Column(Integer)
    reg = Column("PL_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "PL_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("PL_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "PL_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    PL_TYPE = Column(Integer)
    PL_FACTOR_CC = Column(Numeric(precision=18, scale=5))
    PL_FACTOR_PROFIT = Column(Numeric(precision=18, scale=5))

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class Process(Base):
    """Process table model."""

    __tablename__ = "V_PSEX_PROCESS"

    PC_ID = Column(Integer, primary_key=True, nullable=False)
    PC_PATH = Column(Unicode(length=50))
    PC_WC_ID = Column(Unicode(length=36))
    PC_CLIENT = Column(Integer)  # todo: check if this is a link to Customer
    PC_PRODUCT = Column(Unicode(length=255))
    PC_MODEL = Column(Unicode(length=255))
    PC_NAME = Column(Unicode(length=255))
    PC_ORDERTEXT = Column(Unicode(length=255))
    PC_PROJECTMANAGER = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    PC_LOTSIZE = Column(Integer)  # todo: check if this is a link
    PC_STATUS = Column(Integer)  # todo: check if this is a link
    PC_READY_TO_SHOP = Column(Integer)  # todo: check if this is a link
    PC_SHOPDATE = Column(DateTime)  # todo: check if this is a link
    PC_CREATEDBY_TEAM = Column(Integer)  # todo: check if this is a link
    PC_UPDATEBY_TEAM = Column(Integer)  # todo: check if this is a link
    PC_REGDATE = Column(DateTime)
    PC_CREATEDBY = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    PC_DISABLED = Column(Boolean)


class ProcessPhase(Base):
    """ProcessPhase Model."""

    __tablename__ = "V_PSEX_PROCESSPHASE"

    PRP_ID = Column(Integer, primary_key=True)
    PRP_NAME_DE = Column(Unicode(length=256))
    PRP_NAME_EN = Column(Unicode(length=256))
    PRP_NAME_FR = Column(Unicode(length=256))
    PRP_SHORT_DE = Column(Unicode(length=256))
    PRP_SHORT_EN = Column(Unicode(length=256))
    PRP_SHORT_FR = Column(Unicode(length=256))
    PRP_SORT = Column(Integer)
    PRP_SHOW_IN_PSEX = Column(Boolean)
    PRP_EDOC_ACTIVE = Column(Boolean)
    PRP_EDOC_NAME_DE = Column(Unicode(length=256))
    PRP_EDOC_NAME_EN = Column(Unicode(length=256))
    PRP_EDOC_NAME_FR = Column(Unicode(length=256))
    PRP_EDOC_SHORT_DE = Column(Unicode(length=256))
    PRP_EDOC_SHORT_EN = Column(Unicode(length=256))
    PRP_EDOC_SHORT_FR = Column(Unicode(length=256))
    PRP_EDOC_NUMBER = Column(Integer)
    PRP_EDOC_IS_REFERENCE = Column(Boolean)
    PRP_EDOC_IS_DEFAULT = Column(Boolean)


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
    update = Column("HRP_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "HRP_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )

    update_user = relationship("Staff", foreign_keys=[update_by])


class Project(Base):
    """PSE Project (view on PSE database)."""

    __tablename__ = "V_PSEX_PROJECT"

    P_ID = Column(Integer, primary_key=True, nullable=False)
    P_FOLDER = Column(Unicode(length=256))
    P_PRODUCT = Column(NullUnicode(length=256))
    P_MODEL = Column(NullUnicode(length=256))
    PC_ID = Column(Integer, ForeignKey("V_PSEX_PROCESS.PC_ID"))
    P_DATE_DONE = Column(DateTime)
    P_PREDATE = Column(DateTime)
    P_DEADLINE = Column(DateTime)
    P_DATE_ORDER = Column(DateTime)
    MD_ID = Column(Integer, nullable=False)
    P_CUSTOMER_A = Column(Integer, ForeignKey("V_PSEX_CUSTOMER_ADDRESS.CU_ID"))
    P_CUSTOMER_B = Column(Integer, ForeignKey("V_PSEX_CUSTOMER_ADDRESS.CU_ID"))
    P_STATUS = Column(Integer)
    P_DATE_CHECK = Column(DateTime)
    P_CHECKBY = Column(Integer)
    TC_P_ID = Column(Integer)  # todo: not sure what this links to
    P_ORDERTEXT = Column(Unicode(length=2048))
    P_PROJECTINFO = Column(Unicode(length=4000))
    P_IS_QUOTATION = Column(Boolean)
    P_ZARA_NUMBER = Column(Unicode(length=11))
    P_NAME = Column(Unicode(length=31))
    SC_ID = Column(Unicode(length=7))
    P_PROJECTMANAGER = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    P_HANDLEDBY = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    P_DATE_APPOINTMENT = Column(DateTime)
    P_DATE_READY = Column(DateTime)
    P_READYBY = Column(DateTime)
    P_DATE_DISPO = Column(DateTime)
    P_DONEBY = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    RES_ID = Column(Integer)  # todo: not sure what this links to
    P_DELAY = Column(Numeric(precision=18, scale=0))
    DELR_ID = Column(Integer)  # todo: not sure what this links to
    P_ACTION = Column(Boolean)
    P_FORECAST = Column(Numeric(precision=18, scale=2))
    P_WC_ID = Column(Unicode(length=36))
    CC_ID = Column(Unicode(length=10))
    P_CHECKBY_TEAM = Column(Integer)
    P_DONEBY_TEAM = Column(Integer)
    P_HANDLEDBY_TEAM = Column(Integer)
    P_PROJECTMANAGER_TEAM = Column(Integer)
    P_READYBY_TEAM = Column(Integer)
    P_REGBY_TEAM = Column(Integer)
    P_UPDATEBY_TEAM = Column(Integer)
    KOT_ID = Column(Integer, ForeignKey("V_PSEX_KIND_OF_TEST.KOT_ID"))
    P_TS_RECEIPT_ADVISED = Column(Boolean)
    P_ORDERSIZE = Column(Numeric(precision=18, scale=2))
    P_EXPECTED_TS_RECEIPT = Column(DateTime)
    P_PLANNED_ORDERSIZE = Column(Numeric(precision=18, scale=2))
    P_INTERN = Column(Boolean)
    P_CUR_ID = Column(Unicode(length=3))
    P_CURRENCYRATE = Column(Numeric(precision=18, scale=0))
    P_REGBY = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    P_REGDATE = Column(DateTime)
    SAP_QUOTATION_NUMBER = Column(Unicode(length=10))
    P_PROJECTFOLDERCREATED = Column(Boolean)
    BR_ID = Column(Unicode(length=36))
    P_TEAM_ID = Column(Unicode(length=36))
    P_AUDIT_DATE = Column(DateTime)
    P_PROCESSPHASE = Column(Integer)
    P_IAN = Column(Unicode(length=256))
    P_TOKEN = Column(Unicode(length=60))
    CATEGORY_ID = Column(Integer, nullable=False)
    E_ID = Column(Integer)  # todo: link to edoc
    P_CONTACT_CUC_ID = Column(Integer,
                              ForeignKey("V_PSEX_CUSTOMER_CONTACT.CUC_ID"))
    P_REMARK = Column(Unicode(length=1024))
    BATCH_NUMBER = Column(Unicode(length=16))
    P_RETEST = Column(Integer, nullable=False)
    P_RETEST_OF = Column(Integer)

    customer_contact = relationship("CustomerContact")
    ordering_party_address = relationship("CustomerAddress",
                                          foreign_keys=[P_CUSTOMER_A])
    manufacturer_address = relationship("CustomerAddress",
                                        foreign_keys=[P_CUSTOMER_B])
    process = relationship("Process")
    project_manager = relationship("Staff", foreign_keys=[P_PROJECTMANAGER])
    project_handler = relationship("Staff", foreign_keys=[P_HANDLEDBY])
    register_user = relationship("Staff", foreign_keys=[P_REGBY])
    kind_of_test = relationship("KindOfTest")
    sub_orders = relationship("SubOrder", back_populates="project")


class ProofElement(Base):
    """Proof Element of a Package."""

    __tablename__ = "NAV_PACK_ELEMENT_PROOF"

    NPEP_ID = Column(Integer, primary_key=True)
    NPE_ID = Column(Integer, ForeignKey("NAV_PACK_ELEMENT.NPE_ID",
                                        ondelete="CASCADE"))
    NPEP_TYPE = Column(Integer)
    NPR_ID = Column(Integer)
    NPEP_TEXT_DE = Column(Unicode(length=255))
    NPEP_TEXT_EN = Column(Unicode(length=255))
    reg = Column("NPEP_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "NPEP_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("NPEP_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "NPEP_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )

    package_element = relationship("PackageElement",
                                   back_populates="proof_elements")

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class ServiceClass(Base):
    """Service Class of a Package."""

    __tablename__ = "NAV_PACK_SERVICECLASS"

    NPS_ID = Column(Integer, primary_key=True)
    NP_ID = Column(Integer, ForeignKey("NAV_PACK.NP_ID", ondelete="CASCADE"))
    SCL_ID = Column(Integer, ForeignKey("SERVICECLASS.SCL_ID"))

    package = relationship("Package", back_populates="service_classes")
    definition = relationship("ServiceClassDefinition")


class ServiceClassDefinition(Base):
    """Definitions for the service class."""

    __tablename__ = "SERVICECLASS"

    SCL_ID = Column(Integer, primary_key=True)
    SCL_LEVEL = Column(Integer)
    SCL_REMARK_DE = Column(Unicode(length=500))
    SCL_REMARK_EN = Column(Unicode(length=500))
    reg = Column("SCL_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "SCL_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("SCL_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "SCL_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class Staff(Base):
    """Staff table model."""

    __tablename__ = "V_PSEX_STAFF"

    ST_ID = Column(Integer, primary_key=True)
    ST_SURNAME = Column(Unicode(length=60), nullable=False)
    # ST_FORENAME is nullable in database, but never actually NULL
    ST_FORENAME = Column(Unicode(length=50), nullable=False)
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


class StatisticModule(Base):
    """Statistic Module."""

    __tablename__ = "STATISTIC_MODULE"

    STAM_ID = Column(Integer, primary_key=True)
    ST_ID = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"))
    STAT_ID = Column(Integer, ForeignKey("STATISTIC_TYPE.STAT_ID"))
    STAM_REG = Column(DateTime)

    statistic_type = relationship("StatisticType")


class StatisticType(Base):
    """Statistic Type."""

    __tablename__ = "STATISTIC_TYPE"

    STAT_ID = Column(Integer, primary_key=True)
    STAT_NAME_DE = Column(Unicode(length=256))
    STAT_NAME_EN = Column(Unicode(length=256))
    STAT_REG = Column(DateTime)
    STAT_TYPE = Column(Integer)


class SubOrder(Base):
    """
    SubOrder of a PSEX project.

    The PSEX database does not define a primary key for the table. Nevertheless
    we need a PK for SqlAlchemy to work with all it"s features. Therefore we
    define SO_NUMBER as well as P_ID as composite primary key.
    """

    __tablename__ = "V_PSEX_SUBORDERS"

    P_ID = Column(Integer, ForeignKey("V_PSEX_PROJECT.P_ID"), primary_key=True)
    SO_NUMBER = Column(Integer, primary_key=True)
    SO_DISPOBY = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    SO_CREATED = Column(DateTime)
    ST_ID = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    SO_DEADLINE = Column(DateTime)
    SO_TASK = Column(NullUnicode(length=1024))
    SO_HOURS = Column(Numeric(precision=18, scale=6))
    SO_ACC_HOURS = Column(Numeric)
    SO_COMMENT = Column(Unicode(length=2000))
    SO_DATE_READY = Column(DateTime)
    SO_DATE_CHECK = Column(DateTime)
    RES_ID = Column(Integer)  # todo: ForeignKey?
    SO_PREDATE = Column(DateTime)
    SO_WAIT = Column(Boolean)
    SO_REPORT = Column(Unicode(length=255))
    SO_DISABLED = Column(Boolean)
    SO_FORECAST = Column(Numeric(precision=18, scale=2))
    SO_INTERN = Column(Boolean)
    ST_ID_TEAM = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    SO_UPDATEBY_TEAM = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    SO_REGBY_TEAM = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    SO_READYBY_TEAM = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    SO_DISPOBY_TEAM = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    SO_CHECKBY_TEAM = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    ORDER_POSITION = Column(Unicode(length=6))
    ORDER_DATE = Column(DateTime)
    ORDER_SIGN = Column(Unicode(length=35))
    SAP_NO = Column(Unicode(length=10))
    SO_READYBY = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    SO_RATE = Column(Numeric)
    SO_SPENDS = Column(Numeric)
    SO_POST_OUT_DATE = Column(DateTime)
    SO_CONFIRMED_DATE = Column(DateTime)
    ZM_ID = Column(Unicode(length=18))
    SO_REMARK = Column(Unicode(length=1024))
    SO_MODEL = Column(Unicode(length=255))
    SO_SORT = Column(Integer)
    KPI = Column(Boolean)
    S_KPI_NUMBER = Column(Integer)
    REPORT_SENT = Column(DateTime)

    project = relationship("Project", back_populates="sub_orders")
    dispo_user = relationship("Staff", foreign_keys=[SO_DISPOBY])
    user = relationship("Staff", foreign_keys=[ST_ID])
    team = relationship("Staff", foreign_keys=[ST_ID_TEAM])
    update_team = relationship("Staff",
                               foreign_keys=[SO_UPDATEBY_TEAM])
    reg_team = relationship("Staff", foreign_keys=[SO_REGBY_TEAM])
    ready_team = relationship("Staff",
                              foreign_keys=[SO_READYBY_TEAM])
    dispo_team = relationship("Staff",
                              foreign_keys=[SO_DISPOBY_TEAM])
    check_team = relationship("Staff",
                              foreign_keys=[SO_CHECKBY_TEAM])


class Team(Base):
    """Staff table model."""

    __tablename__ = "V_PSEX_HIERARCHY"

    HR_ID = Column(Integer, primary_key=True)
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


class TemplateType(Base):
    """TemplateType."""

    __tablename__ = "V_PSEX_TEMPLATE_TYPE"

    TPT_ID = Column(Integer, primary_key=True)
    TPT_NAME_DE = Column(Unicode(length=256), nullable=False)
    TPT_NAME_EN = Column(Unicode(length=256), nullable=False)
    TPT_NAME_FR = Column(Unicode(length=256), nullable=False)
    TPT_SHORT_DE = Column(Unicode(length=256), nullable=False)
    TPT_SHORT_EN = Column(Unicode(length=256), nullable=False)
    TPT_SHORT_FR = Column(Unicode(length=256), nullable=False)
    TPT_PATH = Column(Unicode(length=256), nullable=False)
    TPT_PREFIX = Column(Unicode(length=256), nullable=False)
    TPT_MODULETYPE = Column(Unicode(length=256))
    TPT_SHOWINPROZESSFOLDER = Column(Boolean, nullable=False)
    TPT_SHOWINTEMPLATEMANAGER = Column(Boolean, nullable=False)


class TestBase(Base):
    """TestBase model."""

    __tablename__ = "BASE"

    B_ID = Column(Integer, primary_key=True)
    B_NAME_DE = Column(Unicode(length=512))
    B_NAME_EN = Column(Unicode(length=512))
    B_NAME_FR = Column(Unicode(length=512))
    DI_ID = Column(Integer, ForeignKey("DEFAULT_ITEM.DI_ID"))
    BT_ID = Column(Integer, ForeignKey("BASE_TYPE.BT_ID"))
    PLK_SHORT = Column(Unicode(length=10))
    reg = Column("B_REG", DateTime, default=datetime.now)
    reg_by = Column(
        "B_REGBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id
    )
    update = Column("B_UPDATE", DateTime, onupdate=datetime.now)
    update_by = Column(
        "B_UPDATEBY", Integer, ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id
    )
    HRC_ID = Column(Integer, ForeignKey("HR_COUNTRY.HRC_ID"), nullable=False)
    B_PARENT = Column(Integer, ForeignKey("BASE.B_ID"))
    B_SHORT_DE = Column(Unicode(length=512))
    B_SHORT_EN = Column(Unicode(length=512))
    B_SHORT_FR = Column(Unicode(length=512))
    B_DOW = Column(DateTime)
    B_COMMENT_DE = Column(Unicode(length=512))
    B_COMMENT_EN = Column(Unicode(length=512))
    B_COMMENT_FR = Column(Unicode(length=512))
    B_DOA = Column(Integer, nullable=False)

    test_base_type = relationship("TestBaseType")
    default_item = relationship("DefaultItem")

    reg_user = relationship("Staff", foreign_keys=[reg_by])
    update_user = relationship("Staff", foreign_keys=[update_by])


class TestBaseType(Base):
    """Type of a TestBase."""

    __tablename__ = "BASE_TYPE"

    BT_ID = Column(Integer, primary_key=True)
    BT_SHORT = Column(Unicode(length=6))
    BT_NAME_DE = Column(Unicode(length=50))
    BT_NAME_EN = Column(Unicode(length=50))
    BT_NAME_FR = Column(Unicode(length=50))
    GT_ID = Column(Integer)  # todo: Add ForeignKey


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
def insert_package_into_nav(nav_id: int, package_id: int,
                            session: Session, copy_pe: bool = True) -> int:
    """
    Insert a copy of the given package into the given navigation.

    Returns the id of the new package.

    If copy_pe is false, the PackageElements won"t be copied along with the
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
    )
    session.add(new_pack)
    session.flush()

    new_pack_id = new_pack.NP_ID

    for service_class in cast(List[ServiceClass], pack.service_classes):
        new_class = ServiceClass(
            NP_ID=new_pack.NP_ID,
            SCL_ID=service_class.SCL_ID
        )
        session.add(new_class)

    if copy_pe:
        for package_element in cast(List[PackageElement],
                                    pack.package_elements):
            copy_package_element(new_pack.NP_ID, package_element, session)
    session.flush()
    return new_pack_id


def copy_package_element(new_pack_id: int, package_element: PackageElement,
                         session: Session) -> int:
    """Copy the PackageElement to the Package with the given id."""
    new_element = PackageElement(
        NP_ID=new_pack_id,
        DM_ID=package_element.DM_ID,
        NL_ID=package_element.NL_ID,
        ZM_LOCATION=package_element.ZM_LOCATION,
        CT_ID=package_element.CT_ID,
        NPE_CREATE=package_element.NPE_CREATE,
        NPE_CREATE_SO=package_element.NPE_CREATE_SO
    )
    session.add(new_element)
    session.flush()
    for calculation in cast(List[PackageElementCalculation],
                            package_element.package_calculations):
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
        )
        session.add(new_calc)
    for proof_element in cast(List[ProofElement],
                              package_element.proof_elements):
        new_proof = ProofElement(
            NPE_ID=new_element.NPE_ID,
            NPEP_TYPE=proof_element.NPEP_TYPE,
            NPR_ID=proof_element.NPR_ID,
            NPEP_TEXT_DE=proof_element.NPEP_TEXT_DE,
            NPEP_TEXT_EN=proof_element.NPEP_TEXT_EN,
        )
        session.add(new_proof)
    return new_element.NPE_ID
