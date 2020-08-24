import os

class Config:

    """CONFIGURABLE APP SETTINGS"""
    RESULTS_PER_PAGE = 5
    CLOUD_DEFAULT_IMG = "https://storage.googleapis.com/flask_blog_67394802/profile_pics/default.jpeg"
    SOURCE_FILE_NAME = './test_data.csv'
#    SOURCE_FILE_NAME = './PPP Data up to 150K - RI.csv'

    """SECURITY"""
    DEBUG_STATUS =  os.environ.get("DEBUG_STATUS")
    REQUIRE_SIGNED_URL = False
    SSL_REDIRECT = True
    SECRET_KEY = os.environ.get("SECRET_KEY")

    """EMAIL"""
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    """POSTGRES DATABASE"""
    #TODO: Change back to environment variable
    RESET_DB = True
    POSTGRES_HOST = "localhost"
    POSTGRES_USER = "rishan"
    POSTGRES_PASSWORD = "IamstrongPG18"
    POSTGRES_PORT = 5432
    DB_NAME = os.path.basename(SOURCE_FILE_NAME)\
        .split(".")[0]\
        .replace(" ", "_")\
        .replace("-", "")\
        .lower()+"_db"
    TABLE_NAME = os.path.basename(SOURCE_FILE_NAME)\
        .split(".")[0]\
        .replace(" ", "_")\
        .replace(" ", "")\
        .lower() +"_table"
#    TABLE_NAME = 'test_data'
    DB_URL = f"postgresql://localhost/{DB_NAME}"\
        + f"?user={POSTGRES_USER}"\
        + f"&password={POSTGRES_PASSWORD}"
    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost/{DB_NAME}'
#    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
#    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/all_test_data?user=rishan&password=IamstrongPG18"
#    SQLALCHEMY_DATABASE_URI = os.environ.get("postgresql:///all_test_data")
#    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    """GOOGLE CLOUD"""
    GCLOUD_CREDENTIALS = "app/service_account.json"
    GCLOUD_DATA_BUCKET_NAME = 'ppp-test-bucket-2'