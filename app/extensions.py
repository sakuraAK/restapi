from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from abc import abstractmethod, ABC
from .config import Config as config
import os
from sqlalchemy import String, DateTime, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship, DeclarativeBase
from sqlalchemy.sql import func




class Base(DeclarativeBase):
    def to_dict(self):
        """Return a dictionary representation of this model."""
        ret_data = {}
        columns = self.__table__.columns.keys()
        for c in columns:
            ret_data[c] = getattr(self, c)
        return ret_data

class Course(Base):
    __tablename__ = "course"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    updated_on: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # posted_by: Mapped[int] = mapped_column(ForeignKey(""))
    # user: Mapped["User"] = relationship(back_populates="")

class DbWrapper(ABC):
    def __init__(self):
        self.set_engine()
        self._session = None
        self.setup()

    @abstractmethod
    def set_engine(self):
        pass

    @abstractmethod
    def setup(self):
        pass

    @property
    def session(self):
        if self._session == None:
            self._session = Session(self._engine)
        return self._session



class SqlAlchemyWrapper(DbWrapper):
    # def __enter__(self):
    #     return self
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self._session.close()
    def __init__(self, db_file_path):
        self._path = db_file_path
        super().__init__()

    def set_engine(self):
        self._engine = create_engine("sqlite:///" + self._path)



    def setup(self):
        if os.path.exists(self._path):
            return
        Base.metadata.create_all(self._engine)

db = SqlAlchemyWrapper(config.DB_FILE_PATH)