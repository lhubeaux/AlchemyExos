from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from Exercice1.dal.models.base import Base

SERVER = r"GOSVDI208\TFTIC"
DATABASE = "AlchemyDemo"

CONNECTION_STRING = (
	f"mssql+pyodbc://@{SERVER}/{DATABASE}"
	"?driver=ODBC+Driver+18+for+SQL+Server"
	"&trusted_connection=yes"
	"&TrustServerCertificate=yes"
)

engine = create_engine(CONNECTION_STRING, echo=True)

session_local = sessionmaker(autocommit=False ,autoflush=False ,bind=engine)

def get_session():
	return session_local()

def init_db(delete=False):
	if delete:
		Base.metadata.drop_all(bind=engine)
		print("❌ - Toutes les tables on été supprimées.")
	Base.metadata.create_all(bind=engine)
	print("✅ - Tables créées / mise à jour.")

def test_connexion():
	try:
		with engine.connect() as conn:
			conn.execute(text("SELECT 1"))
			print("✅ Connexion établie à SQL Server 😊")
			return True
	except Exception as e:
		print(f"❌ Erreur de connexion : {e}")
		return False
	
def table_creation():
	Base.metada.create(bind=engine)