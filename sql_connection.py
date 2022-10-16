import pyodbc


class SQLConnection:
    def __init__(self, server_name):
        DRIVER_NAME = 'SQL Server Native Client 11.0'

        print(pyodbc.drivers())
        cnxn_str = (f"Driver={DRIVER_NAME};"
                    f"Server={server_name};"
                    "Trusted_Connection=yes;")
        cnxn: pyodbc.Connection = pyodbc.connect(cnxn_str)

        self.cursor: pyodbc.Cursor = cnxn.cursor()

    def get_filament_specs(self, order_number):
        if isinstance(order_number, int):
            order_number = "{:>8}".format(order_number)

        query = f"""SELECT a.ord_no, a.item_desc_1, a.item_desc_2, b.diameter, b.amp, b.freq, c.prod_cat 
                        FROM [70_UI].dbo.sfordfil_sql a left outer join [CFF_UI].dbo.fiber_specs b ON a.item_no = b.item_no 
                            inner join [70_UI].dbo.imitmidx_sql c on a.item_no = c.item_no
                            where a.ord_no = {order_number}"""

        self.cursor.execute(query)

        print(self.cursor.fetchall())


if __name__ == '__main__':
    SERVER_NAME = 'MARIUS-LAPTOP\SQLEXPRESS'  # Retrieved using SELECT @@SERVERNAME query

    sql = SQLConnection(SERVER_NAME)
