import os

from flask import Flask, jsonify, request


def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify(
            status="ok",
            environment=os.environ.get("APP_ENV", "unknown"),
        )

    items = [
        {"id": 1, "name": "widget"},
        {"id": 2, "name": "gadget"},
    ]

    @app.get("/items")
    def get_items():
        return jsonify(items=items)

    @app.post("/items")
    def create_item():
        data = request.get_json(silent=True)
        if not data or "name" not in data:
            return jsonify(error="name is required"), 400

        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            return jsonify(error="name must be a non-empty string"), 400

        new_id = max(item["id"] for item in items) + 1
        item = {"id": new_id, "name": name.strip()}
        items.append(item)
        return jsonify(item=item), 201

    @app.put("/items/<int:item_id>")
    def update_item(item_id):
        data = request.get_json(silent=True)
        if not data or "name" not in data:
            return jsonify(error="name is required"), 400

        name = data["name"]
        if not isinstance(name, str) or not name.strip():
            return jsonify(error="name must be a non-empty string"), 400

        item = next((item for item in items if item["id"] == item_id), None)
        if item is None:
            return jsonify(error="item not found"), 404

        item["name"] = name.strip()
        return jsonify(item=item), 200

    return app


app = create_app()
