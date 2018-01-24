import requests
import asyncio

appid = 'd5e2b92e176d4042f863d6ac2e4cb075'

# Проверка наличия в базе информации о нужном населенном пункте
async def get_city_id(s_city_name):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': s_city_name, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        print("city:", cities)
        city_id = data['list'][0]['id']
        print('city_id=', city_id)
    except Exception as e:
        print("Exception (find):", e)
        pass
    assert isinstance(city_id, int)
    return city_id


# Запрос текущей погоды
async def request_current_weather(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        print("city:", data['name'])
        print("conditions:", data['weather'][0]['description'])
        print("temp:", data['main']['temp'])
    except Exception as e:
        print("Exception (weather):", e)
        pass

city_list = ["Kiev,UA", "Moscow,RU"]
#city_id_list = [703448, 524901]

async def asynchronous(city_list):
    city_id_ls = [get_city_id(city_list_id) for city_list_id in city_list]
    done, pending = await asyncio.wait(city_id_ls)
    for item in done:
        weather = [request_current_weather(item.result())]
        done, pending = await asyncio.wait(weather)

ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(asynchronous(city_list))
ioloop.close()
