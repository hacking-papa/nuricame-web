#!/usr/bin/env python3

import os
import time

import cv2
import numpy as np
from flask import Flask, render_template, request, make_response

if os.getenv("GAE_ENV", "").startswith("standard"):
    # Production in the standard environment
    from google.cloud import logging

    client = logging.Client()
    client.setup_logging()
else:
    # Local execution
    pass

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        app.logger.info("GET /index")
        return render_template("index.html", title="ぬりカメ")
    elif request.method == "POST":
        app.logger.info("POST /index")
        start = time.time()
        image = request.files.get("image")
        app.logger.debug(f"Uploaded: {image}")
        img = np.frombuffer(image.read(), dtype=np.uint8)
        img = cv2.imdecode(img, 1)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        data = cv2.imencode(".jpg", img)[1].tostring()
        response = make_response()
        response.data = data
        response.mimetype = "image/jpeg"
        app.logger.debug(f"Elapsed Time: {time.time() - start}")
        return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
