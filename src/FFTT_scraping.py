import requests
from bs4 import BeautifulSoup
import pandas as pd

DEST_FOLDER = "../FFTT_DATA"
URL = "https://www.pongiste.fr/include/pages/clubs_dep.php"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
dep_table = soup.find(id="tab_dep")
dep_elements = dep_table.find_all("tr")

dep_result=[]
for dep_element in dep_elements:
    if dep_element.find("a"):
        # Récupération de l'ID du département
        dep_id = dep_element.find("a").text
        # Récupération du nom du département
        dep_name = dep_element.find_all("a")[1].text
        dep_row=[dep_id,dep_name]
        dep_result.append(dep_row)
df_dep = pd.DataFrame(dep_result, columns=["ID", "Name"])
df_dep.to_csv(DEST_FOLDER+"/departements.csv", sep="\t")
