#!/usr/bin/env python3


from flask import Flask, render_template

# [START gae_python37_app]
app = Flask(__name__)


@app.route("/")
def index():
    app.logger.info("/index")
    return render_template("index.html", title="ぬりカメ")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
# [END gae_python37_app]
