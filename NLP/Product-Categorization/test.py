import requests

# Define the URL and headers
url = "http://localhost:8000/api/analyze"
headers = {"Content-Type": "application/json"}

# Define the JSON data
data = '{"title": "Xiaomi 11i 5G Hypercharge (Stealth Black, 6GB RAM, 128GB Storage)", "thumbnail": "https://m.media-amazon.com/images/I/71BQ8Kjt29L._SL1500_.jpg"}'

# Send the POST request
response = requests.post(url, headers=headers, data=data)

# Check if the request was successful
if response.status_code == 200:
    print("Request successful!")
    print(response.json())
else:
    print("Request failed!")
    print(response.text)
