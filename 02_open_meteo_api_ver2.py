# ------------------------------------------------------

# This code, originally copied from open meteo, was adjusted for our needs. The original code included two lists of coordinate data - one with latitudes, one with longtitudes. The aim of is to rewrite the code so that instead of using a list, it utilizes a reference to a CSV file containing coordinates. This way, it will more versatile in the future, for example, if I manage to obtain a point map of a specific area - eg Czech Republic.

# The original code was processing only the first location, therefore for-loop was added so that the user gets data from all the coordinates in the list. More adjustments were needed in order to be able to obtain a suitable CSV file. I wanted to make sure each row would have coordinates as well, or an index of the location. That would make it easier in the future when analyzing with SQL and joins, or in PowerBi (I will see how I will proceed). Generally I want a tie between the location and the meteorological data.

# Now it is done. Every line will start with its coordinates and elevation.

#For the future: if I get coordinates of the whole country, this will be a lot of data. It will be handy to rewrite the code for date in such a way that I get only dates that I am interested in - eg. 25.11. each year and 24.12. each year. That could be done by adding another for loop in the outer layer which would change start and end date for each run of the for loop. It would mean several downloads from the site. I know open meteo allows me to run only certain amount of downloads - and I do not know if it is number of downloads or data size dependent. I guess I will have to try & see.

# ------------------------------------------------------
    
# Instalations:

# pip install openmeteo-requests
# pip install requests-cache retry-requests numpy pandas

# ------------------------------------------------------

# Ipmorts
import time
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Adjustment - opening the file with coordinates, making lists of latitudes and longtitudes

file_path = "data/02_souradnice.csv"
latitude = []
longitude = []
elevation = []

with open(file_path, mode="r", encoding="utf-8") as my_file:
    print(my_file)
    for index, line in enumerate(my_file):
        if index == 0:
            continue
        line = line.split(",")
        line = [float(item.strip()) for item in line]
        latitude.append(line[0])
        longitude.append(line[1])
        elevation.append(line[2])


latitude = latitude[:5]
longitude = longitude[:5]

# to get a list of days I am interested in so I can download data only for these dates
days = ["11-25", "12-31"]
start_year = 1940
end_year = 2023
all_days = []

for year in range(start_year, end_year + 1):
    for day in days:
        all_days.append(f"{year}-{day}")

whole_data = []

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://archive-api.open-meteo.com/v1/archive"

# for loop to run the code only for days I am interested in. This wau I am downloading only the data I need - 2 days each year, not 365(6)...
for i, single_day in enumerate(all_days, start=1):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": single_day,
        "end_date": single_day,
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean", "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean", "sunrise", "sunset", "daylight_duration", "sunshine_duration", "precipitation_sum", "rain_sum", "snowfall_sum", "precipitation_hours", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant", "shortwave_radiation_sum", "et0_fao_evapotranspiration"]
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    for index, response in enumerate(responses):
        for_list = []

        daily = response.Daily()
        daily_weather_code = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
        daily_temperature_2m_mean = daily.Variables(3).ValuesAsNumpy()
        daily_apparent_temperature_max = daily.Variables(4).ValuesAsNumpy()
        daily_apparent_temperature_min = daily.Variables(5).ValuesAsNumpy()
        daily_apparent_temperature_mean = daily.Variables(6).ValuesAsNumpy()
        daily_sunrise = daily.Variables(7).ValuesAsNumpy()
        daily_sunset = daily.Variables(8).ValuesAsNumpy()
        daily_daylight_duration = daily.Variables(9).ValuesAsNumpy()
        daily_sunshine_duration = daily.Variables(10).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(11).ValuesAsNumpy()
        daily_rain_sum = daily.Variables(12).ValuesAsNumpy()
        daily_snowfall_sum = daily.Variables(13).ValuesAsNumpy()
        daily_precipitation_hours = daily.Variables(14).ValuesAsNumpy()
        daily_wind_speed_10m_max = daily.Variables(15).ValuesAsNumpy()
        daily_wind_gusts_10m_max = daily.Variables(16).ValuesAsNumpy()
        daily_wind_direction_10m_dominant = daily.Variables(17).ValuesAsNumpy()
        daily_shortwave_radiation_sum = daily.Variables(18).ValuesAsNumpy()
        daily_et0_fao_evapotranspiration = daily.Variables(19).ValuesAsNumpy()

        daily_data = {"date": [date.strftime("%Y-%m-%d") for date in pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s", utc=True).date(),
                end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True).date(),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left"
        )]}
        daily_data["weather_code"] = daily_weather_code
        daily_data["temperature_2m_max"] = daily_temperature_2m_max
        daily_data["temperature_2m_min"] = daily_temperature_2m_min
        daily_data["temperature_2m_mean"] = daily_temperature_2m_mean
        daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
        daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
        daily_data["apparent_temperature_mean"] = daily_apparent_temperature_mean
        daily_data["sunrise"] = daily_sunrise
        daily_data["sunset"] = daily_sunset
        daily_data["daylight_duration"] = daily_daylight_duration
        daily_data["sunshine_duration"] = daily_sunshine_duration
        daily_data["precipitation_sum"] = daily_precipitation_sum
        daily_data["rain_sum"] = daily_rain_sum
        daily_data["snowfall_sum"] = daily_snowfall_sum
        daily_data["precipitation_hours"] = daily_precipitation_hours
        daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
        daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
        daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant
        daily_data["shortwave_radiation_sum"] = daily_shortwave_radiation_sum
        daily_data["et0_fao_evapotranspiration"] = daily_et0_fao_evapotranspiration

        for line in for_list:
            whole_data.append(line)

        daily_dataframe = pd.DataFrame(data=daily_data)
        for_list.extend(daily_dataframe.values.tolist())

        lat = latitude[index]
        lon = longitude[index]
        ele = elevation[index]

        for inner_list in for_list:
            inner_list.insert(0, ele)
            inner_list.insert(0, lon)
            inner_list.insert(0, lat)
        
        for line in for_list:
            whole_data.append(line)


    # sleep time is aded due to the fact that open-meteo enables only 600 api requests per minute, 5000 per hour and 10000 per day. This code (that downloads only the dates we need) will be useful only for smaller data sets as otherwise waiting for 'the gate to be opened again' would take ages. In cases of need of a bigger set one needs to download it preferably as the interval (as it is in the previous version of this code) & then clear up the data he/she does not need.
    if i % 600 == 0:
        time.sleep(60)
    elif i % 5000 == 0:
        time.sleep(360)


df_whole_data = pd.DataFrame(whole_data, columns = ["latitude", "longtitude", "elevation", "date", "weather_code", "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean", "apparent_temperature_max", "apparent_temperature_min", "apparent_temperature_mean", "sunrise", "sunset", "daylight_duration", "sunshine_duration", "precipitation_sum", "rain_sum", "snowfall_sum", "precipitation_hours", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant", "shortwave_radiation_sum", "et0_fao_evapotranspiration"])

df_whole_data.to_csv("data/open_meteo_1_ver2.csv", encoding="utf-8")



 