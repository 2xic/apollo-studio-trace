import datetime
from dateutil import parser as dateparser
from Plot import gaussian, histogram
import matplotlib.pyplot as plt

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

def move_legends():
    ax = plt.gca()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.95])

    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
            fancybox=True, shadow=True, ncol=5)
   # plt.tight_layout()
