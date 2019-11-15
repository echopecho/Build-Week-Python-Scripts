import requests
import time
import random
import pickle
from util import *

# base_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"

# auth_header = {"Authorization": "Token 724b204984aee234274039fae647bc65240d399e"}

# reverse = {"n": "s", "s": "n", "e": "w", "w": "e"}
completed = set()

path_graph = {}
names = {}


def save():
    with open("path-graph.pkl", "wb") as f:
        pickle.dump(path_graph, f, pickle.HIGHEST_PROTOCOL)
    with open("room-names.pkl", "wb") as f:
        pickle.dump(names, f, pickle.HIGHEST_PROTOCOL)


def add_to_graph(room):
    path_graph[room["room_id"]] = dict(zip(room["exits"], ["?"] * len(room["exits"])))
    names[room["title"]] = room["room_id"]
    save()


def connect_rooms(current, last, direction):
    path_graph[current["room_id"]][reverse[direction]] = last["room_id"]
    path_graph[last["room_id"]][direction] = current["room_id"]
    save()


response = requests.get(f"{base_url}init/", headers=auth_header)
current_room = response.json()
add_to_graph(current_room)

starting_path = [current_room]

time.sleep(current_room["cooldown"])

response = requests.post(
    f"{base_url}move/",
    json={"direction": "w", "next_room_id": "1"},
    headers=auth_header,
)
shop = response.json()

add_to_graph(shop)
connect_rooms(current=shop, last=current_room, direction="w")
time.sleep(shop["cooldown"])

response = requests.post(
    f"{base_url}move/",
    json={"direction": "e", "next_room_id": "0"},
    headers=auth_header,
)
home = response.json()
time.sleep(home["cooldown"])

starting_direction = random.choice(["n", "s", "e"])

response = requests.post(
    f"{base_url}move/", json={"direction": starting_direction}, headers=auth_header
)
next_room = response.json()
starting_path.append(next_room)
add_to_graph(next_room)

time.sleep(next_room["cooldown"])

connect_rooms(current=next_room, last=current_room, direction=starting_direction)

print(starting_direction)
# with open("path-graph.pkl", "rb") as f:
#     print(pickle.load(f))

s = Stack()
s.push([next_room])

direction = starting_direction

while s.size() > 0:
    current_path = s.pop()
    room = current_path[-1]

    room_exits = path_graph[room["room_id"]]
    if "?" in room_exits.values():
        possible_exits = [key for key, value in room_exits.items() if value == "?"]
    else:
        possible_exits = [key for key in room_exits.keys()]
        possible_exits.remove(reverse[direction])

    direction = random.choice(possible_exits)

    response = requests.post(
        f"{base_url}move/", json={"direction": direction}, headers=auth_header
    )
    next_room = response.json()
    print(f'{next_room["messages"][0]} to {next_room["title"]}: {next_room["cooldown"]} items: {next_room["items"]}')

    if next_room["room_id"] not in path_graph.keys():
        add_to_graph(next_room)
    connect_rooms(current=next_room, last=room, direction=direction)

    if len(path_graph) == 500:
        break

    time.sleep(next_room["cooldown"])

    if len(next_room["exits"]) == 1 or "?" not in path_graph[next_room['room_id']].values():
        # set the return path back to a room that has unexplored exit
        q = Queue()
        q.enqueue([next_room["room_id"]])

        return_path = []
        visited = []
        while q.size() > 0:
            retrace = q.dequeue()
            back_room = retrace[-1]

            if "?" in path_graph[back_room].values():
                return_path = retrace
                break
            
            if back_room not in visited:
                visited.append(back_room)

                possible_directions = [
                    key for key, value in path_graph[back_room].items()     if value != "?"
                ]

                # if len(retrace) > 1 and len(possible_directions) > 1:
                #     possible_directions.remove(reverse[retrace[-2][1]])
                # direction = random.choice(possible_directions)

                # retrace[-1][1] = direction

                for direction in possible_directions:
                    copy_retrace = retrace[:]
                    back_next = path_graph[back_room][direction]
                    # if "?" in path_graph[back_next[0]].values():
                    #     return_path = retrace
                    #     break
                    copy_retrace.append(back_next)
                    q.enqueue(copy_retrace)

        print(return_path)

        for i in range(len(return_path) - 1):
            cur_room_id = return_path[i]
            next_room_id = return_path[i + 1]
            step = [key for key, value in path_graph[cur_room_id].items() if value == next_room_id]
            response = requests.post(
                f"{base_url}move/",
                json={"direction": step[0], "next_room_id": f"{next_room_id}"},
                headers=auth_header,
            )

            new_room = response.json()

            for message in new_room["messages"]:
                print(message)
            print(f'You can move in {new_room["cooldown"]} seconds')

            next_room = new_room
            time.sleep(new_room["cooldown"])
        print(f'Length of graph {len(path_graph)}')
        # break

    copy_path = current_path[:]
    copy_path.append(next_room)
    s.push(copy_path)
