from requests import Session
from warnings import simplefilter
import re


simplefilter("ignore")
statuses = ["-", "\\", "|", "/"]
index = 0
white = " " * 30

data = {"time": "2023-08-17 11:30:00", "queue": 112, "schedule": 26}
json_data = [{"name": "Imię", "value": "<your first name>"}, {"name": "Nazwisko", "value": "<your last name>"}]
url_template_1 = "https://rezerwacje.duw.pl/reservations/updateFormData/{order_id}/{schedule}"
url_template_2 = "https://rezerwacje.duw.pl/reservations/reserv/{order_id}/{schedule}"


client = Session()
client.get("https://rezerwacje.duw.pl/pol/login", verify=False)
client.post(
    "https://rezerwacje.duw.pl/pol/login",
    verify=False,
    data={
        "data[_Token][key]": "abd7ebbf52babfc3175e6056c25ce7a5fcde12dd",
        "data[User][email]": "email@email.xuy",
        "data[User][password]": "passwordpasswrod",
        "data[_Token][fields]": "950d15a2cfde63e0ea9e1fa1b85587c9ff982433%3AUser.return_to"
    }
)

while True:
    index += 1
    try:
        response = client.post("https://rezerwacje.duw.pl/reservations/lock", data=data, verify=False)
        print("\r step: 1", response.text, statuses[index % len(statuses)], white, end="")
    except:
        print("\r 1", "step: error", statuses[index % len(statuses)], white, end="")
        continue
    if pattern := re.match(r"^OK (?P<order_id>\d*)$", response.text):
        order_id = pattern.groupdict()["order_id"]
        url_1 = url_template_1.format(order_id=order_id, schedule=data["schedule"])
        url_2 = url_template_2.format(order_id=order_id, schedule=data["schedule"])
        while True:
            try:
                response = client.post(url_1, json=json_data, verify=False)
                print("\r step: 2", response.text.split("\n")[0], statuses[index % len(statuses)], white, end="")
            except:
                print("\r step: 2", "error", statuses[index % len(statuses)], white, end="")
                continue
            if response.ok:
                break
        while True:
            try:
                response = client.get(url_2, verify=False)
                print("\r step: 3", response.text.split("\n")[0], statuses[index % len(statuses)], white, end="")
            except:
                print("\r step: 3", "error", statuses[index % len(statuses)], white, end="")
                continue
            if response.ok:
                break
        break
        
print("\r Done !!!")
