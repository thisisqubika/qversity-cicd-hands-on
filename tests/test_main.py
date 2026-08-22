from app.main import create_app


def test_health_returns_ok_and_environment(monkeypatch):
    monkeypatch.setenv("APP_ENV", "staging")
    client = create_app().test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "environment": "staging"}


def test_health_defaults_to_unknown_environment(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)
    client = create_app().test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "environment": "unknown"}


def test_items_returns_expected_shape():
    client = create_app().test_client()

    response = client.get("/items")

    assert response.status_code == 200
    body = response.get_json()
    assert body == {
        "items": [
            {"id": 1, "name": "widget"},
            {"id": 2, "name": "gadget"},
        ]
    }
