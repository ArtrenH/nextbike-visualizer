from flask import Blueprint, jsonify
from .read_db import *

api_bp = Blueprint("api", __name__)

@api_bp.route("/countries", methods=["GET"])
def countries():
    return jsonify(get_countries())

@api_bp.route("/cities", methods=["GET"])
def cities():
    return jsonify(get_cities())

@api_bp.route("/places/<city_uid>", methods=["GET"])
def places(city_uid):
    return jsonify(get_places(city_uid))
