import requests
from bs4 import BeautifulSoup
import json
import sys


def get_voice_actor_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    if response.status_code == 200:
        main_content = soup.find("div", attrs={"id": "contentWrapper"})
        if main_content is not None:
            name = main_content.h1.text.strip()

            # screjp role
            roles = []
            rolesHtml = main_content.find(
                "table", {"class": "table-people-character"}
            ).find_all("tr", {"class": "js-people-character"})

            for roleRow in rolesHtml:
                cols = roleRow.find_all("td")
                roleAnime = cols[1].find("div", {"class": "spaceit_pad"}).text.strip()
                roleInfo = (
                    cols[1].find("div", {"class": "anime-info-text"}).text.strip()
                )
                roleName = cols[2].find("div", {"class": "spaceit_pad"}).text.strip()

                roles.append(
                    {"anime": roleAnime, "character": roleName, "info": roleInfo}
                )

            return {"name": name, "roles": roles}
        else:
            print(f"zadnej kontent do pici{url}")
            return None
    else:
        print(f"Error: code {response.status_code}")
        return None


NUMBER_OF_ACTORS = int(sys.argv[1]) if len(sys.argv) > 1 else 1
print(f"GETTING {NUMBER_OF_ACTORS}")

with open("voice_actors.json", "w", newline="", encoding="utf-8") as file:
    file.write("[\n")
    for i in range(1, NUMBER_OF_ACTORS + 1):
        url = f"https://myanimelist.net/people/{i}"
        voice_actor_data = get_voice_actor_data(url)
        jsonData = json.dumps(voice_actor_data, indent=3)
        if i < NUMBER_OF_ACTORS:
            file.write(jsonData + ",")
        else:
            file.write(jsonData + "\n")
    file.write("]")