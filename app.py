from flask import Flask, request, jsonify
from pb import client



collection = client.collection("bootcamp")
app = Flask(__name__)


@app.route("/bootcamp", methods=["POST"])
def index():
    data = request.get_json()
    print(data)

    uid = data["playerUID"]
    record = collection.get_list(1, 1, {"filter": f"playerUID = {uid}"})

    if not record.items:
        collection.create(data)

        return {"message": "OK"}

    item = record.items[0]

    if item.data is None:
        item.data = {}

    section = list(data["data"].keys())[0]

    if section not in item.data:
        item.data[section] = {}

    for key, value in data["data"][section].items():
        if key in item.data[section] and isinstance(value, list):
            item.data[section][key].extend(value)
        else:
            item.data[section][key] = value
    updated_item_data = {
        "playerUID": item.player_uid,
        "playerName": item.player_name,
        "discordUserId": item.discord_user_id,
        "discordChannelId": item.discord_channel_id,
        "data": item.data,
    }
    collection.update(item.id, updated_item_data)

    return {"message": "OK"}


@app.route("/bootcamp/<playerUID>", methods=["GET"])
def get_player_data(playerUID):
    record = collection.get_list(1, 1, {"filter": f"playerUID = {playerUID}"})

    if not record.items:
        return {"message": "Player not found"}, 404

    item = record.items[0]
    data = jsonify(
        {
            "playerUID": str(item.player_uid),
            "playerName": item.player_name,
            "discordUserId": item.discord_user_id,
            "discordChannelId": item.discord_channel_id,
            "data": item.data,
        }
    )

    return data


if __name__ == "__main__":
    app.run()
