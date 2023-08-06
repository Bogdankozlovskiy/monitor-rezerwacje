from httpx import AsyncClient, AsyncHTTPTransport
from asyncio import gather
import webbrowser
import re


data_template = {"time": "2023-08-14 {time}", "queue": 112, "schedule": 29}
time_arr = ["09:00", "09:10", "09:20", "09:30", "09:40", "09:50"]
url = "https://rezerwacje.duw.pl/reservations/updateFormData/{order_id}/{schedule}"
loading = ["-", "\\", "|", "/"]
locked_ids = []
states = ["-"] * len(time_arr)


async def worker(client, worker_index, time):
    index = 1
    data = data_template.copy()
    data["time"] = data["time"].format(time=time)
    while not locked_ids:
        try:
            response = await client.post("https://rezerwacje.duw.pl/reservations/lock", data=data)
        except Exception as exc:
            states[worker_index] = f"{time} * "
        else:
            if pattern := re.match(r"^OK (?P<order_id>\d*)$", response.text):
                order_id = pattern.groupdict()["order_id"]
                states[worker_index] = f"{time} {order_id} "
                locked_ids.append(order_id)
            else:
                states[worker_index] = f"{time} {loading[index % len(loading)]} "
                index += 1
        print("\r", ' '.join(states), end='')


async with AsyncClient(transport=AsyncHTTPTransport(verify=False, retries=50), timeout=30) as client:
    await client.get("https://rezerwacje.duw.pl/pol/login")
    await client.post(
        "https://rezerwacje.duw.pl/pol/login",
        data={
            "data[_Token][key]": "abd7ebbf52babfc3175e6056c25ce7a5fcde12dd",
            "data[User][email]": "email@email.email",
            "data[User][password]": "pssword@paswword",
            "data[_Token][fields]": "950d15a2cfde63e0ea9e1fa1b85587c9ff982433%3AUser.return_to"
        }
    )
    await gather(*[worker(client, index, time) for index, time in enumerate(time_arr)])
    final_url = url.format(order_id=locked_ids[-1], schedule=data_template["schedule"])
    webbrowser.open(final_url)
