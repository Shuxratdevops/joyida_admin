from sqlalchemy import Column, Integer, String, Boolean ,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from src.models.mod_category import Category
from src.db.database import Base

class Service(Base):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), unique=True, index=True, nullable=False)
    status = Column(Boolean, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="SET NULL"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    category = relationship("Category", back_populates="service")