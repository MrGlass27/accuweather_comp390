import requests
import configparser


def get_apikey():
    config = configparser.ConfigParser()
    config.read('app.config')
    apikey_from_file = config['secrets']['apikey']
    return apikey_from_file


class NoSuchLocation(Exception):
    pass


def get_location(zipcode):
    location_url = 'https://dataservice.accuweather.com/locations/v1/' \
                   'postalcodes/search?apikey={}&q={}'.format(get_apikey, zipcode)
    response = requests.get(location_url)

    try:
        key = response.json()[0].get('Key')
    except IndexError:
        raise NoSuchLocation()
    return key


def get_conditions(key):
    conditions_url = 'https://dataservice.accuweather.com/currentconditions/v1/' \
        '{}?apikey={}'.format(key, get_apikey)
    response = requests.get(conditions_url)
    json_version = response.json()
    print("Current Conditions: {}".format(json_version[0].get('WeatherText')))


def get_fivedaycast(key):
    fiveday_url = 'http://dataservice.accuweather.com/forecasts/v1' \
        '/daily/5day/{}?apikey={}'.format(key, get_apikey)
    response = requests.get(fiveday_url)
    json_version = response.json()
    forecast = json_version.get('DailyForecasts')
    for day in forecast:
        date = day.get('Date')
        temp = day.get('Temperature')
        low = temp.get('Minimum')
        high = temp.get('Maximum')
        print("Date:{}".format(date))
        print('High{}'.format(high))
        print('Low:{}'.format(low))


try:
    key = input('Put in zip code:')
    location_key = get_location(key)
    get_conditions(location_key)
    get_fivedaycast(location_key)
except NoSuchLocation:
    print("Unable to get the location")