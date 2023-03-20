import argparse
import datetime
from dateutil import parser as dateparser
from ApolloStudio import ApolloStudio
from Plot import gaussian
import matplotlib.pyplot as plt

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--from', type=lambda d: dateparser.parse(d), help='From date')
    parser.add_argument('-t', '--to', type=lambda d: dateparser.parse(d), default=datetime.date.today(), help='To date')
    parser.add_argument('-q', '--queryId', type=str, help='Query id')
    parser.add_argument('-g', '--graph', type=str, help='graph id')
    parser.add_argument('-c', '--clientName', type=str, action='append', help='Client name')
    parser.add_argument('-n', '--title', type=str, required=True, help="Title of the plot")
    parser.add_argument('-p', '--plot_type', type=str, required=True, help="Type of plot (gaussian)")
    parser.add_argument('-m', '--max_response_time', type=int, default=float('inf'), help="Filter out outliers")
    parser.add_argument('-o', '--output', type=str, required=True, help="Save file as")

    arguments = vars(parser.parse_args())

    from_date:datetime.date = arguments["from"]
    to_date:datetime.date = arguments["to"]

    from_timestamp_offset = -int((datetime.datetime.now() - from_date).total_seconds())
    to_timestamp_offset = -int((datetime.datetime.now() - to_date).total_seconds())
    
    for clientName in arguments["clientName"]:
        results = ApolloStudio().request(
            graph=arguments["graph"],
            queryId=arguments["queryId"],
            clientName=clientName,
            from_timestamp=from_timestamp_offset,
            to_timestamp=to_timestamp_offset
        )
        buckets = list(map(lambda x: x.buckets_speeds, results))
        buckets = list(filter(lambda x: len(x) > 0, buckets))
        buckets = sum(buckets, [])  
        buckets = list(filter(lambda x: x < arguments["max_response_time"], buckets))
        
        print(len(buckets), buckets, clientName)
        gaussian(
            buckets,
            label=clientName
        )

    plt.title(arguments["title"])
    plt.legend(loc="upper left")
    if arguments["output"]:
        plt.savefig(arguments["output"])
    else:
        plt.show()
