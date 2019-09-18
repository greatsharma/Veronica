from __future__ import absolute_import
from __future__ import print_function

from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
# from rasa_core_sdk.events import AllSlotsReset
from city import search_city, search_closest_city
from openWeatherMap import current as owmc
from openWeatherMap import forecast as owmf


class ActionCurrentWeather(Action):
    count = 0

    def name(self):
        return 'action_weather_current'
    
    def run(self, dispatcher, tracker, domain):
        location = tracker.get_slot('location')
        country_code = tracker.get_slot('country_code')
        
        # self.count += 1
        # dispatcher.utter_message('count is : {}'.format(self.count))

        if not location:
            dispatcher.utter_message("unable to parse location:( \n\nEnter location again")
            return []

        if country_code:
            response = owmc.get_current_weather_by_city_and_country(location, country_code)
            dispatcher.utter_message(response)
            return []

        searched_cities = search_city(location)

        if len(searched_cities) == 0:
            response = owmc.get_current_weather_by_city(location)

            if response != '404':
                dispatcher.utter_message(response)
            else:
                response = 'No such location'
                dispatcher.utter_message(response)

                closest_cities = search_closest_city(location)            
                if closest_cities:
            
                    response = 'May be you mean the following\n'
                    for city in closest_cities:
                        response += '* {}\n'.format(city)

                    dispatcher.utter_message(response)

        elif len(searched_cities) == 1:
            response = owmc.get_current_weather_by_city(location)
            dispatcher.utter_message(response)
        
        else:
            response = 'There are more than one location with given name\n\n'
            for city in searched_cities:
                response += '* {}, {}\n'.format(city['name'], city['country'])
            
            dispatcher.utter_message(response)
            dispatcher.utter_template('utter_ask_country', tracker)

        return []


class ActionForecastWeather(Action):

    def name(self):
        return 'action_weather_forecast'

    def run(self, dispatcher, tracker, domain):
        location = tracker.get_slot('location')
        country_code = tracker.get_slot('country_code')

        if not location:
            dispatcher.utter_message("unable to parse location:( \n\nEnter location again")
            return []

        if country_code:
            response = owmf.get_forecast_by_city_and_country(location, country_code)
            dispatcher.utter_message(response)
            return []

        searched_cities = search_city(location)

        if len(searched_cities) == 0:
            closest_cities = search_closest_city(location)
            if closest_cities:
                response = 'No such city'
                dispatcher.utter_message(response)
        
                response = 'May be you are looking for the following\n'
                for city in closest_cities:
                    response += '* {}\n'.format(city)

                dispatcher.utter_message(response)

        elif len(searched_cities) == 1:
            response = owmf.get_forecast_by_city(location)
            dispatcher.utter_message(response)
        
        else:
            response = 'There are more than one location with given name\n\n'
            for city in searched_cities:
                response += '* {}, {}\n'.format(city['name'], city['country'])
            
            dispatcher.utter_message(response)
            dispatcher.utter_template('utter_ask_country', tracker)

        return []


class ActionSlotCountryReset(Action):

    def name(self):
        return 'action_slot_country_reset'

    def run(self, dispatcher, tracker, domain):
        return [SlotSet('country_code', None)]