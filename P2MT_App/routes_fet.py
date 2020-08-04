import os
import secrets
from datetime import datetime
from P2MT_App import app
from flask import Flask, render_template, url_for, flash, redirect, request
from P2MT_App.forms import UploadFetDataForm
from P2MT_App.generateFetOutputFiles import ripFetFiles


@app.route("/fettoolshelp")
def fetToolsHelp():
    print("===   Displaying Help page   ===  ", datetime.now(), "   ===")
    return render_template("fettoolshelp.html", title="Help")


def save_csvFile(form_csvFetFile, filename):
    file_path = os.path.join(app.root_path, "static/fet_data_files", filename)
    form_csvFetFile.save(file_path)
    # file1 = open(file_path, "w")
    # file1.write(form_csvFetFile.data)
    # file1.close()
    return file_path


@app.route("/fettools", methods=["GET", "POST"])
def displayFetTools():
    form = UploadFetDataForm()
    if form.validate_on_submit():
        if form.csvFetStudentInputFile.data:
            FetStudentInputFile = save_csvFile(
                form.csvFetStudentInputFile.data, "FET_Student_Input_File.csv"
            )
        if form.csvFetClassTeacherInputFile.data:
            FetClassTeacherInputFile = save_csvFile(
                form.csvFetClassTeacherInputFile.data,
                "FET_Class_Teacher_Input_File.csv",
            )
        if form.csvFetTimetableInputFile.data:
            FetTimeTableFile = save_csvFile(
                form.csvFetTimetableInputFile.data, "FET_Timetable_File.csv"
            )
        flash("Your account has been updated!", "success")
        output_file_path = os.path.join(app.root_path, "static/fet_data_files")
        ripFetFiles(
            form.yearOfGraduation.data,
            form.schoolYear.data,
            form.semester.data,
            FetStudentInputFile,
            FetClassTeacherInputFile,
            FetTimeTableFile,
            output_file_path,
        )
        print(
            "===   Completed ripFetFiles.  Redirecting to fetOutputFiles   ===",
            datetime.now(),
            "   ===",
        )
        return redirect(url_for("fetOutputFiles"))
    elif request.method == "GET":
        return render_template(
            "fettools.html", title="FET Tools", UploadFetDataForm=form
        )
    print(form.errors)


@app.route("/fetoutputfiles", methods=["GET"])
def fetOutputFiles():
    print("===  Arriving at fetOutputFiles   ===", datetime.now(), "   ===")
    return render_template("fetoutputfiles.html", title="FET Output Files")
