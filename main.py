from requests import Session
from warnings import simplefilter
from datetime import datetime
import re


simplefilter("ignore")
ok_checker = re.compile(r"^OK (?P<order_id>\d*)$")
statuses = ["-", "\\", "|", "/"]
index = 0
white = " " * 30


data = {"time": "2023-08-21 {time}", "queue": 112, "schedule": 26}
time_range = [
    "10:00:00", "10:05:00", "10:10:00", "10:15:00", "10:20:00", "10:25:00",
    "10:30:00", "10:35:00", "10:40:00", "10:45:00", "10:50:00", "10:55:00"
]
json_data = [
    {"name": "Imię", "value": "<first_name>"},
    {"name": "Nazwisko", "value": "<last_name>"},
    {"name": "Data urodzenia", "value": "Y-m-d"}
]
url_template_1 = "https://rezerwacje.duw.pl/reservations/updateFormData/{order_id}/{schedule}"
url_template_2 = "https://rezerwacje.duw.pl/reservations/reserv/{order_id}/{schedule}"
url_template_3 = "https://rezerwacje.duw.pl/reservations/view/{order_id}"
url_qr_code = "https://rezerwacje.duw.pl/qr/generate"
existing_data_list = []


# init session and login user
client = Session()
client.get("https://rezerwacje.duw.pl/pol/login", verify=False)
client.post(
    "https://rezerwacje.duw.pl/pol/login",
    data={
        "data[_Token][key]": "abd7ebbf52babfc3175e6056c25ce7a5fcde12dd",
        "data[User][email]": "email@email.xyu",
        "data[User][password]": "password-password",
        "data[_Token][fields]": "950d15a2cfde63e0ea9e1fa1b85587c9ff982433%3AUser.return_to"
    },
    verify=False
)


for time in time_range:
    copied_data = data.copy()
    copied_data["time"] = copied_data["time"].format(time=time)
    existing_data_list.append(copied_data)


stop_loop = False
while True:
    for existing_data in existing_data_list:
        index += 1
        try:
            response = client.post(
                "https://rezerwacje.duw.pl/reservations/lock", data=existing_data, verify=False
            )
            print(
                "\r step: 1", response.text, statuses[index % len(statuses)], existing_data["time"], white, end=""
            )
        except:
            print("\r step: 1", "error", statuses[index % len(statuses)], existing_data["time"], white, end="")
            continue
        if pattern := ok_checker.match(response.text):
            stop_loop = True
            order_id = pattern.groupdict()["order_id"]
            break
    if stop_loop:
        print("\r step 1: Done", datetime.now().strftime("%H:%M:%S"), order_id, existing_data['time'], white)
        break


url_1 = url_template_1.format(order_id=order_id, schedule=data["schedule"])
while True:
    index += 1
    try:
        response = client.post(url_1, json=json_data, verify=False)
        print("\r step: 2", response.text.split("\n")[0], statuses[index % len(statuses)], white, end="")
    except:
        print("\r step: 2", "error", statuses[index % len(statuses)], white, end="")
        continue
    if response.ok:
        print("\r step 2: Done", datetime.now().strftime("%H:%M:%S"), white)
        break


url_2 = url_template_2.format(order_id=order_id, schedule=data["schedule"])
while True:
    index += 1
    try:
        response = client.get(url_2, verify=False)
        print("\r step: 3", response.text.split("\n")[0], statuses[index % len(statuses)], white, end="")
    except:
        print("\r step: 3", "error", statuses[index % len(statuses)], white, end="")
        continue
    if response.ok:
        print("\r step 3: Done", datetime.now().strftime("%H:%M:%S"), white)
        break


while True:
    index += 1
    try:
        response = client.get(url_qr_code, verify=False)
    except:
        print("\r checking", "error", statuses[index % len(statuses)], white, end="")
        continue
    if response.ok:
        if response.content == b"":
            print("\r checking: FAIL")
        else:
            print("\r checking: OK")
            print(url_template_3.format(order_id=order_id))
        break
