from sqlalchemy import String, DateTime, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship
from sqlalchemy.sql import func
from ..extensions import Base

class Course(Base):
    __tablename__ = "course"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    updated_on: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # posted_by: Mapped[int] = mapped_column(ForeignKey(""))
    # user: Mapped["User"] = relationship(back_populates="")

    def __repr__(self):
        return f"id: {self.id}; name: {self.name}"


"""
Select
Select with filter
Select where
Select filter
Select specific column


Session
Session dirty
Delete
Flush
Rollback


relationship

"""