import lib.mymqtt
import sys
import psycopg2
from lib.config import config
import lib.awattar
import lib.weather
import lib.mytibber
import asyncio
#import lib.my_forecast_solar
from forecast_solar import ForecastSolar
from datetime import datetime, timedelta
import lib.heatpump
import os
from dotenv import load_dotenv

class Manager:

    def __init__(self):
        self.topic = ""
        self.message = ""

    def drop_tables():
        """ drop tables in the PostgreSQL database"""
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
            """
            
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

    def create_tables():
        
        """ create tables in the PostgreSQL database"""
        commands = (
            """
            CREATE TABLE cop (
                t_inside INTEGER,
                t_outside INTEGER,
                efficiency REAL
            )
            """,
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
            """)
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

    
    def insert_cop(t_inside, t_outside, efficiency):
        """ insert new cop data into the cop table """
        sql = """INSERT INTO cop(t_inside, t_outside, cop_specific)
                VALUES(%s,%s,%s);"""
        conn = None
        cop = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (t_inside, t_outside, efficiency))
            
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


    def write_awattar_data(self, data):
        data_awattar = data    

        for element in data_awattar:
            date = element.date
            hour = element.hour
            price_netto = element.price_ct_per_kwh
            price_brutto = element.brutto_price_ct_per_kwh
            
        
            sql = """INSERT INTO hourly_data(date, hour,  
                        price_netto,
                        price_brutto
                        )
                        VALUES(%s,%s,%s,%s) 

                    ON CONFLICT (date, hour)
                    DO 
                    UPDATE SET 
                        price_netto = EXCLUDED.price_netto,
                        price_brutto = EXCLUDED.price_brutto
                        
                    ;"""
            conn = None
            try:
                # read database configuration
                params = config()
                # connect to the PostgreSQL database
                conn = psycopg2.connect(**params)
                # create a new cursor
                #print('connected to db')
                cur = conn.cursor()
                # execute the INSERT statement
                cur.execute(sql, (date, hour, 
                    price_netto,
                    price_brutto,
                    ))
                print('values written to db', date, hour, 
                    price_netto,
                    price_brutto)
                # commit the changes to the database
                conn.commit()
                # close communication with the database
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print('db error: ')
                print(error)
            finally:
                if conn is not None:
                    conn.close()
            
    def write_temperature_data(self, data):
        temperature_data = data
        #print(temperature_data)

        
        for element in temperature_data:
            #print(element)
            date = element.date
            hour = element.hour
            t_forecast = element.temperature

            MyHeatpump = lib.heatpump.Heatpump()
            cop_specific = MyHeatpump.calculateCOP(t_forecast)   
            print('t_forecast', t_forecast, 'cop_specific', cop_specific) 

            sql = """INSERT INTO hourly_data(date, hour, t_forecast, cop_specific )
                    VALUES(%s,%s,%s,%s) 

                ON CONFLICT (date, hour)
                DO 
                UPDATE SET 
                    t_forecast = EXCLUDED.t_forecast,
                    cop_specific = EXCLUDED.cop_specific
                    
                ;"""
            conn = None
            try:
                # read database configuration
                params = config()
                # connect to the PostgreSQL database
                conn = psycopg2.connect(**params)
                # create a new cursor
                #print('connected to db')
                cur = conn.cursor()
                # execute the INSERT statement
                cur.execute(sql, (date, hour, t_forecast, cop_specific))
                print('Temperature and COP written to DB', date, hour, t_forecast, cop_specific)
                # commit the changes to the database
                conn.commit()
                # close communication with the database
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print('db error: ')
                print(error)
            finally:
                if conn is not None:
                    conn.close()

    def write_heatprice(self, date, hour, mixedprice):

            heatprice_perkwh = mixedprice
            sql = """INSERT INTO hourly_data(date, hour, heatprice_perkwh )
                    VALUES(%s,%s,%s) 

                ON CONFLICT (date, hour)
                DO 
                UPDATE SET 

                    heatprice_perkwh = EXCLUDED.heatprice_perkwh
                ;"""
            conn = None
            try:
                # read database configuration
                params = config()
                # connect to the PostgreSQL database
                conn = psycopg2.connect(**params)
                # create a new cursor
                #print('connected to db')
                cur = conn.cursor()
                # execute the INSERT statement
                cur.execute(sql, (date, hour, heatprice_perkwh))
                print('to db: date hour heatprice', date, hour, heatprice_perkwh)
                # commit the changes to the database
                conn.commit()
                # close communication with the database
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print('db error: ')
                print(error)
            finally:
                if conn is not None:
                    conn.close()

    def write_tibber_data(self,home):
        

        for key in home._price_info:
            #print(key , home._price_info[key])        

            #print(key[11:12])
            date = key[0:10]
            hour = key[11:13]
            tibber_netto = 0
            tibber_brutto = home._price_info[key]
            
        
            sql = """INSERT INTO hourly_data(date, hour,  
                        tibber_netto,
                        tibber_brutto
                        )
                        VALUES(%s,%s,%s,%s) 

                    ON CONFLICT (date, hour)
                    DO 
                    UPDATE SET 
                        tibber_netto = EXCLUDED.tibber_netto,
                        tibber_brutto = EXCLUDED.tibber_brutto
                        
                    ;"""
            conn = None
            try:
                # read database configuration
                params = config()
                # connect to the PostgreSQL database
                conn = psycopg2.connect(**params)
                # create a new cursor
                #print('connected to db')
                cur = conn.cursor()
                # execute the INSERT statement
                cur.execute(sql, (date, hour, 
                    tibber_netto,
                    tibber_brutto,
                    ))
                #print('values written to db')
                print('values written to db: ', date, hour, 
                    tibber_netto,
                    tibber_brutto)
                # commit the changes to the database
                conn.commit()
                # close communication with the database
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print('db error: ')
                print(error)
            finally:
                if conn is not None:
                    conn.close()


    def write_load_battery(self, date, hour, load_battery):
        
            sql = """INSERT INTO hourly_data(date, hour,  
                        load_battery
                        )
                        VALUES(%s,%s,%s) 

                    ON CONFLICT (date, hour)
                    DO 
                    UPDATE SET 
                        load_battery = EXCLUDED.load_battery
                        
                    ;"""
            conn = None
            try:
                # read database configuration
                params = config()
                # connect to the PostgreSQL database
                conn = psycopg2.connect(**params)
                # create a new cursor
                print('connected to db')
                cur = conn.cursor()
                # execute the INSERT statement
                cur.execute(sql, (date, hour, 
                    load_battery
                    ))
                print('write value: ', load_battery, ' to column ',  'load_battery')
                # commit the changes to the database
                conn.commit()
                # close communication with the database
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print('db error: ')
                print(error)
            finally:
                if conn is not None:
                    conn.close()

    def write_statehp_recommendation(self, date, hour, statehp_recommendation):
        
            sql = """INSERT INTO hourly_data(date, hour,statehp_recommendation)
                        VALUES(%s,%s,%s) 

                    ON CONFLICT (date, hour)
                    DO 
                    UPDATE SET 
                        statehp_recommendation = EXCLUDED.statehp_recommendation
                        
                    ;"""
            conn = None
            try:
                # read database configuration
                params = config()
                # connect to the PostgreSQL database
                conn = psycopg2.connect(**params)
                # create a new cursor
                #print('connected to db')
                cur = conn.cursor()
                # execute the INSERT statement
                cur.execute(sql, (date, hour, 
                    statehp_recommendation
                    ))
                print('write value: ', statehp_recommendation, ' to column ',  'statehp_recommendation')
                # commit the changes to the database
                conn.commit()
                # close communication with the database
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print('db error: ')
                print(error)
            finally:
                if conn is not None:
                    conn.close()


    def write_pv_forecast(self, date, pv_forecast):
    
        sql = """INSERT INTO demand(date, forecast_solar
                    )
                    VALUES(%s,%s) 

                ON CONFLICT (date)
                DO 
                UPDATE SET 
                    forecast_solar = EXCLUDED.forecast_solar
                    
                ;"""
        conn = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            #print('connected to db')
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (date,  
                pv_forecast
                ))
            print('values written to db')
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('db error: ')
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def write_totalyield(self, date, pv_totalyield):
        sql = """INSERT INTO demand(date, pv_totalyield
                    )
                    VALUES(%s,%s) 

                ON CONFLICT (date)
                DO 
                UPDATE SET 
                    pv_totalyield = EXCLUDED.pv_totalyield
                    
                ;"""
        conn = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            #print('connected to db')
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (date,  
                pv_totalyield
                ))
            print('values written to db')
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('db error: ')
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def write_total_home_consumption(self, date, total_home_consumption):
    
        sql = """INSERT INTO demand(date, total_home_consumption
                    )
                    VALUES(%s,%s) 

                ON CONFLICT (date)
                DO 
                UPDATE SET 
                    total_home_consumption = EXCLUDED.total_home_consumption
                    
                ;"""
        conn = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            #print('connected to db')
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (date,  
                total_home_consumption
                ))
            #print('values written to db')
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('db error: ')
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def write_element_to_hourly_values(self, date, hour, column, data):

            sql = """INSERT INTO hourly_data(date, hour, """ + column + """)
                    VALUES(%s, %s, %s) 
                ON CONFLICT (date, hour) DO UPDATE SET """ + column + """ =  EXCLUDED.""" + column + """;"""
            print('write value: ', data, ' to column ',  column)
            
            conn = None
            try:
                # read database configuration
                params = config()
                # connect to the PostgreSQL database
                conn = psycopg2.connect(**params)
                # create a new cursor
                #print('connected to db')
                cur = conn.cursor()
                # execute the INSERT statement
                cur.execute(sql, (date, hour, 
                    data
                    ))
                # commit the changes to the database
                conn.commit()
                # close communication with the database
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print('db error: ')
                print(error)
            finally:
                if conn is not None:
                    conn.close()

    def write_demand(self, date, column, value):
    
        sql = """INSERT INTO demand(date, """ + column + """)
                    VALUES(%s, %s) 
                ON CONFLICT (date) DO UPDATE SET """ + column + """ =  EXCLUDED.""" + column + """;"""

        conn = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            #print('connected to db')
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (date,  
                value
                ))
            print('write to table demand in column',column, 'value: ', value, ' for date: ' , date)
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('db error: ')
            print(error)
        finally:
            if conn is not None:
                conn.close()
    
    def write_counter(self, value):
    
        sql = """ UPDATE counter SET pv_overshoot_duration='""" + str(value) + """';"""
        conn = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            #print('connected to db')
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (  
                value
                ))
            #print('values written to db')
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('db error: ')
            print(error)
        finally:
            if conn is not None:
                conn.close()


            
    def getcounter(self):
    
        postgreSQL_select_Query = """SELECT pv_overshoot_duration FROM counter ;"""
        #print(postgreSQL_select_Query)
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
                return mobile_records
                #print("PostgreSQL connection is closed")

    
    
    def retrieve_dict(self, date):
        """
        Run generic select query on db, returns a list of dictionaries
        """

        # Open a cursor to perform database operations
        query = """SELECT * FROM hourly_data WHERE date='""" + date +  """';"""
        data=[]

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
    
        sorted_list = sorted(results, key=lambda d:d['hour'])
        return sorted_list
    
    def demand_retrieve_dict(self):

        # Open a cursor to perform database operations
        query = """SELECT * FROM demand;"""
        data=[]

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
    
        sorted_list = sorted(results, key=lambda d:d['date'])
        return sorted_list
    
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