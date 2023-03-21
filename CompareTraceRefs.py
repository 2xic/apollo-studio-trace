import argparse
import datetime
from ApolloStudio import ApolloStudio
import matplotlib.pyplot as plt
from Plot import scatter
from util import parse_date

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--from', type=parse_date, help='From date')
    parser.add_argument('-t', '--to', type=parse_date, default=datetime.date.today(), help='To date')
    parser.add_argument('-q', '--queryId', type=str, help='Query id')
    parser.add_argument('-g', '--graph', type=str, help='graph id')
    parser.add_argument('-c', '--clientName', type=str, action='append', help='Client name')
    parser.add_argument('-n', '--title', type=str, required=True, help="Title of the plot")
    parser.add_argument('-m', '--max_response_time', type=int, default=float('inf'), help="Filter out outliers")
    parser.add_argument('-o', '--output', type=str, required=True, help="Save file as")
    parser.add_argument('-e', '--expression', type=str, required=True, help="Expression used to find array of variables")
    arguments = vars(parser.parse_args())

    from_date:datetime.date = arguments["from"]
    to_date:datetime.date = arguments["to"]

    from_timestamp_offset = -int((datetime.datetime.now() - from_date).total_seconds())
    to_timestamp_offset = -int((datetime.datetime.now() - to_date).total_seconds())

    for clientName in arguments["clientName"]:
        results = ApolloStudio().get_trace_refs(
            graph=arguments["graph"],
            queryId=arguments["queryId"],
            clientName=clientName,
            from_timestamp=from_timestamp_offset,
            to_timestamp=to_timestamp_offset
        )
        response_time = []
        variables_length = []

        for i in results:
            response = i.get_full_trace()
            response_time.append(response.durationMs)
            variables_length_expression = arguments["expression"]
            variables_length.append(response.find_variables_length(expression=variables_length_expression))

        scatter(
            x=variables_length,
            y=response_time,
            label=clientName,
            xlabel="variables length",
            ylabel="Response time (MS)"
        )

    plt.title(arguments["title"])
    plt.legend(loc="upper left")
    if arguments["output"]:
        plt.savefig(arguments["output"])
    else:
        plt.show()
