from flask import Flask, render_template, request, redirect, send_from_directory
from PIL import Image
import os
import datetime
import random
import string
import cv2
import numpy as np

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/customerPicture"
app.config["BW_FOLDER"] = "static/bwPicture"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def remove_background(filename):
    # Load the image
    image = cv2.imread(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    base = image

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to the grayscale image to create a binary image
    ret, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)

    # Find the contours of the binary image
    contours, hierarchy = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on the original image
    cv2.drawContours(image, contours, -1, (255, 255, 255), 5)
    image = cv2.subtract(image, base)


    image = cv2.GaussianBlur(image, (3,3), 0)

    image = cv2.add(base, image)

    return image

    # Save the processed image
    #cv2.imwrite(os.path.join(app.config["PROCESSED_FOLDER"], "processed.jpg"), foreground)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file selected"
        file = request.files["file"]
        if file.filename == "":
            return "No file selected"
        if file and allowed_file(file.filename):
            # Get the current date in YYYYMMDD format
            date = datetime.datetime.today().strftime("%Y%m%d")
            # Generate a random salt of length 8
            salt = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

            # Add the date to the beginning of the filename
            file.filename = "-".join((date, salt, file.filename))

            # Save the file to the customerPicture folder
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
            print(file.filename)

            # Convert the original image to black and white
            bw_image = remove_background(file.filename)
            cv2.imwrite(os.path.join(app.config["BW_FOLDER"], file.filename), bw_image)
            return render_template("preview.html", filepath=os.path.join(app.config["BW_FOLDER"], file.filename))
        else:
            redirect("/")
            #return "Error: Only image files are allowed."
    return render_template("index.html")
    

@app.route('/bw/<filename>')
def bw(filename):
    return send_from_directory(app.config["BW_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True, port=42100, host="192.168.128.202")
