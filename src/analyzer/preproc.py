import glob
import codecs
import csv
from os.path import realpath, dirname, join, split
from datetime import date

import pandas as pd

DATA_DIR = join(dirname(realpath(__file__)), '..', '..', 'data')


def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {unicode(key, 'utf-8'): unicode(value, 'utf-8') for key, value in row.iteritems()}


def read_data_batch():
    try:
        for filepath in glob.glob(join(DATA_DIR, '*.txt')):
            with codecs.open(filepath, 'r', encoding='utf-8') as f:
                first_line = f.readline()
                keys = first_line.strip().split('\t')
                break
    except NameError:
        print("No data found. Run scrape.sh first.")
        return []

    all_data = {k: [] for k in keys}
    all_data['id'] = []
    for filepath in glob.glob(join(DATA_DIR, '*.txt')):
        month = split(filepath)[-1].split('.')[0]
        with open(filepath, 'r') as f:
            for idx, row in enumerate(UnicodeDictReader(f, delimiter='\t')):
                for k in keys:
                    all_data[k].append(row[k])
                all_data['id'].append('{}-{}'.format(month, idx))

    print("Total # of records: ", len(all_data[keys[0]]))
    df = pd.DataFrame.from_dict(all_data)
    return df


def preproc_data(df):
    df.waiting_days = df.waiting_days.astype(int)
    df.waiting_days = df.waiting_days.clip(upper=500, lower=0)
    df.check_date = pd.to_datetime(df.check_date)
    df.complete_date[df.complete_date == '0000-00-00'] = str(date.today())
    df.complete_date = pd.to_datetime(df.complete_date)


def main():
    data = read_data_batch()
    df = pd.DataFrame.from_dict(data)
    preproc_data(df)
    df.to_csv(join(DATA_DIR, 'proced.csv'), encoding='utf-8')
    print("Saved.")


if __name__ == '__main__':
    main()
