import requests
from util import *

response = requests.post(
    f"{base_url}examine/", json={"name": "WELL"}, headers=auth_header
)
result = response.json()

prayer = result["description"]
print(prayer)

code = prayer.split("\n")[2:]
# print(code)
int_list = []
for byte in code:
    int_list.append(int(byte, 2))

print(int_list[2::5])

converted = [chr(num) for num in int_list[2::5]]
print("".join(converted))
