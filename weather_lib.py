# standard library
import os
from datetime import date, timedelta

# third-party libraries
import requests
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def get_weather_data():
    today = date.today()
    end_date = today - timedelta(days=2)
    start_date = end_date - timedelta(days=40)

    url = "https://archive-api.open-meteo.com/v1/era5"
    params = {
        "latitude": 51.509865,
        "longitude": 0.118092,
        "time_mode": "time_interval",
        "start_date": start_date,
        "end_date": end_date,
        "daily": ["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean"],
        "timezone": "GMT"
    }

    response = requests.get(url, params=params)
    resp = response.json()
    return pd.DataFrame(resp["daily"])

def transform(df):
    transformed_df = df.rename(columns={"time":"date"})
    return transformed_df

def save_to_db(df):
    load_dotenv()
    supabase_db_url = os.getenv("SUPABASE_DB_URL")

    engine = create_engine(supabase_db_url)

    df.to_sql("open_meteo_temp", engine, if_exists="replace", index=False)

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO open_meteo (date, temperature_2m_max, temperature_2m_min, temperature_2m_mean)
            SELECT date, temperature_2m_max, temperature_2m_min, temperature_2m_mean FROM open_meteo_temp
            ON CONFLICT (date) DO UPDATE
            SET temperature_2m_max = EXCLUDED.temperature_2m_max,
                temperature_2m_min = EXCLUDED.temperature_2m_min,
                temperature_2m_mean = EXCLUDED.temperature_2m_mean;
        """))

    result = pd.read_sql("select * from open_meteo", engine)
    return result