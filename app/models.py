from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.database import Base

class MagazineInfo(Base):
    __tablename__ = "magazine_info"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_date = Column(Date)
    category = Column(String)

    content = relationship("MagazineContent", back_populates="magazine", uselist=False)

class MagazineContent(Base):
    __tablename__ = "magazine_content"

    id = Column(Integer, primary_key=True, index=True)
    magazine_id = Column(Integer, ForeignKey("magazine_info.id"))
    content = Column(Text)
    vector_representation = Column(Vector(1536))  # Correct usage

    magazine = relationship("MagazineInfo", back_populates="content")
