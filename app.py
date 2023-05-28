from flask import Flask, request, jsonify
from pb import client


collection = client.collection("bootcamp")
app = Flask(__name__)


@app.route("/bootcamp", methods=["POST"])
def index():
    data = request.get_json()
    uid = data["playerUID"]
    record = collection.get_list(1, 1, {"filter": f"playerUID = {uid}"})

    if not record.items:
        collection.create(data)
        return jsonify({"message": "OK"})

    item = record.items[0].collection_id
    item["data"] = item.get("data") if item.get("data") is not None else {}

    section = list(data["data"].keys())[0]
    item["data"][section] = item["data"].get(section, {})

    update_data(item["data"][section], data["data"][section])

    # If player name is empty in the existing item, use player name from the request data
    if not item["playerName"]:
        item["playerName"] = data["playerName"]

    updated_item_data = {
        "playerUID": str(item["playerUID"]),
        "playerName": item["playerName"],
        "discordUserId": item["discordUserId"],
        "discordChannelId": item["discordChannelId"],
        "data": item["data"],
    }

    collection.update(item["id"], updated_item_data)
    return jsonify({"message": "OK"})


def update_data(old_data, new_data):
    for key, value in new_data.items():
        if key in old_data and isinstance(value, list):
            old_data[key].extend(value)
        else:
            old_data[key] = value


@app.route("/bootcamp/<playerUID>", methods=["GET"])
def get_player_data(playerUID):
    record = collection.get_list(1, 1, {"filter": f"playerUID = {playerUID}"})

    if not record.items:
        return {"message": "Player not found"}, 404

    collection_item = record.items[0]
    item = collection_item.collection_id

    return jsonify(
        {
            "playerUID": str(item["playerUID"]),
            "playerName": item["playerName"],
            "discordUserId": item["discordUserId"],
            "discordChannelId": item["discordChannelId"],
            "data": item["data"],
        }
    )


if __name__ == "__main__":
    app.run()
