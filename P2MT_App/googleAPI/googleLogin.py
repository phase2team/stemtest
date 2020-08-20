import requests

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Included for reference. AuthLib handles retrieval of authorization endpoint.
# See https://realpython.com/flask-google-login/
def get_google_provider_cfg():
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    token_endpoint = google_provider_cfg["token_endpoint"]
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    print("authorization_endpoint:", authorization_endpoint)
    print("token_endpoint:", token_endpoint)
    print("userinfo_endpoint:", userinfo_endpoint)
    return google_provider_cfg

