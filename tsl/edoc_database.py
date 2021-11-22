"""
Database connection and models for the PSE database.

WARNING! Delete cascades do not work properly, when delete is executed on a
query. Always use session.delete()!
"""
# pylint: disable=too-many-lines
from __future__ import annotations

import logging
import os
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal
from enum import IntEnum
from typing import Dict, Iterator, List, Optional, cast

from sqlalchemy import (
    DECIMAL,
    NCHAR,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    LargeBinary,
    Numeric,
    String,
    Unicode,
    text,
)
from sqlalchemy.dialects.mssql import BIT, IMAGE, MONEY, UNIQUEIDENTIFIER
from sqlalchemy.orm import (
    Mapped,
    Session,
    backref,
    declarative_base,
    deferred,
    joinedload,
    load_only,
    relationship,
    sessionmaker,
    validates,
)
from sqlalchemy.sql.schema import ForeignKey

from tsl.common_db import NullUnicode, create_db_engine
from tsl.variables import PATH, ClearingState
from tsl.vault import Vault

log = logging.getLogger("tsl.edoc_database")  # pylint: disable=invalid-name

ENGINE = create_db_engine(Vault.Application.EDOC)

Base = declarative_base()
Base.metadata.bind = ENGINE

AdminSession = sessionmaker(bind=ENGINE)  # pylint: disable=invalid-name

USER_ID: Optional[int] = None
TEAM_NAME: Optional[str] = None


# pylint: disable=global-statement
def get_user_id() -> int:
    """Get the database id for the current user."""
    global USER_ID
    if USER_ID is None:
        _fetch_user_id()
    return cast(int, USER_ID)


def get_user_group_name() -> Optional[str]:
    """Get the database id for the current users team."""
    global TEAM_NAME
    if TEAM_NAME is None:
        _fetch_user_id()
    return TEAM_NAME


def _fetch_user_id() -> None:
    """Fetch and set the user id from the database."""
    global USER_ID
    global TEAM_NAME
    with session_scope(False) as session:
        username = os.getlogin()
        log.debug("Getting database id for user %s", username)
        user = (
            session.query(Staff)
            .filter_by(ST_WINDOWSID=username)
            .options(
                load_only(Staff.ST_ID, Staff.ST_TEAM),
                joinedload(Staff.team).options(load_only(Team.HR_SHORT)),
            )
            .one()
        )
        USER_ID = user.ST_ID
        if user.ST_TEAM and user.team:
            TEAM_NAME = user.team.HR_SHORT
        else:
            log.error("Could not get Team for ST_TEAM: %s", user.ST_TEAM)


# pylint: enable=global-statement


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
    except:
        session.rollback()
        raise
    finally:
        session.close()


# pylint: disable=too-few-public-methods
class AppsCount(Base):
    """AppsCount."""

    doc = [
        "AppsCount represents the startup information of an application.",
        "Each time a user starts an application an entry to this table will "
        "be written.",
    ]

    __tablename__ = "APPS_COUNT"
    APPSC_ID: Mapped[int] = Column(Integer, primary_key=True)
    ST_ID = Column(
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        index=True,
        doc="User that uses the application creating the entry.",
        default=get_user_id,
    )
    APPST_ID = Column(Integer, index=True)
    reg = Column(
        "APPSC_REG",
        DateTime,
        server_default=text("(getutcdate())"),
        doc="Time the entry was created / the application started.",
    )
    APPSC_MERKER = Column(
        Integer, doc="DEPRECATED: Last use in 2013, serves unknown purpose."
    )
    APPSC_TEXT = Column(
        Unicode(4000),
        doc="Free text containing debug information, computer name, user etc.",
    )
    APPSC_STARTTIME: Mapped[int] = Column(
        BigInteger,
        nullable=False,
        server_default=text("((0))"),
        doc="UNKNOWN: We do not know, what the purpose of this Column is.",
    )
    APPSC_APP_FOLDER = Column(
        Unicode(255),
        doc="The path on the user's hard drive in which the registered app "
        "is installed.",
    )
    APPSC_WINDOWSID = Column(
        Unicode(30), doc="Windows account name of the user (i.e. krumm-ti)"
    )
    FS_SHORT = Column(
        Unicode(5),
        index=True,
        doc="Location key, can be one of the following: NULL, (-), BAN, BAT, "
        "CHI, FFM, FIL, HAM, HAN, HUN, IMM, IND, ITA, JAP, KOR, MAN, MUC, "
        "SIN, UKI, USA",
    )
    APPSC_SQL_DRIVER = Column(
        BIT, doc="Defines if the SQL driver is installed on the system."
    )
    APPSC_COMPUTER = Column(
        Unicode(512),
        doc="Full computer name from which the entry originated "
        "(i.e. MUSUXYU12345.mobile.itgr.net.)",
    )
    APPSC_IP = Column(
        Unicode(50),
        doc="IP address of the computer from which the entry originated.",
    )
    APPSC_LANGID = Column(
        Unicode(50),
        doc="DEPRECATED: This flag is only used in entries created by "
        "egger-hl.",
    )

    user: Staff = relationship("Staff", uselist=False)


