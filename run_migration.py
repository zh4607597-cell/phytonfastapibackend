import requests

try:
    response = requests.post('http://localhost:8000/api/migrate/add-receiver-id')
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Request failed: {e}")