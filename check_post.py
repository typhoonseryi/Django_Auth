import requests
import json


url = 'http://localhost:8000/api/v1/goods/'
data = {
    "title": "Cheese",
    "description": "Best. Cheese. Ever",
    "price": 10
    }
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'bG9naW46cGFzc3dvcmQ='
}
response = requests.post(url=url, json=data, headers=headers)
print(response.text)
print(response.status_code)