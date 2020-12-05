import os

class Config:

    """CONFIGURATION LOCATION"""
    DB_LOCATION = "cloud" # "local" or "cloud"

    """FILENAME"""
    # SOURCE_FILE_NAME = './PPP Data 150k and up.csv'
    DB_NAME_ROOT_UNDER_150K = 'ppp_data_up_to_150k_080820'
    DB_NAME_ROOT_150K_AND_UP = 'ppp_data_150k_and_up_080820'

    HEADERS_UNDER_150K = ['loanamount', 'city', 'state', 'zip', 'naicscode',
                        'businesstype', 'raceethnicity', 'gender', 'veteran',
                        'nonprofit', 'jobsreported', 'dateapproved', 'lender',
                        'cd']
    HEADERS_150K_AND_UP = ['loanrange', 'businessname', 'address', 'city',
                        'state', 'zip', 'naicscode', 'businesstype',
                        'raceethnicity', 'gender', 'veteran', 'nonprofit',
                        'jobsreported', 'dateapproved', 'lender', 'cd']
    NUMERIC_HEADERS = ["loanamount", "jobsretained", "jobsreported"]
    NAMES_TO_CAPITALIZE = ['businessname', 'address', 'city', 'lender']

    """POSTGRES DATABASE CONNECTION"""
    POSTGRES_HOST = "localhost"

    """CONTACT FORM"""
    CONTACT_EMAIL_ADDR = os.environ.get("CONTACT_EMAIL_ADDR")
    CONTACT_EMAIL_PASS = os.environ.get("CONTACT_EMAIL_PASS")
    
    """SECURITY"""
    # SSL_REDIRECT = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    RECAPTCHA_PUBLIC_KEY = "6LcVnNwZAAAAAKvTGcDvoZv2ZgutD6s3RYFH4beq"
    RECAPTCHA_PRIVATE_KEY = "6LcVnNwZAAAAADF8Mwi45_zInKW0doneW2eTCXTa"
#    TESTING = True #Turn on or off ReCAPTCHA

class ProductionConfig(Config):

    """GOOGLE CLOUD"""
    DEBUG_STATUS = False
    
    GCLOUD_CREDENTIALS = "service_account.json"
    GCLOUD_PROJECT_ID = "ppp-test-283923"
    GCLOUD_INSTANCE_ID = "ppp-test-8-1-02"
    GCLOUD_REGION = "us-central"
    GCLOUD_MACHINE_TYPE = "db-custom-1-3840"
    GCLOUD_REQUIRE_SIGNED_URL = False
#   Machine types: https://cloud.google.com/sql/docs/postgres/create-instance

#    POSTGRES_USER_FOR_CLOUD = "postgres"
#    POSTGRES_PASSWORD_FOR_CLOUD = "postgres"
    POSTGRES_USER = "initial_setup_user"
    POSTGRES_PASSWORD = "initial_setup_password"
    POSTGRES_PORT = 5431


class DevelopmentConfig(Config):
    DEBUG_STATUS = True

    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_PORT = 5432
