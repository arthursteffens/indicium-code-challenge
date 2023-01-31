import pandas as pd
import numpy as np

import logging
from sqlalchemy import create_engine, text

class Database():
    def __init__(self, db_cred):
        self.conn_str = db_cred.conn_str
        self.engine = create_engine(self.conn_str)

    def get_table_names(self, sql):
        """
            Retrieve name of tables from source DB
            return 'list' : 'table_names'
        """
        try:
            with self.engine.connect() as connection:
                results = connection.execute(text(sql))

            table_names = [table_name[0] for table_name in results]
            logging.info(f"Got {len(table_names)} tables: {table_names} \n")
            return table_names
        except Exception as e:
            logging.error(f"Error retrieving table names, check database status or SQL syntax: \n{e}")

    def extract_db(self, table_names, user_date):
        """
            Extract data from source DB.
            Write each table into csv files.
        """
        try:
            with self.engine.connect() as connection:
                for table in table_names:
                    path = f"./data/postgres/{table}/{user_date}/{table}.csv"
                    result = connection.execute(text(f"SELECT * FROM {table};"))
                    columns = result._metadata.keys
                    df = pd.DataFrame(columns=columns, data=result)
                    final_df = df.astype(object).where(pd.notnull(df), 'NULL')
                    final_df.to_csv(path, index=False, sep=',', encoding='utf-8')
            logging.info("Tables extracted.\n")
        except Exception as e:
            logging.error(f"Error while extracting or saving data from Postgres DB: {e}")


    def insert_into_db(self, source, table, user_date):
        """
            Insert data into destination DB.
            return 'bool' : success
        """
        success = False
        if source == "postgres":
            path = f"./data/{source}/{table}/{user_date}/{table}.csv"
        elif source == "csv":
            path = f"./data/{source}/{user_date}/{table}.csv"
        
        try:
            df = pd.read_csv(path, encoding="utf-8")

            with self.engine.connect() as connection:
                df.to_sql(name=table, con=self.engine, if_exists='replace', index=False)
                connection.commit()
            success = True
            return success
        except Exception as e:
            print(f"Error loading data into destination database: {e}")


    def exec_sql(self, sql):
        with self.engine.connect() as connection:
            connection.execute(text(sql))
            connection.commit()


    def final_query(self, user_date, sql):
        """
            Execute final query on destination DB and write result into 'final_query.csv'
        """
        path = f"./data/track/{user_date}/final_query.csv"
        with self.engine.connect() as connection:
            result = connection.execute(text(sql))
            cols = result._metadata.keys
            df = pd.DataFrame(result, columns=cols)
        df.to_csv(path, index=False, sep=',', encoding='utf-8')
