"""Define a client to interact with Weatherflow SmartWeather."""
import asyncio
import logging
from typing import Optional
from datetime import datetime

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from pysmartweatherio.errors import InvalidApiKey, RequestError, ResultError
from pysmartweatherio.helper_functions import ConversionFunctions
from pysmartweatherio.dataclasses import StationData, ForecastDataDaily, ForecastDataHourly, DeviceData
from pysmartweatherio.const import (
    BASE_URL,
    DEFAULT_TIMEOUT,
    DEVICE_TYPE_AIR,
    DEVICE_TYPE_SKY,
    DEVICE_TYPE_TEMPEST,
    DEVICE_TYPES,
    UNIT_SYSTEM_METRIC,
    UNIT_TEMP_CELCIUS,
    UNIT_TEMP_FAHRENHEIT,
    UNIT_PRESSURE_MB,
    UNIT_PRESSURE_HPA,
    UNIT_PRESSURE_INHG,
    UNIT_PRECIP_IN,
    UNIT_PRECIP_MM,
    UNIT_WIND_MS,
    UNIT_WIND_KMH,
    UNIT_WIND_MPH,
    UNIT_DISTANCE_KM,
    UNIT_DISTANCE_MI,
    UNIT_TYPE_TEMP,
    UNIT_TYPE_WIND,
    UNIT_TYPE_RAIN,
    UNIT_TYPE_PRESSURE,
    UNIT_TYPE_DISTANCE,
    FORECAST_TYPE_DAILY,
    FORECAST_TYPE_HOURLY,
)

_LOGGER = logging.getLogger(__name__)


