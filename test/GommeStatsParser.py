import requests, json
from bs4 import BeautifulSoup

def getPlayerStats(username):

    # --- Stats auf der GommeHD-Website aufrufen ---

    URL = f"https://www.gommehd.net/player/index?playerName={username}"
    html = requests.get(URL)
    soup = BeautifulSoup(html.content, "html.parser")
    # Um sich nur auf den Content der Website zu konzentrieren. Ist optional
    content = soup.find(id="content")

    # --- Avatar Link auslesen ---

    avatar_elem = content.find("span", class_="avatar")

    avatar_img = avatar_elem.find("img")
    avatar_link = avatar_img["src"]

    # --- Stats auslesen ---

    # Alle Stats-Container finden
    games_elems = content.find_all("div", class_="stat-table")

    # JSON vorbereiten
    result = {}

    for game in games_elems:

        # Namen von der Spielmodi finden
        gameName = game.find("h5").getText()

        # Stats für die Spielmodi, z.B. Wins
        stats_li = game.find_all("li")
        # JSON vorbereiten
        stats = {}

        # Alle Stats durchiterieren
        for li in stats_li:

            # Text auslesen
            stats_category = li.getText().replace("\n", "") # Der Text ist komisch und hat Zeilenübergänge. Die Schneide ich raus
            # Score auslesen
            score = li.find("span", class_="score").getText()

            # Score und Statskategorie zusammenfügen
            stats[stats_category.replace(score, "")] = score # Ansonsten würde erst der score und dann die Kategorie kommen

        # Stats zur JSON hinzufügen
        result[gameName] = stats

    # print(json.dumps(result, indent=4)) Falls man sich die Ausgabe mal angucken will
    return result

if __name__ == "__main__":
    print(json.dumps(getPlayerStats(input("Username: ")), indent=4))