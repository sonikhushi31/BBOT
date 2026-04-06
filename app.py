from flask import Flask, request, jsonify
import requests
import os

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
    all_matches = []

    while True:
        data = call_api(skip)

        if not data:
            return jsonify({"error": "API error"}), 500

        members = data.get("Results", [])

        if not members:
            break  # ✅ No more data

        for member in members:
            name = member.get("Name", "").lower()

            # 👉 Example: active filter
            status = member.get("MembershipStatus", "").lower()

            if search_text in name or search_text in status:
                all_matches.append(member)

        skip += 200

    if not all_matches:
        return jsonify({"message": "No match found"})

    return jsonify({
        "message": "Matches found",
        "count": len(all_matches),
        "data": all_matches
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
