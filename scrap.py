import requests
from bs4 import BeautifulSoup

def get_voice_actor_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "lxml")
        print(soup.prettify())
        main_content = soup.find("div", attrs={"id": "contentWrapper"})
        if main_content is not None:
            name = main_content.h1.text.strip()

            # screjp role
            roles = []
            roles_section = main_content.find("h2", string="Voice Acting Roles")
            if roles_section is not None:
                roles_table = roles_section.find_next_sibling("table", class_="js-table-people-character table-people-character")
                if roles_table is not None:
                    roles_table['style'] = 'display: table;'
                    for tr in roles_table.find_all("tr"):
                        td = tr.find("td")
                        if td is not None:
                            roles.append(td.text.strip())
                else:
                    print(f"nic do pici 1 {name}")
            else:
                print(f"nic do pici 2{name}")

            return {
                "name": name,
                "roles": roles
            }
        else:
            print(f"zadnej kontent do pici{url}")
            return None
    else:
        print(f"Error: code {response.status_code}")
        return None

for i in range(1, 4):
    url = f"https://myanimelist.net/people/{i}"
    voice_actor_data = get_voice_actor_data(url)
    if voice_actor_data is not None:
        print(f"Name: {voice_actor_data['name']}")
        print("Roles:")
        for role in voice_actor_data['roles']:
            print(role)
        print()