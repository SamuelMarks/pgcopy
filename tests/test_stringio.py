from io import BytesIO
from pgcopy import CopyManager, util
from .test_datatypes import TypeMixin

class Test(TypeMixin):
    datatypes = ['integer', 'bool', 'varchar(12)']

    def test_copy(self, conn, cursor, schema_table, data):
        bincopy = CopyManager(conn, schema_table, self.cols)
        bincopy.copy(data, BytesIO)
        select_list = ','.join(self.cols)
        cursor.execute("SELECT {} from {}".format(select_list, schema_table))
        self.checkResults(cursor, data)

    def cast(self, v):
        try:
            return v.encode()
        except AttributeError:
            return v
