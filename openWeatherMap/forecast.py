import requests
from pprint import pprint
from collections import Counter
from datetime import datetime, timedelta

API_KEY = 'your api key from openweathermap.org'
BASE_URL = 'https://api.openweathermap.org/data/2.5/forecast?appid={}&units=metric'.format(API_KEY)
    

def get_forecast_report(API_ENDPOINT):
    res = requests.get(API_ENDPOINT)
    data = res.json()

    if data['cod'] == '404':
        response = 'Invalid location:(\nTry again...'
    else:
        country_code = data['city']['country']
        country_name = requests.get('https://restcountries.eu/rest/v2/alpha/{}'.format(country_code)).json()['name']

        location = data['city']['name']

        forecast_data = data['list']
        forecast_dict = {}
        
        d = datetime.utcnow() + timedelta(1)
        max_temp = -10000
        min_temp = 10000
        response = "Tomorrow's weather forecast in {}({}) -\n\n".format(location, country_name)
        
        for forecast in forecast_data:
            d_ts = datetime.fromtimestamp(forecast['dt'])

            if d.date() == d_ts.date():
                response += '* {} - {}\n'.format(d_ts.time(), forecast['weather'][0]['description'])

                if max_temp < forecast['main']['temp_max']:
                    max_temp = forecast['main']['temp_max']
                
                if min_temp > forecast['main']['temp_min']:
                    min_temp = forecast['main']['temp_min']

        response += "\nHigh: {}\N{DEGREE SIGN} Low: {}\N{DEGREE SIGN}".format(max_temp, min_temp)
        
    return response


def get_forecast_by_city(city_name):
    API_ENDPOINT = BASE_URL + '&q={}'.format(city_name)

    return get_forecast_report(API_ENDPOINT)


def get_forecast_by_city_and_country(city_name, country_code):
    API_ENDPOINT = BASE_URL + '&q={},{}'.format(city_name, country_code)

    return get_forecast_report(API_ENDPOINT)


def get_forecast_by_coordinates(lat, lon):
    API_ENDPOINT = BASE_URL + '&lat={}&lon={}'.format(lat, lon)

    return get_forecast_report(API_ENDPOINT)


if __name__ == '__main__':
    get_forecast_by_city('london')
