import math
from flask import Flask, jsonify, request

app = Flask(__name__)
num = 0

site = {
    "Shackleton Connecting Ridge": {
        "lat": 89.9,
        "lon": 128.5,
        "elevation_km": 4.2,
        "horizon_deg": 0.8
    },
    "Malapert Mountain (Massif)": {
        "lat": 85.9,
        "lon": 2.9,
        "elevation_km": 5.0,
        "horizon_deg": 0.4
    },
    "Peak of Eternal Light": {
        "lat": 89.5,
        "lon": 152.0,
        "elevation_km": 3.8,
        "horizon_deg": 0.6
    },
    "Haworth Crater Rim": {
        "lat": 87.4,
        "lon": -5.1,
        "elevation_km": 2.3,
        "horizon_deg": 1.4
    },
    "Faustini Rim A": {
        "lat": 87.3,
        "lon": 84.3,
        "elevation_km": 2.9,
        "horizon_deg": 1.1
    },
    "Amundsen South Rim": {
        "lat": 84.5,
        "lon": 105.6,
        "elevation_km": 3.2,
        "horizon_deg": 0.9
    }
}


def calculate_exact_point(lat, lon, date_str, duration_days):
    global num
    polar_factor = max(0, (90 - abs(lat)) / 10)

    timeline = []
    for day in range(duration_days):
        solar_angle = math.sin((day + (lon / 15)) * (2 * math.pi / 29.5))
        sunlight_hours = round(
            max(0, (12 + 12 * solar_angle) * polar_factor), 2)
        timeline.append(sunlight_hours)
    num += 1

    return {
        "name": f"Custom Site {num} ({lat:.3f}°, {lon:.3f}°)",
        "lat": round(lat, 4),
        "lon": round(lon, 4),
        "timeline": timeline,
        "extra_data": {
            "avg_sunlight": round(sum(timeline) / len(timeline), 2),
            "polar_distance_km": round((90 - abs(lat)) * 30.3, 1),
        },
    }


def calculate(id, date, duration):
    polar_factor = max(0, (90 - abs(site[id]['lat'])) / 10)

    timeline = []
    for day in range(duration):
        solar_angle = math.sin(
            (day + (site[id]['lon'] / 15)) * (2 * math.pi / 29.5))
        sunlight_hours = round(
            max(0, (12 + 12 * solar_angle) * polar_factor), 2)
        timeline.append(sunlight_hours)

    return {
        "name": id,
        "lat": round(site[id]['lat'], 4),  # Exact user latitude
        "lon": round(site[id]['lon'], 4),  # Exact user longitude
        "timeline": timeline,
        "extra_data": {
            "avg_sunlight": round(sum(timeline) / len(timeline), 2),
            "polar_distance_km": round((90 - abs(site[id]['lat'])) * 30.3, 1),
        },
    }


@app.route("/manual-site", methods=["POST"])
def manual_site():
    data = request.get_json()
    exact_lat = float(data["lat"])
    exact_lon = float(data["lon"])

    result = calculate_exact_point(
        exact_lat, exact_lon, data["date"], int(data["duration"]))
    return jsonify(result)


@app.route("/auto-site", methods=["POST"])
def autosite():
    data = request.get_json()

    result = calculate(data["id"], data["date"], int(data["duration"]))
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
