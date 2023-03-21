from TraceRequest import TraceRequest

class Trace:
    def __init__(self, entry, graph: str, studio) -> None:
        self.traceId = entry["groupBy"]["traceId"]
        self.graph = graph
        self.studio = studio
    
    def get_full_trace(self) -> TraceRequest:
        return self.studio.get_trace(
            graph=self.graph,
            traceId=self.traceId
        )
