"""Defines the Data Classes used."""
from datetime import datetime as dt
import datetime

class StationData:
    """A representation of all data available for a specific Station ID."""

    def __init__(self, data):
        self._air_density = data["air_density"]
        self._air_temperature = data["air_temperature"]
        self._brightness = data["brightness"]
        self._dew_point = data["dew_point"]
        self._feels_like = data["feels_like"]
        self._heat_index = data["heat_index"]
        self._lightning_strike_last_time = data["lightning_strike_last_time"]
        self._lightning_strike_last_distance = data["lightning_strike_last_distance"]
        self._lightning_strike_count = data["lightning_strike_count"]
        self._lightning_strike_count_last_1hr = data["lightning_strike_count_last_1hr"]
        self._lightning_strike_count_last_3hr = data["lightning_strike_count_last_3hr"]
        self._precip_accum_last_1hr = data["precip_accum_last_1hr"]
        self._precip_accum_local_day = data["precip_accum_local_day"]
        self._precip_accum_local_yesterday = data["precip_accum_local_yesterday"]
        self._precip_rate = data["precip_rate"]
        self._precip_minutes_local_day = data["precip_minutes_local_day"]
        self._precip_minutes_local_yesterday = data["precip_minutes_local_yesterday"]
        self._pressure_trend = data["pressure_trend"]
        self._relative_humidity = data["relative_humidity"]
        self._solar_radiation = data["solar_radiation"]
        self._station_pressure = data["station_pressure"]
        self._sea_level_pressure = data["sea_level_pressure"]
        self._station_name = data["station_name"]
        self._timestamp = data["timestamp"]
        self._uv = data["uv"]
        self._wind_avg = data["wind_avg"]
        self._wind_bearing = data["wind_bearing"]
        self._wind_chill = data["wind_chill"]
        self._wind_gust = data["wind_gust"]

    @property
    def air_density(self) -> float:
        """Return Air Density."""
        return self._air_density

    @property
    def air_temperature(self) -> float:
        """Return Outside Temperature."""
        return self._air_temperature

    @property
    def brightness(self) -> int:
        """Return Brightness in Lux."""
        return self._brightness

    @property
    def dew_point(self) -> float:
        """Return Outside Dewpoint."""
        return self._dew_point

    @property
    def feels_like(self) -> float:
        """Return Outside Feels Like Temp."""
        return self._feels_like

    @property
    def freezing(self) -> bool:
        """Return True if Freezing Outside."""
        if self.air_temperature < 0:
            return True

        return False

    @property
    def heat_index(self) -> float:
        """Return Outside Heat Index."""
        return self._heat_index

    @property
    def lightning(self) -> bool:
        """Return True if it is Lightning."""
        if self.lightning_strike_count > 0:
            return True

        return False
        
    @property
    def lightning_strike_last_time(self) -> datetime:
        """Return the date and time of last strike."""
        return self._lightning_strike_last_time

    @property
    def lightning_strike_last_distance(self) -> int:
        """Return the distance away of last strike."""
        return self._lightning_strike_last_distance

    @property
    def lightning_strike_count(self) -> int:
        """Return the daily strike count."""
        return self._lightning_strike_count

    @property
    def lightning_strike_count_last_1hr(self) -> int:
        """Return the strike count last 1hr."""
        return self._lightning_strike_count_last_1hr

    @property
    def lightning_strike_count_last_3hr(self) -> int:
        """Return the strike count last 3hr."""
        return self._lightning_strike_count_last_3hr
        
    @property
    def precip_accum_last_1hr(self) -> float:
        """Return Precipition for the Last Hour."""
        return self._precip_accum_last_1hr
        
    @property
    def precip_accum_local_day(self) -> float:
        """Return Precipition for the Day."""
        return self._precip_accum_local_day
        
    @property
    def precip_accum_local_yesterday(self) -> float:
        """Return Precipition for Yesterday."""
        return self._precip_accum_local_yesterday

    @property
    def precip_rate(self) -> float:
        """Return current precipitaion rate."""
        return self._precip_rate
        
    @property
    def precip_minutes_local_day(self) -> int:
        """Return Precipition Minutes Today."""
        return self._precip_minutes_local_day
        
    @property
    def precip_minutes_local_yesterday(self) -> int:
        """Return Precipition Minutes Yesterday."""
        return self._precip_minutes_local_yesterday
        
    @property
    def pressure_trend(self) -> int:
        """Return the Pressure Trend."""
        return self._pressure_trend

    @property
    def relative_humidity(self) -> int:
        """Return relative Humidity."""
        return self._relative_humidity

    @property
    def raining(self) -> bool:
        """Return True if it is raining."""
        if self.precip_rate > 0:
            return True

        return False

    @property
    def solar_radiation(self) -> int:
        """Return Solar Radiation."""
        return self._solar_radiation
        
    @property
    def station_pressure(self) -> float:
        """Return Station Pressure."""
        return self._station_pressure
        
    @property
    def sea_level_pressure(self) -> float:
        """Return Sea Level Pressure."""
        return self._sea_level_pressure
        
    @property
    def timestamp(self) -> str:
        """Return Data Timestamp."""
        return self._timestamp
        
    @property
    def station_name(self) -> str:
        """Return Station Name."""
        return self._station_name
        
    @property
    def uv(self) -> float:
        """Return UV Index."""
        return self._uv

    @property
    def wind_avg(self) -> float:
        """Return Wind Speed Average."""
        return self._wind_avg
        
    @property
    def wind_bearing(self) -> int:
        """Return Wind Bearing as Degree."""
        return self._wind_bearing

    @property
    def wind_chill(self) -> float:
        """Return Wind Chill."""
        return self._wind_chill

    @property
    def wind_gust(self) -> float:
        """Return Wind Gust Speed."""
        return self._wind_gust
        
    @property
    def wind_direction(self) -> str:
        """Return Wind Direction Symbol."""
        direction_array = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW","N"]
        direction = direction_array[int((self._wind_bearing + 11.25) / 22.5)]
        return direction

