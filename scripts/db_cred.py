import yaml
import logging


with open("docker-compose.yml", "r") as file:
    yml = yaml.safe_load(file)


class DBCred():
    def __init__(self, service) -> None:
        try:
            db =  yml["services"][service]
            env = db["environment"]

            if service == "pg_db":
                self.db_prefix = "POSTGRES"
                self.db_name = env[f"{self.db_prefix}_DB"]
                self.
            if service == "mysql_db":
                self.db_prefix = "MYSQL"
                self.db_name = env[f"{self.db_prefix}_DATABASE"]

            self.dsn =  f"""
                host={"localhost"}
                dbname={self.db_name}
                user={env[f"{self.db_prefix}_USER"]}
                password={env[f"{self.db_prefix}_PASSWORD"]}
                port={yml["services"][service]["ports"][0].split(":")[0]}
            """
        except Exception as e:
            logging.error(f"Invalid docker-compose.yml: {e}")

# class DBCred():
#     def __init__(self, service) -> None:
#         try:
#             db =  yml["services"][service]
#             env = db["environment"]

#             if service == "pg_db":
#                 self.db_prefix = "POSTGRES"
#                 self.db_name = env[f"{self.db_prefix}_DB"]
#             if service == "mysql_db":
#                 self.db_prefix = "MYSQL"
#                 self.db_name = env[f"{self.db_prefix}_DATABASE"]

#             self.dsn =  f"""
#                 host={"localhost"}
#                 dbname={self.db_name}
#                 user={env[f"{self.db_prefix}_USER"]}
#                 password={env[f"{self.db_prefix}_PASSWORD"]}
#                 port={yml["services"][service]["ports"][0].split(":")[0]}
#             """
#         except Exception as e:
#             logging.error(f"Invalid docker-compose.yml: {e}")



destiny_db_cred = DBCred("mysql_db")