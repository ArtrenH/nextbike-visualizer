import pandas as pd
from dotenv import load_dotenv
import os

from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def query_df(db_url: str, sql: str, params=None) -> list[dict]:
    return pd.read_sql_query(sql, db_url, params=params).to_dict(orient="records")


def get_countries():
    return query_df(
        DATABASE_URL,
        """
        SELECT *
        FROM countries
        """,
    )
    
def get_cities():
    return query_df(
        DATABASE_URL,
        """
        SELECT *
        FROM cities
        """,
    )

def get_places(city_id):
    return query_df(
        DATABASE_URL,
        """
        SELECT p.*
        FROM places p
        JOIN city_places cp ON cp.place_id = p.id
        WHERE cp.city_id = %s
        """,
        params=(city_id,),
    )

def get_active_standing_times(city_uid, timestamp):
    return query_df(
        DATABASE_URL,
        """
        SELECT *
        FROM bike_parking
        WHERE city_uid = %s
        AND start_time <= %s AND end_time >= %s
        """,
        params=(city_uid,timestamp,timestamp),
    )

def get_active_trips(city_uid, timestamp):
    return query_df(
        DATABASE_URL,
        """
        SELECT *
        FROM bike_trips
        WHERE (start_city_uid = %s OR end_city_uid = %s)
        AND start_time <= %s AND end_time >= %s
        """,
        params=(city_uid,timestamp,timestamp),
    )

def get_standing_times_overlapping_interval(city_uid, from_ts, to_ts):
    return query_df(
        DATABASE_URL,
        """
        SELECT *
        FROM bike_parking
        WHERE city_uid = %s
          AND start_time <= %s
          AND end_time >= %s
        """,
        params=(city_uid, to_ts, from_ts),
    )

def get_trips_overlapping_interval(city_uid, from_ts, to_ts):
    return query_df(
        DATABASE_URL,
        """
        SELECT *
        FROM bike_trips
        WHERE (start_city_uid = %s OR end_city_uid = %s)
          AND start_time <= %s
          AND end_time >= %s
        """,
        params=(city_uid, city_uid, to_ts, from_ts),
    )

def get_standing_bikes(city_uid, timestamp):
    ...

def get_moving_bikes_linear(city_uid, timestamp):
    ...

df = query_df(
    DATABASE_URL,
    """
    SELECT name, lat, lng, lat_min, lng_min, lat_max, lng_max
    FROM cities
    """,
)
