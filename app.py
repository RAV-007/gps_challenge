from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "coords.log"  # Datei für alle Koordinaten

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/location", methods=["POST"])
def location():
    data = request.get_json(silent=True)
    print("RAW JSON:", data)

    if not data:
        return jsonify({"state": "Unbekannt"}), 400

    lat = data.get("lat")
    lon = data.get("lon")
    accuracy = data.get("accuracy")

    print("Latitude:", lat)
    print("Longitude:", lon)
    print("Accuracy:", accuracy)

    # ... (dein Bundesland-Kram)
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    response = requests.get(url, headers={"User-Agent": "gps-challenge"})
    result = response.json()
    state = result.get("address", {}).get("state", "Unbekannt")
    print("Bundesland:", state)

    return jsonify({"state": state})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))