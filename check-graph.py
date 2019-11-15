import pickle


def load_graph():
    with open("path-graph.pkl", "rb") as f:
        return pickle.load(f)


def load_names():
    with open("room-names.pkl", "rb") as f:
        return pickle.load(f)


path_graph = load_graph()

print(len(path_graph))


names = load_names()

important_names = [
    (key, value) for key, value in names.items() if value != "A misty room"
]

if len(path_graph) == 500:
    with open("final-path-graph.pkl", "wb") as f:
        pickle.dump((path_graph, important_names), f, pickle.HIGHEST_PROTOCOL)

for name in important_names:
    print(name[0], name[1])
