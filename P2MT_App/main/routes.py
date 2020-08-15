from flask import render_template, redirect, url_for, flash, request, Blueprint
from P2MT_App import db
from P2MT_App.main.setupFunctions import initializeInterventionTypes

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def home():
    return render_template("home.html", title="Home")


@main_bp.route("/about")
def displayAbout():
    return render_template("about.html", title="About")


@main_bp.route("/setupP2mt")
def setupP2mt():
    initializeInterventionTypes()
    return redirect(url_for("p2mtAdmin_bp.displayP2MTAdmin"))


# Temporary routes for testing new features


@main_bp.route("/analytics")
def displayAnalyticsTest():
    return render_template("analytics.html")


@main_bp.route("/sandbox")
def displaySandbox():
    return render_template("sandbox.html")
