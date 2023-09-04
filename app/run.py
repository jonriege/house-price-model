"""Run the Flask application."""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def main() -> str:
    return render_template("home/index.html")


@app.errorhandler(404)
def page_not_found(_: Exception) -> str:
    return render_template("home/page-404.html")


@app.errorhandler(500)
def internal_server_error(_: Exception) -> str:
    return render_template("home/page-500.html")
