import json
from jsonpath_ng import parse

class TraceRequest:
    def __init__(self, entry) -> None:
        self.entry = entry
        self.status = entry["http"]["statusCode"]
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
