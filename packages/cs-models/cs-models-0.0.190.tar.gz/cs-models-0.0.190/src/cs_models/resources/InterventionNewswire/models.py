from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from ...database import Base


class InterventionNewswireModel(Base):
    __tablename__ = "intervention_newswires"

    id = Column(Integer, primary_key=True)
    news_id = Column(
        Integer,
        ForeignKey('newswires.id'),
        nullable=False,
    )
    norm_cui = Column(String(50), nullable=False, index=True)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
