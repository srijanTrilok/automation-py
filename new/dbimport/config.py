import os


db_driver = os.getenv("DB_DRIVER") if os.getenv("DB_DRIVER") else "postgresql"
db_host = os.getenv("DB_HOST") if os.getenv("DB_HOST") else "sealedairchat.cxesxp0yaizx.us-east-1.rds.amazonaws.com"
db_port = os.getenv("DB_PORT") if os.getenv("DB_PORT") else "5432"
db_name = os.getenv("DB_NAME") if os.getenv("DB_NAME") else "lexchat"
db_user = os.getenv("DB_USER") if os.getenv("DB_USER") else "sealedairchat"
db_pass = os.getenv("DB_PASS") if os.getenv("DB_PASS") else "sealedairchat"
table_name = "lexchatbot_algos"