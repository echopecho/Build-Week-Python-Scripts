from util import *
import requests
import time
import pickle
import random


def load():
    with open("path-graph.pkl", "rb") as f:
        return pickle.load(f)


path_graph = load()


def find_path(start, destination):

    q = Queue()
    q.enqueue([start])

    visited = []
    while q.size() > 0:
        current_path = q.dequeue()
        current_room = current_path[-1]

        if current_room == destination:
            return current_path

        if current_room not in visited:
            visited.append(current_room)
            # print(path_graph)
            possible_directions = [
                key for key, value in path_graph[current_room].items() if value != "?"
            ]

            for direction in possible_directions:
                copy_path = current_path[:]
                next_room = path_graph[current_room][direction]
                copy_path.append(next_room)
                q.enqueue(copy_path)
