import datetime as dt
import os
import shutil
import sys
from scripts.constants import DATE_MSG


def get_user_date():
    """
        Ask for user to enter a valid date
        return 'datetime' : 'user_date'
    """
    while True:
        user_date = input(DATE_MSG)
        format = "%Y-%m-%d"
        if user_date == "":
            print("\nUsing today's date.\n")
            return (dt.date.today())    
        else:
            try:
                bool(dt.datetime.strptime(user_date, format))
                if (dt.datetime.strptime(user_date, format) < dt.datetime.today()):
                    return user_date
                else:
                    print("\nFuture date not valid.")
                    continue
            except ValueError:
                print('Date format not valid, please use "yyyy-mm-dd" pattern.\n')
                continue


def save_names(user_date, table_names, csv_list):
    """
        Save table names and csv file names to track operations into text files.
        './data/track/YYYY-MM-DD'
    """
    path = f"./data/track/{user_date}"
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        print("Saving table names and csv names for tracking purpose.\n")
        with open(f"{path}/tables.txt", "w") as tb_names:
            tb_names.write("\n".join(table_names))
            tb_names.write(" ")
        with open(f"{path}/csvs.txt", "w") as csv_names:
            csv_names.write("\n".join(csv_list))
            csv_names.write(" ")
        print(f"Table names and csv list saved in {path}.\n")
    except Exception as e:
        print(f"Error saving file with table names: {e}")


def validate_path(path, user_date):
    """
        Check if paths exist, otherwise creates it.
        Reprocess step 1 in case of path exists.
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Directory {path} created.")
        except Exception as e:
            print(f"Failed to create directories. Check your file system permissions. {e}\n")
    else:
        print(f"Step 1 already executed for this date. Reprocessing it for the selected day ({user_date}).")
        try:
            shutil.rmtree(path, ignore_errors=True)
            os.makedirs(path)
            print(f"{path} recreated.\n")
        except Exception as e:
            print(f"Error: {e}")


def create_db_path(table_names, user_date):
    """
        Create paths for tb tables
    """
    for table in table_names:
        path = f"./data/postgres/{table}/{user_date}"
        validate_path(path, user_date)
    print("\n")


def create_csv_path(user_date):
    """
        Create path for csv sources to destination.
    """
    path = f"./data/csv/{user_date}"
    validate_path(path, user_date)


def extract_csv(user_date):
    """
        Extract data from source csv to destination one (order_details.csv)
    """
    try:
        file_csv = "./data/order_details.csv"
        new_file = f"./data/csv/{user_date}/order_details.csv"
        with open(file_csv, "r", encoding="utf-8") as f, open(new_file, "w", newline="", encoding="utf-8") as nf:
            nf.write(f.read())
        print(f"CSV file extracted.\n")
    except Exception as e:
        print(f"Error extracting CSV file: {e}\n")


def files_are_ok(user_date, table_list, csv_list):
    """
        Check if files structure is consistent before starting step 2.
        return 'bool' : 'step1_done'
    """
    step1_done = False
    for table in table_list:
        path_db = f"./data/postgres/{table}/{user_date}"
        if not os.path.exists(path_db):
            sys.exit("Some folder from DB is missing for this day. Execute step 1 first.\n")
        if not os.path.exists(f"{path_db}/{table}.csv"):
            sys.exit(f"File {table}.csv is missing. Execute step 1 again.\n")
    for file in csv_list:
        path_csv = f"./data/csv/{user_date}"
        if not os.path.exists(path_csv):
            sys.exit("Path with CSV files from CSV folder does not exist for this day. Execute step 1 first.\n")
        if not os.path.exists(f"{path_csv}/{file}.csv"):
            sys.exit(f"File {file}.csv is missing. Execute step 1 again.\n")
    print("\nFiles from step 1 are OK.\n")
    step1_done = True
    return step1_done


def read_table_list(user_date):
    """
        Retrieve name of tables from track folder. (case of source db is offline)
        return 'list' : 'table_list'
    """
    table_list = list()
    with open(f"./data/track/{user_date}/tables.txt", "r") as tables_file:
        for table in tables_file:
            line = table[:-1]
            table_list.append(line)
    return table_list


def list_csvs(user_date):
    """
        Retrieve name of csv files from source csv folder
        return 'list' : 'list_csvs'
    """
    path = f"./data/csv/{user_date}"
    list_csvs = [os.path.splitext(filename)[0] for filename in os.listdir(path)]
    return list_csvs


def read_csv_list(user_date):
    """
        Read name of csv file names from track folder. (case of source csv file is missing)
        return 'list' : 'csv_list'
    """
    csvs_list = list()
    with open(f"./data/track/{user_date}/csvs.txt", "r") as f:
        for name in f:
            line = name[:-1]
            csvs_list.append(line)
    return csvs_list