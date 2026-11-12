import os

import psycopg2
import requests
from flask import Flask, jsonify

app = Flask(__name__)


def db():
    return psycopg2.connect(os.environ["DATABASE_URL"])


@app.get("/orders/<int:order_id>")
def get_order(order_id):
    with db() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, total FROM orders WHERE id = %s", (order_id,))
        row = cur.fetchone()
    if row is None:
        return jsonify(error="not found"), 404
    rate = requests.get(os.environ.get("FX_URL", "https://fx.example.com/krw")).json()["rate"]
    print("order lookup", order_id)
    return jsonify(id=row[0], total=row[1], total_usd=round(row[1] / rate, 2))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
