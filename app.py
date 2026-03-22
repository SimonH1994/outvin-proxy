import os
import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OUTVIN_EMAIL    = os.environ.get("OUTVIN_EMAIL", "")
OUTVIN_PASSWORD = os.environ.get("OUTVIN_PASSWORD", "")
BASE_URL        = "https://www.outvin.com/api/v1"


def auth():
    if not OUTVIN_EMAIL or not OUTVIN_PASSWORD:
        raise ValueError("OUTVIN_EMAIL and OUTVIN_PASSWORD must be set")
    return HTTPBasicAuth(OUTVIN_EMAIL, OUTVIN_PASSWORD)


@app.route("/vehicle/<vin>")
def vehicle(vin):
    try:
        if not OUTVIN_EMAIL or not OUTVIN_PASSWORD:
            return jsonify({"error": "Set OUTVIN_EMAIL and OUTVIN_PASSWORD env vars"}), 400
        r = requests.get(f"{BASE_URL}/vehicle/{vin}", auth=auth(), timeout=15)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
