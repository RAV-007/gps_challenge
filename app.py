from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/location", methods=["POST"])
def location():
    data = request.json
    lat = data.get("lat")
    lon = data.get("lon")
    accuracy = data.get("accuracy")  # Optional, falls JS mitschickt

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ==========================
    # Logging im Server / Render
    # ==========================
    print("===== NEUE KOORDINATEN =====")
    print("Zeit:", timestamp)
    print("Latitude:", lat)
    print("Longitude:", lon)
    if accuracy:
        print("Genauigkeit (Meter):", accuracy)
    print("=============================")

    # Bundesland mit OpenStreetMap Nominatim API ermitteln
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        response = requests.get(url, headers={"User-Agent": "gps-challenge"})
        result = response.json()
        state = result.get("address", {}).get("state", "Unbekannt")
    except Exception as e:
        print("Fehler beim Abrufen des Bundeslandes:", e)
        state = "Unbekannt"

    print("Bundesland:", state)

    # Rückgabe an Browser
    return jsonify({"state": state})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))