import json
from jsonpath_ng import parse
from util import parse_date
from datetime import datetime, timezone

class TraceRequest:
    def __init__(self, entry, traceId) -> None:
        self.entry = entry
        self.traceId = traceId
        self.status = entry["http"]["statusCode"]
        self.started = parse_date(entry["startTime"])
        self.end = parse_date(entry["endTime"])
        self.durationMs = entry["durationMs"]
        self.variables = {}
        for i in entry["variablesJSON"]:
            self.variables[i["key"]] = json.loads(i["value"])

        self.headers = {}
        for i in entry["http"]["requestHeaders"]:
            self.headers[i["key"]] = (i["value"])

    def find_variables_length(self, expression):
        jsonpath_expression = parse(expression)

        match = jsonpath_expression.find(self.variables)
        if len(match) != 1:
            raise Exception("No match found")
        match = match[0]
        value = match.value
        if type(value) != list:
            raise Exception("Expected list")
        return len(value)
