import requests
from bs4 import BeautifulSoup
import json
import sys
import datetime

def get_voice_actor_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    if response.status_code == 200:
        main_content = soup.find("div", attrs={"id": "contentWrapper"})
        if main_content is not None:
            name = main_content.h1.text.strip()

            # scrape roles
            roles = []
            rolesHtml = main_content.find(
                "table", {"class": "table-people-character"}
            ).find_all("tr", {"class": "js-people-character"})

            for roleRow in rolesHtml:
                cols = roleRow.find_all("td")
                anime = cols[1].find("div", {"class": "spaceit_pad"}).text.strip()
                info = cols[1].find("div", {"class": "anime-info-text"}).text.strip()
                role = cols[2].find("div", {"class": "spaceit_pad"}).text.strip()

                roles.append(
                    {"name": name, "role": role, "anime": anime, "info": info}
                )

            return {"data": roles}
        else:
            print(f"No content found for {url}")
            return None
    else:
        print(f"Error: code {response.status_code}")
        return None

NUMBER_OF_ACTORS = int(sys.argv[1]) if len(sys.argv) > 1 else 1
print(f"GETTING {NUMBER_OF_ACTORS}")

start_index = 101 # číslo stránky z people
end_index = start_index + NUMBER_OF_ACTORS - 1
filename = f"voice_actors_{start_index}-{end_index}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"

with open(filename, "w", newline="", encoding="utf-8") as file:
    json_data = []
    for i in range(start_index, end_index + 101):
        url = f"https://myanimelist.net/people/{i}"
        voice_actor_data = get_voice_actor_data(url)
        if voice_actor_data is not None:
            json_data.extend(voice_actor_data["data"])
    json.dump({"data": json_data}, file)
