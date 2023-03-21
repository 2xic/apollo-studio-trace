from dotenv import load_dotenv
from Metric import Metric
from Trace import Trace
from GraphqlRequest import GraphqlRequest
from TraceRequest import TraceRequest
import os
import json
load_dotenv()

class ApolloStudio:
    def __init__(self) -> None:
        self.graphql_request = GraphqlRequest(
            "https://graphql.api.apollographql.com/api/graphql"
        )

    def get_query_stats(
            self,
            graph,
            queryId,
            clientName,
            from_timestamp,
            to_timestamp,
    ):
        with open("GetQueryStats.graphql", "r") as file:
            response = self.graphql_request.request(
                query=file.read(),
                variables={
                    "graph": graph,
                    "queryId": queryId,
                    "clientName": clientName,
                    "from":from_timestamp,
                    "to":to_timestamp
                }
            )

            response_data = response.json()
            if "data" not in response_data:
                raise Exception(response_data)

            stats = response_data["data"]["graph"]["stats"]["queryStats"]
            metrics = list(map(Metric, stats))
            return metrics

    def get_trace_refs(
            self,
            graph,
            queryId,
            clientName,
            from_timestamp,
            to_timestamp,
    ):
        with open("GetQueryTraceRefs.graphql", "r") as file:
            response = self.graphql_request.request(
                query=file.read(),
                variables={
                    "graph": graph,
                    "queryId": queryId,
                    "clientName": clientName,
                    "from":from_timestamp,
                    "to":to_timestamp
                }
            )

            response_data = response.json()
            if "data" not in response_data:
                raise Exception(response_data)
            results = response_data["data"]["graph"]["stats"]["traceRefs"]
            return list(map(lambda x: Trace(entry=x, graph=graph, studio=self), results))

    def get_trace(
            self,
            graph,
            traceId,
    ):
        with open("GetQueryTrace.graphql", "r") as file:
            response_data = self._read_cache(traceId)
            if response_data is None:
                response = self.graphql_request.request(
                    query=file.read(),
                    variables={
                        "graph": graph,
                        "traceId": traceId,
                    }
                )

                response_data = response.json()
                if "data" not in response_data:
                    raise Exception(response_data)

                self._write_cache(
                    traceId,
                    response_data
                )
            results = response_data["data"]["graph"]["trace"]
            if results is None:
                return None
            return TraceRequest(results)

    def _read_cache(self, key):
        file_path = self._get_cache_path(key)
        if not os.path.isfile(file_path):
            return None

        with open(file_path, "r") as file:
            return json.load(
                file
            )

    def _write_cache(self, key, json_response):
        file_path = self._get_cache_path(key)
        with open(file_path, "w") as file:
            json.dump(
                json_response,
                file
            )

    def _get_cache_path(self, key):
        dir_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            ".cache"
        )
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(
            dir_path,
            key
        )
        return file_path

