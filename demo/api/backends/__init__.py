from api.backends.fake_backend import FakeBackend
from api.backends.sentinel_backend import SentinelBackend
from api.backends.planet_backend import PlanetBackend


BACKENDS = {
    "fake": FakeBackend,
    "sentinel": SentinelBackend,
    "planet": PlanetBackend
}