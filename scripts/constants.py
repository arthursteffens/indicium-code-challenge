# Menu
INIT_MSG = """
Select your option:
    [1] Extract data from Postgres and CSV file and write to local disk.
    [2] Load data into final database.
    [3] Execute full pipeline.
    [4] Exit.

Option: """

# User date input
DATE_MSG = """
Type the date you want to extract the data from, leave blank to use today's date ("YYYY-MM-DD"): """

# SQL query to get the names of the tables from the source database
sql_PG_TABLE_NAMES_QUERY = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public';
"""

# Join tables
sql_FINAL_QUERY = """SELECT * FROM orders A
                     INNER JOIN order_details B
                     ON (A.order_id = B.order_id);
"""