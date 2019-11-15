from util import *
import requests
import time
import pickle
import random
from find_path import find_path


def load():
    with open("path-graph.pkl", "rb") as f:
        return pickle.load(f)


path_graph = load()

response = requests.get(f"{base_url}init/", headers=auth_header)
starting_room = response.json()

time.sleep(starting_room["cooldown"])

return_path = find_path(starting_room["room_id"], 0)
print(return_path)

for i in range(len(return_path) - 1):
    cur_room_id = return_path[i]
    next_room_id = return_path[i + 1]
    step = [
        key for key, value in path_graph[cur_room_id].items() if value == next_room_id
    ]
    response = requests.post(
        f"{base_url}move/",
        json={"direction": step[0], "next_room_id": f"{next_room_id}"},
        headers=auth_header,
    )
    new_room = response.json()

    for message in new_room["messages"]:
        print(message)
    print(f'You can move in {new_room["cooldown"]} seconds')

    time.sleep(new_room["cooldown"])

