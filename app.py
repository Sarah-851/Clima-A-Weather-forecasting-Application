from fastapi import FastAPI, HTTPException
import uvicorn
import httpx
from datetime import datetime

from ml.models.model_manager import ModelManager

app = FastAPI()
model_manager = ModelManager()

hour_map = {
    2: 0,
    5: 1,
    8: 2,
    11: 3,
    14: 4,
    17: 5,
    20: 6,
    23: 7
}


@app.get('/')
def root():
    return {"message": "Hello World !!!"}

@app.get('/app/data')
async def app_data():
    url = 'https://api.openweathermap.org/data/2.5/forecast?lat=19.0760&lon=72.8777&appid=4d94b6be7087b50dfe9f8217cea15ae7&units=metric'

    async with httpx.AsyncClient() as client:
        resp = httpx.get(url)
        resp.raise_for_status()

        resp_data = resp.json()
#     resp_data = {
# "cod": "200",
# "message": 0,
# "cnt": 40,
# "list": [
#     {
#         "dt": 1681030800,
#         "main": {
#             "temp": 34,
#             "feels_like": 38.06,
#             "temp_min": 31.48,
#             "temp_max": 34,
#             "pressure": 1013,
#             "sea_level": 1013,
#             "grnd_level": 1009,
#             "humidity": 49,
#             "temp_kf": 2.52
#         },
#         "weather": [
#             {
#                 "id": 803,
#                 "main": "Clouds",
#                 "description": "broken clouds",
#                 "icon": "04d"
#             }
#         ],
#         "clouds": {
#             "all": 61
#         },
#         "wind": {
#             "speed": 6.74,
#             "deg": 276,
#             "gust": 7.6
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-09 09:00:00"
#     },
#     {
#         "dt": 1681041600,
#         "main": {
#             "temp": 32.81,
#             "feels_like": 36.48,
#             "temp_min": 30.42,
#             "temp_max": 32.81,
#             "pressure": 1012,
#             "sea_level": 1012,
#             "grnd_level": 1009,
#             "humidity": 52,
#             "temp_kf": 2.39
#         },
#         "weather": [
#             {
#                 "id": 803,
#                 "main": "Clouds",
#                 "description": "broken clouds",
#                 "icon": "04d"
#             }
#         ],
#         "clouds": {
#             "all": 61
#         },
#         "wind": {
#             "speed": 5.48,
#             "deg": 305,
#             "gust": 6.98
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-09 12:00:00"
#     },
#     {
#         "dt": 1681052400,
#         "main": {
#             "temp": 31.25,
#             "feels_like": 33.68,
#             "temp_min": 29.88,
#             "temp_max": 31.25,
#             "pressure": 1012,
#             "sea_level": 1012,
#             "grnd_level": 1011,
#             "humidity": 53,
#             "temp_kf": 1.37
#         },
#         "weather": [
#             {
#                 "id": 802,
#                 "main": "Clouds",
#                 "description": "scattered clouds",
#                 "icon": "03n"
#             }
#         ],
#         "clouds": {
#             "all": 48
#         },
#         "wind": {
#             "speed": 3.26,
#             "deg": 333,
#             "gust": 3.79
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-09 15:00:00"
#     },
#     {
#         "dt": 1681063200,
#         "main": {
#             "temp": 29.56,
#             "feels_like": 31.01,
#             "temp_min": 29.56,
#             "temp_max": 29.56,
#             "pressure": 1012,
#             "sea_level": 1012,
#             "grnd_level": 1011,
#             "humidity": 54,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 802,
#                 "main": "Clouds",
#                 "description": "scattered clouds",
#                 "icon": "03n"
#             }
#         ],
#         "clouds": {
#             "all": 31
#         },
#         "wind": {
#             "speed": 2.37,
#             "deg": 310,
#             "gust": 2.61
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-09 18:00:00"
#     },
#     {
#         "dt": 1681074000,
#         "main": {
#             "temp": 28.25,
#             "feels_like": 30.2,
#             "temp_min": 28.25,
#             "temp_max": 28.25,
#             "pressure": 1010,
#             "sea_level": 1010,
#             "grnd_level": 1009,
#             "humidity": 63,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 801,
#                 "main": "Clouds",
#                 "description": "few clouds",
#                 "icon": "02n"
#             }
#         ],
#         "clouds": {
#             "all": 14
#         },
#         "wind": {
#             "speed": 4.51,
#             "deg": 334,
#             "gust": 5.04
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-09 21:00:00"
#     },
#     {
#         "dt": 1681084800,
#         "main": {
#             "temp": 27.88,
#             "feels_like": 29.38,
#             "temp_min": 27.88,
#             "temp_max": 27.88,
#             "pressure": 1011,
#             "sea_level": 1011,
#             "grnd_level": 1010,
#             "humidity": 61,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 802,
#                 "main": "Clouds",
#                 "description": "scattered clouds",
#                 "icon": "03n"
#             }
#         ],
#         "clouds": {
#             "all": 30
#         },
#         "wind": {
#             "speed": 5.05,
#             "deg": 345,
#             "gust": 6.67
#         },
#         "visibility": 10000,
#         "pop": 0.04,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-10 00:00:00"
#     },
#     {
#         "dt": 1681095600,
#         "main": {
#             "temp": 29.68,
#             "feels_like": 30.59,
#             "temp_min": 29.68,
#             "temp_max": 29.68,
#             "pressure": 1012,
#             "sea_level": 1012,
#             "grnd_level": 1012,
#             "humidity": 50,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 801,
#                 "main": "Clouds",
#                 "description": "few clouds",
#                 "icon": "02d"
#             }
#         ],
#         "clouds": {
#             "all": 23
#         },
#         "wind": {
#             "speed": 2.77,
#             "deg": 51,
#             "gust": 3.56
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-10 03:00:00"
#     },
#     {
#         "dt": 1681106400,
#         "main": {
#             "temp": 32.99,
#             "feels_like": 33.56,
#             "temp_min": 32.99,
#             "temp_max": 32.99,
#             "pressure": 1012,
#             "sea_level": 1012,
#             "grnd_level": 1011,
#             "humidity": 39,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 801,
#                 "main": "Clouds",
#                 "description": "few clouds",
#                 "icon": "02d"
#             }
#         ],
#         "clouds": {
#             "all": 17
#         },
#         "wind": {
#             "speed": 2.94,
#             "deg": 315,
#             "gust": 3.29
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-10 06:00:00"
#     },
#     {
#         "dt": 1681117200,
#         "main": {
#             "temp": 32.1,
#             "feels_like": 34.07,
#             "temp_min": 32.1,
#             "temp_max": 32.1,
#             "pressure": 1009,
#             "sea_level": 1009,
#             "grnd_level": 1008,
#             "humidity": 48,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 800,
#                 "main": "Clear",
#                 "description": "clear sky",
#                 "icon": "01d"
#             }
#         ],
#         "clouds": {
#             "all": 9
#         },
#         "wind": {
#             "speed": 7.77,
#             "deg": 302,
#             "gust": 7.35
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-10 09:00:00"
#     },
#     {
#         "dt": 1681128000,
#         "main": {
#             "temp": 30.72,
#             "feels_like": 32.54,
#             "temp_min": 30.72,
#             "temp_max": 30.72,
#             "pressure": 1008,
#             "sea_level": 1008,
#             "grnd_level": 1007,
#             "humidity": 52,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 802,
#                 "main": "Clouds",
#                 "description": "scattered clouds",
#                 "icon": "03d"
#             }
#         ],
#         "clouds": {
#             "all": 40
#         },
#         "wind": {
#             "speed": 8.01,
#             "deg": 312,
#             "gust": 10.73
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-10 12:00:00"
#     },
#     {
#         "dt": 1681138800,
#         "main": {
#             "temp": 29.26,
#             "feels_like": 31.32,
#             "temp_min": 29.26,
#             "temp_max": 29.26,
#             "pressure": 1010,
#             "sea_level": 1010,
#             "grnd_level": 1010,
#             "humidity": 59,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 803,
#                 "main": "Clouds",
#                 "description": "broken clouds",
#                 "icon": "04n"
#             }
#         ],
#         "clouds": {
#             "all": 55
#         },
#         "wind": {
#             "speed": 3.39,
#             "deg": 319,
#             "gust": 5.03
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-10 15:00:00"
#     },
#     {
#         "dt": 1681149600,
#         "main": {
#             "temp": 28.71,
#             "feels_like": 30.84,
#             "temp_min": 28.71,
#             "temp_max": 28.71,
#             "pressure": 1011,
#             "sea_level": 1011,
#             "grnd_level": 1010,
#             "humidity": 62,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 802,
#                 "main": "Clouds",
#                 "description": "scattered clouds",
#                 "icon": "03n"
#             }
#         ],
#         "clouds": {
#             "all": 28
#         },
#         "wind": {
#             "speed": 2.9,
#             "deg": 310,
#             "gust": 3.57
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-10 18:00:00"
#     },
#     {
#         "dt": 1681160400,
#         "main": {
#             "temp": 28,
#             "feels_like": 30.03,
#             "temp_min": 28,
#             "temp_max": 28,
#             "pressure": 1010,
#             "sea_level": 1010,
#             "grnd_level": 1009,
#             "humidity": 65,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 800,
#                 "main": "Clear",
#                 "description": "clear sky",
#                 "icon": "01n"
#             }
#         ],
#         "clouds": {
#             "all": 8
#         },
#         "wind": {
#             "speed": 2.58,
#             "deg": 334,
#             "gust": 3.04
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-10 21:00:00"
#     },
#     {
#         "dt": 1681171200,
#         "main": {
#             "temp": 27.89,
#             "feels_like": 29.4,
#             "temp_min": 27.89,
#             "temp_max": 27.89,
#             "pressure": 1010,
#             "sea_level": 1010,
#             "grnd_level": 1009,
#             "humidity": 61,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 800,
#                 "main": "Clear",
#                 "description": "clear sky",
#                 "icon": "01n"
#             }
#         ],
#         "clouds": {
#             "all": 7
#         },
#         "wind": {
#             "speed": 3.45,
#             "deg": 350,
#             "gust": 4.25
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-11 00:00:00"
#     },
#     {
#         "dt": 1681182000,
#         "main": {
#             "temp": 29.1,
#             "feels_like": 30.32,
#             "temp_min": 29.1,
#             "temp_max": 29.1,
#             "pressure": 1012,
#             "sea_level": 1012,
#             "grnd_level": 1012,
#             "humidity": 54,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 801,
#                 "main": "Clouds",
#                 "description": "few clouds",
#                 "icon": "02d"
#             }
#         ],
#         "clouds": {
#             "all": 20
#         },
#         "wind": {
#             "speed": 3.38,
#             "deg": 347,
#             "gust": 4.25
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-11 03:00:00"
#     },
#     {
#         "dt": 1681192800,
#         "main": {
#             "temp": 30.43,
#             "feels_like": 31.88,
#             "temp_min": 30.43,
#             "temp_max": 30.43,
#             "pressure": 1012,
#             "sea_level": 1012,
#             "grnd_level": 1011,
#             "humidity": 51,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 802,
#                 "main": "Clouds",
#                 "description": "scattered clouds",
#                 "icon": "03d"
#             }
#         ],
#         "clouds": {
#             "all": 44
#         },
#         "wind": {
#             "speed": 2.85,
#             "deg": 319,
#             "gust": 3.89
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-11 06:00:00"
#     },
#     {
#         "dt": 1681203600,
#         "main": {
#             "temp": 31.58,
#             "feels_like": 33.61,
#             "temp_min": 31.58,
#             "temp_max": 31.58,
#             "pressure": 1010,
#             "sea_level": 1010,
#             "grnd_level": 1009,
#             "humidity": 50,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 800,
#                 "main": "Clear",
#                 "description": "clear sky",
#                 "icon": "01d"
#             }
#         ],
#         "clouds": {
#             "all": 6
#         },
#         "wind": {
#             "speed": 6.82,
#             "deg": 300,
#             "gust": 7.27
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-11 09:00:00"
#     },
#     {
#         "dt": 1681214400,
#         "main": {
#             "temp": 30.76,
#             "feels_like": 32.41,
#             "temp_min": 30.76,
#             "temp_max": 30.76,
#             "pressure": 1009,
#             "sea_level": 1009,
#             "grnd_level": 1008,
#             "humidity": 51,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 800,
#                 "main": "Clear",
#                 "description": "clear sky",
#                 "icon": "01d"
#             }
#         ],
#         "clouds": {
#             "all": 5
#         },
#         "wind": {
#             "speed": 7.12,
#             "deg": 309,
#             "gust": 9.85
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-11 12:00:00"
#     },
#     {
#         "dt": 1681225200,
#         "main": {
#             "temp": 28.96,
#             "feels_like": 30.67,
#             "temp_min": 28.96,
#             "temp_max": 28.96,
#             "pressure": 1011,
#             "sea_level": 1011,
#             "grnd_level": 1010,
#             "humidity": 58,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 801,
#                 "main": "Clouds",
#                 "description": "few clouds",
#                 "icon": "02n"
#             }
#         ],
#         "clouds": {
#             "all": 12
#         },
#         "wind": {
#             "speed": 3.81,
#             "deg": 310,
#             "gust": 5.7
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-11 15:00:00"
#     },
#     {
#         "dt": 1681236000,
#         "main": {
#             "temp": 28.54,
#             "feels_like": 30.28,
#             "temp_min": 28.54,
#             "temp_max": 28.54,
#             "pressure": 1011,
#             "sea_level": 1011,
#             "grnd_level": 1011,
#             "humidity": 60,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 800,
#                 "main": "Clear",
#                 "description": "clear sky",
#                 "icon": "01n"
#             }
#         ],
#         "clouds": {
#             "all": 8
#         },
#         "wind": {
#             "speed": 3.48,
#             "deg": 329,
#             "gust": 4.44
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-11 18:00:00"
#     },
#     {
#         "dt": 1681246800,
#         "main": {
#             "temp": 27.74,
#             "feels_like": 29.38,
#             "temp_min": 27.74,
#             "temp_max": 27.74,
#             "pressure": 1010,
#             "sea_level": 1010,
#             "grnd_level": 1009,
#             "humidity": 63,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 800,
#                 "main": "Clear",
#                 "description": "clear sky",
#                 "icon": "01n"
#             }
#         ],
#         "clouds": {
#             "all": 8
#         },
#         "wind": {
#             "speed": 3.33,
#             "deg": 335,
#             "gust": 4.18
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-11 21:00:00"
#     },
#     {
#         "dt": 1681257600,
#         "main": {
#             "temp": 27.47,
#             "feels_like": 28.79,
#             "temp_min": 27.47,
#             "temp_max": 27.47,
#             "pressure": 1010,
#             "sea_level": 1010,
#             "grnd_level": 1009,
#             "humidity": 61,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 802,
#                 "main": "Clouds",
#                 "description": "scattered clouds",
#                 "icon": "03n"
#             }
#         ],
#         "clouds": {
#             "all": 25
#         },
#         "wind": {
#             "speed": 3.07,
#             "deg": 0,
#             "gust": 4.22
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-12 00:00:00"
#     },
#     {
#         "dt": 1681268400,
#         "main": {
#             "temp": 28.65,
#             "feels_like": 29.8,
#             "temp_min": 28.65,
#             "temp_max": 28.65,
#             "pressure": 1013,
#             "sea_level": 1013,
#             "grnd_level": 1012,
#             "humidity": 55,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 803,
#                 "main": "Clouds",
#                 "description": "broken clouds",
#                 "icon": "04d"
#             }
#         ],
#         "clouds": {
#             "all": 68
#         },
#         "wind": {
#             "speed": 1.77,
#             "deg": 20,
#             "gust": 2.58
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-12 03:00:00"
#     },
#     {
#         "dt": 1681279200,
#         "main": {
#             "temp": 31.46,
#             "feels_like": 32.98,
#             "temp_min": 31.46,
#             "temp_max": 31.46,
#             "pressure": 1012,
#             "sea_level": 1012,
#             "grnd_level": 1011,
#             "humidity": 48,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 803,
#                 "main": "Clouds",
#                 "description": "broken clouds",
#                 "icon": "04d"
#             }
#         ],
#         "clouds": {
#             "all": 65
#         },
#         "wind": {
#             "speed": 4.26,
#             "deg": 338,
#             "gust": 5.45
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-12 06:00:00"
#     },
#     {
#         "dt": 1681290000,
#         "main": {
#             "temp": 32.88,
#             "feels_like": 34.49,
#             "temp_min": 32.88,
#             "temp_max": 32.88,
#             "pressure": 1008,
#             "sea_level": 1008,
#             "grnd_level": 1008,
#             "humidity": 44,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 802,
#                 "main": "Clouds",
#                 "description": "scattered clouds",
#                 "icon": "03d"
#             }
#         ],
#         "clouds": {
#             "all": 30
#         },
#         "wind": {
#             "speed": 7.62,
#             "deg": 320,
#             "gust": 8.75
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-12 09:00:00"
#     },
#     {
#         "dt": 1681300800,
#         "main": {
#             "temp": 32.18,
#             "feels_like": 33.54,
#             "temp_min": 32.18,
#             "temp_max": 32.18,
#             "pressure": 1007,
#             "sea_level": 1007,
#             "grnd_level": 1006,
#             "humidity": 45,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 802,
#                 "main": "Clouds",
#                 "description": "scattered clouds",
#                 "icon": "03d"
#             }
#         ],
#         "clouds": {
#             "all": 42
#         },
#         "wind": {
#             "speed": 9.75,
#             "deg": 322,
#             "gust": 13.09
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-12 12:00:00"
#     },
#     {
#         "dt": 1681311600,
#         "main": {
#             "temp": 30.48,
#             "feels_like": 32.14,
#             "temp_min": 30.48,
#             "temp_max": 30.48,
#             "pressure": 1010,
#             "sea_level": 1010,
#             "grnd_level": 1009,
#             "humidity": 52,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 803,
#                 "main": "Clouds",
#                 "description": "broken clouds",
#                 "icon": "04n"
#             }
#         ],
#         "clouds": {
#             "all": 63
#         },
#         "wind": {
#             "speed": 5.9,
#             "deg": 322,
#             "gust": 8.22
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-12 15:00:00"
#     },
#     {
#         "dt": 1681322400,
#         "main": {
#             "temp": 28.96,
#             "feels_like": 31.12,
#             "temp_min": 28.96,
#             "temp_max": 28.96,
#             "pressure": 1011,
#             "sea_level": 1011,
#             "grnd_level": 1010,
#             "humidity": 61,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 803,
#                 "main": "Clouds",
#                 "description": "broken clouds",
#                 "icon": "04n"
#             }
#         ],
#         "clouds": {
#             "all": 80
#         },
#         "wind": {
#             "speed": 3.74,
#             "deg": 330,
#             "gust": 5.05
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-12 18:00:00"
#     },
#     {
#         "dt": 1681333200,
#         "main": {
#             "temp": 28.48,
#             "feels_like": 30.45,
#             "temp_min": 28.48,
#             "temp_max": 28.48,
#             "pressure": 1009,
#             "sea_level": 1009,
#             "grnd_level": 1008,
#             "humidity": 62,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 802,
#                 "main": "Clouds",
#                 "description": "scattered clouds",
#                 "icon": "03n"
#             }
#         ],
#         "clouds": {
#             "all": 39
#         },
#         "wind": {
#             "speed": 4.4,
#             "deg": 341,
#             "gust": 5.92
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-12 21:00:00"
#     },
#     {
#         "dt": 1681344000,
#         "main": {
#             "temp": 28.36,
#             "feels_like": 30,
#             "temp_min": 28.36,
#             "temp_max": 28.36,
#             "pressure": 1009,
#             "sea_level": 1009,
#             "grnd_level": 1008,
#             "humidity": 60,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 803,
#                 "main": "Clouds",
#                 "description": "broken clouds",
#                 "icon": "04n"
#             }
#         ],
#         "clouds": {
#             "all": 62
#         },
#         "wind": {
#             "speed": 2.34,
#             "deg": 20,
#             "gust": 2.98
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-13 00:00:00"
#     },
#     {
#         "dt": 1681354800,
#         "main": {
#             "temp": 29.7,
#             "feels_like": 31.39,
#             "temp_min": 29.7,
#             "temp_max": 29.7,
#             "pressure": 1011,
#             "sea_level": 1011,
#             "grnd_level": 1010,
#             "humidity": 55,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 804,
#                 "main": "Clouds",
#                 "description": "overcast clouds",
#                 "icon": "04d"
#             }
#         ],
#         "clouds": {
#             "all": 99
#         },
#         "wind": {
#             "speed": 1.85,
#             "deg": 357,
#             "gust": 2.27
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-13 03:00:00"
#     },
#     {
#         "dt": 1681365600,
#         "main": {
#             "temp": 34.38,
#             "feels_like": 35.57,
#             "temp_min": 34.38,
#             "temp_max": 34.38,
#             "pressure": 1010,
#             "sea_level": 1010,
#             "grnd_level": 1009,
#             "humidity": 38,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 804,
#                 "main": "Clouds",
#                 "description": "overcast clouds",
#                 "icon": "04d"
#             }
#         ],
#         "clouds": {
#             "all": 98
#         },
#         "wind": {
#             "speed": 4.16,
#             "deg": 3,
#             "gust": 5.34
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-13 06:00:00"
#     },
#     {
#         "dt": 1681376400,
#         "main": {
#             "temp": 32.37,
#             "feels_like": 34.31,
#             "temp_min": 32.37,
#             "temp_max": 32.37,
#             "pressure": 1007,
#             "sea_level": 1007,
#             "grnd_level": 1006,
#             "humidity": 47,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 804,
#                 "main": "Clouds",
#                 "description": "overcast clouds",
#                 "icon": "04d"
#             }
#         ],
#         "clouds": {
#             "all": 100
#         },
#         "wind": {
#             "speed": 8.41,
#             "deg": 319,
#             "gust": 10.79
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-13 09:00:00"
#     },
#     {
#         "dt": 1681387200,
#         "main": {
#             "temp": 31.87,
#             "feels_like": 34.36,
#             "temp_min": 31.87,
#             "temp_max": 31.87,
#             "pressure": 1008,
#             "sea_level": 1008,
#             "grnd_level": 1007,
#             "humidity": 51,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 804,
#                 "main": "Clouds",
#                 "description": "overcast clouds",
#                 "icon": "04d"
#             }
#         ],
#         "clouds": {
#             "all": 100
#         },
#         "wind": {
#             "speed": 7.81,
#             "deg": 305,
#             "gust": 10.5
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-13 12:00:00"
#     },
#     {
#         "dt": 1681398000,
#         "main": {
#             "temp": 32.04,
#             "feels_like": 33.31,
#             "temp_min": 32.04,
#             "temp_max": 32.04,
#             "pressure": 1008,
#             "sea_level": 1008,
#             "grnd_level": 1008,
#             "humidity": 45,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 804,
#                 "main": "Clouds",
#                 "description": "overcast clouds",
#                 "icon": "04n"
#             }
#         ],
#         "clouds": {
#             "all": 96
#         },
#         "wind": {
#             "speed": 7.18,
#             "deg": 348,
#             "gust": 10.69
#         },
#         "visibility": 10000,
#         "pop": 0.02,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-13 15:00:00"
#     },
#     {
#         "dt": 1681408800,
#         "main": {
#             "temp": 30.45,
#             "feels_like": 32.47,
#             "temp_min": 30.45,
#             "temp_max": 30.45,
#             "pressure": 1009,
#             "sea_level": 1009,
#             "grnd_level": 1009,
#             "humidity": 54,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 804,
#                 "main": "Clouds",
#                 "description": "overcast clouds",
#                 "icon": "04n"
#             }
#         ],
#         "clouds": {
#             "all": 97
#         },
#         "wind": {
#             "speed": 4.48,
#             "deg": 318,
#             "gust": 6.5
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-13 18:00:00"
#     },
#     {
#         "dt": 1681419600,
#         "main": {
#             "temp": 29.41,
#             "feels_like": 31.92,
#             "temp_min": 29.41,
#             "temp_max": 29.41,
#             "pressure": 1008,
#             "sea_level": 1008,
#             "grnd_level": 1007,
#             "humidity": 61,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 804,
#                 "main": "Clouds",
#                 "description": "overcast clouds",
#                 "icon": "04n"
#             }
#         ],
#         "clouds": {
#             "all": 100
#         },
#         "wind": {
#             "speed": 2.3,
#             "deg": 313,
#             "gust": 3.04
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-13 21:00:00"
#     },
#     {
#         "dt": 1681430400,
#         "main": {
#             "temp": 28.48,
#             "feels_like": 31.78,
#             "temp_min": 28.48,
#             "temp_max": 28.48,
#             "pressure": 1009,
#             "sea_level": 1009,
#             "grnd_level": 1008,
#             "humidity": 71,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 804,
#                 "main": "Clouds",
#                 "description": "overcast clouds",
#                 "icon": "04n"
#             }
#         ],
#         "clouds": {
#             "all": 100
#         },
#         "wind": {
#             "speed": 1.19,
#             "deg": 321,
#             "gust": 3.23
#         },
#         "visibility": 10000,
#         "pop": 0,
#         "sys": {
#             "pod": "n"
#         },
#         "dt_txt": "2023-04-14 00:00:00"
#     },
#     {
#         "dt": 1681441200,
#         "main": {
#             "temp": 29.81,
#             "feels_like": 32.86,
#             "temp_min": 29.81,
#             "temp_max": 29.81,
#             "pressure": 1011,
#             "sea_level": 1011,
#             "grnd_level": 1010,
#             "humidity": 62,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 804,
#                 "main": "Clouds",
#                 "description": "overcast clouds",
#                 "icon": "04d"
#             }
#         ],
#         "clouds": {
#             "all": 100
#         },
#         "wind": {
#             "speed": 1.6,
#             "deg": 82,
#             "gust": 2.01
#         },
#         "visibility": 10000,
#         "pop": 0.12,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-14 03:00:00"
#     },
#     {
#         "dt": 1681452000,
#         "main": {
#             "temp": 32.07,
#             "feels_like": 34.74,
#             "temp_min": 32.07,
#             "temp_max": 32.07,
#             "pressure": 1011,
#             "sea_level": 1011,
#             "grnd_level": 1010,
#             "humidity": 51,
#             "temp_kf": 0
#         },
#         "weather": [
#             {
#                 "id": 804,
#                 "main": "Clouds",
#                 "description": "overcast clouds",
#                 "icon": "04d"
#             }
#         ],
#         "clouds": {
#             "all": 100
#         },
#         "wind": {
#             "speed": 2.81,
#             "deg": 287,
#             "gust": 3.63
#         },
#         "visibility": 10000,
#         "pop": 0.12,
#         "sys": {
#             "pod": "d"
#         },
#         "dt_txt": "2023-04-14 06:00:00"
#     }
# ],
# "city": {
#     "id": 8131499,
#     "name": "Konkan Division",
#     "coord": {
#         "lat": 19.076,
#         "lon": 72.8777
#     },
#     "country": "IN",
#     "population": 0,
#     "timezone": 19800,
#     "sunrise": 1681001771,
#     "sunset": 1681046631
# }
# }

    data = {}

    tmp = resp_data["list"][0]['main']
    tmp['prcp'] = resp_data["list"][0]['pop']
    tmp['icon'] = resp_data["list"][0]['weather'][0]['icon']
    tmp["desc"] = resp_data["list"][0]['weather'][0]['description']
    tmp["wind"] = resp_data["list"][0]['wind']['speed']

    data["today"] = tmp
    data["forecast"] = list()

    curr_time = datetime.fromtimestamp(resp_data["list"][0]['dt'])
    curr_index = hour_map[curr_time.hour]
    offset = 7-curr_index + 1
    index = offset + 3
    size = len(resp_data["list"])
    prev_tmp_data = [tmp['temp_min'], tmp['temp_max'], tmp['prcp']]
    prev_rain_data = [tmp['temp'], tmp["humidity"], tmp["sea_level"], tmp['prcp']]

    for i in range(7):
        tmin_prediction, tmax_prediction = model_manager.temp_model.get_prediction(prev_tmp_data)

        forecast_data = {}
        forecast_data["tmax"] = tmax_prediction
        forecast_data["tmin"] = tmin_prediction

        prcp_prediction = model_manager.rain_model.get_prediction(prev_rain_data)

        forecast_data["prcp"] = prcp_prediction
        forecast_data["icon"] = resp_data["list"][index]['weather'][0]['icon']
        forecast_data["desc"] = resp_data["list"][index]['weather'][0]['description']
        data["forecast"].append(forecast_data)

        index = index + 8
        if index >= size:
            index = size - 1

        if i < 4:
            tt = datetime.fromtimestamp(resp_data["list"][index]['dt'])
            tmp = resp_data["list"][index]['main']
            tmp['prcp'] = resp_data["list"][index]['pop']
            prev_tmp_data = [tmp['temp_min'], tmp['temp_max'], tmp['prcp']]
            prev_rain_data = [tmp['temp'], tmp["humidity"], tmp["sea_level"], tmp['prcp']]
        else:
            prev_tmp_data = [forecast_data["tmin"], forecast_data["tmax"], forecast_data["prcp"]]
            prev_rain_data = [forecast_data["tmax"], resp_data["list"][index]['main']['humidity'], resp_data["list"][index]['main']["sea_level"], resp_data["list"][index]['pop']]

    return data


@app.get('/predict/temp')
def predict_temp(tmin: float = -1, tmax: float = -1, prcp: int = -1):
    if tmin == -1 or tmax == -1 or prcp == -1:
        raise HTTPException(status_code=400, detail= "tmin, tmax, prcp are required parameters")
    tmin_prediction, tmax_prediction = model_manager.temp_model.get_prediction([tmin, tmax, prcp])
    return {
        "data": {
            "tmin": tmin_prediction,
            "tmax": tmax_prediction
        }
    }


@app.get('/predict/rain')
def predict_rain(temp: float = -1, humidity: float = -1, slp: float = -1, prcp: int = -1):
    if temp == -1 or humidity == -1 or slp == -1 or prcp == -1:
        raise HTTPException(status_code=400, detail="temp, humidity, slp, prcp are required parameters")
    prcp_prediction = model_manager.rain_model.get_prediction([temp, humidity, slp, prcp])
    return {
        "data": {
            "prcp": prcp_prediction
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
