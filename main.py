from requests import Session
from requests.adapters import HTTPAdapter
import os
from time import sleep
import warnings
from datetime import datetime
import webbrowser
warnings.filterwarnings("ignore")



required_termin = "2023-08-09"
session = Session()
session.mount('https://', HTTPAdapter(max_retries=25))
session.get("https://rezerwacje.duw.pl/pol/login", verify=False, timeout=120)
session.post(
    "https://rezerwacje.duw.pl/pol/login", 
    data={
        "data[_Token][key]": "abd7ebbf52babfc3175e6056c25ce7a5fcde12dd",
        "data[User][email]": "login",
        "data[User][password]": "password",
        "data[_Token][fields]": "950d15a2cfde63e0ea9e1fa1b85587c9ff982433%3AUser.return_to"
    },
    timeout=120,
    verify=False
)
previous_page = None


while True:
    response = session.get(
        f"https://rezerwacje.duw.pl/pol/queues/112/29/{required_termin}",
        timeout=120,
        verify=False
    )
    if previous_page:
        os.remove(previous_page)
    new_page = f"/Users/bogdankozlovsky/Desktop/page-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.html"
    with open(new_page, "w") as file:
        previous_page = new_page
        file.write(response.text)
    if "WoW" not in response.text and "The specified URL cannot be found." not in response.text:
        break
    sleep(10)

webbrowser.open(f"https://rezerwacje.duw.pl/pol/queues/112/29/{required_termin}")

while True:
    os.system('say "Beer time."')
    sleep(2)