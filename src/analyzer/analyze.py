import os
import glob
import csv

import numpy as np
import matplotlib.pyplot as plt
from itertools import tee


def parse_data(folder):
    data = []
    for filename in glob.glob(os.path.join(folder, '*.txt')):
        with open(filename, 'r') as infile:
            reader = csv.DictReader(infile)
            data.extend(list(reader))
    return data


def filter_data(data, visa_type=None, location=None, status=None, new_renewal=None, major=[], since=None, fields=[]):
    status_filter = lambda x: x["status"].lower() == status if status else True
    loc_filter = lambda x: x["loc"].lower() == location if location else True
    visa_filter = lambda x: x["visa"].lower() == visa_type if visa_type else True
    type_filter = lambda x: x["type"].lower() == new_renewal if new_renewal else True
    major_filter = lambda x: x["major"].lower() in major if major else True
    since_filter = lambda x: x["check_date"] > since if since else True

    filter_func = lambda x: status_filter(x) and loc_filter(x) and visa_filter(x) and type_filter(x) and major_filter(
        x) and since_filter(x)
    it = filter(filter_func, data)
    filter_it, debug_it = tee(it)
    res = [field[0](x[field[1]]) for field in fields for x in filter_it]
    return res


if __name__ == "__main__":
    data = parse_data('../retriever/data/')

    visa_type = 'h1'
    location = 'beijing'
    status = 'clear'
    new_renewal = 'new'
    since = '2018-10-01'

    filtered = filter_data(data,
                           visa_type=visa_type,
                           location=location,
                           status=status,
                           new_renewal=new_renewal,
                           since=since,
                           fields=[(lambda x: int(x), 'waiting_days')])

    if len(filtered) == 0:
        print('Nothing filtered')
        exit(0)

    print('Total ' + str(len(filtered)) + ' samples filtered')
    print('Average waiting days: ' + str(sum(filtered) / float(len(filtered))))

    step = 2
    bins = np.arange(0, max(filtered) + step, step=step)
    plt.hist(filtered, bins=bins)
    title = "Histogram for " + visa_type + " visa at " + location + " consulate " + status + " since " + since
    plt.title(title)
    plt.xlabel("number of days in waiting")
    plt.ylabel("number of applications")
    plt.xticks(bins)

    print(title)
    plt.show()
