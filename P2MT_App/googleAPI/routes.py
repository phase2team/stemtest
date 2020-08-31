# Python standard libraries
import json
import os

# Third-party libraries
from flask import (
    Flask,
    url_for,
    redirect,
    request,
    render_template,
    redirect,
    Blueprint,
    session,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

# P2MT imports
from P2MT_App import db, oauth
from P2MT_App.models import FacultyAndStaff
from P2MT_App.googleAPI.googleLogin import get_google_provider_cfg
from P2MT_App.googleAPI.googleMail import create_message, send_message
from P2MT_App.main.utilityfunctions import printLogEntry
from P2MT_App.googleAPI.googleLogin import (
    updateProfilePic,
    updateGoogleSub,
    getGoogleClientConfig,
    saveGoogleCredentialsAsJson,
    getGoogleCredentialsAsDict,
)

googleAPI_bp = Blueprint("googleAPI_bp", __name__)

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "webapptest.json"
# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar",
]

########################
#   Routes for Login   #
########################


@googleAPI_bp.route("/homepage")
def homepage():
    if current_user.is_authenticated:
        return render_template("login.html", title="Login", user=current_user)
    else:
        print("current_user.is_authenticated =", current_user.is_authenticated)
        return render_template("login.html", title="Login", user=None)


