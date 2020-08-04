from flask import render_template, redirect, flash, request, Blueprint
from P2MT_App import db

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html", title="Home")


@main.route("/about")
def displayAbout():
    return render_template("about.html", title="About")


# Temporary routes for testing new features


@main.route("/analytics")
def displayAnalyticsTest():
    return render_template("analytics.html")
