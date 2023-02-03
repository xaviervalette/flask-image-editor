from flask import Flask, render_template, request, redirect, send_from_directory
from PIL import Image
import os
import datetime
import random
import string
import cv2
import numpy as np
from rembg import remove
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
app = Flask(__name__)
app.config["INPUT_FOLDER"] = "static/ej1JG0QeqnLcHy7OoaZJ-inputImg"
app.config["OUTPUT_FOLDER"] = "static/DWgpqdq6z7n3mBFoIVjU-outputImg"

limiter = Limiter(
    get_remote_address,
    app=app,
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def removeOldFiles(folder_path):
    current_time = datetime.datetime.today()
    for filename in os.listdir(folder_path):
        filename_parts = filename.split("-")
        file_time_str = filename_parts[0]
        file_time = datetime.datetime.strptime(file_time_str, "%Y%m%d%H%M%S")
        time_difference = current_time - file_time
        if time_difference >= datetime.timedelta(minutes=5):
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)

removeOldFiles(app.config["OUTPUT_FOLDER"])
removeOldFiles(app.config["INPUT_FOLDER"])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def backgroundRemove(filename):
    input = cv2.imread(os.path.join(app.config["INPUT_FOLDER"], filename))
    output = remove(input)
    return(output)

@app.route("/", methods=["GET", "POST"])
@limiter.limit("60 per hour")

def home():
    error = request.args.get('error')
    if request.method == "POST":
        if "file" not in request.files:
            return redirect("/?error=noFileSelected")
        file = request.files["file"]
        if file.filename == "":
            return redirect("/?error=noFileSelected")
        if file and allowed_file(file.filename):
            # Get the current date in YYYYMMDD format
            date = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
            # Generate a random salt of length 8
            salt = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

            # Add the date to the beginning of the filename
            file.filename = "-".join((date, salt, file.filename))

            # Save the file to the customerPicture folder
            file.save(os.path.join(app.config["INPUT_FOLDER"], file.filename))
            print(file.filename)

            # Convert the original image to black and white
            bw_image = backgroundRemove(file.filename)
            cv2.imwrite(os.path.join(app.config["OUTPUT_FOLDER"], file.filename), bw_image)
            print("/preview/"+file.filename)
            return redirect("/preview/"+file.filename)
            #return render_template("preview.html", filepath=os.path.join(app.config["OUTPUT_FOLDER"], file.filename))
        else:
            return redirect("/?error=wrongFileType")
            #return "Error: Only image files are allowed."
    return render_template("index.html", error=error)

@app.route('/preview/<filename>', methods=["GET"])
def preview(filename):
    return render_template("preview.html", filepath="/"+os.path.join(app.config["OUTPUT_FOLDER"],filename))

@app.route('/notFound', methods=["GET"])
def noFound():
    return render_template("404.html"), 404

@app.route('/tooManyRequest', methods=["GET"])
def tooManyRequest():
    return render_template("429.html"), 429

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return redirect('/notFound')

@app.errorhandler(429)
def too_many_request(e):
    # note that we set the 404 status explicitly
    return render_template("429.html"), 429
    #return redirect('/tooManyRequest')

if __name__ == "__main__":
    app.run(debug=True, port=42100, host="0.0.0.0")
