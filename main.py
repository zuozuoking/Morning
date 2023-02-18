from datetime import date, datetime,timedelta,timezone
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import json

start_date = os.environ['START_DATE']
city = os.environ['CITY']
cityb = os.environ['CITY_B']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
userb_id = os.environ["USERB_ID"]
template_id = os.environ["TEMPLATE_ID"]

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
beijing = timezone(timedelta(hours=8))
beijing_now = utc_now.astimezone(beijing)
today = beijing_now.now()
clock = json.dumps(today, cls=DateEncoder)

def get_weather():
  url = "http://aider.meizu.com/app/weather/listWeather?cityIds=" + city
  res = requests.get(url).json()
  weather = res['value'][0]['weathers'][0]
  return weather['weather'], weather['temp_day_c'],weather['temp_night_c']

def get_weatherB():
  url = "http://aider.meizu.com/app/weather/listWeather?cityIds=" + cityb
  res = requests.get(url).json()
  weather = res['value'][0]['weathers'][0]
  return weather['weather'], weather['temp_day_c'],weather['temp_night_c']

def get_clothes():
  url = "http://aider.meizu.com/app/weather/listWeather?cityIds=" + city
  res = requests.get(url).json()
  clothes = res['value'][0]['indexes'][0]
  return clothes['content']

def get_clothesb():
  url = "http://aider.meizu.com/app/weather/listWeather?cityIds=" + cityb
  res = requests.get(url).json()
  clothes = res['value'][0]['indexes'][0]
  return clothes['content']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temp_day,temp_night = get_weather()
weab, tempb_day,tempb_night = get_weatherB()
data = {"weather":{"value":wea},"temp_day":{"value":temp_day},"temp_night":{"value":temp_night},"clothes":{"value":get_clothes(), "color":get_random_color()},
        "weatherb":{"value":weab},"tempb_day":{"value":tempb_day},"tempb_night":{"value":tempb_night},"clothesb":{"value":get_clothesb(), "color":get_random_color()},
        "today":{"value":clock},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
user_a = wm.send_template(user_id, template_id, data)
user_b = wm.send_template(userb_id, template_id, data)
print(user_a)
print(user_b)
