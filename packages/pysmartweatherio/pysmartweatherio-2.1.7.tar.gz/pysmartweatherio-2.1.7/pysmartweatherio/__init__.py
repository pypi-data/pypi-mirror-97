""" Communicates with a Smart Weather weatherstation from WeatherFlow using REST. """
# name = "pysmartweatherio"

# from .api import load_devicedata, load_stationdata

from pysmartweatherio.client import SmartWeather
from pysmartweatherio.errors import SmartWeatherError, InvalidApiKey, RequestError, ResultError
from pysmartweatherio.const import (
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
    UNIT_WIND_MS,
    UNIT_WIND_KMH,
    UNIT_WIND_MPH,
    UNIT_TYPE_TEMP,
    UNIT_TYPE_WIND,
    UNIT_TYPE_RAIN,
    UNIT_TYPE_PRESSURE,
    UNIT_TYPE_DISTANCE,
    FORECAST_TYPES,
    FORECAST_TYPE_DAILY,
    FORECAST_TYPE_HOURLY,
)