class ForecastDataDaily:
    """A representation of Day Based Forecast Weather Data."""

    def __init__(self, data):
        self._timestamp = data["timestamp"]
        self._epochtime = data["epochtime"]
        self._conditions = data["conditions"]
        self._icon = data["icon"]
        self._sunrise = data["sunrise"]
        self._sunset = data["sunset"]
        self._temp_high = data["air_temp_high"]
        self._temp_low = data["air_temp_low"]
        self._precip = data["precip"]
        self._precip_probability = data["precip_probability"]
        self._precip_icon = data["precip_icon"]
        self._precip_type = data["precip_type"]
        self._wind_avg = data["wind_avg"]
        self._wind_bearing = data["wind_bearing"]
        self._current_condition = data["current_condition"]
        self._current_icon = data["current_icon"]
        self._temp_high_today= data["temp_high_today"]
        self._temp_low_today= data["temp_low_today"]

    @property
    def timestamp(self) -> dt:
        """Forecast DateTime."""
        return self._timestamp.isoformat()

    @property
    def epochtime(self):
        """Forecast Epoch Time."""
        return self._epochtime

    @property
    def conditions(self) -> str:
        """Return condition text ."""
        return self._conditions

    @property
    def icon(self) -> str:
        """Condition Icon."""
        if self._icon.find("cc-") > -1:
            icon = self._icon[3:]
        else:
            icon = self._icon
        return icon

    @property
    def sunrise(self) -> dt:
        """Return Sunrise Time for Location ."""
        return self._sunrise.isoformat()

    @property
    def sunset(self) -> dt:
        """Return Sunset Time for Location ."""
        return self._sunset.isoformat()

    @property
    def temp_high(self) -> float:
        """Return High temperature."""
        return self._temp_high

    @property
    def temp_low(self) -> float:
        """Return Low temperature."""
        return self._temp_low

    @property
    def precip(self) -> float:
        """Return Precipitation."""
        return self._precip
        
    @property
    def precip_probability(self) -> int:
        """Precipitation Probability."""
        return self._precip_probability

    @property
    def precip_icon(self) -> str:
        """Precipitation Icon."""
        return self._precip_icon

    @property
    def precip_type(self) -> str:
        """Precipitation Icon."""
        return self._precip_type

    @property
    def wind_avg(self) -> float:
        """Return Wind Speed Average."""
        return round(self._wind_avg,2)

    @property
    def wind_bearing(self) -> int:
        """Return Wind Bearing in degrees."""
        return int(self._wind_bearing)

    @property
    def current_condition(self) -> str:
        """Return Current condition text."""
        return self._current_condition

    @property
    def current_icon(self) -> str:
        """Current Condition Icon."""
        if self._current_icon.find("cc-") > -1:
            icon = self._current_icon[3:]
        else:
            icon = self._current_icon
        return icon

    @property
    def temp_high_today(self) -> float:
        """Return High temperature for current day."""
        return self._temp_high_today

    @property
    def temp_low_today(self) -> float:
        """Return Low temperature for current day."""
        return self._temp_low_today

