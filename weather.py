from weather_lib import get_weather_data, transform, save_to_db

def main():
    df = get_weather_data()
    transformed_df = transform(df)
    save_to_db(transformed_df)
    print("Success!")

main()