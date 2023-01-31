import sys
import logging
from scripts.DBCred import DBCred
from scripts.Database import Database
from scripts.functions import read_csv_list, files_are_ok, read_table_list
from scripts.constants import sql_FINAL_QUERY

dest_db_cred = DBCred("pg_db_out")

def execute_step_2(user_date):
    
    # Check if step 1 has already been executed
    try:
        table_list = read_table_list(user_date)
        csv_list = read_csv_list(user_date)
    except FileNotFoundError:
        logging.error(f"Some file or folder was not found for {user_date}. Execute step 1 first/again.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"{e}")
        sys.exit(0)

    # Check if directories/files from step 1 are ok
    logging.info("Checking if files from step 1 are correct before starting step 2...")
    if files_are_ok(user_date, table_list, csv_list):

        logging.info("*** INITIALIZING STEP 2 ***\n")
        # Establish connection with MySQL
        logging.info("Trying to connect to destination database...")
        try:
            dest_db = Database(dest_db_cred)
            logging.info(f"Success: {dest_db}\n")
        except Exception as err:
            sys.exit(f"Destination DB (MySQL) connection error:\n {err} \nError type: {type(err)} \nCheck the credentials or status of the database.")

        # Iterate over list of tables
        source = "postgres"
        for table in table_list:
            dest_db.exec_sql(f"DROP TABLE if exists {table} CASCADE")
            success = dest_db.insert_into_db(source, table, user_date)
            if success:
                logging.info(f"Table {table} loaded into destination database.")

        # Iterate over list of csv files on CSV folder
        source = "csv"
        for file in csv_list:
            success = dest_db.insert_into_db(source, file, user_date)
            if success:
                logging.info(f"Table {file} from CSV folder loaded into destination database.")

        # Apply constraints again into the output database
        with open("./data/constraints_db_out.sql", "r") as file:
            dest_db.exec_sql(file.read())

        # Generate CSV from final query on: /data/final_query.csv
        try:
            logging.info("Querying tables orders and order_details to generage final query...")
            dest_db.final_query(user_date, sql_FINAL_QUERY)
            logging.info(f"Final query generated into /data/track/{user_date}/final_query.csv")
        except Exception as e:
            logging.error(f"Error generating final query: {e}")

        
        logging.info(f"*** STEP 2 for {user_date} FINISHED ***\n")
    else:
        sys.exit("There are inconsistencies in some files. Please execute the pipeline from the beggining.")


