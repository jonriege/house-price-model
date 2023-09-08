"""Run the Flask application."""
import json

from flask import Flask, render_template

from app.utils import load_config

config = load_config()
app = Flask(__name__)


@app.route("/")
def main() -> str:
    with open(config["app"]["data_path"], "r") as file:
        data = json.load(file)
    return render_template("home/index.html", data=data)


@app.errorhandler(404)
def page_not_found(_: Exception) -> str:
    return render_template("home/page-404.html")


@app.errorhandler(500)
def internal_server_error(_: Exception) -> str:
    return render_template("home/page-500.html")
