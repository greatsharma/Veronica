import requests

API_KEY = 'your api key from openweathermap.org'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?appid={}&units=metric'.format(API_KEY)
    

def get_my_location():
    res = requests.get('https://ipinfo.io')
    data = res.json()

    return data['city'], data['loc'].split(',')


def get_current_weather_report(API_ENDPOINT):
    res = requests.get(API_ENDPOINT)
    data = res.json()

    if data['cod'] == '404':
        response = '404'
    else:
        country_code = data['sys']['country']
        country_name = requests.get('https://restcountries.eu/rest/v2/alpha/{}'.format(country_code)).json()['name']

        location = data['name']
        climate_descr = data['weather'][0]['description']
        temp = data['main']['temp']
        max_temp = data['main']['temp_max']
        min_temp = data['main']['temp_min']
        wind_speed = data['wind']['speed']

        response = '{}({}) -\n'.format(location, country_name)
        response += 'Climate is {} with {} deg temperature and {} meters/sec wind speed.'.format(climate_descr, temp, wind_speed)
        response += "\nHigh: {}\N{DEGREE SIGN} Low: {}\N{DEGREE SIGN}".format(max_temp, min_temp)
    
    return response


def get_current_weather_by_city(city_name):
    API_ENDPOINT = BASE_URL + '&q={}'.format(city_name)

    return get_current_weather_report(API_ENDPOINT)


def get_current_weather_by_city_and_country(city_name, country_code):
    API_ENDPOINT = BASE_URL + '&q={},{}'.format(city_name, country_code)

    return get_current_weather_report(API_ENDPOINT)


def get_current_weather_by_coordinates(lat, lon):
    API_ENDPOINT = BASE_URL + '&lat={}&lon={}'.format(lat, lon)

    return get_current_weather_report(API_ENDPOINT)



if __name__ == '__main__':
    city, loc_coord = get_my_location()
    print(get_current_weather_by_coordinates(loc_coord[0], loc_coord[1]))