class Attribute(Base):
    """Attributes of a DefaultModul."""

    __tablename__ = "ATTRIBUTES"

    doc = [
        "Attributes will be used on DefaultModules, DefaultItems and "
        "EdocModules. The are used as Parameter in eDOC and Navigator.",
    ]

    ATT_ID: Mapped[int] = Column(Integer, primary_key=True)
    ATT_SHORT = Column(Unicode(10), doc="Short name of the Attribute")
    ATT_NAME_DE = Column(Unicode(60), doc="German name of the Attribute")
    ATT_NAME_EN = Column(Unicode(60), doc="English name of the Attribute")
    ATT_TYPE = Column(
        Integer,
        ForeignKey("ATTRIBUTES_TYPE.ATT_TYPE"),
        index=True,
        server_default=text("((0))"),
        doc="Type of the Attribute.",
    )
    ATT_IS_FILTER: Mapped[bool] = Column(
        Boolean,
        nullable=False,
        server_default=text("((1))"),
        doc="Defines if an attribute is a filter (there are only 2 out of "
        "over 800 that aren't a filter.",
    )

    reg = Column("ATT_REG", DateTime, server_default=text("(getutcdate())"))
    reg_by = Column(
        "ATT_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("ATT_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "ATT_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )

    attribute_type: AttributeType = relationship(
        "AttributeType", back_populates="attributes", uselist=False
    )
    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class AttributeType(Base):
    """Type of an Attribute."""

    __tablename__ = "ATTRIBUTES_TYPE"

    doc = [
        "Attribute type that is used to categorize Attributes.",
        "Please note: The Column ATT_TYPE isn't the primary key defined in "
        "the table. The real primary key is ATTT_ID which is totally useless"
        " because it isn't used. References to this table are made trough "
        "ATT_TYPE, that's why we use this Column instead as primary key. "
        "The Column ATTT_ID is completely ignored.",
    ]

    # ATTT_ID = Column(Integer, primary_key=True)
    ATT_TYPE: Mapped[int] = Column(Integer, primary_key=True)
    ATTT_NAME_DE = Column(Unicode(100), doc="German name of the Attribute")
    ATTT_NAME_EN = Column(Unicode(100), doc="English name of the Attribute")
    ATTT_NAME_FR = Column(Unicode(100), doc="French name of the Attribute")
    # todo: convert to integer before use programmatically
    ATTT_ORDER = Column(
        NCHAR(10),
        doc="Ordering of the AttributeTypes. This column uses values like "
        "'10        '. It's unknown why one would do that. It is recommended "
        "to convert the values to an integer before use.",
    )

    attributes: List[Attribute] = relationship(
        "Attribute", back_populates="attribute_type", uselist=True
    )


class CalculationType(Base):
    """Type of a calculation."""

    __tablename__ = "CALC_TYPE"

    doc = [
        "Type of a Calculation. Provides the following six values: GENERAL, "
        "BASIS, ADDONS, CERTIFICATE COSTS, LICENSE COSTS, "
        "FACTORY PLANT INSPECTION",
    ]

    CT_ID: Mapped[int] = Column(Integer, primary_key=True)
    CT_NAME = Column(Unicode(50), doc="Name in English")
    CT_ORDER = Column(
        Integer,
        doc="Order number of the CalculationType (which is exactly in the "
        "order of the primary key)",
    )
    CA_ID = Column(
        Integer,
        doc="UNKNOWN: It's not the Id of the CustomerAddress "
        "(V_PSEX_CUSTOMER_ADDRESS.CA_ID) and exactly the same value as CT_ID.",
    )


class Clearing(Base):
    """Clearing status definitions (i.e. 06-Freigegeben)."""

    __tablename__ = "CLEARING"

    doc = [
        "Definition of the clearing states, i.e.: '06-Freigegeben'",
    ]

    CL_ID: Mapped[int] = Column(Integer, primary_key=True)
    CL_NAME_DE: Mapped[str] = Column(
        Unicode(length=100),
        nullable=False,
        doc="German name. Since it's never null in the database, "
        "we set it as nullable=False.",
    )
    CL_NAME_EN: Mapped[str] = Column(
        Unicode(length=100),
        nullable=False,
        doc="English name. Since it's never null in the database, "
        "we set it as nullable=False.",
    )
    CL_DESCRIPTION_DE = Column(
        Unicode(255), doc="DEPRECATED: It's always NULL for every entry."
    )
    CL_DESCRIPTION_EN = Column(
        Unicode(255), doc="DEPRECATED: It's always NULL for every entry."
    )
    # todo: add foreign key
    TPST_ID = Column(
        Integer,
        server_default=text("((1))"),
        doc="Template status as defined in PSEX. Foreign key is not defined!",
    )

    reg = Column("CL_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "CL_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("CL_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "CL_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )

    @property
    def final_state(self) -> ClearingState:
        """Return if the Clearing is a final state."""
        if self.CL_NAME_DE in [
            "06 - Freigegeben",
            "09 - ohne Freigabeverfahren",
            "04 - validiert (ohne Freigabe)",
            "08 – gängige Praxis (nicht validiert)",
            "10 - TCC Status",
        ]:
            return ClearingState.FINAL
        if self.CL_NAME_DE == "05 - Freigabeverfahren läuft":
            return ClearingState.INTERMEDIATE
        return ClearingState.NOT_FINAL


class Country(Base):
    """Countries."""

    __tablename__ = "HR_COUNTRY"

    doc = [
        "Definition of country names as a tree structure. Is used in Navigator"
        "to assign Navigations to a specific region or country.",
    ]

    HRC_ID: Mapped[int] = Column(Integer, primary_key=True)
    HRC_LEFT = Column(Integer, index=True, doc="Sort order left oriented")
    HRC_RIGHT = Column(Integer, index=True, doc="Sort order right oriented")
    HRC_INDENT = Column(Integer, doc="Indentation in the country tree")
    HRC_NAME_DE = Column(Unicode(255), index=True, doc="German country name")
    HRC_NAME_EN = Column(Unicode(255), index=True, doc="Englisch country name")
    HRC_NAME_FR = Column(Unicode(255), doc="French country name")

    update = Column(
        "HRC_UPDATE",
        DateTime,
        onupdate=datetime.utcnow,
        server_default=text("(getdate())"),
    )
    update_by = Column(
        "HRC_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
        server_default=text("((1))"),
    )

    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class CustomList(Base):
    """CustomerList table model."""

    __tablename__ = "CUSTOM_LIST"

    doc = ["Lists that _group CustomListElements together."]

    CUL_ID: Mapped[int] = Column(Integer, primary_key=True)
    CUL_NAME_DE = Column(Unicode(256), doc="German name of the CustomList.")
    CUL_NAME_EN = Column(Unicode(256), doc="English name of the CustomList.")
    reg = Column("CUL_REG", DateTime, server_default=text("(getdate())"))
    reg_by = Column(
        "CUL_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("CUL_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "CUL_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class CustomListElement(Base):
    """CustomerListElement table model."""

    __tablename__ = "CUSTOM_LIST_ELEMENT"

    doc = [
        "Custom list element for categorizing DefaultItems. The "
        "CustomListElements are used i.e. for adding the LIDL EUG category "
        "to the different DefaultItems of a DefaultModule."
    ]

    CULE_ID: Mapped[int] = Column(Integer, primary_key=True)
    CUL_ID = Column(Integer, ForeignKey("CUSTOM_LIST.CUL_ID"))
    CULE_NAME_DE = Column(Unicode(512), doc="German name")
    CULE_NAME_EN = Column(Unicode(512), doc="English name")
    CULE_INDENT = Column(
        Integer, doc="Indentation within the list (CustomList)"
    )
    CULE_ORDER = Column(
        Integer, doc="Order of the items within the list (CustomList)"
    )
    CULE_STYLE: Mapped[int] = Column(
        Integer,
        nullable=False,
        server_default=text("((0))"),
        doc="Style shown in the Field 'Art', used values: 0, 1, 2, 3, 4",
    )
    CULE_TESTBASE: Mapped[int] = Column(
        Integer,
        nullable=False,
        server_default=text("((0))"),
        doc="Testbase shown in Field 'Grundlage in Anforderung', "
        "used values: 0, 3, 4, 6, 7",
    )
    CULE_MODULBASE: Mapped[int] = Column(
        Integer,
        nullable=False,
        server_default=text("((0))"),
        doc="Defines the module base shown in Field 'Modulgrundlage': "
        "0 - From Module, 1 - From Item. Currently this is set to 0 for "
        "alle CustomListElements",
    )
    CULE_DEF_COMMENT_DE = Column(Unicode(2048), doc="German default comment")
    CULE_DEF_COMMENT_EN = Column(Unicode(2048), doc="English default comment")
    DI_ID = Column(
        Integer,
        ForeignKey("DEFAULT_ITEM.DI_ID"),
        doc="Reference to a DefaultItem that is used as template when "
        "inserting a 'Kategoriebaustein'",
    )
    CULE_MARKETABILITY: Mapped[bool] = Column(
        BIT, nullable=False, server_default=text("((0))"), doc="UNKNOWN"
    )
    CULE_NUMBER = Column(
        Unicode(10),
        doc="Number as string, i.e. for LIDL categories: 1.1, 2.1 etc",
    )
    CULE_ID_MAP_LIDL = Column(
        Integer,
        doc="UNKNOWN, but probably the link to the LIDL test plan title "
        "page rows.",
    )

    reg = Column(
        "CULE_REG",
        DateTime,
        server_default=text("(getdate())"),
    )
    reg_by = Column(
        "CULE_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("CULE_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "CULE_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )

    custom_list: CustomList = relationship("CustomList", uselist=False)
    default_item: DefaultItem = relationship(
        "DefaultItem", back_populates="custom_list_elements", uselist=False
    )
    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class Customer(Base):
    """Customer table model."""

    __tablename__ = "V_PSEX_CUSTOMER"

    doc = [
        "View on Customer table of the PSEX database. Some columns are joined"
        " from the Customer address table, so that the reference to the "
        "address table does contain partly redundant data."
    ]

    CU_ID: Mapped[int] = Column(Integer, primary_key=True)
    CA_ID: Mapped[int] = Column(
        Integer, ForeignKey("V_PSEX_CUSTOMER_ADDRESS.CA_ID"), nullable=False
    )
    CU_NUMBER = Column(
        String(10, "SQL_Latin1_General_CP1_CI_AS"),
        doc="UNKNOWN, some internal Customer number, starts offen (or always)"
        " with 130000",
    )
    CU_ACTIVE = Column(BIT, doc="Defines if the Customer is active.")
    CU_NAME: Mapped[str] = Column(
        Unicode(165), nullable=False, doc="Name of the customer"
    )
    CU_NAME_SHORT: Mapped[str] = Column(
        Unicode(60), nullable=False, doc="Short name of the customer"
    )
    CU_COUNTRY = Column(
        String(3, "SQL_Latin1_General_CP1_CI_AS"),
        doc="Country code of the customer (i.e. 'DE')",
    )
    CU_STREET = Column(Unicode(100), doc="Street of address")
    CU_CITY = Column(Unicode(40), doc="City of address")
    CU_ZIPCODE = Column(
        String(10, "SQL_Latin1_General_CP1_CI_AS"), doc="Zipcode of address"
    )
    MD_ID: Mapped[int] = Column(Integer, nullable=False, doc="UNKNOWN")
    CU_SUPPLIER_NO = Column(Unicode(24), doc="Supplier number")
    CU_ATTENDENT = Column(Unicode(40), doc="Attendant of the customer.")
    CU_FAX = Column(
        String(60, "SQL_Latin1_General_CP1_CI_AS"), doc="Fax number"
    )
    CU_PHONE = Column(
        String(60, "SQL_Latin1_General_CP1_CI_AS"), doc="Phone number"
    )
    CU_COMMENT = Column(Unicode(2000), doc="Comment")
    CU_BOOKING_AREA = Column(
        String(4, "SQL_Latin1_General_CP1_CI_AS"),
        doc="TÜV SÜD Booking Area (i.e. 0013)",
    )
    CU_SERVERID = Column(
        Integer, doc="UNKNOWN, but not a Foreign Key as appears nowhere else."
    )

    address: CustomerAddress = relationship(
        "CustomerAddress", back_populates="customer", uselist=False
    )
    contacts: CustomerContact = relationship(
        "CustomerContact", back_populates="customer", uselist=False
    )


class CustomerAddress(Base):
    """CustomerAddress table model."""

    __tablename__ = "V_PSEX_CUSTOMER_ADDRESS"

    doc = [
        "View on the PSE's customer adresses.",
        "The view is malformed as it defines the CA_ID and a CU_ID which "
        "stands in contradiction to the customer view where the same keys are "
        "defined. A one-to-one relationship should define the foreign key "
        "on one side.",
    ]

    CA_ID: Mapped[int] = Column(
        Integer,
        primary_key=True,
        doc="WARNING: Is defined as not nullable and not as primary key in "
        "the database.",
    )
    # totally useless, there is a CA_ID on V_PSEX_CUSTOMER to build this
    # one to one relationship. MS SQL would actually prevent this if someone
    # would have defined the foreign keys correctly.
    # CU_ID = Column(Integer, ForeignKey("V_PSEX_CUSTOMER.CU_ID"))
    CA_ADDRNUMBER = Column(
        String(10, "SQL_Latin1_General_CP1_CI_AS"),
        doc="UNKOWN: Purpose of this column is unknown.",
    )
    CA_NATION: Mapped[str] = Column(
        String(1, "SQL_Latin1_General_CP1_CI_AS"),
        nullable=False,
        doc="UNKNOWN: Possible values are A, C, H, I, K, M, V",
    )
    CA_TITLE = Column(
        Unicode(4),
        doc="UNKNOWN: Possible values are 0001 to 0007. Looks like someone "
        "formatted an Integer as a 4 character string.",
    )
    CA_NAME: Mapped[str] = Column(
        Unicode(165), nullable=False, doc="Name of the company"
    )
    CA_NAME_SHORT: Mapped[str] = Column(
        Unicode(60), nullable=False, doc="Short name of the company"
    )
    CA_NAME1 = Column(Unicode(40), doc="Additional name field")
    CA_NAME2 = Column(Unicode(40), doc="Additional name field")
    CA_NAME3 = Column(Unicode(40), doc="Additional name field")
    CA_NAME4 = Column(Unicode(40), doc="Additional name field")
    CA_CITY = Column(Unicode(40), doc="City")
    CA_DISTRICT = Column(Unicode(50), doc="District")
    CA_COUNTRY = Column(
        String(3, "SQL_Latin1_General_CP1_CI_AS"),
        doc="Country code i.e. 'DE'. Is also used for states "
        "i.e. 'FL' which should be CA_REGION",
    )
    CA_LANGUAGE = Column(
        String(2, "SQL_Latin1_General_CP1_CI_AS"),
        doc="Language code i.e. 'DE'",
    )
    CA_REGION = Column(
        String(3, "SQL_Latin1_General_CP1_CI_AS"), doc="Region code i.e. 'BY'"
    )
    CA_PHONE = Column(
        String(60, "SQL_Latin1_General_CP1_CI_AS"), doc="Phone number"
    )
    CA_PHONE2 = Column(
        String(60, "SQL_Latin1_General_CP1_CI_AS"),
        doc="Additional phone number",
    )
    CA_FAX = Column(
        String(60, "SQL_Latin1_General_CP1_CI_AS"), doc="Fax number"
    )
    CA_FAX2 = Column(
        String(60, "SQL_Latin1_General_CP1_CI_AS"), doc="Additional fax number"
    )
    CA_ZIPCODE = Column(
        String(10, "SQL_Latin1_General_CP1_CI_AS"), doc="Zip code"
    )
    CA_PO_POSTCODE = Column(
        String(10, "SQL_Latin1_General_CP1_CI_AS"), doc="Post code"
    )
    CA_CO_POSTCODE = Column(
        Unicode(50), doc="UNKOWN: Maybe additional post code"
    )
    CA_STREET = Column(Unicode(100), doc="Street name")
    CA_STREET1 = Column(Unicode(60), doc="Additional street name")
    CA_PO_BOX = Column(
        String(10, "SQL_Latin1_General_CP1_CI_AS"), doc="Post box name"
    )
    CA_PO_BOX_LOC = Column(Unicode(40), doc="Post box location")
    CA_PO_BOX_REG = Column(
        String(3, "SQL_Latin1_General_CP1_CI_AS"), doc="Post box region"
    )
    CA_PO_BOX_CTY = Column(
        String(3, "SQL_Latin1_General_CP1_CI_AS"), doc="Post box city"
    )
    CA_HOUSE_NUM1 = Column(Unicode(10), doc="House number")
    CA_HOUSE_NUM2 = Column(Unicode(10), doc="Additional house number")
    CA_HOUSE_NUM3 = Column(Unicode(10), doc="Additional house number")
    CA_STR_SUPPL1 = Column(Unicode(40), doc="Supplier street name")
    CA_STR_SUPPL2 = Column(Unicode(40), doc="Additional supplier street name")
    CA_STR_SUPPL3 = Column(Unicode(40), doc="Additional supplier street name")
    CA_LOCATION = Column(Unicode(40), doc="Location name")
    CA_BUILDING = Column(Unicode(20), doc="Building name")
    CA_FLOOR = Column(Unicode(10), doc="Floor number")
    CA_ROOMNUMBER = Column(Unicode(10), doc="Room number")
    CA_PHONE1 = Column(
        String(60, "SQL_Latin1_General_CP1_CI_AS"),
        doc="Additional phone number",
    )
    CA_FAX1 = Column(
        String(60, "SQL_Latin1_General_CP1_CI_AS"), doc="Additional fax number"
    )
    CA_COMMENT = Column(Unicode(2000), doc="Free text comment field")
    RUN_ID = Column(Integer, doc="UNKNOWN")

    reg: Mapped[datetime] = Column(
        "CA_CREATED",
        DateTime,
        nullable=False,
        server_default=text("(getdate())"),
    )
    update: Mapped[datetime] = Column(
        "CA_UPDATED", DateTime, nullable=False, onupdate=datetime.utcnow
    )

    customer: Customer = relationship(
        "Customer", back_populates="address", uselist=False
    )


class CustomerContact(Base):
    """CustomerContact table model."""

    __tablename__ = "V_PSEX_CUSTOMER_CONTACT"

    doc = ["View on the customer contacts in the PSEX database."]

    CUC_ID: Mapped[int] = Column(Integer, primary_key=True)
    CU_ID = Column(Integer, ForeignKey("V_PSEX_CUSTOMER.CU_ID"))
    CUC_FORENAME = Column(Unicode(35), doc="First name.")
    CUC_SURNAME = Column(Unicode(35), doc="Last name.")
    CUC_PHONE = Column(Unicode(50), doc="Phone number.")
    CUC_MOBILE = Column(Unicode(50), doc="Mobile phone number.")
    CUC_FAX = Column(Unicode(50), doc="Fax number")
    CUC_MAIL = Column(Unicode(255), doc="Mail address")
    CUC_SCOPE = Column(
        Unicode(60), doc="Scope of the contact, i.e. 'Geschäftsführer'"
    )

    customer: Customer = relationship(
        "Customer", back_populates="contacts", uselist=False
    )


class DefaultItem(Base):
    """Default item (Prüfbaustein)."""

    __tablename__ = "DEFAULT_ITEM"

    doc = ["DefaultItem ('Prüfbaustein') that is used in a DefaultModule"]

    DI_ID: Mapped[int] = Column(Integer, primary_key=True)
    DI_VERSION = Column(
        Integer,
        doc="Version of the DefaultItem. Should increase with every change "
        "made.",
    )
    DI_NAME = Column(
        Unicode(100), index=True, doc="German name of the DefaultItem."
    )
    TPT_ID = Column(
        Integer, ForeignKey("V_PSEX_TEMPLATE_TYPE.TPT_ID"), index=True
    )
    TPSC_ID = Column(
        Integer, ForeignKey("V_PSEX_TEMPLATE_SCOPE.TPSC_ID"), index=True
    )
    DI_REQUIREMENT_DE = Column(
        Unicode(1500), doc="German requirement definition"
    )
    DI_REQUIREMENT_EN = Column(
        Unicode(1500), doc="English requirement definition"
    )
    DI_REQUIREMENT_FR = Column(
        Unicode(1500), doc="French requirement definition"
    )
    DI_NORM = Column(
        Unicode(512),
        doc="Normative source, i.e. 'EN 62079:2001; DIN EN 82079-1:2013 / "
        "4.8.1.2 und Tabelle 1'",
    )
    PSI_ID = Column(
        Integer,
        server_default=text("((1))"),
        doc="Used as rank ('Rangfolge') only some (~400 out of 90000) use "
        "something else than ID 1 (undefined). ForeignKey not defined!",
    )  # todo: link ForeignKey
    DI_TIME = Column(
        DECIMAL(18, 2), server_default=text("((0))"), doc="Execution time"
    )
    DI_COST = Column(
        DECIMAL(18, 2),
        server_default=text("((0))"),
        doc="Costs for the DefaultItem (currency)",
    )
    DI_TIME_MIN = Column(
        DECIMAL(18, 2),
        server_default=text("((0))"),
        doc="Minimum duration in days, only set for some (~600 out of 90000)",
    )
    DI_INFO = Column(Unicode(4000), doc="Info text")
    DI_INFO_CN = Column(Unicode(2048), doc="Chinese info text")
    TP_ID = Column(
        Integer, doc="Template,  ForeignKey not defined!"
    )  # todo: link ForeignKey
    TPER_ID = Column(
        Integer, doc="Test person,  ForeignKey not defined!"
    )  # todo: link ForeignKey
    DI_KENNWERT = Column(
        Unicode(60),
        doc="UNKNOWN: Unclear what this is, combination of the following "
        "values separated by commas: '@Five', 'a', 'd', 'f', 'g', 'i', 'k', "
        "'l', 'm', 'o', 'v', 'w', 'z', '§'",
    )
    DI_PRUEFLEVEL = Column(
        Unicode(100),
        doc="DEPRECATED: It's en empty string on 33 items, for the rest it's "
        "NULL.",
    )
    DI_TITLE = Column(
        BIT,
        server_default=text("((0))"),
        doc="Defines if the DefaultItem is a title",
    )
    DI_KEYNOTE = Column(
        BIT,
        server_default=text("((0))"),
        doc="Defines if the DefaultItem is a main item",
    )
    CL_ID = Column(
        Integer, ForeignKey("CLEARING.CL_ID"), server_default=text("((1))")
    )
    DI_CLEAR_BY = Column(
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        server_default=text("((1))"),
        doc="Person wo set the clearing state (must not be the person "
        "that actually set it but who is responsible.",
    )
    DI_CLEAR_DATE = Column(
        DateTime,
        server_default=text("(getdate())"),
        doc="Date on which the clearing state was set",
    )
    reg = Column("DI_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "DI_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
        server_default=text("((1))"),
    )
    update = Column("DI_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "DI_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    DI_MAINFEATURE = Column(
        BIT,
        server_default=text("((0))"),
        doc="Defines if the DefaultItem is a main feature",
    )
    DI_ADD = Column(
        BIT,
        server_default=text("((0))"),
        doc="Defines if the DefaultItem is an additional requirement "
        "('Zusatzanforderung')",
    )
    WST_ID = Column(
        Integer,
        server_default=text("((1))"),
        doc="DEPRECATED: Workstation id. Not used anymore in eDOC. ForeignKey "
        "not set!",
    )
    DI_DELETED: Mapped[bool] = Column(
        BIT,
        nullable=False,
        server_default=text("((0))"),
        doc="Defines if a DefaultItem is deleted. It's actually hidden in "
        "the database.",
    )
    HRC_ID = Column(
        Integer,
        ForeignKey("HR_COUNTRY.HRC_ID"),
        index=True,
        server_default=text("((1))"),
        doc="Country of the Default Item",
    )
    HRP_ID = Column(
        Integer,
        ForeignKey("HR_PRODUCT.HRP_ID"),
        index=True,
        server_default=text("((1))"),
        doc="Product of the Default Item",
    )
    DI_IS_INFO: Mapped[bool] = Column(
        BIT,
        nullable=False,
        index=True,
        server_default=text("((0))"),
        doc="Defines if the DefaultItem is an info ('Infobaustein')",
    )
    DI_SOURCE = Column(
        Integer,
        doc="DEPRECATED: It's 0 for DefaultItem with DI_ID 1, for all others "
        "the value is NULL/None",
    )
    DI_PROCEDURE = Column(
        Integer,
        doc="DEPRECATED: It's 0 for DefaultItem with DI_ID 1, for all others "
        "the value is NULL/None",
    )
    DI_TESTSAMPLE_DE = Column(
        Unicode(1000),
        doc="Defines the necessary amount of test samples for this "
        "DefaultItem in German.",
    )
    DI_TESTSAMPLE_EN = Column(
        Unicode(1000),
        doc="Defines the necessary amount of test samples for this "
        "DefaultItem in Englisch.",
    )
    DI_TESTSAMPLE_FR = Column(
        Unicode(1000),
        doc="Defines the necessary amount of test samples for this "
        "DefaultItem in French.",
    )
    REL_ID: Mapped[int] = Column(
        Integer,
        nullable=False,
        server_default=text("((1))"),
        doc="Relevance of the DefaultItem. ForeignKey not set!",
    )
    DI_NAME_EN = Column(
        Unicode(100), index=True, doc="English name of the DefaultItem."
    )
    DI_PARENT = Column(
        Integer,
        ForeignKey("DEFAULT_ITEM.DI_ID"),
        index=True,
        doc="Parent DefaultItem",
    )
    DI_OLD: Mapped[Decimal] = Column(
        MONEY,
        nullable=False,
        server_default=text("((1))"),
        doc="DEPRECATED: Is always 1",
    )
    DI_OWNER: Mapped[int] = Column(
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        nullable=False,
        server_default=text("((1))"),
        doc="Owner of the DefaultItem",
    )
    ST_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        nullable=False,
        server_default=text("((1))"),
        doc="Team for the DefaultItem",
    )
    NL_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("NAVLEVEL.NL_ID"),
        nullable=False,
        server_default=text("((1))"),
    )
    DI_PRICE_EUR = Column(
        DECIMAL(18, 2),
        doc="DEPRECATED: Price for the default item. (Marked as OLD in eDOC)",
    )
    DI_COSTITEM = Column(
        Unicode(100), doc="SAP cost item: Some string like 'PS3517'"
    )
    ND_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("NAVDOMAIN.ND_ID"),
        nullable=False,
        server_default=text("((1))"),
    )
    DI_NORM_ALT = Column(Unicode(80), doc="DEPRECATED: Normative as text")
    DI_HIDE_COL1: Mapped[bool] = Column(
        BIT,
        nullable=False,
        server_default=text("((0))"),
        doc="UNKNOWN: sets the checkbox in eDOC labelled: 'CB Unterp. "
        "ausblenden'",
    )
    DI_INSERT_STANDARD: Mapped[bool] = Column(
        BIT,
        nullable=False,
        server_default=text("((0))"),
        doc="Defines if the normative shall be inserted. Sets the checkbox in "
        "eDOC labelled: 'Norm einfügen'",
    )
    DI_TESTCODE = Column(Unicode(512), doc="UNKNOWN")
    DI_SECTION = Column(Unicode(512), doc="UNKNOWN")
    DI_PROTECTED: Mapped[bool] = Column(
        BIT,
        nullable=False,
        server_default=text("((0))"),
        doc="Protects a DefaultItem. Only set to True for DefaultItem with "
        "DI_ID 1",
    )
    DI_RESULT_DE = Column(
        Unicode(2048),
        server_default=text("(N'')"),
        doc="German result text template",
    )
    DI_RESULT_EN = Column(
        Unicode(2048),
        server_default=text("(N'')"),
        doc="English result text template",
    )
    DI_RESULT_FR = Column(
        Unicode(2048),
        server_default=text("(N'')"),
        doc="French result text template",
    )

    clearing: Clearing = relationship("Clearing", uselist=False)
    annexes: List[DefaultItemAnnex] = relationship(
        "DefaultItemAnnex", back_populates="default_item", uselist=True
    )
    customs: List[DefaultItemCustom] = relationship(
        "DefaultItemCustom", back_populates="default_item", uselist=True
    )
    pictures: List[DefaultItemPicture] = relationship(
        "DefaultItemPicture", back_populates="default_item", uselist=True
    )
    template_type: TemplateType = relationship("TemplateType", uselist=False)
    template_scope: TemplateScope = relationship(
        "TemplateScope", uselist=False
    )
    test_bases: List[DefaultItemBase] = relationship(
        "DefaultItemBase", back_populates="default_item", uselist=True
    )
    custom_list_elements: List[CustomListElement] = relationship(
        "CustomListElement", back_populates="default_item", uselist=True
    )
    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )
    level: NavLevel = relationship("NavLevel", uselist=False)
    attributes: List[DefaultItemAttribute] = relationship(
        "DefaultItemAttribute", back_populates="default_item", uselist=True
    )
    children: DefaultItem = relationship(
        "DefaultItem",
        backref=backref("parent", remote_side=[DI_ID]),
        uselist=False,
    )

    owner: Staff = relationship(
        "Staff", foreign_keys=[DI_OWNER], uselist=False
    )
    team: Staff = relationship("Staff", foreign_keys=[ST_ID], uselist=False)


class DefaultItemAnnex(Base):
    """Annex for a DefaultItem."""

    __tablename__ = "DEFAULT_ITEM_ANNEX"

    doc = ["File annex for a DefaultItem that can be copied to a protocol."]

    DIAX_ID: Mapped[int] = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, ForeignKey("DEFAULT_ITEM.DI_ID"), index=True)
    DIAX_NAME_DE = Column(Unicode(500), doc="German annex name")
    DIAX_NAME_EN = Column(Unicode(500), doc="English annex name")
    DIAX_NAME_FR = Column(Unicode(500), doc="French annex name")
    DIAX_FILENAME = Column(Unicode(255), doc="Filename of the annex")
    DIAX_CHECKSUM = Column(Unicode(32), doc="Checksum of the file")
    DIAX_DATA = deferred(Column(IMAGE, doc="File that is the annex"))
    DIAX_COPY: Mapped[bool] = Column(
        BIT,
        nullable=False,
        server_default=text("((1))"),
        doc="Flag that defines if the annex shall be copied into a protocol",
    )

    default_item: DefaultItem = relationship(
        "DefaultItem", back_populates="annexes", lazy="joined", uselist=False
    )


