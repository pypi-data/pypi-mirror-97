""" Contains Helper functions for SmartWeather."""
import asyncio
import logging
import datetime

from pysmartweatherio.const import (
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
    UNIT_TEMP_CELCIUS,
    UNIT_TEMP_FAHRENHEIT,
    UNIT_PRESSURE_HPA,
    UNIT_PRESSURE_MB,
    UNIT_PRESSURE_INHG,
    UNIT_PRECIP_IN,
    UNIT_PRECIP_MM,
    UNIT_WIND_MS,
    UNIT_WIND_KMH,
    UNIT_WIND_MPH,
    UNIT_DISTANCE_KM,
    UNIT_DISTANCE_MI,
)

_LOGGER = logging.getLogger(__name__)

class ConversionFunctions:
    """Convert between different Weather Units."""

    async def temperature(self, value, from_unit, to_unit) -> float:
        """Convert Temperature Value."""
        if from_unit == UNIT_TEMP_CELCIUS:
            return round(value, 1) if to_unit == UNIT_TEMP_CELCIUS else round((value * 9 / 5) + 32, 2)
        else:
            return round(value, 2) if to_unit == UNIT_TEMP_FAHRENHEIT else round((value - 32) / 1.8, 1)

    async def pressure(self, value, from_unit, to_unit) -> float:
        """Convert Pressure Value."""
        if from_unit == UNIT_PRESSURE_HPA:
            from_unit = UNIT_PRESSURE_MB

        if from_unit == UNIT_PRESSURE_MB:
            return value if to_unit == UNIT_PRESSURE_HPA else value * 0.030
        else:
            return value if to_unit == UNIT_PRESSURE_INHG else value * 33.86

    async def wind(self, value, from_unit, to_unit) -> float:
        """Convert Wind Speed Value."""
        if from_unit == UNIT_WIND_MS:
            if to_unit == UNIT_WIND_MS:
                return value
            elif to_unit == UNIT_WIND_KMH:
                return round(value * 3.6, 1)
            else:
                return round(value * 2.24, 1)
        else:
            return value if to_unit == UNIT_WIND_MPH else value * 9 / 20

    async def precip(self, value, from_unit, to_unit, current_entity=False) -> float:
        """Convert Precipitation Value."""

        if not current_entity and value == 0: return None

        if from_unit == UNIT_PRECIP_MM:
            return value if to_unit == UNIT_PRECIP_MM else value * 0.04
        else:
            return value if to_unit == UNIT_PRECIP_IN else value * 25.4

    async def distance(self, value, from_unit, to_unit) -> float:
        """Convert Distance Value."""
        if from_unit == UNIT_DISTANCE_KM:
            return value if to_unit == UNIT_DISTANCE_KM else value * 0.62
        else:
            return value if to_unit == UNIT_DISTANCE_MI else value * 1.61

    async def epoch_to_datetime(self, value) -> str:
        """Converts EPOC time to Date Time String."""
        return datetime.datetime.fromtimestamp(int(value)).strftime("%Y-%m-%d %H:%M:%S")

    async def epoch_to_isodatetime(self, value) -> datetime:
        """Converts EPOC time to ISO Date Time."""
        dt_obj = datetime.datetime.fromtimestamp(int(value))
        return dt_obj.isoformat()

