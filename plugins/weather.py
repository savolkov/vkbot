# Ping plugin
import requests

class Plugin:
    api = None
    f = None
    apiKey = '4a71f83b36067372d577d8b40aa816ed'

    def __init__(self, api, f):
        self.api = api
        self.f = f
        print('Weather')

    def getkeys(self):
        keys = ['погода']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def getWeatherEmoji(self, weatherID):
        # Openweathermap Weather codes and corressponding emojis
        thunderstorm = "⛈"    # Code: 200's, 900, 901, 902, 905
        drizzle = "🌧"         # Code: 300's
        rain = "☔🌧"            # Code: 500's
        snowflake = "❄"       # Code: 600's snowflake
        snowman = "⛄"         # Code: 600's snowman, 903, 906
        atmosphere = "🌫"      # Code: 700's foogy
        clearSky = "☀"        # Code: 800 clear sky
        fewClouds = "⛅"       # Code: 801 sun behind clouds
        clouds = "☁"          # Code: 802-803-804 clouds general
        hot = "♨"             # Code: 904
        defaultEmoji = "🌀"    # default emojis
        weatherID = str(weatherID)
        if (weatherID[1] == '2' or weatherID == '900' or weatherID == '901' or weatherID == '902' or weatherID == '905'):
            return thunderstorm
        elif (weatherID[1] == '3'):
            return drizzle
        elif (weatherID[1] == '5'):
            return rain
        elif (weatherID[1] == '6' or weatherID == '903' or weatherID == '906'):
            return snowflake + ' ' + snowman
        elif (weatherID[1] == '7'):
            return atmosphere
        elif (weatherID == '800'):
            return clearSky
        elif (weatherID == '801'):
            return fewClouds
        elif (weatherID == '802' or weatherID == '803' or weatherID == '803'):
            return clouds
        elif (weatherID == '904'):
            return hot
        else:
            return defaultEmoji

    def call(self, msg):
        words = msg[5].split()
        if (len (words) <= 1): 
            return
        city = words[1]
        url = 'https://api.openweathermap.org/data/2.5/weather?q=%s&APPID=%s&lang=ru&units=metric' % (
            city,  self.apiKey)
        reply = requests.get(url)
        res = reply.json()
        
        weather = {
            'description': res['weather'][0]['description'],
            'region': res['name'] +', ' + res['sys']['country'],
            'emoji': self.getWeatherEmoji(res['weather'][0]['id']),
            'temp': res['main']['temp']
        }

        s = "Погода в %(region)s:\n 🌡%(temp)s°C \n%(emoji)s %(description)s" % weather
        
        self.f.replyToMessage(
            api=self.api, msg=msg, text=s, attachment='')
        
