from find_path import find_path
import requests
import time
import pickle
import random
from util import *


def load():
    with open("final-path-graph.pkl", "rb") as f:
        graph, titles = pickle.load(f)
        return {"graph": graph, "titles": titles}


data = load()

path_graph = data["graph"]
landmarks = data["titles"]

print(landmarks)
print("Where would you like to go?")
destination = int(input())

start = init()
route = find_path(start["room_id"], destination)

print(route)

for i in range(len(route) - 1):
    cur_room_id = route[i]
    next_room_id = route[i + 1]
    step = [
        key for key, value in path_graph[cur_room_id].items() if value == next_room_id
    ]
    new_room = move(step[0], next_room_id)
