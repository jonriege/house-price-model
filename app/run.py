"""Run the Flask application."""
import json

from flask import Flask, render_template

from app.data_loading import load_house_prices
from app.model import store_data_and_model_preds, train_validate_model
from app.utils import load_config

config = load_config()
app = Flask(__name__)


def run_model_pipeline() -> None:
    """Runs the model pipeline and stores the results."""
    data = load_house_prices(config=config)["value"]
    model, mape = train_validate_model(config=config, data=data)
    store_data_and_model_preds(config=config, data=data, model=model, mape=mape)


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
