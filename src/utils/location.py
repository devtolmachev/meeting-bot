import asyncio
from math import pi, sqrt, sin, cos, atan2

from aiohttp import ClientSession, TCPConnector
from fake_useragent import UserAgent

from src.decorators.async_parse import aiohttp_timeout_receiver


def haversine(pos1: dict[str, float],
              pos2: dict[str, float]):

    lat1 = float(pos1['lat'])
    long1 = float(pos1['long'])
    lat2 = float(pos2['lat'])
    long2 = float(pos2['long'])

    degree_to_rad = float(pi / 180.0)

    d_lat = (lat2 - lat1) * degree_to_rad
    d_long = (long2 - long1) * degree_to_rad

    a = pow(sin(d_lat / 2), 2) + cos(lat1 * degree_to_rad) * cos(lat2 * degree_to_rad) * pow(sin(d_long / 2), 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    km = 6367 * c

    return round(km * 1000, 2)


@aiohttp_timeout_receiver(timeout=1.5)
async def get_city(session: ClientSession, long: float, lat: float):
    async with session as s:
        geo = {'format': 'json',
               'lat': f'{lat}',
               'lon': f'{long}'}
        async with s.get('https://nominatim.openstreetmap.org/reverse', params=geo) as resp:
            response = (await resp.json(content_type=None))["address"]["city"]

    return response
