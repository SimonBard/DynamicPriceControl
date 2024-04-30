
import psycopg2
from lib.config import config


class Manager:
    def __init__(self):
        
        self.topic = ""
        self.message = ""

    def drop_tables(self):
        """drop tables in the PostgreSQL database"""
        drop_commands = (
            """
            DROP TABLE IF EXISTS COP CASCADE
            """,
            """
            DROP TABLE IF EXISTS demand CASCADE
            """,
            """
            DROP TABLE IF EXISTS hourly_data CASCADE
            """,
            """
            DROP TABLE IF EXISTS counter CASCADE
            """,
        )
        conn = None
        try:
            # read the connection parameters
            params = config()
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            # create table one by one
            for command in drop_commands:
                cur.execute(command)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def create_tables(self):
        """create tables in the PostgreSQL database"""
        commands = (
            """ 
            CREATE TABLE demand (
                date DATE,
                PRIMARY KEY (date),
                demand_forecast REAL,
                forecast_solar REAL,
                total_home_consumption REAL,
                home_consumption REAL,
                forecast_solar REAL,
                pv_totalyield REAL,
                pv_production REAL,
                totalactogrid REAL,
                ac2grid REAL,
                solcast REAL,
                temperature_avg REAL

            )
            
            """,
            """ 
            CREATE TABLE counter (
                pv_overshoot_duration INTEGER,
                useless INTEGER
                
            )
            
            """,
            """
            CREATE TABLE hourly_data (
                    date DATE,
                    hour INTEGER,
                    PRIMARY KEY (date, hour),
                    t_forecast REAL,
                    cop_specific REAL,
                    forecast_solar REAL,
                    tibber_netto REAL,
                    tibber_brutto REAL,
                    mixedprice REAL,
                    heatprice_perkwh REAL,
                    statehp_recommendation BOOLEAN,
                    load_battery BOOLEAN
            )
            """,
        )
        conn = None
        try:
            # read the connection parameters
            params = config()
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            # create table one by one
            for command in commands:
                cur.execute(command)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def write_element_to_hourly_values(self, date: str, hour: int, column: str, data):
        sql = (
            """INSERT INTO hourly_data(date, hour, """
            + column
            + """)
                    VALUES(%s, %s, %s) 
                ON CONFLICT (date, hour) DO UPDATE SET """
            + column
            + """ =  EXCLUDED."""
            + column
            + """;"""
        )
        print("write value: ", data, " to column ", column, "in line ", date, " ", hour)

        conn = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            # print('connected to db')
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (date, hour, data))
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("db error: ")
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def write_demand(self, date, column, value):
        sql = (
            """INSERT INTO demand(date, """
            + column
            + """)
                    VALUES(%s, %s) 
                ON CONFLICT (date) DO UPDATE SET """
            + column
            + """ =  EXCLUDED."""
            + column
            + """;"""
        )

        conn = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            # print('connected to db')
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (date, value))
            print(
                "write to table demand in column",
                column,
                "value: ",
                value,
                " for date: ",
                date,
            )
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("db error: ")
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def write_counter(self, value: int):
        sql = """ UPDATE counter SET pv_overshoot_duration='""" + str(value) + """';"""
        conn = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            # print('connected to db')
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (value))
            # print('values written to db')
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print("db error: ")
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def getcounter(self) -> int:
        postgreSQL_select_Query = """SELECT pv_overshoot_duration FROM counter ;"""
        # print(postgreSQL_select_Query)
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            connection = psycopg2.connect(**params)
            # create a new cursor
            cursor = connection.cursor()
            cursor.execute(postgreSQL_select_Query)
            mobile_records = cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()
                return mobile_records[0][0]
                # print("PostgreSQL connection is closed")

    def retrieve_dict_from_hourly_values(self, date: str) -> list:
        # returns a list of dict from database hourly_data for the specific date (so hour = 0..23).
        # keys are the column names of the table.
        """
        Run generic select query on db, returns a list of dictionaries
        """

        # Open a cursor to perform database operations
        query = """SELECT * FROM hourly_data WHERE date='""" + date + """';"""
        data = []
        # execute the query
        try:
            params = config()
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()
            if len(data):
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            columns = list(cursor.description)
            result = cursor.fetchall()

        except (Exception, psycopg2.DatabaseError) as e:
            cursor.close()
            print(e)
            exit(1)

        cursor.close()
        connection.close()
        # make dict
        results = []
        for row in result:
            row_dict = {}
            for i, col in enumerate(columns):
                row_dict[col.name] = row[i]
            results.append(row_dict)

        sorted_list = sorted(results, key=lambda d: d["hour"])
        return sorted_list

    def demand_retrieve_list(self) -> list:
        # Open a cursor to perform database operations
        query = """SELECT * FROM demand;"""
        data = []
        # execute the query
        try:
            params = config()
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()
            if len(data):
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            columns = list(cursor.description)
            result = cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as e:
            cursor.close()
            print(e)
            exit(1)
        cursor.close()
        connection.close()
        # make dict
        results = []
        for row in result:
            row_dict = {}
            for i, col in enumerate(columns):
                row_dict[col.name] = row[i]
            results.append(row_dict)

        sorted_list = sorted(results, key=lambda d: d["date"])
        return sorted_list

    def demand_retrieve_dict(self, date) -> dict:
        # Open a cursor to perform database operations
        query = """SELECT * FROM demand WHERE date='""" + date + """';"""
        data = []
        # execute the query
        try:
            params = config()
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()
            if len(data):
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            columns = list(cursor.description)
            row = cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as e:
            cursor.close()
            print(e)
            exit(1)
        cursor.close()
        connection.close()
        # make dict
        row_dict = {}
        for i, col in enumerate(columns):
            # print (i, col, row[0][i])
            row_dict[col.name] = row[0][i]

        return row_dict


def main():
    # inst = Manager()
    # row_list = inst.retrieve_dict('2024-01-29')

    # for n in range(0, len(row_list)):
    #   print (n, row_list[n]['hour'], row_list[n]['tibber_brutto'])

    inst = Manager()
    inst.write_counter(3)
    # demand = inst.demand_retrieve_dict()
    # for n in range(0, len(demand)-1):
    #     try:
    #         homeconsumption = demand[n]['total_home_consumption'] - demand[n-1]['total_home_consumption']
    #         #print (demand[n]['date'], demand[n]['total_home_consumption'], homeconsumption)
    #         print('write consumption for date' , demand[n]['date'], demand[n]['total_home_consumption'], homeconsumption)
    #         inst.write_demand(demand[n]['date'], 'home_consumption', homeconsumption)
    #         print('write production for date' , demand[n]['date'])
    #         pv_production = demand[n]['pv_totalyield'] - demand[n-1]['pv_totalyield']
    #         inst.write_demand(demand[n]['date'], 'pv_production', pv_production)
    #     except Exception as e:
    #         print(e)


if __name__ == "__main__":
    main()
