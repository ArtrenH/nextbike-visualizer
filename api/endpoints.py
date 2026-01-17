from flask import Blueprint, jsonify, request, abort
from .read_db import *
from datetime import datetime
import pandas as pd

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

@api_bp.route("/active_standing_times/<city_uid>", methods=["GET"])
def active_standing_times(city_uid):
    # format: 2025-11-03 12:50:00
    ts = request.args.get("timestamp")
    ts_start = request.args.get("timestamp_start")
    ts_end = request.args.get("timestamp_end")
    if (not ts) and (not ts_start and ts_end):
        abort(400, description="Missing timestamp")
    if ts:
        return jsonify(get_active_standing_times(city_uid, ts))
    return jsonify(get_standing_times_overlapping_interval(city_uid, ts_start, ts_end))

@api_bp.route("/active_trips/<city_uid>", methods=["GET"])
def active_trips(city_uid):
    # format: 2025-11-03 12:50:00
    ts = request.args.get("timestamp")
    ts_start = request.args.get("timestamp_start")
    ts_end = request.args.get("timestamp_end")
    if (not ts) and (not ts_start and ts_end):
        abort(400, description="Missing timestamp")
    if ts:
        return jsonify(get_active_trips(city_uid, ts))
    return jsonify(get_trips_overlapping_interval(city_uid, ts_start, ts_end))
