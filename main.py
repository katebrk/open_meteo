import functions_framework
from weather_lib import get_weather_data, transform, save_to_db

@functions_framework.http
def extract_and_store_weather_data(request):

    df = get_weather_data()
    transformed_df = transform(df)
    save_to_db(transformed_df)

    print("Success!")