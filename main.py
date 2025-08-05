from flask import Flask, request, render_template, flash, send_file
from werkzeug.utils import secure_filename
import os
import cv2  # opencv python library

# upload file settings
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"webp", "png", "jpg", "jpeg", "gif"}

# base dir
basedir = os.path.abspath(os.path.dirname(__file__))

# init flask app
app = Flask(__name__)
app.secret_key = "super secret key"

# apps upload folder
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# limiting allowed files
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# processing image
def processImage(filename, operation):
    print(filename, operation)
    img = cv2.imread(f"{basedir}/uploads/{filename}")
    match operation:
        case "cgray":
            name = filename
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFile = f"{basedir}/static/{filename}"
            cv2.imwrite(newFile, imgProcessed)
            return name
        case "cpng":
            name = f"{filename.split('.')[0]}.png"
            newFile = f"{basedir}/static/{name}"
            cv2.imwrite(newFile, img)
            return name
        case "cjpeg":
            name = f"{filename.split('.')[0]}.jpeg"
            newFile = f"{basedir}/static/{name}"
            cv2.imwrite(newFile, img)
            return name
        case "cjpg":
            name = f"{filename.split('.')[0]}.jpg"
            newFile = f"{basedir}/static/{name}"
            cv2.imwrite(newFile, img)
            return name


# first web page
@app.route("/")
def home():
    return render_template("index.html")


# image editing
@app.route("/edit", methods=["GET", "POST"])
def edit():
    operation = request.form.get("operation")
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file Submission")
            return render_template("index.html")
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return render_template("index.html")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(basedir, app.config["UPLOAD_FOLDER"], filename))
            processedImg = processImage(filename, operation)
            flash(
                f"Your image has been processed and is available <a href='/static/{processedImg}' target ='_blank'> here</a> ",
                "success"
            )
            return render_template("index.html")
    return render_template("index.html")


# runserver - updated for Render deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
