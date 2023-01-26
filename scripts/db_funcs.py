import pandas as pd
import numpy as np

def get_table_names(cursor, sql):
    """
        Retrieve name of tables from source DB
        return 'list' : 'table_names'
    """
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        table_names = [table_name[0] for table_name in results]
        print(f"Got {len(table_names)} tables: {table_names} \n")
        return table_names
    except Exception as e:
        print(f"Error retrieving table names, check database status or SQL syntax: \n{e}")


def extract_db(cursor, table_names, user_date):
    """
        Extract data from source DB.
        Write each table into csv files.
    """
    try:
        for table in table_names:
            path = f"./data/postgres/{table}/{user_date}/{table}.csv"
            cursor.execute(f"SELECT * FROM {table};")
            columns = [col[0] for col in cursor.description]
            result = cursor.fetchall()
            df = pd.DataFrame(columns=columns, data=result)
            final_df = df.astype(object).where(pd.notnull(df), 'NULL')
            final_df.to_csv(path, index=False, sep=',', encoding='utf-8')
        print("Tables extracted.\n")
    except Exception as e:
        print(f"Error while extracting or saving data from Postgres DB: {e}")


def insert_into_mysql(source, table, user_date, cursor):
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
        df.replace(to_replace=np.nan, value='NULL', inplace=True)
            
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        cursor.execute(f"DELETE FROM {table};")
        
        for i in range(len(df)):
            row_tuple = tuple(df.to_records(index=False))
            
            sql = f'''
                INSERT INTO {table} VALUES {row_tuple[i]};
            '''

            cursor.execute(sql)
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        success = True
        return success
    except Exception as e:
        print(f"Error loading data into destination database: {e}")


def final_query(user_date, cursor, sql):
    """
        Execute final query on destination DB and write result into 'final_query.csv'
    """
    path = f"./data/track/{user_date}/final_query.csv"
    cursor.execute(sql)
    cols = [col[0] for col in cursor.description]
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=cols)
    df.to_csv(path, index=False, sep=',', encoding='utf-8')