# No AI was used to create this file.

import os
import requests

FIREBASE_DB = os.environ["FIREBASE_DB"]


class Database:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    def create_guardrail(self, guardrail_id, data):
        body = {str(guardrail_id): data}
        return requests.patch(f"{self.base_url}/guardrails.json", json=body)

    def get_guardrail(self, guardrail_id):
        return requests.get(f"{self.base_url}/guardrails/{guardrail_id}.json")

    def delete_guardrail(self, guardrail_id):
        # Attempting to delete a guardrail that doesn't exist won't error, but I don't think we should waste time checking if the ID is valid first
        return requests.delete(f"{self.base_url}/guardrails/{guardrail_id}.json")

    def list_guardrail_ids(self):
        return requests.get(f"{self.base_url}/guardrails.json")

    def clear(self):
        return requests.delete(f"{self.base_url}/guardrails.json")


db = Database(FIREBASE_DB)
