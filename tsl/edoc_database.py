"""Database connection and models for the PSE database."""
from sqlalchemy import create_engine, Column, Integer, Unicode, DateTime, \
    Boolean
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql.schema import ForeignKey

STD_DB_PATH = "mssql+pyodbc://lv_edoc:hooters@psexplorerhost.muc.de.itgr.net" \
              "/EDOC?driver=" \
              "SQL+Server+Native+Client+11.0;MultiSubnetFailover=Yes"

ENGINE = create_engine(STD_DB_PATH, connect_args={'timeout': 25})

Base = declarative_base()
Base.metadata.bind = ENGINE

AdminSession = sessionmaker(bind=ENGINE)  # pylint: disable=invalid-name


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
    ST_TEAM = Column(UNIQUEIDENTIFIER)


class Team(Base):
    """Staff table model."""

    __tablename__ = 'V_PSEX_HIERARCHY'

    HR_ID = Column(Integer, primary_key=True, nullable=False)
    HR_SHORT = Column(Unicode(length=21))


class PackageElement(Base):
    """Package element table model."""

    __tablename__ = "NAV_PACK_ELEMENT"

    NPE_ID = Column(Integer, primary_key=True, nullable=False)
    NP_ID = Column(Integer, ForeignKey('NAV_PACK.NP_ID'))
    DM_ID = Column(Integer)
    NL_ID = Column(Integer)
    ZM_LOCATION = Column(Unicode(length=5))
    NPE_CREATE = Column(Boolean)
    CT_ID = Column(Integer)
    NPE_REG = Column(DateTime)
    NPE_REGBY = Column(Integer)
    NPE_UPDATE = Column(DateTime)
    NPE_UPDATEBY = Column(Integer)
    NPE_CREATE_SO = Column(Boolean, nullable=False)

    package = relationship("Package", back_populates="package_elements")


class Package(Base):
    """Package table model."""

    __tablename__ = "NAV_PACK"

    NP_ID = Column(Integer, primary_key=True, nullable=False)
    N_ID = Column(Integer, ForeignKey('NAV.N_ID'))
    NP_NAME_DE = Column(Unicode(length=150))
    NP_NAME_EN = Column(Unicode(length=150))
    NP_COMMENT_DE = Column(Unicode(length=800))
    NP_COMMENT_EN = Column(Unicode(length=800))
    CL_ID = Column(Integer, nullable=False)
    NP_CLEARDATE = Column(DateTime)
    NP_CLEARBY = Column(Integer)
    ZM_PRODUCT = Column(Unicode(length=5))
    PT_ID = Column(Integer, nullable=False)
    NP_TESTSAMPLES = Column(Integer, nullable=False)
    NP_IS_TEMPLATE = Column(Boolean, nullable=False)
    NP_TEMPLATE_ID = Column(Integer)
    NP_REG = Column(DateTime)
    NP_REGBY = Column(Integer)
    NP_UPDATE = Column(DateTime)
    NP_UPDATEBY = Column(Integer)
    PN_ID = Column(Integer, nullable=False)

    package_elements = relationship("PackageElement")

    navigation = relationship("Navigation", back_populates="packages")


class Navigation(Base):
    """Navigation table model."""

    __tablename__ = "NAV"

    N_ID = Column(Integer, primary_key=True, nullable=False)
    N_TEMPLATE = Column(Integer)
    N_NAME_DE = Column(Unicode(length=120))
    N_NAME_EN = Column(Unicode(length=120))
    BEGR_ID = Column(Integer)
    N_COMMENT_DE = Column(Unicode(length=500))
    N_COMMENT_EN = Column(Unicode(length=500))
    N_DURATION = Column(Integer)
    N_MASTER = Column(Boolean, nullable=False)
    HR_NEW_ID = Column(Integer, nullable=False)
    HRC_ID = Column(Integer, nullable=False)
    HRP_ID = Column(Integer, nullable=False)
    ZM_OBJECT = Column(Unicode(length=5))
    KOT_ID = Column(Integer, nullable=False)
    N_REG = Column(DateTime)
    N_REGBY = Column(Integer)
    N_UPDATE = Column(DateTime)
    N_UPDATEBY = Column(Integer)

    packages = relationship("Package")
