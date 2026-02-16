# No AI was used to create this file.

from flask import Flask, request

import os
import requests

app = Flask(__name__)

MISTRAL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_API_KEY = os.environ["MISTRAL_API_KEY"]


@app.route("/llm", methods=["POST"])
def prompt_llm():
    js = request.get_json()
    prompt = js.get("prompt")

    if not prompt:
        return {"error": "Missing required field 'prompt'"}, 400

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
    }

    body = {
        "model": "mistral-large-latest",
        "messages": [
            {"role": "system", "content": "Do not use markdown formatting, only plaintext. Keep answers brief."},
            {"role": "user", "content": prompt},
        ],
    }

    rsp = requests.post(MISTRAL, headers=headers, json=body)

    if not rsp.ok:
        return {"error": "Mistral error."}, rsp.status_code

    js = rsp.json()
    output = js.get("choices")[0].get("message").get("content")

    return {"output": output, "prompt": prompt}, 200

if __name__ == "__main__":
    app.run(host="localhost", port=3000)
