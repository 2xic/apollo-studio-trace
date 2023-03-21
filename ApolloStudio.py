from dotenv import load_dotenv
from Metric import Metric
from Trace import Trace
from GraphqlRequest import GraphqlRequest
from TraceRequest import TraceRequest
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
            results = response_data["data"]["graph"]["trace"]
            return TraceRequest(results)