class DefaultItemAttribute(Base):
    """Attribute of a DefaultItem."""

    __tablename__ = "DEFAULT_ITEM_ATTRIBUTES"

    doc = ["Link between an Attribute and a DefaultItem."]

    DIA_ID: Mapped[int] = Column(Integer, primary_key=True)
    DI_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("DEFAULT_ITEM.DI_ID"),
        index=True,
        nullable=False,
        doc="It's nullable in the database, which doesn't make sense, "
        "therefore it's not nullable in TSL lib.",
    )
    ATT_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("ATTRIBUTES.ATT_ID"),
        index=True,
        nullable=False,
        doc="It's nullable in the database, which doesn't make sense, "
        "therefore it's not nullable in TSL lib.",
    )

    default_item: DefaultItem = relationship(
        "DefaultItem", back_populates="attributes", uselist=False
    )
    attribute: Attribute = relationship("Attribute", uselist=False)


class DefaultItemCustom(Base):
    """DefaultItemCustom table model."""

    __tablename__ = "DEFAULT_ITEM_CUSTOM"

    DICU_ID: Mapped[int] = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, ForeignKey("DEFAULT_ITEM.DI_ID"), index=True)
    reg: Mapped[datetime] = Column(
        "DICU_REG",
        DateTime,
        nullable=False,
        server_default=text("(getdate())"),
    )
    reg_by = Column(
        "DICU_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("DICU_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "DICU_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    CUL_ID: Mapped[int] = Column(
        Integer, ForeignKey("CUSTOM_LIST.CUL_ID"), nullable=False, index=True
    )
    CULE_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("CUSTOM_LIST_ELEMENT.CULE_ID"),
        nullable=False,
        index=True,
        server_default=text("((1))"),
    )

    custom_list: CustomList = relationship("CustomList", uselist=False)
    custom_list_element: CustomListElement = relationship(
        "CustomListElement", uselist=False
    )
    default_item: DefaultItem = relationship(
        "DefaultItem", back_populates="customs", lazy="joined", uselist=False
    )


class DefaultItemBase(Base):
    """Test base for a default item."""

    __tablename__ = "DEFAULT_ITEM_BASE"

    doc = ["Link between a TestBase and a DefaultItem"]

    DIB_ID: Mapped[int] = Column(Integer, primary_key=True)
    DI_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("DEFAULT_ITEM.DI_ID"),
        index=True,
        nullable=False,
        doc="Set to nullable in TSL database.",
    )
    B_ID: Mapped[int] = Column(
        Integer, ForeignKey("BASE.B_ID"), nullable=False
    )
    DIB_TYPE: Mapped[int] = Column(
        Integer,
        ForeignKey("BASE_TYPE.BT_ID"),
        nullable=False,
        server_default=text("((0))"),
    )
    DIB_SUBCLAUSE = Column(
        Unicode(512),
        server_default=text("(N'')"),
        doc="Subclause that is referenced in the base.",
    )
    DIB_SUBCLAUSE_MERKER = Column(
        Unicode(512),
        doc="DEPRECATED: Subclause that was referenced in the base (old).",
    )

    default_item: DefaultItem = relationship(
        "DefaultItem", back_populates="test_bases", uselist=False
    )
    test_base: TestBase = relationship("TestBase", uselist=False)


class DefaultModuleItemParameter(Base):
    """Parameter for a DefaultItem."""

    __tablename__ = "DEFAULT_MODUL_ITEM_PARAMETER"

    doc = ["Link between a DefaultModuleItem and a ModulParameter"]

    DMIP_ID: Mapped[int] = Column(Integer, primary_key=True)
    DMI_ID = Column(
        Integer, ForeignKey("DEFAULT_MODUL_ITEM.DMI_ID"), index=True
    )
    reg: Mapped[datetime] = Column(
        "DMIP_REG",
        DateTime,
        nullable=False,
        server_default=text("(getdate())"),
    )
    reg_by = Column(
        "DMIP_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("DMIP_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "DMIP_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    MP_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("MODUL_PARAMETER.MP_ID"),
        nullable=False,
        server_default=text("((1))"),
    )

    default_module_item: List[DefaultModuleItem] = relationship(
        "DefaultModuleItem", back_populates="parameters", uselist=True
    )
    parameter: ModuleParameter = relationship("ModuleParameter", uselist=False)


class DefaultItemPicture(Base):
    """Picture for a DefaultItem."""

    __tablename__ = "DEFAULT_ITEM_PICTURE"

    doc = ["Picture included in a DefaultItem."]

    DIP_ID: Mapped[int] = Column(Integer, primary_key=True)
    DI_ID = Column(Integer, ForeignKey("DEFAULT_ITEM.DI_ID"), index=True)
    DIP_NUMBER = Column(Integer, doc="Number of the picture for ordering")
    DIP_TEXT_DE = Column(Unicode(500), doc="German picture description")
    DIP_TEXT_EN = Column(Unicode(500), doc="English picture description")
    DIP_TEXT_FR = Column(Unicode(500), doc="French picture description")
    DIP_FILENAME = Column(Unicode(255), doc="Filename of the picture")
    DIP_CHECKSUM = Column(Unicode(32), doc="Checksum of the picture")
    DIP_WIDTH = Column(Integer, doc="Width")
    DIP_HEIGHT = Column(Integer, doc="Height")
    DIP_DATA = deferred(Column(IMAGE), doc="Picture data")

    default_item: DefaultItem = relationship(
        "DefaultItem", back_populates="pictures", lazy="joined", uselist=False
    )


