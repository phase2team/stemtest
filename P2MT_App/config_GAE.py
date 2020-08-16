from P2MT_App.gcloud_functions import getCloudSqlUrl, getSqlEngineOptions


class Config:
    SECRET_KEY = "1f9c17c87d50c86558bff9c2517253c9"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    cloudSqlUrl = getCloudSqlUrl()
    cloudSqlEngineOptions = getSqlEngineOptions()

    SQLALCHEMY_DATABASE_URI = cloudSqlUrl
    SQLALCHEMY_ENGINE_OPTIONS = cloudSqlEngineOptions