@googleAPI_bp.route("/login")
def login():
    printLogEntry("Running login()")
    redirect_uri = url_for("googleAPI_bp.auth", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@googleAPI_bp.route("/login/callback")
def auth():
    printLogEntry("Running auth()")
    get_google_provider_cfg()
    token = oauth.google.authorize_access_token()
    userinfo_response = oauth.google.parse_id_token(token)
    print("userinfo_response:", userinfo_response)
    if userinfo_response:
        if userinfo_response["email_verified"]:
            unique_id = userinfo_response["sub"]
            users_email = userinfo_response["email"]
            picture = userinfo_response["picture"]
            users_name = userinfo_response["given_name"]
            print("unique_id:", unique_id)
            print("users_email:", users_email)
            print("picture:", picture)
            print("users_name:", users_name)
            # Create a user in your db with the information provided
            # by Google
            # user = User(
            #     id_=unique_id, name=users_name, email=users_email, profile_pic=picture
            # )

            # Verify user is approved to access the apps
            user = FacultyAndStaff.query.filter(
                FacultyAndStaff.email == users_email
            ).first()
            print("User query result =", user)
            print("User type =", type(user))

            if user:
                printLogEntry("This is a valid user")
                # Begin user session by logging the user in
                try:
                    updateProfilePic(user.id, picture)
                    updateGoogleSub(user.id, unique_id)
                    db.session.commit()
                    credentials = getGoogleCredentialsAsDict(user.id)
                    # if credentials:
                    #     session["credentials"] = credentials
                    # printLogEntry("Updated Google profile pic and unique id")
                except:
                    printLogEntry("Unable to update Google profile pic or unique id")
                    pass
                login_user(user)

    # if False:
    #     # Doesn't exist? Add it to the database.
    #     if not User.get(unique_id):
    #         User.create(unique_id, users_name, users_email, picture)

    return redirect("/logintest")


@googleAPI_bp.route("/logintest")
def logintest():
    print("current_user =", current_user)
    if current_user.is_authenticated:
        return render_template(
            "logintest.html", title="Login Test Page", user=current_user
        )
    else:
        return render_template("logintest.html", title="Login Test Page", user=None)


@googleAPI_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


########################
#   Routes for Gmail   #
########################

# Simple page for testing email
@googleAPI_bp.route("/mailtest")
@login_required
def mailTest():
    return render_template("mailtest.html", title="Send Mail", user=current_user)


# Using stored credentials to send email on behalf of system account
@googleAPI_bp.route("/sendofflinemail")
@login_required
def sendOfflineMail():
    printLogEntry("runnning sendOfflineMail()")
    requiredScope = ["https://www.googleapis.com/auth/gmail.send"]

    storedCredentials = {
        "token": "ya29.a0AfH6SMAwdC7ZmyPJv1HS30X7RVkcIK3uGwwyGYv2PZJ7c3sc77rok8LRInd1t1WSrM52PZFpSUDjhg_pHZCjRR1z-_K5ADtRdjkkL8X0fycDDqBHuJV8NZ6N5ZgrS_mala2-JURyUTCZKm0EcpB9sqg4dD99BWnFX_w",
        "refresh_token": "1//01LWa-NRxr9c7CgYIARAAGAESNwF-L9IraeTRelgvqrjJTAQVlzwXOakskTT8PNYxn-jUH-ltH__dLFxb4lieXjOWCQBfLAEZvQE",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": os.getenv(GOOGLE_CLIENT_ID),
        "client_secret": os.getenv(GOOGLE_CLIENT_SECRET),
        "scopes": requiredScope,
    }

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(**storedCredentials)
    print("Credentials from DB:", retrieveGoogleCredentials(current_user.id))

    # Create a Gmail API service with the authorized user credentials
    apiServiceName = "gmail"
    apiVersion = "v1"
    gmailService = googleapiclient.discovery.build(
        apiServiceName, apiVersion, credentials=credentials
    )

    # Set email to, from, and message content
    emailFrom = "phase2team@students.hcde.org"
    EmailTo = current_user.email
    emailSubject = "STEM School Intervention"
    emailContent = "(Practice) This is a STEM School Intervention notification."

    # Create the MIME-formatted message
    message = create_message(emailFrom, EmailTo, emailSubject, emailContent)

    # Call the Gmail API service to send the message
    sent = send_message(gmailService, "me", message)

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    # session["credentials"] = credentials_to_dict(credentials)
    credentials_json = credentials.to_json()
    print("credentials_json:", credentials_json)
    saveGoogleCredentialsAsJson(current_user.id, credentials_json)
    db.session.commit()
    return redirect("/emailresult")
    # return jsonify(credentials_to_dict(credentials))


# Using user authorized credentials to send email on behalf of the user
@googleAPI_bp.route("/sendmail")
@login_required
def sendMail():
    printLogEntry("runnning sendMail()")
    requiredScope = ["https://www.googleapis.com/auth/gmail.send"]
    if "credentials" not in session:
        return redirect("authorize")
    print('session["credentials"] =', session["credentials"])
    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])
    print("Credentials from DB:", retrieveGoogleCredentials(current_user.id))
    # Create a Gmail API service with the authorized user credentials
    apiServiceName = "gmail"
    apiVersion = "v1"
    gmailService = googleapiclient.discovery.build(
        apiServiceName, apiVersion, credentials=credentials
    )

    # Set email to, from, and message content
    emailFrom = "phase2team@students.hcde.org"
    EmailTo = current_user.email
    emailSubject = "STEM School Intervention"
    emailContent = "(Practice) This is a STEM School Intervention notification."

    # Create the MIME-formatted message
    message = create_message(emailFrom, EmailTo, emailSubject, emailContent)

    # Call the Gmail API service to send the message
    sent = send_message(gmailService, "me", message)

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    # session["credentials"] = credentials_to_dict(credentials)
    # credentials_json = json.dumps(credentials_to_dict(credentials))
    credentials_json = credentials.to_json()
    print("credentials_json:", credentials_json)
    saveGoogleCredentialsAsJson(current_user.id, credentials_json)
    db.session.commit()
    return redirect("/emailresult")
    # return jsonify(credentials_to_dict(credentials))


