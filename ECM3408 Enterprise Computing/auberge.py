# No AI was used to create this file.

from flask import Flask, request

import requests
import re
from typing import List, Tuple

LLM = "http://localhost:3000/llm"
GUARDRAILS = "http://localhost:3001/guardrails"

app = Flask(__name__)

@app.route("/auberge", methods=["POST"])
def auberge():
    js = request.get_json()
    prompt = js.get("prompt")

    if not prompt:
        return {"error": "Missing required field 'prompt'"}, 400

    rsp = requests.get(GUARDRAILS)

    if not rsp.ok:
        return {"error": "Could not get guardrail list."}, rsp.status_code

    # A list of (regx, sub) tuples
    guardrails = []

    for guardrail_id in rsp.json():
        guardrail_rsp = requests.get(f"{GUARDRAILS}/{guardrail_id}")

        if not guardrail_rsp.ok:
            return {"error": f"Could not get guardrail with ID {guardrail_id}."}, rsp.status_code
        
        guardrail = guardrail_rsp.json()
        guardrails.append((guardrail.get("regx"), guardrail.get("sub")))

    # Sanitise the input prompt
    clean_prompt = sanitise(prompt, guardrails)

    js = { "prompt": clean_prompt }
    rsp = requests.post(LLM, json=js)

    if not rsp.ok:
        return {"error": "Post to LLM failed."}, rsp.status_code

    output = rsp.json().get("output")
    clean_output = sanitise(output, guardrails)

    return {
        "prompt": clean_prompt,
        "output": clean_output,
        "unsanitised_prompt": prompt,
        "usanitised_output": output,
    }, 200
    

def sanitise(text: str, guardrails: List[Tuple[str, str]]):
    for regx, sub in guardrails:
        text = re.sub(regx, sub, text)

    return text

if __name__ == "__main__":
    app.run(host="localhost", port=3002)
