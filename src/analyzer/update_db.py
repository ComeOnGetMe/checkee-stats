import sqlite3
import glob
import codecs
from os.path import realpath, dirname, join

DATA_DIR = join(dirname(realpath(__file__)), '..', '..', 'data')
TABLE_NAME = 'CHECKEE'


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


def check_table_exists(cur, name):
    cur.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table' AND name='{}';
    """.format(name.replace('\'', '\'\'')))
    if cur.fetchone() is not None:
        return True
    return False


if __name__ == '__main__':
    db_file = join(DATA_DIR, 'checkee.db')
    conn = sqlite3.connect(db_file)

    for filepath in glob.glob(join(DATA_DIR, '*.txt')):
        with codecs.open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            keys = first_line.strip().split('\001')
            break
    try:
        print(keys)
    except NameError:
        print("No data found. Run scrape.sh first.")

    cur = conn.cursor()
    if not check_table_exists(cur, TABLE_NAME):
        cur.execute("CREATE TABLE {} ({});".format(TABLE_NAME, ','.join(keys)))

    n_records = 0
    for filepath in glob.glob(join(DATA_DIR, '*.txt')):
        with codecs.open(filepath, 'r', encoding='utf-8') as f:
            f.readline()
            to_db = [tuple(line.strip().split('\001')) for line in f.readlines()]
        cur.executemany("""
        INSERT INTO {} ({}) VALUES ({});
        """.format(TABLE_NAME, ','.join(keys), ','.join(['?'] * len(keys))), to_db)
        n_records += len(to_db)

    conn.commit()
    conn.close()
