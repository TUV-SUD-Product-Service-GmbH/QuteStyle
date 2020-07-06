"""Database connection and models for the PSE database."""
from sqlalchemy import create_engine, Column, Integer, Unicode, DateTime
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
