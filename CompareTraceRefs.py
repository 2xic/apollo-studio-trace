import argparse
import datetime
from ApolloStudio import ApolloStudio
import matplotlib.pyplot as plt
from Plot import scatter, scatter_3d
from util import parse_date, move_legends

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--from', nargs='+', type=parse_date, help='From date')
    parser.add_argument('-t', '--to', nargs='+', type=parse_date, default=datetime.date.today(), help='To date')
    parser.add_argument('-q', '--queryId', type=str, help='Query id')
    parser.add_argument('-g', '--graph', type=str, help='graph id')
    parser.add_argument('-c', '--clientName', type=str, action='append', help='Client name')
    parser.add_argument('-n', '--title', type=str, required=True, help="Title of the plot")
    parser.add_argument('-m', '--max_response_time', type=int, default=float('inf'), help="Filter out outliers")
    parser.add_argument('-o', '--output', type=str, required=True, help="Save file as")
    parser.add_argument('-e', '--expression', type=str, required=True, help="Expression used to find array of variables")
    parser.add_argument('-l', '--legends', nargs='+', type=str, required=False, help="Title of the legends")
    parser.add_argument('--x_axis',
                    choices=['variables', 'timestamp', 'variables_timestamp'],
                    help='Value for x-axis')

    arguments = vars(parser.parse_args())

    assert len(arguments["from"]) == len(arguments["to"])
    if arguments["legends"]:
        assert len(arguments["from"]) == len(arguments["legends"])

    x = []
    y = []
    z = []
    point_symbol = []
    symbols = ["x", "o"]

    for index, (from_date, to_date) in enumerate(zip(arguments["from"], arguments["to"])):
        from_date:datetime.date = from_date
        to_date:datetime.date = to_date

        from_timestamp_offset = -int((datetime.datetime.now() - from_date).total_seconds())
        to_timestamp_offset = -int((datetime.datetime.now() - to_date).total_seconds())

        for client_index, clientName in enumerate(arguments["clientName"]):
            results = ApolloStudio().get_trace_refs(
                graph=arguments["graph"],
                queryId=arguments["queryId"],
                clientName=clientName,
                from_timestamp=from_timestamp_offset,
                to_timestamp=to_timestamp_offset
            )
            response_time = []
            x_axis = []
            z_axis = []

            for i in results:
                response = i.get_full_trace()
                if response is None:
                    continue
                if response.durationMs < arguments["max_response_time"]:
                    response_time.append(response.durationMs)
                    variables_length_expression = arguments["expression"]
                    if arguments["x_axis"] == "variables":
                        x_axis.append(response.find_variables_length(expression=variables_length_expression))
                    elif arguments["x_axis"] == "timestamp":
                        x_axis.append(i.timestamp)
                    elif arguments["x_axis"] == "variables_timestamp":
                        x_axis.append(int(i.timestamp.hour))
                        z_axis.append(response.find_variables_length(expression=variables_length_expression))
                    else:
                        raise Exception("Unknown value for x-axis")
            if arguments["x_axis"] != "variables_timestamp":                
                scatter(
                    x=x_axis,
                    y=response_time,
                    label=(clientName if not arguments["legends"] else arguments["legends"][index]),
                    xlabel="variables length",
                    ylabel="Response time (MS)"
                )
            else:
                x.append(x_axis)
                y.append(response_time)
                z.append(z_axis)
                point_symbol.append(symbols[client_index])
                
    # scatter_3d
    if len(z):
        axes = plt.subplot(111, projection='3d')
        for (x, y, z, symbol, clientName) in zip(x, y, z, point_symbol, arguments["clientName"]):
            scatter_3d(
                axes,
                x, 
                y,
                z,
                label=clientName,
                symbol=symbol,
            )
        plt.xlabel("Hour")
        plt.ylabel("Response time (ms)")
        axes.set_zlabel("Variables size")

    plt.title(arguments["title"])
    plt.legend(loc="upper left")
    if arguments["output"]:
        move_legends()
        plt.savefig(arguments["output"])
    else:
        plt.show()
