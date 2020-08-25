from P2MT_App.gcloud_functions import getCloudSqlUrl, getSqlEngineOptions
import os


class Config:
    SECRET_KEY = "1f9c17c87d50c86558bff9c2517253c9"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    cloudSqlUrl = getCloudSqlUrl()
    cloudSqlEngineOptions = getSqlEngineOptions()

    SQLALCHEMY_DATABASE_URI = cloudSqlUrl
    SQLALCHEMY_ENGINE_OPTIONS = cloudSqlEngineOptions

    # Set environment variables necessary for Google login and API usage
    USE_GOOGLE_LOGIN_AND_API = "True"
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    WTF_CSRF_TIME_LIMIT = None
