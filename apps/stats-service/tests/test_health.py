from fastapi.testclient import TestClient

from loadlab_stats import __version__
from loadlab_stats.api import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": __version__}
