import yaml
import logging


with open("docker-compose.yml", "r") as file:
    yml = yaml.safe_load(file)


class DBCred():
    def __init__(self, service) -> None:
        try:
            db =  yml["services"][service]
            env = db["environment"]
            
            self.db_prefix = "POSTGRES"
            self.eng_driver = "postgresql+psycopg2"
            self.db_name = env[f"{self.db_prefix}_DB"]
            self.user=env[f"{self.db_prefix}_USER"]
            self.passwd=env[f"{self.db_prefix}_PASSWORD"]
            self.port=yml["services"][service]["ports"][0].split(":")[0]
            self.host="localhost"
                
            self.conn_str = f"{self.eng_driver}://{self.user}:{self.passwd}@{self.host}:{self.port}/{self.db_name}"

        except Exception as e:
            logging.error(f"Invalid docker-compose.yml: {e}")