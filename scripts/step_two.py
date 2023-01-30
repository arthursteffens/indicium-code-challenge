import sys
from scripts.db_cred import DBCred
from scripts.db_funcs import Database
from scripts.db_funcs import insert_into_mysql, final_query
from scripts.functions import read_csv_list, files_are_ok, read_table_list
from scripts.constants import sql_FINAL_QUERY

dest_db_cred = DBCred("mysql_db")

def execute_step_2(user_date):
    
    # Check if step 1 has already been executed
    try:
        table_list = read_table_list(user_date)
        csv_list = read_csv_list(user_date)
    except FileNotFoundError:
        sys.exit(f"Some file or folder was not found for {user_date}. Execute step 1 first/again.\n")
    except Exception as e:
        sys.exit(f"ERROR:\n {e}")

    # Check if directories/files from step 1 are ok
    print("Checking if files from step 1 are correct before starting step 2...")
    if files_are_ok(user_date, table_list, csv_list):

        print("\n*** INITIALIZING STEP 2 ***\n")
        # Establish connection with MySQL
        print("Trying to connect to destination database...")
        try:
            dest_db = Database(dest_db_cred)



            # conn = pymysql.connect(host='localhost', port=3306, user="user", password="userpass")
            # cursor = conn.cursor()
            print(f"Success: {conn}\n")
        except Exception as err:
            sys.exit(f"Destination DB (MySQL) connection error:\n {err} \nError type: {type(err)} \nCheck the credentials or status of the database.")
        
        # cursor.execute("USE mysql_northwind")

        # Iterate over list of tables
        for table in table_list:
            source = "postgres"
            success = dest_db.insert_into_mysql(source, table, user_date)
            if success:
                connection.commit()
                print(f"Table {table} loaded into destination database.")

        # Iterate over list of csv files on CSV folder
        for file in csv_list:
            source = "csv"
            success = insert_into_mysql(source, file, user_date, cursor)
            if success:
                conn.commit()
                print(f"Table {file} from CSV folder loaded into destination database.")

        # Generate CSV from final query on: /data/final_query.csv
        try:
            print("\nQuerying tables orders and order_details to generage final query...")
            final_query(user_date, cursor, sql_FINAL_QUERY)
            print(f"\nFinal query generated into /data/track/{user_date}/final_query.csv")
        except Exception as e:
            print(f"\nError generating final query: {e}")

        # Close cursor and connection with DB
        try:
            cursor.close()
            conn.close()
            print(f"\n*** STEP 2 for {user_date} FINISHED ***\n\n")
        except Exception as e:
            sys.exit(f"Error closing connection, check database status: {e}")

    else:
        sys.exit(0)