class DefaultModule(Base):
    """Default module table model."""

    __tablename__ = "DEFAULT_MODUL"

    DM_ID: Mapped[int] = Column(Integer, primary_key=True)
    DM_VERSION = Column(
        Integer,
        doc="Version number of the DefaultModule. Should increase with every "
        "update of the DefaultModule.",
    )
    DM_ACTIVE = Column(
        BIT,
        server_default=text("((1))"),
        doc="Defines if the DefaultModule is active (still in use)",
    )
    DM_NAME: Mapped[str] = Column(
        Unicode(255),
        index=True,
        nullable=False,
        doc="German name of the DefaultModule. Set to not nullable in TSL "
        "Library.",
    )
    DM_LETTER = Column(
        Unicode(10),
        doc="Letter affix when generating the DefaultModuleItem numbers.",
    )
    HEAD_ID = Column(Integer, ForeignKey("HEADER.HEAD_ID"))
    TPT_ID = Column(
        Integer, ForeignKey("V_PSEX_TEMPLATE_TYPE.TPT_ID"), index=True
    )
    TPSC_ID = Column(
        Integer, ForeignKey("V_PSEX_TEMPLATE_SCOPE.TPSC_ID"), index=True
    )
    DM_IS_MASTER = Column(
        BIT, doc="Defines if the DefaultModule is a Master Module."
    )
    DM_COMMENT = Column(Unicode(500), doc="Free text comment.")
    CL_ID = Column(Integer, ForeignKey("CLEARING.CL_ID"))
    DM_CLEAR_BY = Column(
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        doc="Person who was responsible for the Clearing.",
    )
    DM_CLEAR_DATE = Column(
        DateTime, doc="Date on which the DefaultModule was cleared."
    )
    reg = Column("DM_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "DM_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("DM_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "DM_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    DM_TESTBASE_DE = Column(Unicode(500), doc="German test base text")
    DM_TESTBASE_EN = Column(Unicode(500), doc="Englisch test base text")
    DM_TESTBASE_FR = Column(Unicode(500), doc="French test base text")
    DM_IS_CUSTOMER = Column(
        BIT,
        server_default=text("((0))"),
        doc="Defines if DefaultModule is for Customer",
    )
    DM_IS_MARKETABILITY = Column(
        BIT,
        server_default=text("((0))"),
        doc="Defines if DefaultModule is for Marketability",
    )
    DM_IS_USABILITY = Column(
        BIT,
        server_default=text("((0))"),
        doc="Defines if DefaultModule is for Usability",
    )
    CT_ID = Column(
        Integer, ForeignKey("CALC_TYPE.CT_ID"), server_default=text("((1))")
    )
    DM_SCOPE_DE = Column(
        Unicode(length=500), doc="Scope of the DefaultModule in German"
    )
    DM_SCOPE_EN = Column(
        Unicode(length=500), doc="Scope of the DefaultModule in German"
    )
    DM_SCOPE_FR = Column(
        Unicode(length=500), doc="Scope of the DefaultModule in German"
    )
    DM_CLEAR_BY_VT = Column(
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        doc="Responsible person in sales for Clearing",
    )
    DM_CLEAR_DATE_VT = Column(DateTime, doc="Clearing date for sales")
    DM_CREATED_FOR = Column(
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        server_default=text("((1))"),
        doc="Person for whom the module was created.",
    )
    DM_CREATED_FOR_DATE = Column(
        DateTime,
        doc="Date on which the person for whom the module was created was "
        "set.",
    )
    HRC_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("HR_COUNTRY.HRC_ID"),
        nullable=False,
        index=True,
        server_default=text("((1))"),
    )
    HRP_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("HR_PRODUCT.HRP_ID"),
        nullable=False,
        index=True,
        server_default=text("((1))"),
    )
    DM_IS_INFO: Mapped[bool] = Column(
        BIT,
        nullable=False,
        server_default=text("((0))"),
        doc="UNKNOWN: sets the checkbox 'info?' in eDOC.",
    )
    DM_SOURCE = Column(Integer, doc="UNKNOWN")
    DM_PROCEDURE = Column(Integer, doc="UNKNOWN")
    DM_COMMENT_DE = Column(Unicode(1024), doc="German free text comment")
    DM_COMMENT_EN = Column(Unicode(1024), doc="German free text comment")
    DM_COMMENT_FR = Column(Unicode(1024), doc="German free text comment")
    DM_NAME_EN = Column(
        Unicode(255), index=True, doc="English name of the DefaultModule."
    )
    ND_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("NAVDOMAIN.ND_ID"),
        nullable=False,
        server_default=text("((1))"),
    )
    DM_ALIAS_DE = Column(Unicode(255), doc="German alias name.")
    DM_ALIAS_EN = Column(Unicode(255), doc="English alias name.")
    DM_PARENT = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"))
    DM_REVISION = Column(
        Unicode(60),
        doc="Revision number used by TGR when editing DefaultModules",
    )
    DM_HIDE_VALUE: Mapped[bool] = Column(
        BIT,
        nullable=False,
        server_default=text("((0))"),
        doc="UNKNOWN: Used to hide the 'Wertespalte'",
    )
    DM_TSL_VERIFIED: Mapped[bool] = Column(
        BIT,
        nullable=False,
        server_default=text("((0))"),
        doc="DEPRECATED: Introduced on our request, but doesn't do what it "
        "should.",
    )
    DM_TSL_COMMENT = Column(
        Unicode(1024),
        doc="DEPRECATED: Introduced on our request, but doesn't do what it "
        "should.",
    )

    children: DefaultModule = relationship(
        "DefaultModule",
        backref=backref("parent", remote_side=[DM_ID]),
        uselist=False,
    )
    nav_domain: NavDomain = relationship("NavDomain", uselist=False)
    attributes: List[DefaultModuleAttribute] = relationship(
        "DefaultModuleAttribute", back_populates="default_module", uselist=True
    )
    header: Header = relationship("Header", uselist=False)
    items: List[DefaultModuleItem] = relationship(
        "DefaultModuleItem",
        back_populates="default_module",
        order_by="DefaultModuleItem.DMI_NUMBER",
        uselist=True,
    )

    calculations: List[DefaultModuleCalc] = relationship(
        "DefaultModuleCalc", back_populates="default_module", uselist=True
    )
    template_type: TemplateType = relationship("TemplateType", uselist=False)
    template_scope: TemplateScope = relationship(
        "TemplateScope", uselist=False
    )
    links: DefaultModuleLink = relationship(
        "DefaultModuleLink", back_populates="default_module", uselist=False
    )
    test_bases: DefaultModuleTestBase = relationship(
        "DefaultModuleTestBase", uselist=False
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )
    clearing: Clearing = relationship("Clearing", uselist=False)

    history: List["DefaultModuleHistory"] = relationship(
        "DefaultModuleHistory", back_populates="default_module", uselist=True
    )

    tf_user: Staff = relationship(
        "Staff", foreign_keys=[DM_CLEAR_BY], uselist=False
    )
    vt_user: Staff = relationship(
        "Staff", foreign_keys=[DM_CLEAR_BY_VT], uselist=False
    )
    created_for_user: Staff = relationship(
        "Staff", foreign_keys=[DM_CREATED_FOR], uselist=False
    )


class DefaultModuleAttribute(Base):
    """Attribute of a DefaultModule."""

    __tablename__ = "DEFAULT_MODUL_ATTRIBUTES"

    doc = ["Links an Attribute to a DefaultModule."]

    DMA_ID: Mapped[int] = Column(Integer, primary_key=True)
    DM_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("DEFAULT_MODUL.DM_ID"),
        index=True,
        nullable=False,
        doc="Set to not nullable in TSL lib.",
    )
    ATT_ID: Mapped[int] = Column(
        Integer, ForeignKey("ATTRIBUTES.ATT_ID"), nullable=False
    )

    default_module: DefaultModule = relationship(
        "DefaultModule", back_populates="attributes", uselist=False
    )
    attribute: Attribute = relationship("Attribute", uselist=False)


class DefaultModuleTestBase(Base):
    """TestBase for a DefaultModule."""

    __tablename__ = "DEFAULT_MODUL_BASE"

    doc = [
        "Link between a TestBase and a DefaultModule. "
        "The link is classified by the TestBaseType."
    ]

    DMB_ID: Mapped[int] = Column(Integer, primary_key=True)
    DM_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("DEFAULT_MODUL.DM_ID"),
        index=True,
        nullable=False,
        doc="Set to not nullable in TSL lib.",
    )
    B_ID: Mapped[int] = Column(
        Integer, ForeignKey("BASE.B_ID"), nullable=False
    )
    DMB_TYPE: Mapped[int] = Column(
        Integer,
        ForeignKey("BASE_TYPE.BT_ID"),
        nullable=False,
        server_default=text("((0))"),
    )

    test_base_type: TestBaseType = relationship("TestBaseType", uselist=False)
    test_base: TestBase = relationship("TestBase", uselist=False)
    default_module: DefaultModule = relationship(
        "DefaultModule", back_populates="test_bases", uselist=False
    )


class DefaultModuleCalc(Base):
    """Calculation for a DefaultModule."""

    __tablename__ = "DEFAULT_MODUL_CALC"

    doc = ["Calculation for a DefaultModule."]

    DMC_ID: Mapped[int] = Column(Integer, primary_key=True)
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"), index=True)
    WST_ID = Column(
        Integer,
        doc="Workstation the DefaultModule is executed on. "
        "ForeignKey not set.",
    )  # todo: add foreign key
    DMC_TASK = Column(Unicode(500), doc="Task text for the calculation")
    DMC_TIME_HOURS = Column(
        Float(53),
        server_default=text("((0))"),
        doc="Execution time in hours (time the tester will spend working "
        "on this DefaultModule)",
    )
    DMC_TIME_DAYS = Column(
        Float(53),
        server_default=text("((1))"),
        doc="Execution time in days (time the DefaultModule is worked on in "
        "the laboratory).",
    )
    DMC_COSTS = Column(
        DECIMAL(18, 2),
        server_default=text("((0))"),
        doc="Additional costs for the DefaultModule's execution.",
    )
    DMC_TRAVEL = Column(
        DECIMAL(18, 2),
        server_default=text("((0))"),
        doc="Travel costs when executing the DefaultModule.",
    )
    DMC_COMMENT = Column(Unicode(500), doc="Comment for the calculation.")
    ST_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        nullable=False,
        server_default=text("((1))"),
        doc="Team that will execute the DefaultModule.",
    )
    DMC_COSTS_EXTERNAL = Column(
        DECIMAL(18, 2), server_default=text("((0))"), doc="External costs."
    )

    default_module: DefaultModule = relationship(
        "DefaultModule", back_populates="calculations", uselist=False
    )
    team: Staff = relationship("Staff", uselist=False)


class DefaultModuleHistory(Base):
    """DefaultModuleHistory."""

    __tablename__ = "MODUL_HISTORY"

    doc = ["History entry for tracking changes in a DefaultModule."]

    MH_ID: Mapped[int] = Column(Integer, primary_key=True)
    MH_COMMENT = Column(Unicode(1000), doc="Comment for the history entry")
    MH_DOCUMENT_NAME = Column(
        Unicode(255), doc="Document name of the attached document."
    )
    MH_DOCUMENT = deferred(Column(IMAGE), doc="Document attached")
    MH_CLEAR_DOCUMENT_NAME = Column(
        Unicode(255), doc="Document name of the attached clearing sheet."
    )
    MH_CLEAR_DOCUMENT = deferred(Column(IMAGE), doc="Clearing sheet attached")
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"), index=True)
    DM_VERSION = Column(
        Integer, server_default=text("((1))"), doc=DefaultModule.DM_VERSION.doc
    )
    DM_NAME = Column(Unicode(255), doc=DefaultModule.DM_NAME.doc)
    DM_LETTER = Column(Unicode(10), doc=DefaultModule.DM_LETTER.doc)
    CL_ID = Column(
        Integer, ForeignKey("CLEARING.CL_ID"), server_default=text("((1))")
    )
    DM_CLEAR_BY = Column(
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        doc=DefaultModule.DM_CLEAR_BY.doc,
    )
    DM_CLEAR_DATE = Column(DateTime, doc=DefaultModule.DM_CLEAR_DATE.doc)
    reg = Column("MH_REG", DateTime, server_default=text("(getutcdate())"))
    reg_by = Column(
        "MH_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
        server_default=text("((1))"),
    )
    update = Column("MH_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "MH_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    DM_TESTBASE_DE = Column(Unicode(500), doc=DefaultModule.DM_TESTBASE_DE.doc)
    DM_TESTBASE_EN = Column(Unicode(500), doc=DefaultModule.DM_TESTBASE_EN.doc)
    DM_TESTBASE_FR = Column(Unicode(500), doc=DefaultModule.DM_TESTBASE_FR.doc)
    DM_IS_CUSTOMER = Column(
        BIT, server_default=text("((0))"), doc=DefaultModule.DM_IS_CUSTOMER.doc
    )
    DM_IS_MARKETABILITY = Column(
        BIT,
        server_default=text("((0))"),
        doc=DefaultModule.DM_IS_MARKETABILITY.doc,
    )
    DM_IS_USABILITY = Column(
        BIT,
        server_default=text("((0))"),
        doc=DefaultModule.DM_IS_USABILITY.doc,
    )
    CT_ID = Column(
        Integer,
        ForeignKey("CALC_TYPE.CT_ID"),
        server_default=text("((1))"),
        doc=DefaultModule.CT_ID.doc,
    )
    DM_SCOPE_DE = Column(Unicode(500), doc=DefaultModule.DM_SCOPE_DE.doc)
    DM_SCOPE_EN = Column(Unicode(500), doc=DefaultModule.DM_SCOPE_EN.doc)
    DM_SCOPE_FR = Column(Unicode(500), doc=DefaultModule.DM_SCOPE_FR.doc)
    DM_CLEAR_BY_VT = Column(
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        doc=DefaultModule.DM_CLEAR_BY_VT.doc,
    )
    DM_CLEAR_DATE_VT = Column(DateTime, doc=DefaultModule.DM_CLEAR_DATE_VT.doc)
    DM_CREATED_FOR = Column(
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        server_default=text("((1))"),
        doc=DefaultModule.DM_CREATED_FOR.doc,
    )
    DM_CREATED_FOR_DATE = Column(
        DateTime, doc=DefaultModule.DM_CREATED_FOR_DATE.doc
    )
    DM_REVISION = Column(Unicode(60), doc=DefaultModule.DM_REVISION.doc)

    default_module: DefaultModule = relationship(
        "DefaultModule", back_populates="history", uselist=False
    )
    clearing: Clearing = relationship("Clearing", uselist=False)
    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )
    tf_user: Staff = relationship(
        "Staff", foreign_keys=[DM_CLEAR_BY], uselist=False
    )
    vt_user: Staff = relationship(
        "Staff", foreign_keys=[DM_CLEAR_BY_VT], uselist=False
    )
    created_for_user: Staff = relationship(
        "Staff", foreign_keys=[DM_CREATED_FOR], uselist=False
    )


