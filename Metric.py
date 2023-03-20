from dateutil import parser

class Metric:
    def __init__(self, entry) -> None:
        self.timestamp = parser.parse(entry["timestamp"])
        self.totalCount = entry["metrics"]["uncachedHistogram"]["totalCount"]
        self.averageDurationMs = entry["metrics"]["uncachedHistogram"]["averageDurationMs"]

        self.buckets_speeds = sum(list(
            map(
                lambda x: [x["rangeEndMs"], ] * x["count"],
                entry["metrics"]["uncachedHistogram"]["buckets"]
            )
        ), [])
