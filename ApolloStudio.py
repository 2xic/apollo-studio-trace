import requests
import os
from dotenv import load_dotenv
from Metric import Metric
load_dotenv()

class ApolloStudio:
    def request(
            self,
            graph,
            queryId,
            clientName,
            from_timestamp,
            to_timestamp,
    ):
        with open("GetTraceRefs.graphql", "r") as file:
            response = requests.post(
                "https://graphql.api.apollographql.com/api/graphql",
                headers={
                        "Cookie": os.getenv("APOLLO_STUDIO_COOKIE")
                },
                json={
                    "query": file.read(),
                    "variables": {
                        "graph": graph,
                        "queryId": queryId,
                        "clientName": clientName,
                        "from":from_timestamp,
                        "to":to_timestamp
                    }
                }
            )
            response_data = response.json()
            if "data" not in response_data:
                raise Exception(response_data)

            stats = response_data["data"]["graph"]["stats"]["queryStats"]
            metrics = list(map(Metric, stats))
            return metrics