class DefaultModuleItem(Base):
    """DefaultModuleItem (Link between DefaultModule and DefaultItem)."""

    __tablename__ = "DEFAULT_MODUL_ITEM"

    doc = ["Links DefaultItems to a DefaultModule"]

    DMI_ID: Mapped[int] = Column(Integer, primary_key=True)
    # keys of DefaultItem and DefaultModule are nullable in database,
    # but the item isn't useful without
    DM_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("DEFAULT_MODUL.DM_ID"),
        nullable=False,
        index=True,
        doc="Set to not nullable in TSL Library.",
    )
    DI_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("DEFAULT_ITEM.DI_ID"),
        nullable=False,
        index=True,
        doc="Set to not nullable in TSL Library.",
    )
    DMI_NUMBER: Mapped[int] = Column(
        Integer,
        nullable=False,
        doc="Order of the items within the DefaultModule. Set to not nullable "
        "in TSL Library.",
    )
    # nullable in DB, but never NULL and also useless when NULL
    DMI_INDENT: Mapped[int] = Column(
        Integer,
        nullable=False,
        doc="Indentation of the DefaultItem in the DefaultModule. Set to not "
        "nullable in TSL Library.",
    )
    DMI_KENNWERT = Column(
        Unicode(255), doc="UNKNOWN: Same values as DEFAULT_ITEM.DI_KENNWERT"
    )
    DMI_PRUEFLEVEL = Column(
        Unicode(100),
        doc="UNKNOWN: Old links to NavLevel? Values used are 2, 3, 4 and 5 "
        "and combinations separated by commas.",
    )
    DMI_TITLE = Column(
        BIT, doc="Defines if the DefaultItem shall be treated as a title."
    )
    reg = Column("DMI_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "DMI_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("DMI_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "DMI_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    WST_ID = Column(
        Integer,
        server_default=text("((1))"),
        doc="Workstation the DefaultModuleItem is executed on. ForeignKey "
        "not set.",
    )  # todo: Check if ForeignKey
    ST_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        nullable=False,
        server_default=text("((1))"),
        doc="UNKNOWN: We don't know what the team is used for at this place.",
    )
    DMI_FACTOR = Column(
        DECIMAL(18, 2),
        server_default=text("((1))"),
        doc="Faktor of the price.",
    )
    DMI_PRICE = Column(
        DECIMAL(18, 2),
        doc="Specific price for the DefaultItem within the DefaultModule",
    )

    default_module: DefaultModule = relationship(
        "DefaultModule", back_populates="items", uselist=False
    )
    default_item: DefaultItem = relationship("DefaultItem", uselist=False)

    parameters: List[DefaultModuleItemParameter] = relationship(
        "DefaultModuleItemParameter",
        back_populates="default_module_item",
        uselist=True,
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class DefaultModuleLink(Base):
    """Link of a DefaultModule."""

    __tablename__ = "DEFAULT_MODUL_LINK"

    doc = [
        "Defines a link (i.e. web link) providing additional information "
        "to a DefaultModule."
    ]

    DML_ID: Mapped[int] = Column(Integer, primary_key=True)
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"), index=True)
    # the next four columns are never NULL, so we set the not nullable
    DML_TEXT_DE: Mapped[str] = Column(
        Unicode(1024), nullable=False, doc="German link description"
    )
    DML_TEXT_EN: Mapped[str] = Column(
        Unicode(1024), nullable=False, doc="English link description"
    )
    DML_TEXT_FR: Mapped[str] = Column(
        Unicode(1024), nullable=False, doc="French link description"
    )
    DML_URL: Mapped[str] = Column(
        Unicode(512), nullable=False, doc="Url for the link"
    )
    update = Column("DML_UPDATE", DateTime, server_default=text("(getdate())"))
    update_by = Column(
        "DML_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )

    default_module: DefaultModule = relationship(
        "DefaultModule", back_populates="links", uselist=False
    )

    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class Edoc(Base):
    """eDOC model."""

    __tablename__ = "EDOC"

    E_ID: Mapped[int] = Column(Integer, primary_key=True)
    E_VERSION = Column(
        Integer,
        default=1,
        doc="Version number of the protocol. Should/must be increased by "
        "1 when saving changes.",
    )
    # E_NAME is nullable in database, but never actually NULL
    E_NAME: Mapped[str] = Column(
        Unicode(255),
        index=True,
        nullable=False,
        doc="Name of the protocol. Set to not nullable in TSL-Lib since "
        "there's no sense in a protocol without name.",
    )
    # default header is "Modulvorlage Standard" from HEADER table
    HEAD_ID = Column(
        Integer, ForeignKey("HEADER.HEAD_ID"), server_default=text("(6)")
    )
    E_YN_SYMBOL = Column(
        BIT,
        server_default=text("((1))"),
        doc="Defines if Y/N is used for the protocol or P/F.",
    )
    reg = Column("E_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "E_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("E_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "E_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    NP_ID = Column(Integer, ForeignKey("NAV_PACK.NP_ID"))
    E_REMINDER = Column(Integer, doc="UNKNOWN")
    E_ANNEX = Column(Unicode(4000), doc="UNKNOWN")
    E_TABLE = Column(Unicode(4000), doc="UNKNOWN")

    package: Package = relationship(
        "Package", back_populates="edocs", uselist=False
    )
    header: Header = relationship("Header", uselist=False)
    phases: List["EdocPhase"] = relationship(
        "EdocPhase", back_populates="edoc", uselist=True
    )
    modules: List["EdocModule"] = relationship(
        "EdocModule",
        back_populates="edoc",
        order_by="EdocModule.EM_NUMBER",
        uselist=True,
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )
    items: EdocModuleItem = relationship(
        "EdocModuleItem", back_populates="edoc", uselist=True
    )
    project: Project = relationship(
        "Project", back_populates="edoc", uselist=False
    )


class EdocModuleItem(Base):
    """ModulItem in an eDOC protocol (Prüfbaustein)."""

    __tablename__ = "EDOC_MODUL_ITEM"

    EMI_ID: Mapped[int] = Column(Integer, primary_key=True)
    EMI_VERSION = Column(Integer)
    EMI_NUMBER = Column(Integer)
    E_ID = Column(Integer, ForeignKey("EDOC.E_ID"))
    EM_ID = Column(Integer, ForeignKey("EDOC_MODUL.EM_ID"))
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"))
    DI_ID = Column(Integer, ForeignKey("DEFAULT_ITEM.DI_ID"))
    DI_VERSION = Column(Integer)
    EMI_REQUIREMENT_DE: Mapped[str] = Column(
        NullUnicode(length=1500), nullable=False, default=""
    )
    EMI_REQUIREMENT_EN: Mapped[str] = Column(
        NullUnicode(length=1500), nullable=False, default=""
    )
    EMI_REQUIREMENT_FR: Mapped[str] = Column(
        NullUnicode(length=1500), nullable=False, default=""
    )
    # column is nullable in db, but actually never is. there are 6 items
    # without indent, but they are from 2009/2010
    EMI_INDENT: Mapped[int] = Column(Integer, nullable=False)
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
    reg = Column("EMI_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "EMI_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("EMI_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "EMI_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    EMI_MAINFEATURE = Column(Boolean)
    ST_ID = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    NL_ID = Column(Integer, ForeignKey("NAVLEVEL.NL_ID"))

    edoc: Edoc = relationship("Edoc", back_populates="items", uselist=False)
    edoc_module: EdocModule = relationship(
        "EdocModule", back_populates="items", uselist=False
    )
    default_module: DefaultModule = relationship(
        "DefaultModule", uselist=False
    )
    default_item: DefaultItem = relationship("DefaultItem", uselist=False)
    nav_level: NavLevel = relationship("NavLevel", uselist=False)
    phase_results: List[EdocModuleItemPhase] = relationship(
        "EdocModuleItemPhase", back_populates="edoc_module_item", uselist=True
    )
    comparisons: List[EdocModuleItemComparison] = relationship(
        "EdocModuleItemComparison", back_populates="item", uselist=True
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class EdocModuleItemComparison(Base):
    """Comparison table for EdocModuleItems."""

    __tablename__ = "EDOC_MODUL_ITEM_COMPARISON"

    EMIC_ID: Mapped[int] = Column(Integer, primary_key=True)
    EMI_ID = Column(Integer, ForeignKey("EDOC_MODUL_ITEM.EMI_ID"))
    EM_ID = Column(Integer, ForeignKey("EDOC_MODUL.EM_ID"))
    EMIC_ORDER = Column(Integer)
    EMIC_TEXT_DE = Column(Unicode(length=500))
    EMIC_TEXT_EN = Column(Unicode(length=500))
    EMIC_TEXT_FR = Column(Unicode(length=500))
    reg = Column("EMIC_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "EMIC_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("EMIC_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "EMIC_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )

    module: EdocModule = relationship("EdocModule", uselist=False)
    item: EdocModuleItem = relationship(
        "EdocModuleItem", back_populates="comparisons", uselist=False
    )


class EdocModuleItemComparisonPhase(Base):
    """Comparison table for EdocModuleItems."""

    __tablename__ = "EDOC_MODUL_ITEM_COMPARISON_PHASE"

    EMICP_ID: Mapped[int] = Column(Integer, primary_key=True)
    EMIC_ID = Column(Integer, ForeignKey("EDOC_MODUL_ITEM_COMPARISON.EMIC_ID"))
    EMI_ID = Column(Integer, ForeignKey("EDOC_MODUL_ITEM.EMI_ID"))
    EM_ID = Column(Integer, ForeignKey("EDOC_MODUL.EM_ID"))
    PRP_ID = Column(
        Integer, ForeignKey("V_PSEX_PROCESSPHASE.PRP_ID"), default=1
    )
    EMICP_TEXT_DE = Column(Unicode(length=500), default="")
    EMICP_TEXT_EN = Column(Unicode(length=500), default="")
    EMICP_TEXT_FR = Column(Unicode(length=500), default="")
    ER_ID = Column(Integer, ForeignKey("EDOCRESULT.ER_ID"), default=1)
    update = Column("ER_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "ER_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )

    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class EdocModuleItemPhase(Base):
    """Phase result for an EdocModulItem."""

    __tablename__ = "EDOC_MODUL_ITEM_PHASE"

    EMIP_ID: Mapped[int] = Column(Integer, primary_key=True)
    EM_ID = Column(Integer, ForeignKey("EDOC_MODUL.EM_ID"))
    EMI_ID = Column(Integer, ForeignKey("EDOC_MODUL_ITEM.EMI_ID"))
    PRP_ID = Column(Integer, ForeignKey("V_PSEX_PROCESSPHASE.PRP_ID"))
    EMIP_RESULT_DE = Column(Unicode(length=2048), default="")
    EMIP_RESULT_EN = Column(Unicode(length=2048), default="")
    EMIP_RESULT_FR = Column(Unicode(length=2048), default="")
    EMIP_COMMENT = Column(Unicode(length=500), default="")
    EMIP_READY = Column(Boolean, default=False)
    ER_ID = Column(Integer, ForeignKey("EDOCRESULT.ER_ID"), default=1)
    EMIP_HANDLEDBY = Column(
        Integer, ForeignKey("V_PSEX_STAFF.ST_ID"), default=1
    )
    EMIP_HINT = Column(Boolean, default=False)
    reg = Column("EMIP_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "EMIP_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("EMIP_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "EMIP_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    WST_ID = Column(Integer)  # todo: add ForeignKey
    SO_NUMBER = Column(Integer)
    ST_ID = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"), default=1)
    EMIP_IS_COPY: Mapped[bool] = Column(Boolean, nullable=False, default=False)

    edoc_module: EdocModule = relationship("EdocModule", uselist=False)
    edoc_module_item: EdocModuleItem = relationship(
        "EdocModuleItem", back_populates="phase_results", uselist=False
    )
    phase: ProcessPhase = relationship("ProcessPhase", uselist=False)
    handleby: Staff = relationship(
        "Staff", foreign_keys=[EMIP_HANDLEDBY], uselist=False
    )
    result: EdocResult = relationship("EdocResult", uselist=False)
    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class EdocModuleItemPhaseAnnex(Base):
    """Module for an annex of an eDOC phase."""

    __tablename__ = "EDOC_MODUL_ITEM_PHASE_ANNEX"

    EMIPA_ID: Mapped[int] = Column(Integer, primary_key=True)
    EMIP_ID = Column(Integer, ForeignKey("EDOC_MODUL_ITEM_PHASE.EMIP_ID"))
    EMIPA_NAME_DE = Column(Unicode(length=500))
    EMIPA_NAME_EN = Column(Unicode(length=500))
    EMIPA_NAME_FR = Column(Unicode(length=500))
    EMIPA_FILENAME = Column(Unicode(length=255))
    EMIPA_CHECKSUM = Column(Unicode(length=32))
    EMIPA_DATA = Column(LargeBinary)
    reg = Column("EMIPA_UPLOAD", DateTime, onupdate=datetime.utcnow)
    reg_by = Column(
        "EMIPA_UPLOAD_BY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )

    edoc_module_item_phase: EdocModuleItemPhase = relationship(
        "EdocModuleItemPhase", uselist=False
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )


class EdocModuleItemPicture(Base):
    """Picture for an EdocModuleItem."""

    __tablename__ = "EDOC_MODUL_ITEM_PICTURE"

    EMIPC_ID: Mapped[int] = Column(Integer, primary_key=True)
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

    edoc_module_item: EdocModuleItem = relationship(
        "EdocModuleItem", uselist=False
    )
    edoc_module: EdocModule = relationship("EdocModule", uselist=False)


class EdocModulePhase(Base):
    """Phase for an EdocModule."""

    __tablename__ = "EDOC_MODUL_PHASE"

    EMP_ID: Mapped[int] = Column(Integer, primary_key=True)
    E_ID = Column(Integer, ForeignKey("EDOC.E_ID"))
    EM_ID = Column(Integer, ForeignKey("EDOC_MODUL.EM_ID"))
    # PRP_ID can't be null as this will surely break eDOC, it's nullable in
    # the DB tough
    PRP_ID: Mapped[int] = Column(
        Integer, ForeignKey("V_PSEX_PROCESSPHASE.PRP_ID"), nullable=False
    )
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

    edoc_module: EdocModule = relationship(
        "EdocModule", back_populates="phases", uselist=False
    )


class EdocModule(Base):
    """Module table model."""

    __tablename__ = "EDOC_MODUL"

    EM_ID: Mapped[int] = Column(Integer, primary_key=True)
    E_ID = Column(Integer, ForeignKey("EDOC.E_ID"))
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"))
    DM_VERSION = Column(Integer)
    # there is no module in the db that is NULL, name can be empty tough
    EM_NAME: Mapped[str] = Column(Unicode(length=255), nullable=False)
    EM_LETTER = Column(Unicode(length=10))
    EM_NUMBER = Column(Integer)
    SO_NUMBER = Column(Integer)
    EM_OFFLINE_BY = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    EM_OFFLINE_SINCE = Column(DateTime)
    reg = Column("EM_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "EM_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("EM_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "EM_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    EM_FILTER_LEVEL = Column(Unicode(length=100))
    EM_FILTER_PARAM = Column(Unicode(length=512))
    EM_FILTER_ITEMS = Column(Unicode(length=2048))

    edoc: Edoc = relationship("Edoc", back_populates="modules", uselist=False)
    default_module: DefaultModule = relationship(
        "DefaultModule", uselist=False
    )
    offline_by: Staff = relationship(
        "Staff", foreign_keys=[EM_OFFLINE_BY], uselist=False
    )
    phases: List[EdocModulePhase] = relationship(
        "EdocModulePhase", back_populates="edoc_module", uselist=True
    )
    items: List[EdocModuleItem] = relationship(
        "EdocModuleItem", back_populates="edoc_module", uselist=True
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )

    @validates(
        "EM_NAME",
        "EM_LETTER",
        "EM_FILTER_LEVEL",
        "EM_FILTER_PARAM",
        "EM_FILTER_ITEMS",
    )
    def validate_str(self, key: str, value: str) -> str:
        """Validate and if necessary truncate a str value."""
        max_len = getattr(self.__class__, key).prop.columns[0].type.length
        if value and len(value) > max_len:
            log.warning(
                "Truncating string by %s characters: %s",
                len(value) - max_len,
                value,
            )
            return value[:max_len]
        return value


class EdocPhase(Base):
    """eDOC phase model."""

    __tablename__ = "EDOC_PHASE"

    EP_ID: Mapped[int] = Column(Integer, primary_key=True)
    E_ID = Column(Integer, ForeignKey("EDOC.E_ID"))
    PRP_ID = Column(
        Integer, ForeignKey("V_PSEX_PROCESSPHASE.PRP_ID"), default=1
    )
    P_ID = Column(Integer, ForeignKey("V_PSEX_PROJECT.P_ID"))
    P_ID_2 = Column(Integer, ForeignKey("V_PSEX_PROJECT.P_ID"))
    SO_NUMBER: Mapped[int] = Column(Integer, nullable=False, default=0)
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

    edoc: Edoc = relationship("Edoc", back_populates="phases", uselist=False)
    project: Project = relationship(
        "Project", foreign_keys=[P_ID], uselist=False
    )
    importer_project: Project = relationship(
        "Project", foreign_keys=[P_ID_2], uselist=False
    )
    result: EdocResult = relationship(
        "EdocResult", foreign_keys=[ER_ID], uselist=False
    )
    usability_result: EdocResult = relationship(
        "EdocResult", foreign_keys=[EP_USABILITY_RESULT], uselist=False
    )
    marketability_result: EdocResult = relationship(
        "EdocResult", foreign_keys=[EP_MARKETABILITY_RESULT], uselist=False
    )
    process_phase: ProcessPhase = relationship("ProcessPhase", uselist=False)


class EdocResult(Base):
    """EdocResult model."""

    __tablename__ = "EDOCRESULT"

    ER_ID: Mapped[int] = Column(Integer, primary_key=True)
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
    reg = Column("ER_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "ER_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("ER_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "ER_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    ER_SHOW_IN_PROOF = Column(Boolean)

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class Header(Base):
    """Header for a Module."""

    __tablename__ = "HEADER"

    HEAD_ID: Mapped[int] = Column(Integer, primary_key=True)
    HEAD_ACTIVE = Column(Boolean)
    HEAD_FILENAME = Column(Unicode(length=255))
    HEAD_NAME = Column(Unicode(length=120))
    HEAD_DATA = deferred(Column(LargeBinary))
    reg = Column("HEAD_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "HEAD_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("HEAD_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "HEAD_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    HEAD_DEFAULT_PROTOCOL = Column(Boolean)
    HEAD_DEFAULT_REPORT = Column(Boolean)
    HEAD_NAME_EN = Column(Unicode(length=120))

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class KindOfTest(Base):
    """Kind of test."""

    __tablename__ = "V_PSEX_KIND_OF_TEST"

    KOT_ID: Mapped[int] = Column(Integer, primary_key=True)
    KOT_NAME_DE = Column(Unicode(length=256))
    KOT_NAME_EN = Column(Unicode(length=256))
    KOT_NAME_FR = Column(Unicode(length=256))
    WORKING_CLUSTER = Column(Unicode(length=36))
    HR_SHORT = Column(Unicode(length=20))


class ModuleParameter(Base):
    """ModuleParameter."""

    __tablename__ = "MODUL_PARAMETER"

    MP_ID: Mapped[int] = Column(Integer, primary_key=True)
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"))
    MP_PARAMETER_DE = Column(Unicode(length=256))
    MP_PARAMETER_EN = Column(Unicode(length=256))
    reg = Column("MP_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "MP_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("MP_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "MP_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class NavCountModuleExport(Base):
    """Count for module exports."""

    __tablename__ = "NAV_COUNT_MODULEEXPORT"

    NCM_ID: Mapped[int] = Column(Integer, primary_key=True)
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"))
    NCM_TYPE = Column(Integer)
    reg = Column("NCM_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "NCM_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )

    default_module: DefaultModule = relationship(
        "DefaultModule", uselist=False
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )


class NavDomain(Base):
    """Domain of a Navigation/Module."""

    __tablename__ = "NAVDOMAIN"

    ND_ID: Mapped[int] = Column(Integer, primary_key=True)
    # names are never null in the database
    ND_SHORT: Mapped[str] = Column(Unicode(length=10), nullable=False)
    ND_NAME_DE: Mapped[str] = Column(Unicode(length=100), nullable=False)
    ND_NAME_EN: Mapped[str] = Column(Unicode(length=100), nullable=False)
    reg = Column("ND_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "ND_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    ND_ORDER = Column(Integer)
    ND_ORDER_EXPORT: Mapped[int] = Column(Integer, nullable=False)
    ND_ORDER_PLAN_DEFAULT: Mapped[int] = Column(Integer, nullable=False)

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )


class Navigation(Base):
    """Navigation table model."""

    __tablename__ = "NAV"

    N_ID: Mapped[int] = Column(Integer, primary_key=True)
    N_TEMPLATE = Column(Integer)
    N_NAME_DE = Column(Unicode(length=120))
    N_NAME_EN = Column(Unicode(length=120))
    BEGR_ID = Column(Integer)  # not clear what this is
    N_COMMENT_DE = Column(Unicode(length=500))
    N_COMMENT_EN = Column(Unicode(length=500))
    N_DURATION = Column(Integer)
    N_MASTER: Mapped[bool] = Column(Boolean, nullable=False)
    HR_NEW_ID: Mapped[int] = Column(
        Integer, nullable=False
    )  # not clear what this is
    HRC_ID: Mapped[int] = Column(
        Integer, ForeignKey("HR_COUNTRY.HRC_ID"), nullable=False
    )
    HRP_ID: Mapped[int] = Column(
        Integer, ForeignKey("HR_PRODUCT.HRP_ID"), nullable=False
    )
    ZM_OBJECT = Column(Unicode(length=5))
    KOT_ID: Mapped[int] = Column(
        Integer, ForeignKey("V_PSEX_KIND_OF_TEST.KOT_ID"), nullable=False
    )
    reg = Column("N_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "N_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("N_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "N_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )

    packages: List["Package"] = relationship(
        "Package", back_populates="navigation"
    )

    country: Country = relationship("Country", uselist=False)
    product: Product = relationship("Product", uselist=False)
    kind_of_test: KindOfTest = relationship("KindOfTest", uselist=False)

    nav_saves: NavSave = relationship(
        "NavSave", back_populates="navigation", uselist=False
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )

    @property
    def lidl_phasen(self) -> List["Package"]:
        """Return the LIDL phasen services."""
        # convert the name to a str since it could be None
        return [
            pack
            for pack in self.packages
            if "lidl" in str(pack.NP_NAME_DE).lower()
            and "phasen" in str(pack.NP_NAME_DE).lower()
        ]

    def default_zara_product(self) -> str:
        """Calculate the default ZaraProduct."""
        log.debug("Calculation ZaraProduct for Navigation %s", self.N_ID)
        products: Dict[str, int] = defaultdict(int)
        for package in self.packages:
            assert package.ZM_PRODUCT
            products[package.ZM_PRODUCT] += 1

        if products["T10"] > products["T20"]:
            log.debug("ZaraProduct is T10")
            return "T10"
        log.debug("ZaraProduct is T20")
        return "T20"

    def calculations(self) -> List["PackageElementCalculation"]:
        """Return all PackageElementCalculation."""
        calcs = (
            Session.object_session(self)
            .query(PackageElementCalculation)
            .join(PackageElement)
            .join(Package)
            .filter(Package.N_ID == self.N_ID)
            .all()
        )
        return cast(List[PackageElementCalculation], calcs)


class NavEdoc(Base):
    """Edoc template model."""

    __tablename__ = "NAV_EDOC"

    NE_ID: Mapped[int] = Column(Integer, primary_key=True)
    NE_NAME: Mapped[str] = Column(Unicode(length=255), nullable=False)
    HEAD_ID = Column(Integer, ForeignKey("HEADER.HEAD_ID"), default=1)
    NE_RANDOM: Mapped[int] = Column(Integer, nullable=False)
    ST_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        nullable=False,
        default=get_user_id,
    )
    P_ID = Column(Integer, ForeignKey("V_PSEX_PROJECT.P_ID"))


class NavEdocModule(Base):
    """EdocModule template model."""

    __tablename__ = "NAV_EDOC_MODULE"

    NEM_ID: Mapped[int] = Column(Integer, primary_key=True)
    NE_RANDOM: Mapped[int] = Column(Integer, nullable=False)
    DM_ID: Mapped[int] = Column(
        Integer, ForeignKey("DEFAULT_MODUL.DM_ID"), nullable=False
    )
    ST_ID: Mapped[int] = Column(
        Integer, ForeignKey("V_PSEX_STAFF.ST_ID"), nullable=False, default=1
    )
    NE_NUMBER = Column(Integer)


class NavEdocModuleItem(Base):
    """EdocModuleItem template model."""

    __tablename__ = "NAV_EDOC_MODULE_ITEM"

    NEMI_ID: Mapped[int] = Column(Integer, primary_key=True)
    NE_RANDOM: Mapped[int] = Column(Integer, nullable=False)
    DM_ID: Mapped[int] = Column(
        Integer, ForeignKey("DEFAULT_MODUL.DM_ID"), nullable=False
    )
    DI_ID: Mapped[int] = Column(
        Integer, ForeignKey("DEFAULT_ITEM.DI_ID"), nullable=False
    )
    NEMI_INDENT: Mapped[int] = Column(Integer, nullable=False, default=0)
    DMI_ID: Mapped[int] = Column(
        Integer, ForeignKey("DEFAULT_MODUL_ITEM.DMI_ID"), nullable=False
    )
    NE_NUMBER = Column(Integer)


class NavLevel(Base):
    """Level of a PackageElement."""

    __tablename__ = "NAVLEVEL"

    NL_ID: Mapped[int] = Column(Integer, primary_key=True)
    NL_LEVEL: Mapped[int] = Column(Integer, unique=True, nullable=False)
    NL_NAME_DE: Mapped[str] = Column(Unicode(length=30), nullable=False)
    NL_NAME_EN: Mapped[str] = Column(Unicode(length=30), nullable=False)


class NavPosition(Base):
    """NavPosition (Rechnungsposition)."""

    __tablename__ = "NAVPOSITION"

    NPOS_ID: Mapped[int] = Column(Integer, primary_key=True)
    NPOS_POSITION = Column(Integer)
    NPOS_TEXT_DE = Column(Unicode(length=2048))
    NPOS_TEXT_EN = Column(Unicode(length=2048))
    reg = Column("NPOS_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "NPOS_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("NPOS_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "NPOS_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class NavSave(Base):
    """Navigation Save model (called Auswahl in Navigator)."""

    __tablename__ = "NAV_SAVE"

    NS_ID: Mapped[int] = Column(Integer, primary_key=True)
    NS_COMMENT = Column(Unicode(length=512))
    N_ID = Column(Integer, ForeignKey("NAV.N_ID", ondelete="CASCADE"))
    P_ID = Column(Integer, ForeignKey("V_PSEX_PROJECT.P_ID"))
    E_ID = Column(Integer, ForeignKey("EDOC.E_ID"))
    # the names could be null, but are never in the db.
    NS_NAME_DE: Mapped[str] = Column(Unicode(length=256), nullable=False)
    NS_NAME_EN: Mapped[str] = Column(Unicode(length=256), nullable=False)
    NS_CRM = Column(Unicode(length=256))
    NS_TYPE: Mapped[int] = Column(Integer, nullable=False)
    reg = Column("NS_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "NS_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )

    navigation: Navigation = relationship(
        "Navigation", back_populates="nav_saves", uselist=False
    )
    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    project: Project = relationship("Project", uselist=False)

    save_calculations: NavSaveCalculation = relationship(
        "NavSaveCalculation", back_populates="nav_save", uselist=False
    )
    selections: List[NavSaveSelection] = relationship(
        "NavSaveSelection", back_populates="nav_save", uselist=True
    )

    @property
    def nav_save_type(self) -> "NavSaveType":
        """Return the NavSaveType for the NavSave object."""
        assert isinstance(self.NS_TYPE, int)
        return NavSaveType(self.NS_TYPE)

    @nav_save_type.setter
    def nav_save_type(self, value: "NavSaveType") -> None:
        """Set the NavSaveType for the NavSave object."""
        self.NS_TYPE = value.value  # pylint: disable=invalid-name


class NavSaveCalculation(Base):
    """Calculation data for a NavSave."""

    __tablename__ = "NAV_SAVE_CALC"

    NSC_ID: Mapped[int] = Column(Integer, primary_key=True)
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
    ST_ID: Mapped[int] = Column(
        Integer, ForeignKey("V_PSEX_STAFF.ST_ID"), nullable=False
    )
    NSC_COSTS_EXTERNAL = Column(Numeric(precision=18, scale=2))

    nav_save: NavSave = relationship(
        "NavSave", back_populates="save_calculations", uselist=False
    )
    calculation: PackageElementCalculation = relationship(
        "PackageElementCalculation", uselist=False
    )
    user: Staff = relationship("Staff", uselist=False)
    nav_position: NavPosition = relationship("NavPosition", uselist=False)


class NavSaveSelection(Base):
    """Selection for a NavSave."""

    __tablename__ = "NAV_SAVE_SELECTION"

    NSS_ID: Mapped[int] = Column(Integer, primary_key=True)
    NS_ID = Column(Integer, ForeignKey("NAV_SAVE.NS_ID"))
    NP_ID = Column(Integer, ForeignKey("NAV_PACK.NP_ID"))

    nav_save: NavSave = relationship(
        "NavSave", back_populates="selections", uselist=False
    )
    package: Package = relationship(
        "Package", back_populates="selections", uselist=False
    )


class NavSaveType(IntEnum):
    """Values for the different NavSaveTypes."""

    MANUAL = 1
    PROJECT = 2
    OFFER = 3
    OPPORTUNITY = 4


class Package(Base):
    """Package table model."""

    __tablename__ = "NAV_PACK"

    NP_ID: Mapped[int] = Column(Integer, primary_key=True)
    N_ID = Column(Integer, ForeignKey("NAV.N_ID", ondelete="CASCADE"))
    NP_NAME_DE: Mapped[str] = Column(
        NullUnicode(length=150), nullable=False, default=""
    )
    NP_NAME_EN = Column(Unicode(length=150))
    NP_COMMENT_DE = Column(Unicode(length=800))
    NP_COMMENT_EN = Column(Unicode(length=800))
    CL_ID: Mapped[int] = Column(
        Integer, ForeignKey("CLEARING.CL_ID"), nullable=False
    )
    NP_CLEARDATE = Column(DateTime)
    NP_CLEARBY = Column(Integer)
    ZM_PRODUCT = Column(Unicode(length=5))
    PT_ID: Mapped[int] = Column(
        Integer, ForeignKey("PACKAGE_TYPE.PT_ID"), nullable=False
    )
    NP_TESTSAMPLES: Mapped[int] = Column(Integer, nullable=False)
    NP_IS_TEMPLATE: Mapped[bool] = Column(Boolean, nullable=False)
    NP_TEMPLATE_ID = Column(Integer, ForeignKey("NAV_PACK.NP_ID"))
    reg = Column("NP_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "NP_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("NP_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "NP_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    PN_ID: Mapped[int] = Column(
        Integer, ForeignKey("PACKAGE_NAME.PN_ID"), nullable=False
    )

    clearing_state: Clearing = relationship("Clearing", uselist=False)

    package_elements: List[PackageElement] = relationship(
        "PackageElement",
        back_populates="package",
        cascade="all, delete",
        uselist=True,
    )

    navigation: Navigation = relationship(
        "Navigation", back_populates="packages", uselist=False
    )

    service_classes: List[ServiceClass] = relationship(
        "ServiceClass",
        back_populates="package",
        cascade="all, delete",
        uselist=True,
    )

    package_type: PackageType = relationship("PackageType", uselist=False)

    package_name: PackageName = relationship("PackageName", uselist=False)

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )
    selections: NavSaveSelection = relationship(
        "NavSaveSelection", back_populates="package", uselist=False
    )
    edocs: List[Edoc] = relationship(
        "Edoc", back_populates="package", uselist=True
    )

    created_from: Package = relationship(
        "Package",
        backref=backref("template", remote_side=[NP_ID]),
        uselist=False,
    )


class PackageCategory(Base):
    """Category of a Package (linked to the type)."""

    __tablename__ = "PACKAGE_CAT"

    PC_ID: Mapped[int] = Column(Integer, primary_key=True)
    PC_NAME_DE = Column(Unicode(length=50))
    PC_NAME_EN = Column(Unicode(length=50))
    reg = Column("PC_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "PC_REG_BY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )


class PackageElement(Base):
    """Package element table model."""

    __tablename__ = "NAV_PACK_ELEMENT"

    NPE_ID: Mapped[int] = Column(Integer, primary_key=True)
    NP_ID = Column(Integer, ForeignKey("NAV_PACK.NP_ID", ondelete="CASCADE"))
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"))
    NL_ID = Column(Integer, ForeignKey("NAVLEVEL.NL_ID"))
    ZM_LOCATION = Column(Unicode(length=5))
    NPE_CREATE = Column(Boolean)
    CT_ID = Column(Integer, ForeignKey("CALC_TYPE.CT_ID"))
    reg = Column("NPE_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "NPE_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("NPE_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "NPE_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    NPE_CREATE_SO: Mapped[bool] = Column(Boolean, nullable=False)

    package: Package = relationship(
        "Package", back_populates="package_elements", uselist=False
    )
    package_calculations: List[PackageElementCalculation] = relationship(
        "PackageElementCalculation",
        back_populates="package_element",
        cascade="all, delete",
        uselist=True,
    )
    proof_elements: List[ProofElement] = relationship(
        "ProofElement",
        cascade="all, delete",
        back_populates="package_element",
        uselist=True,
    )

    default_module: DefaultModule = relationship(
        "DefaultModule", uselist=False
    )

    level: NavLevel = relationship("NavLevel", uselist=False)
    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )
    filters: List[PackageElementFilter] = relationship(
        "PackageElementFilter", back_populates="package_element", uselist=True
    )


class PackageElementCalculation(Base):
    """Calculation data for a PackageElement."""

    __tablename__ = "NAV_PACK_ELEMENT_CALC"

    NPEC_ID: Mapped[int] = Column(Integer, primary_key=True)
    NPE_ID = Column(
        Integer, ForeignKey("NAV_PACK_ELEMENT.NPE_ID", ondelete="CASCADE")
    )
    ST_ID: Mapped[int] = Column(
        Integer, ForeignKey("V_PSEX_STAFF.ST_ID"), nullable=False
    )
    NPEC_DELTA_START = Column(Float)
    NPEC_TIME_DAYS = Column(Integer)
    NPEC_TIME_HOURS: Mapped[Decimal] = Column(
        Float, nullable=False, default=0.0
    )
    NPEC_RATE = Column(Numeric(precision=18, scale=2))
    NPEC_COSTS = Column(Numeric(precision=18, scale=2))
    NPEC_TRAVEL = Column(
        Numeric(precision=18, scale=2),
    )
    NPEC_FACTOR = Column(Float)
    NPEC_PRICE = Column(Numeric(precision=18, scale=2))
    NPEC_COMMENT = Column(Unicode(length=500))
    NPEC_TASK: Mapped[str] = Column(
        NullUnicode(length=500), nullable=False, default=""
    )
    ZM_ID = Column(Unicode(length=50))
    NPOS_ID = Column(Integer, ForeignKey("NAVPOSITION.NPOS_ID"))
    reg = Column("NPEC_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "NPEC_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("NPEC_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "NPEC_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    CBC_ID = Column(Integer)
    NPEC_COSTS_EXTERNAL = Column(Numeric(precision=18, scale=2))
    NPEC_COSTS_OLD = Column(Numeric(precision=18, scale=2))
    NPEC_COSTS_EXTERNAL_OLD = Column(Numeric(precision=18, scale=2))

    package_element: PackageElement = relationship(
        "PackageElement", back_populates="package_calculations", uselist=False
    )

    nav_position: NavPosition = relationship("NavPosition", uselist=False)

    team: Staff = relationship("Staff", foreign_keys=[ST_ID], uselist=False)
    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class PackageElementFilter(Base):
    """Filter for a PackageElement."""

    __tablename__ = "NAV_PACK_ELEMENT_FILTER"

    NPEF_ID: Mapped[int] = Column(Integer, primary_key=True)
    NPE_ID: Mapped[int] = Column(
        Integer,
        ForeignKey("NAV_PACK_ELEMENT.NPE_ID", ondelete="CASCADE"),
        nullable=False,
    )
    DMI_ID: Mapped[int] = Column(
        Integer, ForeignKey("DEFAULT_MODUL_ITEM.DMI_ID"), nullable=False
    )
    reg = Column("NPEF_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "NPEF_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )

    package_element: PackageElement = relationship(
        "PackageElement", back_populates="filters", uselist=False
    )
    default_module_item: DefaultModuleItem = relationship(
        "DefaultModuleItem", uselist=False
    )


class PackageName(Base):
    """Name of a Package."""

    __tablename__ = "PACKAGE_NAME"

    PN_ID: Mapped[int] = Column(Integer, primary_key=True)
    PN_NAME_DE = Column(Unicode(length=255))
    PN_NAME_EN = Column(Unicode(length=255))
    reg = Column("PN_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "PN_REG_BY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("PN_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "PN_UPDATE_BY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class PackageType(Base):
    """Type of a Package."""

    __tablename__ = "PACKAGE_TYPE"

    PT_ID: Mapped[int] = Column(Integer, primary_key=True)
    PT_NAME_DE = Column(Unicode(length=255))
    PT_NAME_EN = Column(Unicode(length=255))
    reg = Column("PT_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "PT_REG_BY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    PC_ID = Column(Integer, ForeignKey("PACKAGE_CAT.PC_ID"))

    package_category: PackageCategory = relationship(
        "PackageCategory", uselist=False
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )


class PriceList(Base):
    """Pricelist model."""

    __tablename__ = "PRICELIST"

    PL_ID: Mapped[int] = Column(Integer, primary_key=True)
    PL_SHORT = Column(Unicode(length=10))
    PL_NAME_DE = Column(Unicode(length=100))
    PL_NAME_EN = Column(Unicode(length=100))
    CUR_ID = Column(Unicode(length=3))
    PL_ORDER = Column(Integer)
    reg = Column("PL_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "PL_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("PL_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "PL_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    PL_TYPE = Column(Integer)
    PL_FACTOR_CC = Column(Numeric(precision=18, scale=5))
    PL_FACTOR_PROFIT = Column(Numeric(precision=18, scale=5))

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class Process(Base):
    """Process table model."""

    __tablename__ = "V_PSEX_PROCESS"

    PC_ID: Mapped[int] = Column(Integer, primary_key=True, nullable=False)
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
    PC_KEY2 = Column(Unicode(length=16))
    PC_KEY3 = Column(Unicode(length=16))

    projects: List[Project] = relationship(
        "Project", back_populates="process", uselist=True
    )

    @property
    def process_archive(self) -> str:
        """Return the full path to the process archive of the Process."""
        assert self.PC_PATH is not None
        return os.path.join(PATH, "PSEX", self.PC_PATH)


class ProcessPhase(Base):
    """ProcessPhase Model."""

    __tablename__ = "V_PSEX_PROCESSPHASE"

    PRP_ID: Mapped[int] = Column(Integer, primary_key=True)
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
    PRP_EDOC_SHORT_DE: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )
    PRP_EDOC_SHORT_EN: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )
    PRP_EDOC_SHORT_FR: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )
    PRP_EDOC_NUMBER = Column(Integer)
    PRP_EDOC_IS_REFERENCE = Column(Boolean)
    PRP_EDOC_IS_DEFAULT = Column(Boolean)


class Product(Base):
    """Products."""

    __tablename__ = "HR_PRODUCT"

    HRP_ID: Mapped[int] = Column(Integer, primary_key=True)
    HRP_LEFT = Column(Integer)
    HRP_RIGHT = Column(Integer)
    HRP_INDENT = Column(Integer)
    HRP_NAME_DE = Column(Unicode(length=255))
    HRP_NAME_EN = Column(Unicode(length=255))
    HRP_NAME_FR = Column(Unicode(length=255))
    update = Column("HRP_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "HRP_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )

    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class Project(Base):
    """PSE PROJECT (view on PSE database)."""

    __tablename__ = "V_PSEX_PROJECT"

    P_ID: Mapped[int] = Column(Integer, primary_key=True, nullable=False)
    P_FOLDER = Column(Unicode(length=256))
    P_PRODUCT: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )
    P_MODEL: Mapped[str] = Column(
        NullUnicode(length=256), nullable=False, default=""
    )
    PC_ID = Column(Integer, ForeignKey("V_PSEX_PROCESS.PC_ID"))
    P_DATE_DONE = Column(DateTime)
    P_PREDATE = Column(DateTime)
    P_DEADLINE = Column(DateTime)
    P_DATE_ORDER = Column(DateTime)
    MD_ID: Mapped[int] = Column(Integer, nullable=False)
    P_CUSTOMER_A = Column(Integer, ForeignKey("V_PSEX_CUSTOMER.CU_ID"))
    P_CUSTOMER_B = Column(Integer, ForeignKey("V_PSEX_CUSTOMER.CU_ID"))
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
    CATEGORY_ID: Mapped[int] = Column(Integer, nullable=False)
    E_ID = Column(Integer, ForeignKey("EDOC.E_ID"))
    P_CONTACT_CUC_ID = Column(
        Integer, ForeignKey("V_PSEX_CUSTOMER_CONTACT.CUC_ID")
    )
    P_REMARK = Column(Unicode(length=1024))
    BATCH_NUMBER = Column(Unicode(length=16))
    P_RETEST: Mapped[int] = Column(Integer, nullable=False)
    P_RETEST_OF = Column(Integer)

    customer_contact: CustomerContact = relationship(
        "CustomerContact", uselist=False
    )
    ordering_party_address: Customer = relationship(
        "Customer", foreign_keys=[P_CUSTOMER_A], uselist=False
    )
    manufacturer_address: Customer = relationship(
        "Customer", foreign_keys=[P_CUSTOMER_B], uselist=False
    )
    process: Process = relationship(
        "Process", back_populates="projects", uselist=False
    )
    project_manager: Staff = relationship(
        "Staff", foreign_keys=[P_PROJECTMANAGER], uselist=False
    )
    project_handler: Staff = relationship(
        "Staff", foreign_keys=[P_HANDLEDBY], uselist=False
    )
    register_user: Staff = relationship(
        "Staff", foreign_keys=[P_REGBY], uselist=False
    )
    kind_of_test: KindOfTest = relationship("KindOfTest", uselist=False)
    sub_orders: SubOrder = relationship(
        "SubOrder", back_populates="project", uselist=False
    )
    edoc: Edoc = relationship("Edoc", back_populates="project", uselist=False)

    @property
    def project_folder(self) -> str:
        """Return the full path to the project folder of the Project."""
        assert self.P_FOLDER is not None
        return os.path.join(PATH, self.P_FOLDER)


class ProofElement(Base):
    """Proof Element of a Package."""

    __tablename__ = "NAV_PACK_ELEMENT_PROOF"

    NPEP_ID: Mapped[int] = Column(Integer, primary_key=True)
    NPE_ID = Column(
        Integer, ForeignKey("NAV_PACK_ELEMENT.NPE_ID", ondelete="CASCADE")
    )
    NPEP_TYPE = Column(Integer)
    NPR_ID = Column(Integer)
    NPEP_TEXT_DE = Column(Unicode(length=255))
    NPEP_TEXT_EN = Column(Unicode(length=255))
    reg = Column("NPEP_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "NPEP_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("NPEP_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "NPEP_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )

    package_element: PackageElement = relationship(
        "PackageElement", back_populates="proof_elements", uselist=False
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class ServiceClass(Base):
    """Service Class of a Package."""

    doc = [
        "Defines the service class of a Package by creating a link between "
        "the Package and the ServiceClassDefinition"
    ]

    __tablename__ = "NAV_PACK_SERVICECLASS"

    NPS_ID: Mapped[int] = Column(Integer, primary_key=True)
    NP_ID = Column(
        Integer, ForeignKey("NAV_PACK.NP_ID", ondelete="CASCADE"), index=True
    )
    SCL_ID = Column(Integer, ForeignKey("SERVICECLASS.SCL_ID"))

    package: Package = relationship(
        "Package", back_populates="service_classes", uselist=False
    )
    definition: ServiceClassDefinition = relationship(
        "ServiceClassDefinition", uselist=False
    )


class ServiceClassDefinition(Base):
    """Definitions for the service class."""

    __tablename__ = "SERVICECLASS"

    SCL_ID: Mapped[int] = Column(Integer, primary_key=True)
    SCL_LEVEL: Mapped[int] = Column(Integer, nullable=False)
    SCL_REMARK_DE = Column(Unicode(length=500))
    SCL_REMARK_EN = Column(Unicode(length=500))
    reg = Column("SCL_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "SCL_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("SCL_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "SCL_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class Staff(Base):
    """Staff table model."""

    __tablename__ = "V_PSEX_STAFF"

    ST_ID: Mapped[int] = Column(Integer, primary_key=True)
    ST_SURNAME: Mapped[str] = Column(Unicode(length=60), nullable=False)
    # ST_FORENAME is nullable in database, but never actually NULL
    ST_FORENAME: Mapped[str] = Column(Unicode(length=50), nullable=False)
    ST_COSTID = Column(Unicode(length=10))
    ST_ACTIVE: Mapped[bool] = Column(Boolean, nullable=False)
    ST_NUMBER = Column(Unicode(length=8))
    ST_SHORT = Column(Unicode(length=3))
    ST_PHONE = Column(Unicode(length=40))
    ST_FAX = Column(Unicode(length=40))
    ST_EMAIL = Column(Unicode(length=80))
    ST_WINDOWSID = Column(Unicode(length=32))
    ST_TEAM: Mapped[Optional[str]] = Column(
        UNIQUEIDENTIFIER, ForeignKey("V_PSEX_HIERARCHY.HR_ID")
    )
    ST_TYPE: Mapped[int] = Column(Integer, nullable=False)
    ST_LOCATION = Column(Unicode(length=50))
    ST_UNIT = Column(Unicode(length=12))
    ST_SERVERID = Column(Integer)
    ST_HOURS_PER_DAY = Column(Integer)
    ST_SKILLGROUP: Mapped[str] = Column(Unicode(length=8), nullable=False)
    ST_DOMAIN = Column(Unicode(length=32))
    ST_GENDER = Column(Unicode(length=50))

    @property
    def full_name(self) -> str:
        """Get the user's full name."""
        assert isinstance(self.ST_SURNAME, str)
        full_name = self.ST_SURNAME
        if self.ST_FORENAME:
            full_name += ", "
            full_name += self.ST_FORENAME
        return full_name

    team: Optional[Team] = relationship(
        "Team", uselist=False, back_populates="users"
    )


class StatisticModule(Base):
    """Statistic Module."""

    __tablename__ = "STATISTIC_MODULE"

    STAM_ID: Mapped[int] = Column(Integer, primary_key=True)
    ST_ID = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    DM_ID = Column(Integer, ForeignKey("DEFAULT_MODUL.DM_ID"))
    STAT_ID = Column(Integer, ForeignKey("STATISTIC_TYPE.STAT_ID"))
    STAM_REG = Column(DateTime)

    statistic_type: StatisticType = relationship(
        "StatisticType", uselist=False
    )


class StatisticType(Base):
    """Statistic Type."""

    __tablename__ = "STATISTIC_TYPE"

    STAT_ID: Mapped[int] = Column(Integer, primary_key=True)
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

    P_ID: Mapped[int] = Column(
        Integer, ForeignKey("V_PSEX_PROJECT.P_ID"), primary_key=True
    )
    SO_NUMBER: Mapped[int] = Column(Integer, primary_key=True)
    SO_DISPOBY = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    SO_CREATED = Column(DateTime)
    ST_ID = Column(Integer, ForeignKey("V_PSEX_STAFF.ST_ID"))
    SO_DEADLINE = Column(DateTime)
    SO_TASK: Mapped[str] = Column(
        NullUnicode(length=1024), nullable=False, default=""
    )
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

    project: Project = relationship(
        "Project", back_populates="sub_orders", uselist=False
    )
    dispo_user: Staff = relationship(
        "Staff", foreign_keys=[SO_DISPOBY], uselist=False
    )
    user: Staff = relationship("Staff", foreign_keys=[ST_ID], uselist=False)
    team: Staff = relationship(
        "Staff", foreign_keys=[ST_ID_TEAM], uselist=False
    )
    update_team: Staff = relationship(
        "Staff", foreign_keys=[SO_UPDATEBY_TEAM], uselist=False
    )
    reg_team: Staff = relationship(
        "Staff", foreign_keys=[SO_REGBY_TEAM], uselist=False
    )
    ready_team: Staff = relationship(
        "Staff", foreign_keys=[SO_READYBY_TEAM], uselist=False
    )
    dispo_team: Staff = relationship(
        "Staff", foreign_keys=[SO_DISPOBY_TEAM], uselist=False
    )
    check_team: Staff = relationship(
        "Staff", foreign_keys=[SO_CHECKBY_TEAM], uselist=False
    )


class Team(Base):
    """Staff table model."""

    __tablename__ = "V_PSEX_HIERARCHY"

    HR_ID: Mapped[str] = Column(UNIQUEIDENTIFIER, primary_key=True)
    HR_SHORT: Mapped[str] = Column(Unicode(20))
    HR_NEW_ID: Mapped[int] = Column(Integer, nullable=False)
    ST_ID: Mapped[int] = Column(Integer)

    HR_TYPE: Mapped[str] = Column(Unicode(50))
    HR_PARENT: Mapped[str] = Column(UNIQUEIDENTIFIER)
    HR_LOCATION: Mapped[str] = Column(Unicode(40))
    HR_PREFIX: Mapped[str] = Column(Unicode(20))
    HR_ACTIVE: Mapped[bool] = Column(BIT, nullable=False)
    HR_CURRENT: Mapped[bool] = Column(BIT)
    HR_EMAIL: Mapped[str] = Column(String(80, "SQL_Latin1_General_CP1_CI_AS"))
    CC_ID: Mapped[str] = Column(String(10, "SQL_Latin1_General_CP1_CI_AS"))

    users: List[Staff] = relationship(
        Staff, uselist=True, back_populates="team"
    )

    sub_locations: List[TeamSublocation] = relationship(
        "TeamSublocation", uselist=True, back_populates="team"
    )


class TeamSublocation(Base):
    """Sublocation of a team."""

    __tablename__ = "V_TEAM_SUBLOCATION"

    ST_ID: Mapped[int] = Column(Integer, primary_key=True)
    ST_SURNAME: Mapped[str] = Column(Unicode(length=60), nullable=False)
    ST_TEAM = Column(UNIQUEIDENTIFIER, ForeignKey("V_PSEX_HIERARCHY.HR_ID"))
    Sublocation = Column(Unicode(length=6))  # is always NULL as of 16.10.2020

    @property
    def name(self) -> Optional[str]:
        """Return the name of the team."""
        return self.ST_SURNAME

    team: Team = relationship(
        "Team", uselist=False, back_populates="sub_locations"
    )


class TemplateScope(Base):
    """TemplateScope table model."""

    __tablename__ = "V_PSEX_TEMPLATE_SCOPE"

    TPSC_ID: Mapped[int] = Column(Integer, primary_key=True, nullable=False)
    TPSC_NAME_DE: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPSC_NAME_EN: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPSC_NAME_FR: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPSC_SHORT_DE: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPSC_SHORT_EN: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPSC_SHORT_FR: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPSC_PATH: Mapped[str] = Column(Unicode(length=256), nullable=False)


class TemplateType(Base):
    """TemplateType."""

    __tablename__ = "V_PSEX_TEMPLATE_TYPE"

    TPT_ID: Mapped[int] = Column(Integer, primary_key=True)
    TPT_NAME_DE: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_NAME_EN: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_NAME_FR: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_SHORT_DE: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_SHORT_EN: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_SHORT_FR: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_PATH: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_PREFIX: Mapped[str] = Column(Unicode(length=256), nullable=False)
    TPT_MODULETYPE = Column(Unicode(length=256))
    TPT_SHOWINPROZESSFOLDER: Mapped[bool] = Column(Boolean, nullable=False)
    TPT_SHOWINTEMPLATEMANAGER: Mapped[bool] = Column(Boolean, nullable=False)


class TestBase(Base):
    """TestBase model."""

    __tablename__ = "BASE"

    B_ID: Mapped[int] = Column(Integer, primary_key=True)
    B_NAME_DE = Column(Unicode(length=512))
    B_NAME_EN = Column(Unicode(length=512))
    B_NAME_FR = Column(Unicode(length=512))
    DI_ID = Column(Integer, ForeignKey("DEFAULT_ITEM.DI_ID"))
    BT_ID = Column(Integer, ForeignKey("BASE_TYPE.BT_ID"))
    PLK_SHORT = Column(Unicode(length=10))
    reg = Column("B_REG", DateTime, default=datetime.utcnow)
    reg_by = Column(
        "B_REGBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        default=get_user_id,
    )
    update = Column("B_UPDATE", DateTime, onupdate=datetime.utcnow)
    update_by = Column(
        "B_UPDATEBY",
        Integer,
        ForeignKey("V_PSEX_STAFF.ST_ID"),
        onupdate=get_user_id,
    )
    HRC_ID: Mapped[int] = Column(
        Integer, ForeignKey("HR_COUNTRY.HRC_ID"), nullable=False
    )
    B_PARENT = Column(Integer, ForeignKey("BASE.B_ID"))
    B_SHORT_DE = Column(Unicode(length=512))
    B_SHORT_EN = Column(Unicode(length=512))
    B_SHORT_FR = Column(Unicode(length=512))
    B_DOW = Column(DateTime)
    B_COMMENT_DE = Column(Unicode(length=512))
    B_COMMENT_EN = Column(Unicode(length=512))
    B_COMMENT_FR = Column(Unicode(length=512))
    B_DOA: Mapped[int] = Column(Integer, nullable=False)

    test_base_type: TestBaseType = relationship("TestBaseType", uselist=False)

    reg_user: Staff = relationship(
        "Staff", foreign_keys=[reg_by], uselist=False
    )
    update_user: Staff = relationship(
        "Staff", foreign_keys=[update_by], uselist=False
    )


class TestBaseType(Base):
    """Type of a TestBase."""

    __tablename__ = "BASE_TYPE"

    BT_ID: Mapped[int] = Column(Integer, primary_key=True)
    BT_SHORT = Column(Unicode(length=6))
    BT_NAME_DE = Column(Unicode(length=50))
    BT_NAME_EN = Column(Unicode(length=50))
    BT_NAME_FR = Column(Unicode(length=50))
    GT_ID = Column(Integer)  # todo: Add ForeignKey


class ZaraObject(Base):
    """Zara Object table model."""

    __tablename__ = "V_PSEX_ZOBJECT"

    ZM_PRIMARY_FAKE: Mapped[int] = Column(Integer, primary_key=True)
    ZM_OBJECT = Column(Unicode(length=5))
    ZM_OBJECT_NAME = Column(Unicode(length=255))
    ZM_OBJECT_LANGUAGE = Column(Unicode(length=2))


class ZaraProduct(Base):
    """Zara Product table model."""

    __tablename__ = "V_PSEX_ZPRODUCT"

    ZM_PRIMARY_FAKE: Mapped[int] = Column(Integer, primary_key=True)
    ZM_PRODUCT = Column(Unicode(length=5))
    ZM_PROUDCT_NAME = Column(Unicode(length=255))
    ZM_PRODUCT_LANGUAGE = Column(Unicode(length=2))
