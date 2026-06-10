from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base

class Details(Base):
    __tablename__ = "details"


    livre_id = Column(Integer, ForeignKey("livres.livre_id"), primary_key=True)
    resume = Column(Text)
    nbre_pages = Column(Integer)
    note = Column(Integer)


    livre = relationship("Livre", back_populates="details")