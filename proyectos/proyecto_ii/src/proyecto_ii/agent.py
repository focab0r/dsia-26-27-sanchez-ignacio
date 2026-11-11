

import json
import os
import requests

def call_agent(text):
    response = requests.post(
        os.environ["FOUNDRY_AGENT_ENDPOINT"],
        params={"api-version": os.environ.get("FOUNDRY_API_VERSION", "v1")},
        headers={"api-key": os.environ["FOUNDRY_API_KEY"]},
        json={"input": text},
        timeout=60,
    )
    response.raise_for_status()

    answer = "".join(
        part["text"]
        for item in response.json()["output"]
        if item.get("type") == "message"
        for part in item["content"]
        if part.get("type") == "output_text"
    )
    return json.loads(answer)
