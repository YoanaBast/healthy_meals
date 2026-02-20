import requests
import json

url = "http://127.0.0.1:8000/recipes/12/add_ingredient/"  # your actual URL
payload = {
    "ingredient_id": 5,
    "quantity": 100,
    "unit_id": 2
}

response = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
print(response.status_code)
print(response.json())