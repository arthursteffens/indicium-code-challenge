import sys
import psycopg2
import logging
from scripts.db_cred import source_db_cred
from scripts.db_funcs import get_table_names, extract_db
from scripts.functions import extract_csv, create_csv_path, create_db_path, save_names, list_csvs
from scripts.constants import sql_PG_TABLE_NAMES_QUERY

def execute_step_1(user_date):
    logging.info("\n*** INITIALIZING STEP 1 ***\n")

    try:
        logging.info("Trying to connect to source database...")
        conn = psycopg2.connect(source_db_cred)
        cursor = conn.cursor()
        print(f"Success: {conn}\n")
    except Exception as err:
        sys.exit(f"Source DB (Postgres) connection error:\n {err} \nError type: {type(err)} \nCheck the credentials or status of the database.")

    # Retrieve the names of tables in Postgres DB
    print("Retrieving table and CSV names...\n")
    table_names = get_table_names(cursor, sql_PG_TABLE_NAMES_QUERY)
    
    
    # Create paths to store data from DB and CSV
    print("Creating paths:\n")
    create_db_path(table_names, user_date)
    create_csv_path(user_date)

    # Extract data from Postgres and CSV and save into the specified folders
    print("\nExtracting and saving data...\n")
    extract_db(cursor, table_names, user_date)
    extract_csv(user_date)

    
    csvs = list_csvs(user_date)

    save_names(user_date, table_names, csvs)

    

    # Close cursor and connection with DB
    try:
        cursor.close()
        conn.close()
        print(f"*** STEP 1 for {user_date} FINISHED ***\n\n")
    except Exception as e:
        print(f"Error closing connection, check database status: {e}")
        