class SmartWeather:
    """SmartWeather Communication Client."""

    def __init__(
        self,
        token: str,
        station_id: int,
        to_units: str = UNIT_SYSTEM_METRIC,
        to_wind_unit: str = UNIT_WIND_MS,
        session: Optional[ClientSession] = None,
        ):
        self._token = token
        self._station_id = station_id
        self._to_units = to_units
        self._to_wind_unit = to_wind_unit
        self._session: ClientSession = session
        self.req = session
        self._latitude = None
        self._longitude = None

        if self._to_units == UNIT_SYSTEM_METRIC:
            self._to_units_temp = UNIT_TEMP_CELCIUS
            self._to_units_pressure = UNIT_PRESSURE_HPA
            self._to_units_wind = UNIT_WIND_MS
            if self._to_wind_unit == UNIT_WIND_KMH:
                self._to_units_wind = UNIT_WIND_KMH
            self._to_units_precip = UNIT_PRECIP_MM
            self._to_units_distance = UNIT_DISTANCE_KM
        else:
            self._to_units_temp = UNIT_TEMP_FAHRENHEIT
            self._to_units_pressure = UNIT_PRESSURE_INHG
            self._to_units_wind = UNIT_WIND_MPH
            self._to_units_precip = UNIT_PRECIP_IN
            self._to_units_distance = UNIT_DISTANCE_MI

    async def get_station_name(self) -> None:
        """Returns the Station Name."""
        return await self._station_name_by_station_id()

    async def get_station_data(self) -> None:
        """Returns current sensor data."""
        return await self._current_station_data()

    async def get_station_hardware(self) -> None:
        """Returns station hardware data."""
        return await self._station_information()

    async def get_forecast(self, forecast_type=FORECAST_TYPE_DAILY, hours_to_show=24) -> None:
        """Returns station Weather Forecast."""
        return await self._forecast_data(forecast_type, hours_to_show)

    async def get_daily_forecast(self) -> None:
        """Returns station Weather Forecast."""
        return await self._forecast_data(FORECAST_TYPE_DAILY, 0)

    async def get_hourly_forecast(self) -> None:
        """Returns station Weather Forecast."""
        return await self._forecast_data(FORECAST_TYPE_HOURLY, 72)

    async def get_daily_forecast_raw(self) -> None:
        """Returns raw Daily Based station Weather Forecast."""
        return await self._raw_forecast_data(FORECAST_TYPE_DAILY, 0)

    async def get_device_data(self) -> None:
        """Returns Data for devices attached to station."""
        return await self._device_info()

    async def get_units(self) -> None:
        """Returns the units used for Values."""
        if self._to_units == UNIT_SYSTEM_METRIC:
            unit_temp = "°C"
            unit_wind = "m/s"
            if self._to_units_wind == UNIT_WIND_KMH:
                unit_wind = "km/h"
            unit_rain = "mm"
            unit_pressure = "hPa"
            unit_distance = "km"
        else:
            unit_temp = "°F"
            unit_wind = "mi/h"
            unit_rain = "in"
            unit_pressure = "inHg"
            unit_distance = "mi"

        units = {
            UNIT_TYPE_TEMP: unit_temp,
            UNIT_TYPE_WIND: unit_wind,
            UNIT_TYPE_RAIN: unit_rain,
            UNIT_TYPE_PRESSURE: unit_pressure,
            UNIT_TYPE_DISTANCE: unit_distance,
        }
        return units

    async def _station_information(self) -> None:
        """Return Information about the station HW."""
        endpoint = f"stations/{self._station_id}?token={self._token}"
        json_data = await self.async_request("get", endpoint)
        
        for row in json_data["stations"]:
            items = []
            name = row["name"]
            self._latitude = row["latitude"]
            self._longitude = row["longitude"]
            if [x for x in row["devices"] if x.get('device_type')==DEVICE_TYPE_TEMPEST]:
                station_type = "TEMPEST"
            else:
                station_type = "AIR & SKY"
            for item in row["devices"]:
                if "device_type" in item:
                    device = {
                        "device_id": item["device_id"],
                        "device_type": item["device_type"],
                        "device_name": item["device_meta"]["name"],
                        "station_name": name,
                        "station_type": station_type,
                        "latitude": self._latitude,
                        "longitude": self._longitude,
                        "serial_number": item["serial_number"],
                        "firmware_revision": item["firmware_revision"],
                        "hardware_revision": item["hardware_revision"],
                    }
                    items.append(device)

            if items:
                return items


    async def _station_name_by_station_id(self) -> None:
        """Return Station name from the Station ID."""
        endpoint = f"observations/station/{self._station_id}?token={self._token}"
        json_data = await self.async_request("get", endpoint)

        return self._station_id if json_data.get("station_name") is None else json_data.get("station_name")

    async def _current_station_data(self) -> None:
        """Return current observation data for the Station."""
        endpoint = f"observations/station/{self._station_id}?token={self._token}"
        json_data = await self.async_request("get", endpoint)

        station_name = json_data.get("station_name")

        cnv = ConversionFunctions()
        items = []
        observations = json_data.get("obs")
        if observations is None:
            observations = {"nodata": "NoData"}
        
        for row in observations:
            item = {
                "air_density": 0 if "air_density" not in row else row["air_density"],
                "air_temperature": 0 if "air_temperature" not in row else
                await cnv.temperature(row["air_temperature"], UNIT_TEMP_CELCIUS, self._to_units_temp),
                "brightness": 0 if "brightness" not in row else row["brightness"],
                "dew_point": 0 if "dew_point" not in row else
                await cnv.temperature(row["dew_point"], UNIT_TEMP_CELCIUS, self._to_units_temp),
                "feels_like": 0 if "feels_like" not in row else
                await cnv.temperature(row["feels_like"], UNIT_TEMP_CELCIUS, self._to_units_temp),
                "heat_index": 0 if "heat_index" not in row else
                await cnv.temperature(row["heat_index"], UNIT_TEMP_CELCIUS, self._to_units_temp),
                "lightning_strike_last_time": None if "lightning_strike_last_epoch" not in row else
                await cnv.epoch_to_isodatetime(row["lightning_strike_last_epoch"]),
                "lightning_strike_last_distance": 0 if "lightning_strike_last_distance" not in row else
                await cnv.distance(row["lightning_strike_last_distance"], UNIT_DISTANCE_KM, self._to_units_distance),
                "lightning_strike_count": 0 if "lightning_strike_count" not in row else row["lightning_strike_count"],
                "lightning_strike_count_last_1hr": 0 if "lightning_strike_count_last_1hr" not in row else row["lightning_strike_count_last_1hr"],
                "lightning_strike_count_last_3hr": 0 if "lightning_strike_count_last_3hr" not in row else row["lightning_strike_count_last_3hr"],
                "precip_accum_last_1hr": 0 if "precip_accum_last_1hr" not in row else
                await cnv.precip(row["precip_accum_last_1hr"], UNIT_PRECIP_MM, self._to_units_precip, True),
                "precip_accum_local_day": 0 if "precip_accum_local_day" not in row else
                await cnv.precip(row["precip_accum_local_day"], UNIT_PRECIP_MM, self._to_units_precip, True),
                "precip_accum_local_yesterday": 0 if "precip_accum_local_yesterday" not in row else
                await cnv.precip(row["precip_accum_local_yesterday"], UNIT_PRECIP_MM, self._to_units_precip, True),
                "precip_rate": 0 if "precip" not in row else
                await cnv.precip(row["precip"], UNIT_PRECIP_MM, self._to_units_precip, True) * 60,
                "precip_minutes_local_day": 0 if "precip_minutes_local_day" not in row else row["precip_minutes_local_day"],
                "precip_minutes_local_yesterday": 0 if "precip_minutes_local_yesterday" not in row else row["precip_minutes_local_yesterday"],
                "relative_humidity": 0 if "relative_humidity" not in row else row["relative_humidity"],
                "station_pressure": 0 if "station_pressure" not in row else
                await cnv.pressure(row["station_pressure"], UNIT_PRESSURE_HPA, self._to_units_pressure),
                "sea_level_pressure": 0 if "sea_level_pressure" not in row else
                await cnv.pressure(row["sea_level_pressure"], UNIT_PRESSURE_HPA, self._to_units_pressure),
                "station_name": station_name,
                "solar_radiation": 0 if "solar_radiation" not in row else row["solar_radiation"],
                "pressure_trend": "" if "pressure_trend" not in row else row["pressure_trend"],
                "timestamp": None if "timestamp" not in row else
                await cnv.epoch_to_datetime(row["timestamp"]),
                "uv": 0 if "uv" not in row else row["uv"],
                "wind_avg": 0 if "wind_avg" not in row else
                await cnv.wind(row["wind_avg"], UNIT_WIND_MS, self._to_units_wind),
                "wind_bearing": 0 if "wind_direction" not in row else row["wind_direction"],
                "wind_chill": 0 if "wind_chill" not in row else
                await cnv.temperature(row["wind_chill"], UNIT_TEMP_CELCIUS, self._to_units_temp),
                "wind_gust": 0 if "wind_gust" not in row else
                await cnv.wind(row["wind_gust"], UNIT_WIND_MS, self._to_units_wind),
            }
            items.append(StationData(item))

        return items

    async def _forecast_data(self, forecast_type, hours_to_show) -> None:
        """Return Forecast data for the Station."""
        if self._latitude is None:
            # _LOGGER.debug(f"LAT: {self._latitude}")
            await self._station_information()

        cnv = ConversionFunctions()
        endpoint = f"better_forecast?station_id={self._station_id}&token={self._token}"
        json_data = await self.async_request("get", endpoint)
        items = []

        # We need a few Items from the Current Conditions section
        current_cond = json_data.get("current_conditions")
        current_condition = current_cond["conditions"]
        current_icon = current_cond["icon"]
        today = datetime.now()

        forecast = json_data.get("forecast")

        # We also need Day hign and low Temp from Today
        temp_high_today = forecast[FORECAST_TYPE_DAILY][0]["air_temp_high"]
        temp_low_today = forecast[FORECAST_TYPE_DAILY][0]["air_temp_low"]

        if forecast_type == FORECAST_TYPE_DAILY:
            for row in forecast[FORECAST_TYPE_DAILY]:
                # Skip over past forecasts - seems the API sometimes returns old forecasts
                forecast_time = datetime.fromtimestamp(row["day_start_local"])
                if today > forecast_time:
                    continue

                # Calculate data from hourly that's not summed up in the daily.
                precip = 0
                wind_avg = []
                wind_bearing = []
                for hourly in forecast['hourly']:
                    if hourly['local_day'] == row['day_num']:
                        precip += hourly["precip"]
                        wind_avg.append(hourly['wind_avg'])
                        wind_bearing.append(hourly['wind_direction'])
                sum_wind_avg = sum(wind_avg) / len(wind_avg)
                sum_wind_bearing = sum(wind_bearing) / len(wind_bearing)

                item = {
                    "timestamp": forecast_time,
                    "epochtime": row["day_start_local"],
                    "conditions": row["conditions"],
                    "icon": row["icon"],
                    "sunrise": datetime.fromtimestamp(row["sunrise"]),
                    "sunset": datetime.fromtimestamp(row["sunset"]),
                    "air_temp_high": row["air_temp_high"],
                    "air_temp_low": row["air_temp_low"],
                    "precip": await cnv.precip(precip, UNIT_PRECIP_MM, self._to_units_precip),
                    "precip_probability": row["precip_probability"],
                    "precip_icon": row.get("precip_icon", ""),
                    "precip_type": row.get("precip_type", ""),
                    "wind_avg": await cnv.wind(sum_wind_avg, UNIT_WIND_MS, self._to_units_wind),
                    "wind_bearing": sum_wind_bearing,
                    "current_condition": current_condition,
                    "current_icon": current_icon,
                    "temp_high_today": temp_high_today,
                    "temp_low_today": temp_low_today,
                }
                items.append(ForecastDataDaily(item))
        else:
            cnt = 0
            for row in forecast[FORECAST_TYPE_HOURLY]:
                # Skip over past forecasts - seems the API sometimes returns old forecasts
                forecast_time = datetime.fromtimestamp(row["time"])
                if today > forecast_time:
                    continue

                item = {
                    "timestamp": datetime.fromtimestamp(row["time"]),
                    "epochtime": row["time"],
                    "conditions": row["conditions"],
                    "icon": row["icon"],
                    "air_temperature": row["air_temperature"],
                    "sea_level_pressure": await cnv.pressure(row["sea_level_pressure"], UNIT_PRESSURE_MB, self._to_units_pressure),
                    "relative_humidity": row["relative_humidity"],
                    "precip": await cnv.precip(row["precip"], UNIT_PRECIP_MM, self._to_units_precip),
                    "precip_probability": row["precip_probability"],
                    "precip_icon": row.get("precip_icon", ""),
                    "precip_type": row.get("precip_type", ""),
                    "wind_avg": await cnv.wind(row["wind_avg"], UNIT_WIND_MS, self._to_units_wind),
                    "wind_gust": await cnv.wind(row["wind_gust"], UNIT_WIND_MS, self._to_units_wind),
                    "wind_direction": row["wind_direction"],
                    "wind_direction_cardinal": row["wind_direction_cardinal"],
                    "uv": row["uv"],
                    "feels_like": row["feels_like"],
                    "current_condition": current_condition,
                    "current_icon": current_icon,
                    "temp_high_today": temp_high_today,
                    "temp_low_today": temp_low_today,
                }
                items.append(ForecastDataHourly(item))
                # Limit number of Hours
                cnt += 1
                if cnt >= hours_to_show:
                    break

        return items

    async def _device_info(self) -> None:
        """Returns Device Data for attached devices to station."""

        devices = await self._station_information()
        items = []
        for device in devices:
            if device["device_type"] in DEVICE_TYPES:
                endpoint = f"observations/device/{device['device_id']}?token={self._token}"
                json_data = await self.async_request("get", endpoint)
                obs = json_data["obs"][0]
                obs_time = obs[0]
                if device["device_type"] == DEVICE_TYPE_AIR:
                    device_type_desc = "AIR"
                    battery = obs[6]
                    station_type = "AIR & SKY"
                elif device["device_type"] == DEVICE_TYPE_SKY:
                    device_type_desc = "SKY"
                    station_type = "AIR & SKY"
                    battery = obs[8]
                else:
                    device_type_desc = "TEMPEST"
                    battery = obs[16]
                    station_type = "TEMPEST"
                
                item = {
                    "obs_time": datetime.fromtimestamp(obs_time),
                    "device_type": device["device_type"],
                    "device_type_desc": device_type_desc,
                    "device_name": device["device_name"],
                    "device_id": device["device_id"],
                    "battery": battery,
                    "station_type": station_type,
                    "serial_number": device["serial_number"],
                    "firmware_revision": device["firmware_revision"],
                    "hardware_revision": device["hardware_revision"],
                }
                items.append(DeviceData(item))
        
        return items

 
    async def _raw_forecast_data(self, forecast_type, hours_to_show) -> None:
        """Return Forecast data for the Station."""
        if self._latitude is None:
            await self._station_information()

        endpoint = f"better_forecast?station_id={self._station_id}&token={self._token}&lat={self._latitude}&lon={self._longitude}"
        json_data = await self.async_request("get", endpoint)

        forecast = json_data.get("forecast")
        return forecast

    async def async_request(self, method: str, endpoint: str) -> dict:
        """Make a request against the SmartWeather API."""

        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        try:
            async with session.request(
                method, f"{BASE_URL}/{endpoint}"
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data
        except asyncio.TimeoutError:
            raise RequestError("Request to endpoint timed out: {endpoint}")
        except ClientError as err:
            if "Unauthorized" in str(err):
                raise InvalidApiKey("Your API Key is invalid or does not support this operation")
            elif "Not Found" in str(err):
                raise ResultError("The Station ID does not exist")
            else:
                raise RequestError(
                    f"Error requesting data from {endpoint}: {err}"
                ) from None

        finally:
            if not use_running_session:
                await session.close()
