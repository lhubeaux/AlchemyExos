from dal.models import Jeu, DetailJeu
from dal.database import get_session, init_db, test_connexion
from datetime import *
from decimal import Decimal
from dal.models import Jeu, DetailJeu
from sqlalchemy.orm import joinedload
from sqlalchemy import select, update
from dal.database import get_session, init_db, test_connexion
from dal.models import Developpeur, Jeu, DetailJeu, Plateforme

def seed(session):
	#création d'un dev
	nintendo = Developpeur(
		nom="Nintendo",
		pays="Japon"
	)
	session.add(nintendo)
	session.flush()		# Pour otenir mon id 

	# Création d'un jeu avec ses relations
	pokemon = Jeu(
		titre="Pokemon",
		date_sortie=date(2027,3,15),
		prix=Decimal("59.99"),
		developpeur=nintendo
	)

	pokemon.details = DetailJeu(
		description="jeu de monstre",
		note_metacritic=2,
		multijoueur=True
	)

	switch = Plateforme(
		nom="Switch",
		fabricant ="Nintendo"
	)
	pokemon.plateformes.append(switch)

	session.add(pokemon)
	session.commit()
	print("Données initiales crées avec succès 😊💦🍆")

def lire_jeux(session):
	jeux =	session.query(Jeu).options(
		joinedload(Jeu.developpeur),
		joinedload(Jeu.details),
		joinedload(Jeu.plateformes)
	).all()

	for jeu in jeux:
		print(f"\n {jeu.titre} (ID:{jeu.jeu_id})")
		print(f"   => Développeur		: {jeu.developpeur.nom if jeu.developpeur else 'N/A'}")
		print(f"   => Prix				: {jeu.prix} €")
		print(f"   => Note Metacritic	: {jeu.details.note_metacritic}/20")
		print(f"   => Platforme(s)		: {[p.nom for p in jeu.plateformes]}")

def creer_jeux(session):

		#création d'un dev
	fromsoft = Developpeur(
		nom="Fromsoft",
		pays="Japon"
	)
	session.add(fromsoft)
	session.flush()


	titre = input("Veuillez entrez le nom du jeu :\n")
	date_sortie = input("Veuillez entrer la date de sortie du jeu (format: AAAA-MM-DD): \n")
	date = datetime.strptime(date_sortie, "%Y-%m-%d")
	prix = Decimal(input("Veuillez entrer le prix du jeu : \n"))
	dev = fromsoft
	
	jeu_cree = Jeu(titre=titre, date_sortie=date, prix=prix, developpeur = dev)

	jeu_cree.details = DetailJeu(description = "Jeu soulslike",note_metacritic = 18, multijoueur = True)


	session.add(jeu_cree)
	session.commit()


def mettre_a_jour(session):
	upd = session.execute(select(Jeu).filter_by(titre="Pokemon")).scalar_one()
	upd.titre = "Pokemon Ruby"
	session.commit()

def supprimer(session):
	to_delete = session.execute(select(Jeu).filter_by(titre="Pokemon Ruby")).scalar_one()
	session.delete(to_delete)
	session.commit()


def main():
	if not test_connexion():
		return

	session = get_session()

	init_db(delete=True)
	seed(session)
	retry = True
	while retry:
		print("\n" + "*" * 50)

		print("MENU CRUD")
		print( "*" * 30)
		print("[1] Lister tout les jeux")
		print("[2] Créer un nouveau jeu")
		print("[3] Modifier un jeu")
		print("[4] Supprimer un jeu")
		print("[5] Reset (drop + create)")
		print("[0] Quitter")
		print( "*" * 30)

		choix = int(input("\nVotre choix :\n"))

		if choix == 1:
			lire_jeux(session)
		elif choix == 2 :
			creer_jeux(session)
		elif choix == 3 :
			mettre_a_jour(session)
		elif choix == 4:
			supprimer(session)
		elif choix == 5:
			validation = input("Reinitilialiser toutes les tables ? (o/n) : ").lower()
			if validation == 'o':
				init_db(delete=True)
				seed(session)
		elif choix == 0:
			print("Bye bye !!!")
			retry = False
		else:
			print("Choix invalide")


if __name__ == "__main__":
	main()