# Initiating user authorization via Google for required Google API scopes
@googleAPI_bp.route("/authorize")
def authorize():
    printLogEntry("runnning authorize()")
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    # This version uses a client config mapping
    googleClientConfig = getGoogleClientConfig()
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        googleClientConfig, scopes=SCOPES
    )
    # This version uses the json (but not safe to upload json to GitHub)
    # flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    #     CLIENT_SECRETS_FILE, scopes=SCOPES
    # )

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = url_for("googleAPI_bp.sendmailCallback", _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type="offline",
        state="thisisthestate",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="false",
    )

    # Store the state so the callback can verify the auth server response.
    session["state"] = state
    print("state =", state)

    return redirect(authorization_url)


# Handle the response from Google authorization server with authorization code and request token
@googleAPI_bp.route("/sendmail/callback")
def sendmailCallback():

    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session["state"]
    googleClientConfig = getGoogleClientConfig()
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        googleClientConfig, scopes=SCOPES, state=state
    )
    # flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    #     CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
    # )
    flow.redirect_uri = url_for("googleAPI_bp.sendmailCallback", _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    print("authorization_response =", authorization_response)
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    # session["credentials"] = credentials_to_dict(credentials)
    credentials_json = credentials.to_json()
    print("credentials_json from flow:", credentials_json)
    saveGoogleCredentialsAsJson(current_user.id, credentials_json)
    db.session.commit()
    return redirect(url_for("googleAPI_bp.sendMail"))


@googleAPI_bp.route("/emailresult")
@login_required
def emailResult():
    emailResult = "Email sent successfully"
    return render_template(
        "mailresults.html",
        title="Email Result",
        user=current_user,
        emailResult=emailResult,
    )


@googleAPI_bp.route("/revoke")
def revoke():
    if "credentials" not in session:
        return (
            'You need to <a href="/authorize">authorize</a> before '
            + "testing the code to revoke credentials."
        )

    credentials = google.oauth2.credentials.Credentials(**session["credentials"])

    revoke = requests.post(
        "https://oauth2.googleapis.com/revoke",
        params={"token": credentials.token},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    status_code = getattr(revoke, "status_code")
    if status_code == 200:
        return "Credentials successfully revoked." + print_index_table()
    else:
        return "An error occurred." + print_index_table()


@googleAPI_bp.route("/clear")
def clear_credentials():
    if "credentials" in session:
        del session["credentials"]
    return "Credentials have been cleared.<br><br>" + print_index_table()


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def print_index_table():
    return (
        "<table>"
        + '<tr><td><a href="/test">Test an API request</a></td>'
        + "<td>Submit an API request and see a formatted JSON response. "
        + "    Go through the authorization flow if there are no stored "
        + "    credentials for the user.</td></tr>"
        + '<tr><td><a href="/testmail">Test Gmail API request</a></td>'
        + "<td>Send a test message. </td></tr>"
        + '<tr><td><a href="/authorize">Test the auth flow directly</a></td>'
        + "<td>Go directly to the authorization flow. If there are stored "
        + "    credentials, you still might not be prompted to reauthorize "
        + "    the application.</td></tr>"
        + '<tr><td><a href="/revoke">Revoke current credentials</a></td>'
        + "<td>Revoke the access token associated with the current user "
        + "    session. After revoking credentials, if you go to the test "
        + "    page, you should see an <code>invalid_grant</code> error."
        + "</td></tr>"
        + '<tr><td><a href="/clear">Clear Flask session credentials</a></td>'
        + "<td>Clear the access token currently stored in the user session. "
        + '    After clearing the token, if you <a href="/test">test the '
        + "    API request</a> again, you should go back to the auth flow."
        + "</td></tr></table>"
    )


###########################
#   Routes for Calendar   #
###########################

# Provide authentication credentials to your application code by setting the
# environment variable GOOGLE_APPLICATION_CREDENTIALS. Replace [PATH] with
# the file path of the JSON file that contains your service account key.
# This variable only applies to your current shell session, so if you open
# a new session, set the variable again.
# Example: export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
# See https://cloud.google.com/docs/authentication/production


from google.oauth2 import service_account


@googleAPI_bp.route("/submitcalendarevent")
def submitCalendarEvent():
    return render_template(
        "calendartest.html", title="Submit Calendar Event", calendarResult=None,
    )


@googleAPI_bp.route("/addcalendarevent")
def addCalendarEvent():
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    SERVICE_ACCOUNT_FILE = "google_credentials/p2mt_service_account_alpha816.json"

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = googleapiclient.discovery.build("calendar", "v3", credentials=credentials)

    event = {
        "summary": "Google I/O 2015",
        "location": "800 Howard St., San Francisco, CA 94103",
        "description": "A chance to hear more about Google's developer products.",
        "start": {
            "dateTime": "2020-08-19T09:00:00-07:00",
            "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": "2020-08-19T17:00:00-07:00",
            "timeZone": "America/Los_Angeles",
        },
        "recurrence": ["RRULE:FREQ=DAILY;COUNT=2"],
        "attendees": [{"email": "lpage@example.com"}, {"email": "sbrin@example.com"},],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 10},
            ],
        },
    }
    calendarId = "k4p5gughd8coai0f8j2afbc1m4@group.calendar.google.com"
    # event = service.events().insert(calendarId='primary', body=event).execute()
    event = service.events().insert(calendarId=calendarId, body=event).execute()
    print("Event created: %s" % (event.get("htmlLink")))
    eventLink = event.get("htmlLink")
    return render_template(
        "calendartest.html",
        title="Submit Calendar Event",
        calendarResult=flask.jsonify(eventLink),
    )


    printLogEntry("runnning sendMail()")
    requiredScope = ["https://www.googleapis.com/auth/gmail.send"]
    if "credentials" not in session:
        return redirect("authorize")
    print('session["credentials"] =', session["credentials"])
    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])
    print("Credentials from DB:", retrieveGoogleCredentials(current_user.id))
    # Create a Gmail API service with the authorized user credentials
    apiServiceName = "gmail"
    apiVersion = "v1"
    gmailService = googleapiclient.discovery.build(
        apiServiceName, apiVersion, credentials=credentials
    )

    # Call the Gmail API service to send the message
    sent = send_message(gmailService, "me", message)

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    # session["credentials"] = credentials_to_dict(credentials)
    # credentials_json = json.dumps(credentials_to_dict(credentials))
    credentials_json = credentials.to_json()
    print("credentials_json:", credentials_json)
    saveGoogleCredentialsAsJson(current_user.id, credentials_json)
    db.session.commit()
    return redirect("/emailresult")
    # return jsonify(credentials_to_dict(credentials))


