from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://burnabyboardoftrade.growthzoneapp.com/api/memberships/all"
API_KEY = "A1Y8akSXMjWhCUtRvEwCALwoyOaaLLUhdwHouCWy"  # 🔴 Replace with your key


def call_api(skip, top=200):
    headers = {
        "Accept": "application/json",
        "Authorization": f"ApiKey {API_KEY}"
    }

    params = {
        "$skip": skip,
        "$top": top
    }

    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code != 200:
        print("API Error:", response.status_code)
        return None

    return response.json()


@app.route("/search-member", methods=["GET"])
def search_member():
    search_text = request.args.get("search")

    if not search_text:
        return jsonify({"error": "Please provide search parameter"}), 400

    search_text = search_text.lower()
    skip = 0

    while True:
        data = call_api(skip)

        if not data:
            return jsonify({"error": "API error"}), 500

        # ✅ Correct key
        members = data.get("Results", [])

        # 🔚 No more data
        if not members:
            return jsonify({"message": "No match found"})

        # 🔍 Search logic
        for member in members:
            name = member.get("Name", "").lower()

            if search_text in name:
                return jsonify({
                    "message": "Match found",
                    "data": member,
                    "skip_used": skip
                })

        # 🔁 Next batch
        skip += 200


if __name__ == "__main__":
    app.run(debug=True)