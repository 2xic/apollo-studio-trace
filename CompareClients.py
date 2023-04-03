import argparse
import datetime
from ApolloStudio import ApolloStudio
import matplotlib.pyplot as plt
from util import parse_date, flat_buckets, plot, move_legends

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--from', type=parse_date, help='From date')
    parser.add_argument('-t', '--to', type=parse_date, default=datetime.date.today(), help='To date')
    parser.add_argument('-q', '--queryId', type=str, help='Query id')
    parser.add_argument('-g', '--graph', type=str, help='graph id')
    parser.add_argument('-c', '--clientName', type=str, action='append', help='Client name')
    parser.add_argument('-n', '--title', type=str, required=True, help="Title of the plot")
    parser.add_argument('-p', '--plot_type', type=str, default="gaussian", help="Type of plot (gaussian)")
    parser.add_argument('-m', '--max_response_time', type=int, default=float('inf'), help="Filter out outliers")
    parser.add_argument('-o', '--output', type=str, required=True, help="Save file as")

    arguments = vars(parser.parse_args())

    from_date:datetime.date = arguments["from"]
    to_date:datetime.date = arguments["to"]

    from_timestamp_offset = -int((parse_date('now') - from_date).total_seconds())
    to_timestamp_offset = -int((parse_date('now') - to_date).total_seconds())

    for clientName in arguments["clientName"]:
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
            label=clientName
        )

    plt.title(arguments["title"])
    plt.legend(loc="upper left")
    if arguments["output"]:
        move_legends()
        plt.savefig(arguments["output"])
    else:
        plt.show()
