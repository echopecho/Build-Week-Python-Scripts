from find_path import find_path
import requests
import time
import pickle
import random
from util import *


def load():
    with open("final-path-graph.pkl", "rb") as f:
        return pickle.load(f)


path_graph = load()


stats = status()
while stats["gold"] < 1000:
    start = init()

    end = random.randint(300, 499)
    route = find_path(start["room_id"], end)
    print(route)
    for i in range(len(route) - 1):
        cur_room_id = route[i]
        next_room_id = route[i + 1]
        step = [
            key
            for key, value in path_graph[cur_room_id].items()
            if value == next_room_id
        ]
        new_room = move(step[0], next_room_id)

        for treasure in new_room["items"]:
            if stats["encumbrance"] == stats["strength"]:
                break
            loot(treasure)
            stats = status()

        if stats["encumbrance"] == stats["strength"]:
            break

    start = init()
    route = find_path(start["room_id"], 1)
    print("Returning!")
    print(route)

    for i in range(len(route) - 1):
        cur_room_id = route[i]
        next_room_id = route[i + 1]
        step = [
            key
            for key, value in path_graph[cur_room_id].items()
            if value == next_room_id
        ]
        new_room = move(step[0], next_room_id)

    for treasure in stats["inventory"]:
        sell(treasure)

    stats = status()

print(f'Done! You have {stats["gold"]} gold')
# for message in new_room["messages"]:
#     print(message)
# print(f'You can move in {new_room["cooldown"]} seconds')

# time.sleep(new_room["cooldown"])
