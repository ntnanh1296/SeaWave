import requests
import json

# Set the API endpoint
api_url = "http://localhost:8000/api/users/"

# Create 20 users
for i in range(1, 21):
    user_data = {
        "email": f"user{i}@gmail.com",
        "username": f"user{i}",
        "password": f"user{i}",
        "gender": "Male",  # Adjust gender as needed
        "birthday": "1996-01-01",  # Adjust birthday as needed
    }

    # Make a POST request to create a user
    response = requests.post(api_url, headers={"Content-Type": "application/json"}, data=json.dumps(user_data))

    # Check if the request was successful (status code 201)
    if response.status_code == 201:
        print(f"User {i} created successfully.")
    else:
        print(f"Failed to create user {i}. Status code: {response.status_code}")
        print(response.text)
