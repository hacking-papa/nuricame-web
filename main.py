#!/usr/bin/env python3

import os
import time
from base64 import b64encode

import cv2
import numpy as np
import opencensus.trace.tracer
from flask import Flask, flash, redirect, render_template, request, send_from_directory
from flask_debugtoolbar import DebugToolbarExtension
from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter

import Frame
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


def redirect_with_flash(url, message, category):
    app.logger.debug(message)
    flash(message, category)
    return redirect(url)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory("static", "favicon.ico")


@app.route("/manifest.json")
def manifest():
    return send_from_directory("static", "manifest.json")


@app.route("/apple-touch-icon.png")
def apple_touch_icon():
    return send_from_directory("static", "apple-touch-icon.png")


@app.route("/android-chrome-192x192.png")
def android_chrome_192x192():
    return send_from_directory("static", "android-chrome-192x192.png")


@app.route("/android-chrome-512x512.png")
def android_chrome_512x512():
    return send_from_directory("static", "android-chrome-512x512.png")


@app.route("/", methods=["GET"])
def index():
    app.logger.debug("GET /index")
    allowed_extensions = ["." + x for x in ALLOWED_EXTENSIONS]
    return render_template("index.html", allowed_extensions=allowed_extensions)


@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "GET":
        app.logger.debug("GET /result")
        return redirect("/")
    app.logger.debug("POST /result")
    start = time.time()

    if "image" not in request.files:
        app.logger.warning("Image parameter not POSTed!")
        return redirect_with_flash("/", "Warning: イメージパラメータがありません！", "is-warning")
    image = request.files.get("image")
    app.logger.debug(f"Uploaded: {image}")
    if image.filename == "":
        app.logger.warning("No image has been selected!")
        return redirect_with_flash("/", "Warning: 画像が選ばれていません。もう一度はじめからやりなおしてください。", "is-warning")
    if not allowed_file(image.filename):
        app.logger.warning("Unauthorized extensions!")
        return redirect_with_flash("/", "Warning: ぬりえにできない種類の画像です。違う画像でお試しください。", "is-warning")

    try:
        img = image.read()
        img = np.frombuffer(img, dtype=np.uint8)
        img = cv2.imdecode(img, 1)
    except Exception as e:
        app.logger.error(f"Exception: {e}")
        return redirect_with_flash("/", "Warning: 画像の読み込みに失敗しました。 もう一度はじめからやりなおしてください。", "is-warning")
    img = HED.convert(img)
    framed = Frame.compose(img)
    data = cv2.imencode(".png", framed)[1].tostring()
    nurie = b64encode(data).decode("utf-8")
    app.logger.debug(f"Elapsed Time: {time.time() - start}")
    return render_template("result.html", nurie=nurie)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
