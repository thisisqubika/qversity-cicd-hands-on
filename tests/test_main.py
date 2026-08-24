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


def test_create_item_returns_201_with_new_item():
    client = create_app().test_client()

    response = client.post("/items", json={"name": "sprocket"})

    assert response.status_code == 201
    assert response.get_json() == {"item": {"id": 3, "name": "sprocket"}}


def test_create_item_is_visible_on_get_items():
    client = create_app().test_client()

    client.post("/items", json={"name": "sprocket"})
    response = client.get("/items")

    assert response.get_json()["items"][-1] == {"id": 3, "name": "sprocket"}


def test_create_item_rejects_missing_name():
    client = create_app().test_client()

    response = client.post("/items", json={})

    assert response.status_code == 400
    assert response.get_json() == {"error": "name is required"}


def test_create_item_rejects_empty_name():
    client = create_app().test_client()

    response = client.post("/items", json={"name": "   "})

    assert response.status_code == 400
    assert response.get_json() == {"error": "name must be a non-empty string"}


def test_update_item_returns_200_with_updated_item():
    client = create_app().test_client()

    response = client.put("/items/1", json={"name": "renamed-widget"})

    assert response.status_code == 200
    assert response.get_json() == {"item": {"id": 1, "name": "renamed-widget"}}


def test_update_item_is_visible_on_get_items():
    client = create_app().test_client()

    client.put("/items/2", json={"name": "renamed-gadget"})
    response = client.get("/items")

    assert response.get_json()["items"][1] == {"id": 2, "name": "renamed-gadget"}


def test_update_item_rejects_missing_name():
    client = create_app().test_client()

    response = client.put("/items/1", json={})

    assert response.status_code == 400
    assert response.get_json() == {"error": "name is required"}


def test_update_item_rejects_empty_name():
    client = create_app().test_client()

    response = client.put("/items/1", json={"name": "   "})

    assert response.status_code == 400
    assert response.get_json() == {"error": "name must be a non-empty string"}


def test_update_item_returns_404_for_missing_item():
    client = create_app().test_client()

    response = client.put("/items/999", json={"name": "ghost"})

    assert response.status_code == 404
    assert response.get_json() == {"error": "item not found"}
