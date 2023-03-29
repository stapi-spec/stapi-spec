from api.backends.fake_backend import FakeBackend
from api.backends.sentinel_backend import HistoricalBackend
from api.backends.blacksky_backend import BlackskyBackend
from api.backends.planet_backend import PlanetBackend
from api.backends.base import Backend


BACKENDS: dict[str, Backend] = {
    "fake": FakeBackend(),
    "historical": HistoricalBackend(),
    "planet": PlanetBackend(),
    "blacksky": BlackskyBackend()

}
