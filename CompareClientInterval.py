import argparse
import datetime
from dateutil import parser as dateparser
from ApolloStudio import ApolloStudio
import matplotlib.pyplot as plt
from util import flat_buckets, plot

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--from', nargs='+', type=dateparser.parse, help='From date')
    parser.add_argument('-t', '--to', nargs='+', type=dateparser.parse, default=datetime.date.today(), help='To date')
    parser.add_argument('-g', '--graph', type=str, required=True, help='graph id')
    parser.add_argument('-q', '--queryId', type=str, required=True, help='Query id')
    parser.add_argument('-c', '--clientName', type=str, required=True, help='Client name')
    parser.add_argument('-n', '--title', type=str, required=True, help="Title of the plot")
    parser.add_argument('-l', '--legends', nargs='+', type=str, required=True, help="Title of the legends")
    parser.add_argument('-p', '--plot_type', type=str, required=True, help="Type of plot (gaussian)")
    parser.add_argument('-m', '--max_response_time', type=int, default=float('inf'), help="Filter out outliers")
    parser.add_argument('-o', '--output', type=str, required=True, help="Save file as")

    arguments = vars(parser.parse_args())
    print(arguments)

    assert len(arguments["from"]) == len(arguments["to"])
    if arguments["legends"]:
        assert len(arguments["from"]) == len(arguments["legends"])

    for index, (from_date, to_date) in enumerate(zip(arguments["from"], arguments["to"])):
        from_timestamp_offset = -int((datetime.datetime.now() - from_date).total_seconds())
        to_timestamp_offset = -int((datetime.datetime.now() - to_date).total_seconds())
                
        clientName = arguments["clientName"]
        results = ApolloStudio().get_query_stats(
            graph=arguments["graph"],
            queryId=arguments["queryId"],
            clientName=clientName,
            from_timestamp=from_timestamp_offset,
            to_timestamp=to_timestamp_offset
        )
        buckets = flat_buckets(
            results,
            arguments["max_response_time"]
        )
        print(len(buckets), arguments["plot_type"])
        plot(
            plot_type=arguments["plot_type"],
            data=buckets,
            label=(f"{from_date.strftime('%Y-%m-%d')} -> {to_date.strftime('%Y-%m-%d')}" if not arguments["legends"] else arguments["legends"][index])
        )
    plt.title(arguments["title"])
    plt.legend(loc="upper left")
    if arguments["output"]:
        plt.savefig(arguments["output"])
    else:
        plt.show()
