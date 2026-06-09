from .base import Base
from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class DetailJeu(Base):
	__tablename__ = "details_jeux"

	# La clé primaire est aussi une clé étrangère => on force le 1:1
	jeu_id = Column(Integer, ForeignKey("jeux.jeu_id"), primary_key=True)

	deescription = Column(Text)
	note_metacritic = Column(Integer)
	multijoueur = Column(Boolean, default=False)

	# Relation inverse One-to-One
	jeu = relationship("Jeu", back_populates="details")