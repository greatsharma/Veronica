import re
import json
import difflib

# download city.list.json.gz from http://bulk.openweathermap.org/sample/
with open('city.list.json', 'r') as file:
   cities = json.load(file)


def search_city(location):
   matched_cities = []
   for city in cities:
      if location.lower() == city['name'].lower():
      # if re.match(location, city['name'], re.IGNORECASE):
         matched_cities.append(city)

   return matched_cities


def search_closest_city(location):
   city_list = []
   for city in cities:
      city_list.append(city['name'])

   return difflib.get_close_matches(location, city_list, n=3, cutoff = 0.7)


# print(search_city('Sydney'))
