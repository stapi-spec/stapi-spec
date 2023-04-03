from api.backends.base import Backend
from api.backends.blacksky_backend import BlackskyBackend
from api.backends.fake_backend import FakeBackend
from api.backends.planet_backend import PlanetBackend
from api.backends.earthsearch_backend import EarthSearchBackend
from api.backends.umbra_backend import UmbraBackend

BACKENDS: dict[str, Backend] = {
    "fake": FakeBackend,
    "earthsearch": EarthSearchBackend,
    "blacksky": BlackskyBackend,
    "planet": PlanetBackend,
    "umbra": UmbraBackend,
}
