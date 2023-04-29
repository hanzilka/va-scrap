import requests
from bs4 import BeautifulSoup
import json
import sys


def get_voice_actor_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    if response.status_code == 200:
        main_content = soup.find("div", attrs={"id": "mainContent"})
        if main_content is not None:
            name = main_content.find("h1").text.strip()

            # scrape roles
            roles = []
            rolesHtml = main_content.find_all("div", {"class": "mediaItem"})
            for roleRow in rolesHtml:
                anime = roleRow.find("div", {"class": "mediaHeading"}).text.strip()
                character = roleRow.find("div", {"class": "mediaSubHeading"}).text.strip()
                roleInfo = roleRow.find("div", {"class": "mediaDesc"}).text.strip()
                roles.append({"anime": anime, "character": character, "info": roleInfo})

            return {"name": name, "roles": roles}
        else:
            print(f"No content found for {url}")
            return None
    else:
        print(f"Error: code {response.status_code}")
        return None


NUMBER_OF_ACTORS = int(sys.argv[1]) if len(sys.argv) > 1 else 1
print(f"GETTING {NUMBER_OF_ACTORS}")

with open("voice_actors.json", "w", newline="", encoding="utf-8") as file:
    file.write("[\n")
    for i in range(1, NUMBER_OF_ACTORS + 1):
        url = f"https://www.behindthevoiceactors.com/voice-over-artist/{i}"
        voice_actor_data = get_voice_actor_data(url)
        jsonData = json.dumps(voice_actor_data, indent=3)
        if i < NUMBER_OF_ACTORS:
            file.write(jsonData + ",")
        else:
            file.write(jsonData + "\n")
    file.write("]")