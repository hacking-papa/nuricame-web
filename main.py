#!/usr/bin/env python3

import os
import time

import cv2
import numpy as np
import opencensus.trace.tracer
from flask import Flask, flash, render_template, request, redirect, make_response, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter

import HED

app = Flask(__name__)
app.secret_key = os.urandom(24)


def initialize_tracer(project_id):
    exporter = stackdriver_exporter.StackdriverExporter(
        project_id=project_id
    )
    tracer = opencensus.trace.tracer.Tracer(
        exporter=exporter,
        sampler=opencensus.trace.tracer.samplers.AlwaysOnSampler()
    )
    return tracer


if os.getenv("GAE_ENV", "").startswith("standard"):
    """ Production in the standard environment """
    from google.cloud import logging
    import googlecloudprofiler

    client = logging.Client()
    client.setup_logging()

    try:
        googlecloudprofiler.start(verbose=3)
    except (ValueError, NotImplementedError) as exc:
        app.logger.error(exc)
else:
    """ Local execution """
    app.debug = True

    import flask_monitoringdashboard as dashboard

    dashboard.bind(app)  # for Profiling
    toolbar = DebugToolbarExtension(app)  # for Profiling
    app.config["DEBUG_TB_PROFILER_ENABLED"] = True  # for Profiling

app.config["TRACER"] = initialize_tracer("nuricame-web")  # for Profiling

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MiB
ALLOWED_EXTENSIONS = {"bmp", "dib", "jpg", "jpeg", "jpe", "jp2", "png", "webp", "pbm", "pgm", "ppm", "pxm", "pnm",
                      "pfm", "sr", "ras", "tiff", "tif", "exr", "hdr", "pic"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        app.logger.debug("GET /index")
        return render_template("index.html")
    elif request.method == "POST":
        app.logger.debug("POST /index")
        start = time.time()

        if "image" not in request.files:
            app.logger.warning("Image parameter not POSTed!")
            return jsonify({"error_code": 40000, "message": "Warning: Image parameter not POSTed!"}), 400
        image = request.files.get("image")
        app.logger.debug(f"Uploaded: {image}")
        if image.filename == "":
            app.logger.warning("No image has been selected!")
            return jsonify({"error_code": 41500, "message": "Warning: No image has been selected!"}), 415
        if not allowed_file(image.filename):
            app.logger.warning("Unauthorized extensions!")
            return jsonify({"error_code": 41501, "message": "Warning: Unauthorized extensions!"}), 415

        img = np.frombuffer(image.read(), dtype=np.uint8)
        img = cv2.imdecode(img, 1)
        img = HED.convert(img)
        data = cv2.imencode(".png", img)[1].tostring()
        response = make_response()
        response.data = data
        response.mimetype = "image/png"
        app.logger.debug(f"Elapsed Time: {time.time() - start}")
        return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
