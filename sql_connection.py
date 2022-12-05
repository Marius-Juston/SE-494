import json
import logging
from datetime import datetime

import pyodbc

from configuration import Config


class SQLConnection:
    def __init__(self, config: Config):
        self.config = config

        server_name = config.SQL_SERVER_NAME
        """
        @param config:  Retrieved using SELECT @@SERVERNAME query
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

    def query(self, query):
        logging.debug("Executing query: " + query)
        self.cursor.execute(query)
        logging.debug("Completed query")

    def get_filament_specs(self, order_number):
        if isinstance(order_number, int):
            order_number = "{:>8}".format(order_number)

        logging.info(f"Getting filament specs for order number: '{order_number}'")

        query = f"""SELECT a.ord_no, a.item_no, a.item_desc_1, a.item_desc_2, b.diameter, b.amp, b.freq, c.prod_cat 
                        FROM [70_UI].dbo.sfordfil_sql a left outer join [CFF_UI].dbo.fiber_specs b ON a.item_no = b.item_no 
                            inner join [70_UI].dbo.imitmidx_sql c on a.item_no = c.item_no
                            where a.ord_no = {order_number}"""

        self.query(query)

        return self.cursor.fetchone()

    def collect_sample_number(self, order_number: int, database: str):
        query = f"""SELECT TOP 1 [Sample Number] FROM [QA_UI].[dbo].[{database}]  
        where [Shop Floor Order Number]={order_number} order by  [Sample Number] desc"""

        self.query(query)

        return self.cursor.fetchone()

    def get_key(self, database):
        query = f'SELECT TOP 1 * FROM [QA_UI].[dbo].[{database}] order by [key] desc'

        self.query(query)

        return self.cursor.fetchone()

    def insert_to_table(self, database: str, values, max_samples_num):
        logging.debug(f"Inserting to table {database}: {values}")

        total_samples = [f"Sample{i + 1}" for i in range(max_samples_num)]

        fields = [
            "key",
            "Shop Floor Order Number",
            "Line Number",
            "Item Number",
            "Material",
            "Nominal",
            "USL",
            "LSL",
            "Date",
            "Operator",
            "AVG",
            "Sample range",
            "Sample Upper",
            "Sample Lower",
            "Sample Number"
        ]
        fields.extend(total_samples)

        fields = [f"[{i}]" for i in fields]

        out_values = [
            values['data']['key'],
            values["Shop Floor Order Number"],
            values["Line Number"],
            values["Item Number"],
            values['Material'],
            values["Nominal"],
            values["USL"],
            values["LSL"],
            values["Date"],
            values["Operator"],
            values['data']["avg"],
            values['data']['range'],
            values['data']['max'],
            values['data']['min'],
            values['data']['samp_num'],
        ]
        out_values.extend(values['data']['samp'])
        out_values.extend([0.0 for _ in range(max_samples_num - len(values['data']['samp']))])

        out_values = [f"'{d}'" if isinstance(d, str) else str(d) for d in out_values]

        query = f'INSERT INTO [QA_UI].[dbo].[{database}] ({",".join(fields)}) VALUES ({",".join(out_values)})'

        self.query(query)
        self.cursor.commit()

    def collect_previous_data(self, order_number):

        if isinstance(order_number, str):
            order_number = int(order_number)

        output = {}

        for d in ["Diameter", "Aplitude", "Frequency"]:

            if d == "Aplitude":
                nom = 'b.amp'
            elif d == "Frequency":
                nom = 'b.freq'
            else:
                nom = "b.diameter"

            query = f"""
            SELECT TOP 100 d.Date, d.[Sample Number], {nom}, d.AVG, d.USL, d.LSL
                    FROM [70_UI].dbo.sfordfil_sql a left outer join [CFF_UI].dbo.fiber_specs b ON a.item_no = b.item_no 
                        inner join [70_UI].dbo.imitmidx_sql c on a.item_no = c.item_no
                        left join [QA_UI].dbo.{d} d on d.[Shop Floor Order Number] = a.ord_no
                        where a.ord_no = {order_number}            
                        order by d.Date desc, d.[Sample Number] desc"""

            self.query(query)

            outs = self.cursor.fetchall()

            if outs is not None and len(outs) > 0:

                nom = float(outs[0][2])
                uls = float(outs[0][4])
                lls = float(outs[0][5])

                x = []
                y = []

                for out in outs:
                    date: datetime = out[0]
                    x.append(date.isoformat())
                    y.append(float(out[3]))

                data = {
                    "ULS": uls,
                    "LSL": lls,
                    "NOM": nom,
                    "dates": x,
                    "avgs": y
                }

                output[d] = data

                logging.debug("Saving to database output " + str(data))

        return output

    def insert_data(self, order_number: int, line_number: int, operator: str, diameters: list[float],
                    amplitudes: list[float], frequencies: list[float]):
        orders = self.get_filament_specs(order_number)

        order_number_s, item_number, material_p1, material_p2, nominal_d, nominal_a, nominal_f, prod_cat = orders
        nominal_d = float(nominal_d)
        nominal_f = float(nominal_f)
        nominal_a = float(nominal_a)

        material = material_p1 + material_p2

        date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

        product_cat_tolerances = self.config.PRODUCT_TOL
        tol_percent = product_cat_tolerances['default']

        if prod_cat in product_cat_tolerances:
            tol_percent = product_cat_tolerances[prod_cat]

        outputs = {
        }

        names = ["Diameter", "Aplitude", "Frequency"]
        datas = [diameters, amplitudes, frequencies]
        noms = [nominal_d, nominal_a, nominal_f]

        for name, data, nom in zip(names, datas, noms):
            if data is not None and len(data) > 0:
                outputs[name] = {}

                key = int(self.get_key(name)[0])

                outputs[name]["Shop Floor Order Number"] = order_number_s
                outputs[name]['Operator'] = operator
                outputs[name]['Line Number'] = line_number
                outputs[name]["Material"] = material
                outputs[name]["Item Number"] = item_number
                outputs[name]["Date"] = date

                outputs[name]['Nominal'] = nom
                nom = outputs[name]['Nominal']

                outputs[name]['USL'] = nom * (1 + tol_percent)
                outputs[name]['LSL'] = nom * (1 - tol_percent)

                max_data = 10
                if name == "Diameter":
                    max_data = 20

                counter = self.collect_sample_number(order_number, name)
                if counter is not None:
                    counter = int(counter[0])
                else:
                    counter = 0

                for i in range(0, len(data), max_data):
                    data_cut = data[i:i + max_data]

                    max_data_v = max(data_cut)
                    min_data = min(data_cut)
                    average_data = sum(data_cut) / len(data_cut)

                    counter += 1
                    key += 1

                    outputs[name]["data"] = {
                        'min': min_data,
                        'max': max_data_v,
                        'avg': average_data,
                        'samp': data_cut,
                        'samp_num': counter,
                        'range': max_data_v - min_data,
                        'key': key
                    }

                    self.insert_to_table(name, outputs[name], max_data)


if __name__ == '__main__':
    config = Config()

    sql = SQLConnection(config)
    sql.insert_data(282618, 1, "John", [i for i in range(22)], [i for i in range(22)], [i for i in range(22)])

    data = sql.collect_previous_data(282353)

    with open("example_data.json", "w") as f:
        json.dump(data, f)
