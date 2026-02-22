from flask import Flask, render_template, request, jsonify
import requests
import os
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/location", methods=["POST"])
def location():
    data = request.get_json(silent=True)

    lat = (data or {}).get("lat")
    lon = (data or {}).get("lon")
    accuracy = (data or {}).get("accuracy")

    # Render zeigt ERROR extrem zuverlässig
    logger.error("🔥🔥🔥 COORDS lat=%s lon=%s acc=%s RAW=%s", lat, lon, accuracy, data)
    sys.stderr.flush()

    # Bundesland (optional)
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    response = requests.get(url, headers={"User-Agent": "gps-challenge"})
    result = response.json()
    state = result.get("address", {}).get("state", "Unbekannt")

    logger.error("🔥🔥🔥 STATE=%s", state)
    sys.stderr.flush()

    return jsonify({"state": state, "debug": "server-logged-coords"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))