import requests
from datetime import date, timedelta
import pandas as pd

today = date.today()
end_date = today - timedelta(days=2)
start_date = end_date - timedelta(days=30)

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

df = pd.DataFrame(resp["daily"])
print(df)