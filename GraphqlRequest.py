import requests
import os
import time

class GraphqlRequest:
    def __init__(self, endpoint) -> None:
        self.cookie = os.getenv("APOLLO_STUDIO_COOKIE")
        self.endpoint = endpoint

    def request(self, query, variables):
        response = requests.post(
            self.endpoint,
            headers={
                    "Cookie": self.cookie
            },
            json={
                "query": query,
                "variables": variables,
            }
        )
        time.sleep(0.2)
        return response
