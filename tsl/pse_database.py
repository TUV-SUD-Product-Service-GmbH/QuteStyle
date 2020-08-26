"""Database connection and models for the PSE database."""
from sqlalchemy import create_engine, Column, Integer, Unicode, Float
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

STD_DB_PATH = "mssql+pyodbc://lv_edoc:hooters@psexplorerhost.muc.de.itgr.net" \
              "/PSExplorer?driver=" \
              "SQL+Server+Native+Client+11.0;MultiSubnetFailover=Yes"

ENGINE = create_engine(STD_DB_PATH, connect_args={'timeout': 25})

Base = declarative_base()
Base.metadata.bind = ENGINE

AdminSession = sessionmaker(bind=ENGINE)  # pylint: disable=invalid-name


# pylint: disable=too-few-public-methods
class Process(Base):
    """Process table model."""

    __tablename__ = 'PROCESS'

    PC_ID = Column(Integer, primary_key=True, nullable=False)
    PC_IAN = Column(Unicode(length=256))
    PC_PATH = Column(Unicode(length=50))


class Project(Base):
    """Project table model."""

    __tablename__ = 'PROJECT'

    P_ID = Column(Integer, primary_key=True, nullable=False)
    P_IAN = Column(Unicode(length=256))
    P_PRODUCT = Column(Unicode(length=256))
    P_ORDERSIZE = Column(Float)
    P_MODEL = Column(Unicode(length=256))
    P_ZARA_NUMBER = Column(Unicode(length=11))
    P_FOLDER = Column(Unicode(length=256))
    DELR_ID = Column(Integer)
    P_WC_ID = Column(UNIQUEIDENTIFIER)
    P_NAME = Column(Unicode(length=31))
    BATCH_NUMBER = Column(Unicode(length=16))
