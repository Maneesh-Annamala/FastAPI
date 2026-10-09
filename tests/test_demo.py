from fastapi import FastAPI
from fastapi.testclient import AsyncClient, TestClient

demo_app = FastAPI()


@demo_app.get("/health")
def health_check():
    return {"health": "Good"}


test_client = AsyncClient(app=demo_app)


def test_health_check():
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"health": "Good"}
