import os

from flask import Flask, jsonify


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

    return app


app = create_app()
