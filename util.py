import datetime
from dateutil import parser as dateparser
from Plot import gaussian, histogram
import matplotlib.pyplot as plt
import json
from datetime import timezone

def parse_date(date):
    now = datetime.datetime.now()
    if date == "now":
        return now.replace(tzinfo=timezone.utc).astimezone(tz=None)
    parsed = dateparser.parse(date)
    parsed = parsed.replace(tzinfo=None)
    if (now - parsed).total_seconds() < 0:
        return now.replace(tzinfo=timezone.utc).astimezone(tz=None)
    return parsed.replace(tzinfo=timezone.utc).astimezone(tz=None)

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

def is_timestamp_within_ranges(
        from_to,
        ranges
): 
    for i in ranges:
        from_range, to_range = i

        from_, to_ = from_to

        from_range: datetime.datetime = from_range
        to_range: datetime.datetime = to_range

        if (from_range - from_).total_seconds() < 0 and (from_ - to_range).total_seconds() < 0:
            return True
    return False

def read_timestamp_file(path):
    timestamps = []
    with open(path, "r") as file:
        data = json.loads(file.read())
        for i in data:
            timestamps.append((
                parse_date(i["from"]),
                parse_date(i["to"])
            ))
    return timestamps

def get_label(arguments, index, default):
    if arguments["legends"]:
        return arguments["legends"][index]
    elif arguments["alias"]:
        return arguments["alias"][index]
    return default
