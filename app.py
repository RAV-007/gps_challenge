from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/location", methods=["POST"])
def location():
    data = request.json
    lat = data.get("lat")
    lon = data.get("lon")

    print("Koordinaten erhalten:", lat, lon)

    # Bundesland mit OpenStreetMap Nominatim API ermitteln
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
    response = requests.get(url, headers={"User-Agent": "gps-challenge"})
    result = response.json()
    state = result.get("address", {}).get("state", "Unbekannt")
    print("Bundesland:", state)

    # Rückgabe an Browser
    return jsonify({"state": state})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)