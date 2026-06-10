from .auteur import Auteur
from .base import Base
from .details import Details
from .livre import Livre
from .genres import Genre

from sqlalchemy import Column, Integer, String, Table, ForeignKey

livres_genres = Table(
	"livres_genres",
	Base.metadata,
	Column("livre_id", Integer, ForeignKey("livres.livre_id"), primary_key=True),
	Column("genre_id", Integer, ForeignKey("genres.genre_id"), primary_key=True)
)