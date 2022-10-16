import logging

import pyodbc

from configuration import Config


class SQLConnection:
    def __init__(self, server_name: str):
        """
        @param server_name:  Retrieved using SELECT @@SERVERNAME query
        """
        driver_name = 'SQL Server Native Client 11.0'

        logging.debug("Available drivers: " + str(pyodbc.drivers()))

        connection_str = (f"Driver={driver_name};"
                          f"Server={server_name};"
                          "Trusted_Connection=yes;")
        logging.info("Connection to SQL server using connection interface: " + str(connection_str))

        connection: pyodbc.Connection = pyodbc.connect(connection_str)

        logging.info("Successfully connected to database")

        self.cursor: pyodbc.Cursor = connection.cursor()

        self.get_filament_specs(0)

    def get_filament_specs(self, order_number):
        if isinstance(order_number, int):
            order_number = "{:>8}".format(order_number)

        logging.info(f"Getting filament specs for order number: '{order_number}'")

        query = f"""SELECT a.ord_no, a.item_desc_1, a.item_desc_2, b.diameter, b.amp, b.freq, c.prod_cat 
                        FROM [70_UI].dbo.sfordfil_sql a left outer join [CFF_UI].dbo.fiber_specs b ON a.item_no = b.item_no 
                            inner join [70_UI].dbo.imitmidx_sql c on a.item_no = c.item_no
                            where a.ord_no = {order_number}"""

        logging.debug("Executing query: " + query)
        self.cursor.execute(query)
        logging.debug("Completed query")

        print(self.cursor.fetchall())


if __name__ == '__main__':
    config = Config()

    sql = SQLConnection(config.SQL_SERVER_NAME)
