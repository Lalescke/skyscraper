from sqlalchemy import Column, DateTime, func

from app.core.database import Base


class BaseModel(Base):
    __abstract__ = True
    created_at = Column(DateTime(timezone=True), server_default=func.now())
