from api.backends.base import Backend
from api.backends.blacksky_backend import BlackskyBackend
from api.backends.earthsearch_backend import EarthSearchBackend
from api.backends.fake_backend import FakeBackend
from api.backends.planet_backend import PlanetBackend
from api.backends.umbra_backend import UmbraBackend

BACKENDS: dict[str, Backend] = {
    "fake": FakeBackend(),  # type: ignore
    "earthsearch": EarthSearchBackend(),  # type: ignore
    "blacksky": BlackskyBackend(),  # type: ignore
    "planet": PlanetBackend(),  # type: ignore
    "umbra": UmbraBackend(),  # type: ignore
}
