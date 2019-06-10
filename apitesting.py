import requests
import json
parameters = {"lat": 37.78, "lon": -122.41}
response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
data=response.json()
print("Here is the data:")
print(data)
print("Here are the headers")
print(response.headers)
print("Here are the content type headers")
print(response.headers["content-type"])

response = requests.get("http://api.open-notify.org/astros.json")
data = response.json()
# 9 people are currently in space.
print("Number of people in space")
print(data["number"])
print("Full JSON data:")
print(data)

