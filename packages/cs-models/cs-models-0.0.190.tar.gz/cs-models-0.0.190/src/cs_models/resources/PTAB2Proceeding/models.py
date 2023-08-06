from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
)
from datetime import datetime

from ...database import Base


class PTAB2ProceedingModel(Base):
    __tablename__ = 'ptab2_proceedings'

    id = Column(Integer, primary_key=True)
    accorded_filing_date = Column(DateTime)
    max_document_date = Column(DateTime)
    decision_date = Column(DateTime)
    institution_decision_date = Column(DateTime)
    petitioner_application_number_text = Column(String(256))
    petitioner_counsel_name = Column(String(256))
    petitioner_grant_date = Column(DateTime)
    petitioner_group_art_unit_number = Column(String(20))
    petitioner_inventor_name = Column(String(100))
    petitioner_party_name = Column(String(256))
    petitioner_patent_number = Column(String(20))
    petitioner_patent_owner_name = Column(String(256))
    petitioner_technology_center_number = Column(String(256))
    proceeding_filing_date = Column(DateTime)
    proceeding_last_modified_date = Column(DateTime)
    proceeding_number = Column(String(20), nullable=False, unique=True, index=True)
    proceeding_status_category = Column(String(100))
    proceeding_type_category = Column(String(100))
    respondent_application_number_text = Column(String(100))
    respondent_counsel_name = Column(String(100))
    respondent_grant_date = Column(DateTime)
    respondent_group_art_unit_number = Column(String(20))
    respondent_inventor_name = Column(String(100))
    respondent_party_name = Column(String(256))
    respondent_patent_number = Column(String(20), index=True)
    respondent_patent_owner_name = Column(String(256))
    respondent_technology_center_number = Column(String(20))
    subproceeding_type_category = Column(String(20))
    proceeding_status = Column(String(100))
    appealed = Column(Boolean)
    respondent_subsidiary_id = Column(
        Integer,
        ForeignKey('subsidiaries.id'),
        nullable=True,
    )
    petitioner_subsidiary_id = Column(
        Integer,
        ForeignKey('subsidiaries.id'),
        nullable=True,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
