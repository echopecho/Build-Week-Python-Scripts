import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("KEY")


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)


base_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"


auth_header = {"Authorization": f"Token {key}"}

reverse = {"n": "s", "s": "n", "e": "w", "w": "e"}


def init():
    response = requests.get(f"{base_url}init/", headers=auth_header)
    start = response.json()
    time.sleep(start["cooldown"])

    return start


def move(direction, room):
    response = requests.post(
        f"{base_url}move/",
        json={"direction": direction, "next_room_id": f"{room}"},
        headers=auth_header,
    )
    new_room = response.json()
    for message in new_room["messages"]:
        print(message)
    print(f'You can move in {new_room["cooldown"]} seconds')
    time.sleep(new_room["cooldown"])

    return new_room


def status():
    response = requests.post(f"{base_url}status/", headers=auth_header)
    stats = response.json()
    time.sleep(stats["cooldown"])

    return stats


def loot(item):
    response = requests.post(
        f"{base_url}take/", json={"name": item}, headers=auth_header
    )
    treasure = response.json()
    print(treasure["messages"][0])
    time.sleep(treasure["cooldown"])


def drop(item):
    response = requests.post(
        f"{base_url}drop/", json={"name": item}, headers=auth_header
    )
    treasure = response.json()
    print(treasure["messages"][0])
    time.sleep(treasure["cooldown"])


def sell(item):
    response = requests.post(
        f"{base_url}sell/", json={"name": item, "confirm": "yes"}, headers=auth_header
    )
    treasure = response.json()
    print(treasure["messages"][1])
    time.sleep(treasure["cooldown"])