class ForecastDataHourly:
    """A representation of Hour Based Forecast Weather Data."""

    def __init__(self, data):
        self._timestamp = data["timestamp"]
        self._epochtime = data["epochtime"]
        self._conditions = data["conditions"]
        self._icon = data["icon"]
        self._temperature = data["air_temperature"]
        self._pressure = data["sea_level_pressure"]
        self._humidity = data["relative_humidity"]
        self._precip = data["precip"]
        self._precip_probability = data["precip_probability"]
        self._precip_icon = data["precip_icon"]
        self._precip_type = data["precip_type"]
        self._wind_avg = data["wind_avg"]
        self._wind_gust = data["wind_gust"]
        self._wind_bearing = data["wind_direction"]
        self._wind_direction = data["wind_direction_cardinal"]
        self._uv = data["uv"]
        self._feels_like = data["feels_like"]
        self._current_condition = data["current_condition"]
        self._current_icon = data["current_icon"]
        self._temp_high_today= data["temp_high_today"]
        self._temp_low_today= data["temp_low_today"]

    @property
    def timestamp(self) -> dt:
        """Forecast DateTime."""
        return self._timestamp.isoformat()

    @property
    def epochtime(self):
        """Forecast Epoch Time."""
        return self._epochtime

    @property
    def conditions(self) -> str:
        """Return condition text ."""
        return self._conditions

    @property
    def icon(self) -> str:
        """Condition Icon."""
        if self._icon.find("cc-") > -1:
            icon = self._icon[3:]
        else:
            icon = self._icon
        return icon

    @property
    def temperature(self) -> float:
        """Return temperature."""
        return self._temperature

    @property
    def pressure(self) -> float:
        """Return Sea Level Pressure."""
        return self._pressure

    @property
    def humidity(self) -> int:
        """Return Relative Humidity."""
        return self._humidity

    @property
    def precip(self) -> float:
        """Return Precipitation."""
        return self._precip
        
    @property
    def precip_probability(self) -> int:
        """Precipitation Probability."""
        return self._precip_probability

    @property
    def precip_icon(self) -> str:
        """Precipitation Icon."""
        return self._precip_icon

    @property
    def precip_type(self) -> str:
        """Precipitation Icon."""
        return self._precip_type

    @property
    def wind_avg(self) -> float:
        """Return Wind Speed Average."""
        return self._wind_avg

    @property
    def wind_gust(self) -> float:
        """Return Wind Gust."""
        return self._wind_gust

    @property
    def wind_bearing(self) -> int:
        """Return Wind Bearing in degrees."""
        return self._wind_bearing

    @property
    def wind_direction(self) -> str:
        """Return Wind Direction Cardinal."""
        return self._wind_direction

    @property
    def wind_direction_icon(self) -> str:
        """Return Wind Direction Icon."""
        return self._wind_direction_icon

    @property
    def uv(self) -> float:
        """Return UV Index."""
        return self._uv

    @property
    def feels_like(self) -> float:
        """Return Feels Like Temperature."""
        return self._feels_like

    @property
    def current_condition(self) -> str:
        """Return Current condition text."""
        return self._current_condition

    @property
    def current_icon(self) -> str:
        """Current Condition Icon."""
        if self._current_icon.find("cc-") > -1:
            icon = self._current_icon[3:]
        else:
            icon = self._current_icon
        return icon

    @property
    def temp_high_today(self) -> float:
        """Return High temperature for current day."""
        return self._temp_high_today

    @property
    def temp_low_today(self) -> float:
        """Return Low temperature for current day."""
        return self._temp_low_today

class DeviceData:
    """A representation of Devices attached to the station."""

    def __init__(self, data):
        self._timestamp = data["obs_time"]
        self._device_type = data["device_type"]
        self._device_type_desc = data["device_type_desc"]
        self._device_name = data["device_name"]
        self._device_id = data["device_id"]
        self._battery = data["battery"]
        self._serial_number = data["serial_number"]
        self._firmware_revision = data["firmware_revision"]
        self._hardware_revision = data["hardware_revision"]

    @property
    def timestamp(self) -> dt:
        """Return observation time."""
        return self._timestamp.isoformat()

    @property
    def device_type(self) -> str:
        """Returns Device Type."""
        return self._device_type

    @property
    def device_type_desc(self) -> str:
        """Returns Device Type Description."""
        return self._device_type_desc

    @property
    def device_name(self) -> str:
        """Returns Device Name."""
        return self._device_name

    @property
    def device_id(self) -> str:
        """Returns Device ID."""
        return self._device_id

    @property
    def battery(self) -> float:
        """Returns Battery (volts)."""
        return self._battery

    @property
    def serial_number(self) -> str:
        """Returns Device Serial Number."""
        return self._serial_number

    @property
    def firmware_revision(self) -> str:
        """Returns Device FW Version."""
        return self._firmware_revision

    @property
    def hardware_revision(self) -> str:
        """Returns Device HW Version."""
        return self._hardware_revision
