import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

DEST_FOLDER = "../FFTT_DATA"
URL_DEPARTEMENT = "https://www.pongiste.fr/include/pages/clubs_dep.php"
page = requests.get(URL_DEPARTEMENT)
soup = BeautifulSoup(page.content, "html.parser")
dep_table = soup.find(id="tab_dep")
dep_elements = dep_table.find_all("tr")

# List Départements
dep_result = []
for dep_element in dep_elements:
    if dep_element.find("a"):
        # Récupération de l'ID du département
        dep_id = dep_element.find("a").text
        # Récupération du nom du département
        dep_name = dep_element.find_all("a")[1].text
        dep_row = [dep_id, dep_name]
        dep_result.append(dep_row)
df_dep = pd.DataFrame(dep_result, columns=["ID", "Name"])
csv_departement_file = DEST_FOLDER + "/departements.csv"
df_dep.to_csv(csv_departement_file, sep="\t")
print(f"#Département Fichier {csv_departement_file} créé avec succès.")

# List Clubs par Département
all_club = []
for dep in dep_result:
    is_extracted = False
    while (is_extracted == False):
        try:
            dep_id = dep[0]
            dep_name = dep[1]
            URL_CLUB = "https://www.pongiste.fr/include/pages/clubs_dep.php?num_dep="
            page = requests.get(URL_CLUB + dep_id)
            soup = BeautifulSoup(page.content, "html.parser")
            if (soup.find(id="tab_clubs_dep")):
                club_table = soup.find(id="tab_clubs_dep")
                club_elements = club_table.find_all("tr")
                club_result = []
                for club_element in club_elements:
                    if club_element.find("a"):
                        numero = club_element.find("a").text
                        nom = club_element.find_all("a")[1].text
                        date_validation = club_element.find_all("td")[2].text
                        club_row = [numero, nom, date_validation]
                        club_result.append(club_row)
                        all_club.append([numero, nom])
                df_club = pd.DataFrame(club_result, columns=["Numero", "NOM", "Date validation"])
                csv_club_file = DEST_FOLDER + "/clubs/" + dep_id + "_" + dep_name.replace("/", "_") + ".csv"
                df_club.to_csv(csv_club_file)
                print(f"#Club Fichier {csv_club_file} créé avec succès.")
        except:
            print(
                "Une exception est survenue lors de l'exportation des clubs du département :" + dep_id + " / " + dep_name)
            is_extracted = False
            print("retrying ...")
            time.sleep(5)
        else:
            is_extracted = True
# List Joueurs
URL_JOUEUR = 'https://www.pongiste.fr/include/pages/joueurs.php?num_club='
REFERER_URL = 'https://www.pongiste.fr/'
headers = {
    'Referer': REFERER_URL,
}
for club in all_club:
    is_extracted = False
    while (is_extracted == False):
        try:
            club_num = club[0]
            club_nom = club[1]
            page = requests.get(URL_JOUEUR + club_num, headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")
            joueur_table = soup.find(id="tab_joueurs")
            joueur_elements = joueur_table.find_all("tr")
            joueurs_result = []
            for joueur_element in joueur_elements[1:]:
                nom = joueur_element.find_all("td")[0].text
                prenom = joueur_element.find_all("td")[1].text
                licence = joueur_element.find_all("td")[2].text
                sexe_element = joueur_element.find_all("td")[3].find('span', class_='tooltip-bottom')
                sexe = 'M' if 'Masculin' in sexe_element['data-tooltip'] else 'F' if 'Féminin' in sexe_element['data-tooltip'] else ''
                pts_cls = joueur_element.find_all("td")[4].text
                certif_medical = joueur_element.find_all("td")[5].text
                cat_age = joueur_element.find_all("td")[6].text
                type_licence = joueur_element.find_all("td")[7].text
                joueurs_row = [nom, prenom, licence, sexe, pts_cls, certif_medical, cat_age, type_licence, club_num]
                joueurs_result.append(joueurs_row)
            df_joueurs = pd.DataFrame(joueurs_result,
                                      columns=["NOM", "Prénom", "Licence", "Sexe", "Pts Cls", "Certif. médical",
                                               "Cat. d'âge",
                                               "Type licence", "Num club"])

            csv_joueur_file = DEST_FOLDER + "/joueurs/" + club_nom.replace("/", "_").strip() + ".csv"
            df_joueurs.to_csv(csv_joueur_file)
            print(f"#Joueurs: Fichier {csv_joueur_file} créé avec succès.")

        except:
            print(
                "Une exception est survenue lors de l'exportation des joueurs du club :" + club_num + " / " + club_nom)
            is_extracted = False
            print("retrying ...")
            time.sleep(5)
        else:
            is_extracted = True

# List equipe TODO

URL_EQUIPE = 'https://www.pongiste.fr/include/pages/equipes.php?num_club='
REFERER_URL = 'https://www.pongiste.fr/'
headers = {
    'Referer': REFERER_URL,
}
for club in all_club:
    is_extracted = False
    while (is_extracted == False):
        try:
            club_num = club[0]
            club_nom = club[1]
            page = requests.get(URL_EQUIPE + club_num, headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")
            joueur_table = soup.find(id="tab_joueurs")
            joueur_elements = joueur_table.find_all("tr")
            joueurs_result = []
            for joueur_element in joueur_elements[1:]:
                nom = joueur_element.find_all("td")[0].text
                prenom = joueur_element.find_all("td")[1].text
                licence = joueur_element.find_all("td")[2].text
                sexe = joueur_element.find_all("td")[3].text
                pts_cls = joueur_element.find_all("td")[4].text
                certif_medical = joueur_element.find_all("td")[5].text
                cat_age = joueur_element.find_all("td")[6].text
                type_licence = joueur_element.find_all("td")[7].text
                joueurs_row = [nom, prenom, licence, sexe, pts_cls, certif_medical, cat_age, type_licence, club_num]
                joueurs_result.append(joueurs_row)
            df_joueurs = pd.DataFrame(joueurs_result,
                                      columns=["NOM", "Prénom", "Licence", "Sexe", "Pts Cls", "Certif. médical",
                                               "Cat. d'âge",
                                               "Type licence", "Num club"])

            csv_joueur_file = DEST_FOLDER + "/joueurs/" + club_nom.replace("/", "_").strip() + ".csv"
            df_joueurs.to_csv(csv_joueur_file)
            print(f"#Joueurs: Fichier {csv_joueur_file} créé avec succès.")

        except:
            print(
                "Une exception est survenue lors de l'exportation des joueurs du club :" + club_num + " / " + club_nom)
            is_extracted = False
            print("retrying ...")
            time.sleep(5)
        else:
            is_extracted = True


#list matche par equipe : phase + detail equipe + poule  + score TODO


