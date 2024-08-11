import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.common.db.database import Base


class Image(Base):
    __tablename__ = 'image'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    recording_time: Mapped[datetime.datetime] = mapped_column(DateTime())
    size: Mapped[str] = mapped_column(String(50))
