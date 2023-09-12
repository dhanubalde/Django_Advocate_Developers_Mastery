import requests
from getpass import getpass

endpoint = "http://127.0.0.1:8000/auth/"
username = input("What is your username? \n")
password = getpass("what is your password? \n")
auth_response = requests.post(
    endpoint, json={'username': username, 'password': password})
print(auth_response.json())
if auth_response.status_code == 200:
    token = auth_response.json()['token']
    headers = {"Authorization": f"Token {token}"}
    endpoint = "http://127.0.0.1:8000/api/advocate/"
    get_response = requests.get(endpoint, headers=headers)
    print(get_response.json())
