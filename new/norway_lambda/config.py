import os

db_driver = os.getenv("DB_DRIVER") if os.getenv("DB_DRIVER") else "postgres"
db_host = os.getenv("DB_HOST") if os.getenv("DB_HOST") else "automation.cxesxp0yaizx.us-east-1.rds.amazonaws.com"
db_port = os.getenv("DB_PORT") if os.getenv("DB_PORT") else "5432"
db_name = os.getenv("DB_NAME") if os.getenv("DB_NAME") else "automation"
db_user = os.getenv("DB_USER") if os.getenv("DB_USER") else "automation"
db_pass = os.getenv("DB_PASS") if os.getenv("DB_PASS") else "automation"

glacier_bucket = os.getenv("GLACIER_BUCKET") if os.getenv("GLACIER_BUCKET") else "automation-s3-lambda-glacie"
s3bucket = os.getenv("S3_BUCKET") if os.getenv("S3_BUCKET") else "automation-s3-lambda-glacier"