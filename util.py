import datetime
from dateutil import parser as dateparser
from Plot import gaussian, histogram

def parse_date(date):
    if date == "now":
        return datetime.datetime.now()
    return dateparser.parse(date)

def flat_buckets(results, max_response_time):
    buckets = list(map(lambda x: x.buckets_speeds, results))
    buckets = list(filter(lambda x: len(x) > 0, buckets))
    buckets = sum(buckets, [])  
    buckets = list(filter(lambda x: x < max_response_time, buckets))
    return buckets

def plot(plot_type, data, label):
    if plot_type == "gaussian":
        gaussian(
            data,
            label=label
        )
    else:
        print("histogram")
        histogram(
            data,
            label=label
        )