# Initiating user authorization via Google for required Google API scopes
@googleAPI_bp.route("/authorizecalendar")
def authorize():
    printLogEntry("runnning authorize()")
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    # This version uses a client config mapping
    googleClientConfig = getGoogleClientConfig()
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        googleClientConfig, scopes=SCOPES
    )
    # This version uses the json (but not safe to upload json to GitHub)
    # flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    #     CLIENT_SECRETS_FILE, scopes=SCOPES
    # )

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = url_for("googleAPI_bp.sendmailCallback", _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type="offline",
        state="thisisthestate",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="false",
    )

    # Store the state so the callback can verify the auth server response.
    session["state"] = state
    print("state =", state)

    return redirect(authorization_url)


# Handle the response from Google authorization server with authorization code and request token
@googleAPI_bp.route("/addcalendarevent/callback")
def addCalendarEventCallback():

    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session["state"]
    googleClientConfig = getGoogleClientConfig()
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        googleClientConfig, scopes=SCOPES, state=state
    )
    # flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    #     CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
    # )
    flow.redirect_uri = url_for("googleAPI_bp.sendmailCallback", _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    print("authorization_response =", authorization_response)
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    # session["credentials"] = credentials_to_dict(credentials)
    credentials_json = credentials.to_json()
    print("credentials_json from flow:", credentials_json)
    saveGoogleCredentialsAsJson(current_user.id, credentials_json)
    db.session.commit()
    return redirect(url_for("googleAPI_bp.sendMail"))