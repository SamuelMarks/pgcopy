from datetime import datetime, date, time, timedelta
from random import randint
import hashlib

import psycopg2.sql

from pgcopy import util


genbool = lambda i: 0 == (i % 3)
genint = lambda i: i
genfloat = lambda i: 1.125 * i
gendate = lambda i: date(1708, 1, 1) + timedelta(i % (250 * 365))
gentime = lambda i: time(randint(0, 23), randint(0, 59), randint(0, 59), randint(0, 999999))
gendatetime = lambda i: datetime(1970, 1, 1) + timedelta(hours=i)
gendatetimetz = lambda i: util.to_utc(datetime(1970, 1, 1) + timedelta(hours=i))
genstr12 = lambda i: hashlib.md5(str(i).encode()).hexdigest()[:12 - (i % 3)].encode()

datagen = {
        'bool': genbool,
        'smallint': genint,
        'integer': genint,
        'bigint': genint,
        'real': genfloat,
        'double precision': genfloat,
        'date': gendate,
        'time': gentime,
        'timestamp': gendatetime,
        'timestamp with time zone': gendatetimetz,
        'varchar(12)': genstr12,
        'char(12)': genstr12,
    }

colname = lambda i: chr(ord('a') + i)


class TemporaryTable(object):
    tempschema = True
    null = 'NOT NULL'
    data = None
    record_count = 0

    def setup_method(self):
        self.table = self.__class__.__name__.lower()
        self.cols = [colname(i) for i in range(len(self.datatypes))]

    def create_sql(self, tempschema=None):
        colsql = ((c, t, self.null) for c, t in zip(self.cols, self.datatypes))
        collist = psycopg2.sql.Composed(', '.join(map(' '.join, colsql)))
        return psycopg2.sql.SQL(
            "CREATE TEMPORARY TABLE {} ({})" if tempschema else "CREATE TABLE public.{} ({})"
        ).format(psycopg2.sql.Identifier(self.table), collist)

    def generate_data(self, count):
        gen = [datagen[t] for t in self.datatypes]
        return [tuple(g(i) for g in gen) for i in range(count)]
