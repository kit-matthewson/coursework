# No AI was used to create this file.

import database

from flask import Flask, request, jsonify
import re

app = Flask(__name__)


@app.route("/guardrails/<string:param_id>", methods=["PUT"])
def create_guardrail(param_id):
    js = request.get_json(silent=True)

    if not js:
        return {"error": "Missing JSON body"}, 400

    guardrail_id = js.get("id")
    regx = js.get("regx")
    sub = js.get("sub")

    if not guardrail_id or not regx or not sub:
        return {"error": "Invalid JSON body: Must have 'id', 'regx', and 'sub' fields."}, 400

    # Verify the regx
    try:
        re.compile(regx)
    except re.error as e:
        return {"error": f"Invalid regex: {e}"}, 400

    if param_id != guardrail_id:
        return {
            "error": f"ID passed as route parameter ({param_id}) is different from the one passed in body ({guardrail_id})."
        }, 400

    rsp = database.db.create_guardrail(
        guardrail_id,
        {
            "id": guardrail_id,
            "regx": regx,
            "sub": sub,
        },
    )

    if not rsp.ok:
        return {"error": "Database error."}, rsp.status_code

    return rsp.json(), 201


@app.route("/guardrails/<string:guardrail_id>", methods=["GET"])
def get_guardrail(guardrail_id):
    rsp = database.db.get_guardrail(guardrail_id)

    if not rsp.ok:
        return {"error": "Database error"}, rsp.status_code

    if rsp.content == b"null":
        return {"error": "No guardrail for ID"}, 404

    return rsp.json(), 200


@app.route("/guardrails/<string:guardrail_id>", methods=["DELETE"])
def delete_guardrail(guardrail_id):
    rsp = database.db.delete_guardrail(guardrail_id)

    if not rsp.ok:
        return {"error": "Database error."}, rsp.status_code

    return {}, 200


@app.route("/guardrails", methods=["GET"])
def list_guardrails():
    rsp = database.db.list_guardrail_ids()

    if not rsp.ok:
        return {"error": "Database error."}, rsp.status_code

    js = rsp.json()
    if not js:
        return jsonify([]), 200

    # Firebase will either return a list filled with `None`s for missing consecutive IDs or a dict
    # Debatable whether or not the `Database` class should abstract this
    guardrails = js.values() if isinstance(js, dict) else js

    # Get IDs only and filter out `None`s
    rules = [rule["id"] for rule in guardrails if rule is not None]

    return jsonify(rules), 200


if __name__ == "__main__":
    app.run(host="localhost", port=3001)
