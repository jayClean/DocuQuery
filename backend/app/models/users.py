from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    documents = relationship("DocumentMetadata", back_populates="user")


class DocumentMetadata(Base):
    __tablename__ = 'documents'
    __table_args__ = {"schema": "public"}  # Ensure the same schema is used

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    s3_url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('public.users.id'))  # Add the schema name in ForeignKey
    parsed_data = Column(Text, nullable=False)

    user = relationship("User", back_populates="documents")
