from __future__ import print_function

import sqlite3
import os
from update_db import DATA_DIR


class Server(object):
    def __init__(self):
        self.db_file = os.path.join(DATA_DIR, 'checkee.db')
        self.conn = sqlite3.connect(self.db_file)
