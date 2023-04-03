from api.backends.base import Backend
from api.backends.blacksky_backend import BlackskyBackend
from api.backends.fake_backend import FakeBackend
from api.backends.planet_backend import PlanetBackend
from api.backends.sentinel_backend import HistoricalBackend
from api.backends.umbra_backend import UmbraBackend

BACKENDS: dict[str, Backend] = {
    "fake": FakeBackend,
    "historical": HistoricalBackend,
    "blacksky": BlackskyBackend,
    "planet": PlanetBackend,
    "umbra": UmbraBackend,
}
