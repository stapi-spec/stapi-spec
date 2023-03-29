from api.backends.fake_backend import FakeBackend
from api.backends.sentinel_backend import SentinelBackend


BACKENDS = {
    "fake": FakeBackend,
    "sentinel": SentinelBackend,
}
