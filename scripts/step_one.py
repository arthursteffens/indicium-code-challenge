import sys
import logging
from scripts.functions import extract_csv, create_csv_path, create_db_path, save_names, list_csvs
from scripts.constants import sql_PG_TABLE_NAMES_QUERY
from scripts.DBCred import DBCred
from scripts.Database import Database

source_db_cred = DBCred("pg_db_in")

def execute_step_1(user_date):
    logging.info("*** INITIALIZING STEP 1 ***\n")

    try:
        logging.info("Trying to connect to source database...")
        source_db = Database(source_db_cred)
        conn = source_db.engine.connect()
        logging.info(f"Success: {source_db.engine}\n")
        conn.close()
    except Exception as err:
        logging.error(f"Source DB (Postgres) connection error:\n {err} \nError type: {type(err)} \nCheck the credentials or status of the database.")
        sys.exit(0)

    # Retrieve the names of tables in Postgres DB
    logging.info("Retrieving table and CSV names...\n")
    src_tables = source_db.get_table_names(sql_PG_TABLE_NAMES_QUERY)
    
    
    # Create paths to store data from DB and CSV
    logging.info("Creating paths:\n")
    create_db_path(src_tables, user_date)
    create_csv_path(user_date)

    # Extract data from Postgres and CSV and save into the specified folders
    logging.info("Extracting and saving data...\n")
    source_db.extract_db(src_tables, user_date)
    extract_csv(user_date)

    # Save table names and csv names
    csvs = list_csvs(user_date)
    save_names(user_date, src_tables, csvs)

    logging.info(f"*** STEP 1 for {user_date} FINISHED ***\n")