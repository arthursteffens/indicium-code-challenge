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
                self.db_name = env["POSTGRES_DB"]
            if service == "mysql_db":
                self.db_name = env["MYSQL_DATABASE"]

            self.dsn =  f"""
                host={"localhost"}
                dbname={self.db_name}
                user={env["POSTGRES_USER"]}
                password={env["POSTGRES_PASSWORD"]}
                port={yml["services"][service]["ports"][0].split(":")[0]}
            """
        except Exception as e:
            logging.error(f"Invalid docker-compose.yml: {e}")


source_db_cred = DBCred("pg_db")
destiny_db_cred = DBCred("mysql_db")