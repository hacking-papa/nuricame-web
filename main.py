#!/usr/bin/env python3

import os
import time

import cv2
import numpy as np
import opencensus.trace.tracer
from flask import Flask, flash, render_template, request, redirect, make_response
from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter

import HED

if os.getenv("GAE_ENV", "").startswith("standard"):
    """ Production in the standard environment """
    from google.cloud import logging
    import googlecloudprofiler

    client = logging.Client()
    client.setup_logging()

    # TODO: Profiler for Debug.
    # It starts a daemon thread which continuously collects and uploads profiles.
    # Best done as early as possible.
    try:
        googlecloudprofiler.start(verbose=3)
    except (ValueError, NotImplementedError) as exc:
        app.logger.error(exc)
else:
    """ Local execution """
    pass

ALLOWED_EXTENSIONS = {"bmp", "dib", "jpg", "jpeg", "jpe", "jp2", "png", "webp", "pbm", "pgm", "ppm", "pxm", "pnm",
                      "pfm", "sr", "ras", "tiff", "tif", "exr", "hdr", "pic"}


def initialize_tracer(project_id):
    exporter = stackdriver_exporter.StackdriverExporter(
        project_id=project_id
    )
    tracer = opencensus.trace.tracer.Tracer(
        exporter=exporter,
        sampler=opencensus.trace.tracer.samplers.AlwaysOnSampler()
    )
    return tracer


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def redirect_with_flash(url, message, category):
    app.logger.debug(message)
    flash(message, category)
    return redirect(url)


app = Flask(__name__)
app.secret_key = b"}\xa8\xc3\xc3\xf60%\xe95\xfb\xb2}7\xdbb\xf7"
app.config["TRACER"] = initialize_tracer("nuricame-web")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        app.logger.info("GET /index")
        return render_template("index.html")
    elif request.method == "POST":
        app.logger.info("POST /index")
        start = time.time()

        if "image" not in request.files:
            return redirect_with_flash(request.url, "Warning: Image parameter not POSTed!", "is-warning")
        image = request.files.get("image")
        app.logger.debug(f"Uploaded: {image}")
        if image.filename == "":
            return redirect_with_flash(request.url, "Warning: No image has been selected!", "is-warning")
        if not allowed_file(image.filename):
            return redirect_with_flash(request.url, "Warning: Unauthorized extensions!", "is-warning")

        img = np.frombuffer(image.read(), dtype=np.uint8)
        img = cv2.imdecode(img, 1)
        img = HED.convert(img)
        data = cv2.imencode(".png", img)[1].tostring()
        response = make_response()
        response.data = data
        response.mimetype = "image/png"
        app.logger.info(f"Elapsed Time: {time.time() - start}")
        return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
