from Exercice1.dal.models import Jeu, DetailJeu
from Exercice1.dal.database import get_session, init_db, test_connexion


def main():
	print("=" * 20)

	if not test_connexion():
		return

	init_db()

	print("=" * 20)

if __name__ == "__main__":
	main()