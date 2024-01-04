import os
from pathlib import Path
from dotenv import dotenv_values
BASE_DIR = Path(__file__).parent

config = dotenv_values(os.path.join(BASE_DIR, ".env"))

class AppConfig:
    email = config["EMAIL"]
    password = config["PASSWORD"]
    host = config["HOST"]
    port = config["PORT"]
    use_ssl = config['USE_SSL']
    use_tls = config["USE_TLS"]




