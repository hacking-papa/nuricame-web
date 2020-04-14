#!/usr/bin/env python3
import os

from flask import Flask, render_template

if os.getenv("GAE_ENV", "").startswith("standard"):
    # Production in the standard environment
    from google.cloud import logging

    client = logging.Client()
    client.setup_logging()
else:
    # Local execution
    pass

app = Flask(__name__)


@app.route("/")
def index():
    app.logger.info("/index from app.logger")
    return render_template("index.html", title="ぬりカメ")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
