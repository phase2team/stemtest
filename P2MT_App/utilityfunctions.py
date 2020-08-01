import os
from flask import send_file
from P2MT_App import app


def save_File(form_UploadedFileData, filename):
    file_path = os.path.join(app.root_path, "static/upload", filename)
    form_UploadedFileData.save(file_path)
    return file_path


def download_File(filename):
    file_path = os.path.join(app.root_path, "static/uploadfiles", filename)
    print("download_File function called with filename=", file_path)
    return send_file(file_path, as_attachment=True, cache_timeout=0)
