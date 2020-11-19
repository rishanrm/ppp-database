import os

class Config:

    """FILENAME"""
#    SOURCE_FILE_NAME = 'data/test_data.csv'
#    SOURCE_FILE_NAME = './test_data.csv'
    SOURCE_FILE_NAME = './PPP Data up to 150K - RI.csv'
    SOURCE_FILE_NAME_2 = './PPP Data 150k and up.csv'

    """POSTGRES DATABASE RESET SETTINGS"""
    RESET_DB = False
    RESET_TABLE = False
    RESET_DATA = False
    MANUALLY_CREATE_TABLE = False

    """POSTGRES DATABASE CONNECTION"""
    POSTGRES_HOST = "localhost"

    POSTGRES_USER_FOR_LOCAL = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD_FOR_LOCAL = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_PORT_FOR_LOCAL = 5432

#    POSTGRES_USER_FOR_CLOUD = "postgres"
#    POSTGRES_PASSWORD_FOR_CLOUD = "postgres"
    POSTGRES_USER_FOR_CLOUD = "initial_setup_user"
    POSTGRES_PASSWORD_FOR_CLOUD = "initial_setup_password"

    POSTGRES_PORT_FOR_CLOUD = 5431

    POSTGRES_NAME_ROOT = os.path.basename(SOURCE_FILE_NAME)\
        .split(".")[0]\
        .replace(" ", "_")\
        .replace("-", "")\
        .lower()
    DB_NAME = POSTGRES_NAME_ROOT + "_db"
    TABLE_NAME = POSTGRES_NAME_ROOT + "_table"

#    DB_URL = f"postgresql://localhost/{DB_NAME}"\
#        + f"?user={POSTGRES_USER_FOR_LOCAL}"\
#        + f"&password={POSTGRES_PASSWORD_FOR_LOCAL}"
#    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER_FOR_LOCAL}:{POSTGRES_PASSWORD_FOR_LOCAL}@localhost/{DB_NAME}'
#    SQLALCHEMY_TRACK_MODIFICATIONS = False

    """CONTACT FORM"""
    CONTACT_EMAIL_ADDR = os.environ.get("CONTACT_EMAIL_ADDR")
    CONTACT_EMAIL_PASS = os.environ.get("CONTACT_EMAIL_PASS")
    
    """SECURITY"""
    DEBUG_STATUS =  os.environ.get("DEBUG_STATUS")
    SSL_REDIRECT = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    RECAPTCHA_PUBLIC_KEY = "6LcVnNwZAAAAAKvTGcDvoZv2ZgutD6s3RYFH4beq"
    RECAPTCHA_PRIVATE_KEY = "6LcVnNwZAAAAADF8Mwi45_zInKW0doneW2eTCXTa"
#    TESTING = True #Turn on or off ReCAPTCHA

    """GOOGLE CLOUD"""
    GCLOUD_CREDENTIALS = "service_account.json"
#    GCLOUD_DATA_BUCKET_NAME = 'ppp-test-bucket-8-1-01'
#    GCLOUD_BLOB_NAME = SOURCE_FILE_NAME
    GCLOUD_PROJECT_ID = "ppp-test-283923"
    GCLOUD_INSTANCE_ID = "ppp-test-8-1-02"
    GCLOUD_REGION = "us-central"
    GCLOUD_MACHINE_TYPE = "db-custom-1-3840"
    GCLOUD_REQUIRE_SIGNED_URL = False
#   Machine types: https://cloud.google.com/sql/docs/postgres/create-instance
