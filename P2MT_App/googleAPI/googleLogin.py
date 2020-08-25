import requests
import os
import json

from P2MT_App.models import FacultyAndStaff
from P2MT_App.main.utilityfunctions import printLogEntry

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Included for reference. AuthLib handles retrieval of authorization endpoint.
# See https://realpython.com/flask-google-login/
def get_google_provider_cfg():
    printLogEntry("Running get_google_provider_cfg()")
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    token_endpoint = google_provider_cfg["token_endpoint"]
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    print("authorization_endpoint:", authorization_endpoint)
    print("token_endpoint:", token_endpoint)
    print("userinfo_endpoint:", userinfo_endpoint)
    return google_provider_cfg


def updateProfilePic(user_id, profilePicUrl):
    printLogEntry("Running updateProfilePic()")
    user = FacultyAndStaff.query.get(user_id)
    print("user_id =", user_id)
    print("user =", user)
    print("profilePicUrl =", profilePicUrl)
    user.google_picture = profilePicUrl
    return


def updateGoogleSub(user_id, googleSubId):
    printLogEntry("Running updateGoogleSub()")
    user = FacultyAndStaff.query.get(user_id)
    user.google_sub = googleSubId
    return


# Return the Google Client Config parameters needed to create a OAuth2 Flow object
# These parameters are from the Google client credentials json which
# is downloaded from the Google Cloud API Console
# Google Client ID and Google Client Secret are stored as environment variables
def getGoogleClientConfig():
    printLogEntry("Running getGoogleClientConfig()")
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    redirect_uris = [
        "http://localhost:8080/oauth2callback",
        "https://alpha816.uk.r.appspot.com/oauth2callback",
        "http://localhost:8080/googlelogin",
        "http://localhost:8080/tokensignin",
        "http://localhost:8080/login/callback",
        "https://alpha816.uk.r.appspot.com/login/callback",
        "https://8080-cs-905398832503-default.us-east1.cloudshell.dev/login/callback",
        "https://p2mt-test-2hzxr2gybq-ue.a.run.app/login/callback",
        "http://p2mt-test-2hzxr2gybq-ue.a.run.app/login/callback",
        "http://run-mysql-2hzxr2gybq-uk.a.run.app/login/callback",
        "http://localhost:8080/sendmail/callback",
    ]
    auth_uri = "https://accounts.google.com/o/oauth2/auth"
    token_uri = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
    javascript_origins = [
        "http://localhost:8080",
        "https://alpha816.uk.r.appspot.com",
        "https://8080-cs-905398832503-default.us-east1.cloudshell.dev",
        "https://p2mt-test-2hzxr2gybq-ue.a.run.app",
        "https://run-mysql-2hzxr2gybq-uk.a.run.app",
    ]
    return {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": redirect_uris,
            "auth_uri": auth_uri,
            "token_uri": token_uri,
            "javascript_origins": javascript_origins,
            "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
        }
    }


def saveGoogleCredentialsAsJson(user_id, new_credentials_json):
    printLogEntry("Running saveGoogleCredentials()")
    user = FacultyAndStaff.query.get(user_id)
    # Only update the credentials if the credentials are not in the database
    # or if the refresh token in the new credentials is not null
    if user.google_credentials:
        print("User credentials found in database for user:", user)
        # Convert credentials from database to dictionary and
        # check for refresh token
        credentials_dict = json.loads(new_credentials_json)
        # Update credentials if the refresh token is not null
        if "refresh_token" not in credentials_dict:
            print("Refresh token not found in new credentials for user", user)
        elif credentials_dict["refresh_token"]:
            print("Updating credentials with refresh token for user:", user)
            user.google_credentials = new_credentials_json
        else:
            print("Credentials not saved since refresh token is null for user:", user)
    else:
        # Save new credentials to database
        print("Saving user credentials in database for user", user)
        user.google_credentials = new_credentials_json
    return


def getGoogleCredentialsAsDict(user_id):
    printLogEntry("Running retrieveGoogleCredentials()")
    user = FacultyAndStaff.query.get(user_id)
    credentials_dict = json.loads(user.google_credentials)
    return credentials_dict
