"""Run the Flask application."""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def main() -> str:
    return "Hello world!"
