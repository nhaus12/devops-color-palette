import json
import os
import pathlib

from flask import Flask, request
from flask.logging import create_logger
from werkzeug.utils import secure_filename
import pywal

UPLOAD_FOLDER = "./tmp/"
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'svg']

pathlib.Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
app = Flask(__name__)
LOG = create_logger(app)


def color_dict_to_json(color_dict):
    color_dict.pop("wallpaper")
    color_dict.pop("alpha")
    return json.dumps(color_dict)


def gen_color_palette(filepath):
    palette_dict = pywal.colors.get(filepath)
    palette = color_dict_to_json(palette_dict)
    return palette


@app.route("/")
def index():
    return "This is the color palette API"


@app.route("/palette", methods=['POST'])
def palette_endpoint():

    if not 'image' in request.files:
        return "(!) Please upload an image\n"
    
    file = request.files['image']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        file.save(filepath)
        palette = gen_color_palette(filepath)
    except Exception as e:
        LOG.error(f"Could not save image {filename} to {UPLOAD_FOLDER}: {e}")
        return "Error: could not process the provided image. Please try again or upload a different image."

    return palette


app.run(host="0.0.0.0", port=80)