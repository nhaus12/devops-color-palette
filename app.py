import json
import os
import pathlib

from flask import Flask, request
from flask.logging import create_logger
from werkzeug.utils import secure_filename
import pywal

UPLOAD_FOLDER = "./tmp/"
# TODO populate with image type extensions
ALLOWED_EXTENSIONS = []

pathlib.Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
app = Flask(__name__)
# TODO: fix duplicate logs – see https://stackoverflow.com/questions/7173033/duplicate-log-output-when-using-python-logging-module/55877763#55877763
LOG = create_logger(app)

def gen_color_palette(filepath):

    palette_dict = pywal.colors.get(filepath)
    palette_dict.pop("wallpaper")
    palette_dict.pop("alpha")

    return json.dumps(palette_dict)


@app.route("/")
def index():
    # TODO: return welcome message and help information 
    return "This is the color palette API"


@app.route("/palette", methods=['POST'])
def palette_endpoint():

    if not 'image' in request.files:
        return "[!] Please upload an image\n"
    
    file = request.files['image']
    # TODO: check if file type is allowed
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try: 
        file.save(filepath)
    except:
        LOG.error(f"Could not save image {filename} to {UPLOAD_FOLDER}")
        return f"Error: could not process the provided image. Please try again or upload a different image."

    try: 
        palette = gen_color_palette(filepath)
    except:
        LOG.error(f"Could not generate color palette for {filepath}")
        return f"Error: could not generate color palette for the provided image."

    return palette


app.run(host="0.0.0.0", port=80)