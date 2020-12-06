import os

from cloud_secrets import CloudSecrets

class Config:

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

    """GOOGLE CLOUD"""
    GCLOUD_CREDENTIALS = "ppp-data-us-service-account.json"
    GCLOUD_PROJECT_ID = "ppp-data-us"
    GCLOUD_INSTANCE_ID = "ppp-data"
    GCLOUD_REGION = "us-central"
    GCLOUD_ZONE = "us-central1-a"
    GCLOUD_MACHINE_TYPE = "db-custom-1-3840"
    GCLOUD_REQUIRE_SIGNED_URL = False
#   Machine types: https://cloud.google.com/sql/docs/postgres/create-instance

class ProductionConfig(Config):

    DEBUG_STATUS = False
    POSTGRES_USER = CloudSecrets.get_cloud_secret(
        Config.GCLOUD_PROJECT_ID, "POSTGRES_USER")
    POSTGRES_PASSWORD = CloudSecrets.get_cloud_secret(
        Config.GCLOUD_PROJECT_ID, "POSTGRES_PASSWORD")
    POSTGRES_PORT = 5431

    """CONTACT FORM"""
    CONTACT_EMAIL_ADDR = CloudSecrets.get_cloud_secret(
        Config.GCLOUD_PROJECT_ID, "CONTACT_EMAIL_ADDR")
    CONTACT_EMAIL_PASS = CloudSecrets.get_cloud_secret(
        Config.GCLOUD_PROJECT_ID, "CONTACT_EMAIL_PASS")

    """SECURITY"""
    # SSL_REDIRECT = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    RECAPTCHA_PUBLIC_KEY = CloudSecrets.get_cloud_secret(
        Config.GCLOUD_PROJECT_ID, "RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = CloudSecrets.get_cloud_secret(
        Config.GCLOUD_PROJECT_ID, "RECAPTCHA_PRIVATE_KEY")

#    TESTING = True #Turn on or off ReCAPTCHA

class DevelopmentConfig(Config):

    DEBUG_STATUS = True
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_PORT = 5432

    """CONTACT FORM"""
    CONTACT_EMAIL_ADDR = os.environ.get("CONTACT_EMAIL_ADDR")
    CONTACT_EMAIL_PASS = os.environ.get("CONTACT_EMAIL_PASS")

    """SECURITY"""
    # SSL_REDIRECT = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")
    # RECAPTCHA_PUBLIC_KEY = "6LdH9_oZAAAAAPr6GNAc6-ylfVEHc0AHzc4UhwwU"
    # RECAPTCHA_PRIVATE_KEY = "6LdH9_oZAAAAAE2iY2dKeUHqiq-4Jb7SFnOK1Tvu"

    
    # TESTING = True #Turn on or off ReCAPTCHA
