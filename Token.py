import requests

def generate_access_token(client_id, client_secret):
    url = "https://bitbucket.org/site/oauth2/access_token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        print("Failed to generate access token")
        return None

# Usage example
client_id = "your_client_id"
client_secret = "your_client_secret"

access_token = generate_access_token(client_id, client_secret)
if access_token:
    print("Access Token:", access_token)
