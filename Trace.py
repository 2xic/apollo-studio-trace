from TraceRequest import TraceRequest
from util import parse_date

class Trace:
    def __init__(self, entry, graph: str, studio) -> None:
        self.timestamp = parse_date(entry["timestamp"])
        self.traceId = entry["groupBy"]["traceId"]
        self.graph = graph
        self.studio = studio
    
    def get_full_trace(self) -> TraceRequest:
        return self.studio.get_trace(
            graph=self.graph,
            traceId=self.traceId
        )
