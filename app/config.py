import os

from cloud_secrets import CloudSecrets

class Config:

    """FILENAME"""
    DB_NAME_ROOT_ALL_DATA = 'ppp_data_all'
    DB_NAME_ROOT_UNDER_150K = 'ppp_data_up_to_150k_080820'
    DB_NAME_ROOT_150K_AND_UP = 'ppp_data_150k_and_up_080820'

    HEADERS_ALL_DATA = ['loanamount', 'businessname', 'address', 'city',
                        'state', 'zip', 'naicscode', 'businesstype',
                        'raceethnicity', 'gender', 'veteran', 'nonprofit',
                        'jobsreported', 'dateapproved', 'lender', 'cd']
    HEADERS_DATA_SUMMARY = ['state', 'loancount', 'totaljobs',
                            'totalloanamount', 'avgloansize',
                            'jobsperloan', 'dollarsperjob', 'loancountnojobs',
                            'totalloansnojobs', 'avgloansizenojobs']
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

    """GOOGLE CLOUD"""
    GCLOUD_CREDENTIALS = "ppp-data-us-service-account.json"
    GCLOUD_PROJECT_ID = "ppp-data-us"
    GCLOUD_INSTANCE_ID = "ppp-data"
    GCLOUD_INSTANCE_REGION = "us-central1"
    GCLOUD_INSTANCE_ZONE = "us-central1-a"
    GCLOUD_INSTANCE_MACHINE_TYPE = "db-custom-1-3840"
    GCLOUD_REQUIRE_SIGNED_URL = False
#   Machine types: https://cloud.google.com/sql/docs/postgres/create-instance

class ProductionConfig(Config):

    DEBUG_STATUS = False
    """POSTGRES DATABASE CONNECTION"""
    POSTGRES_HOST = f"/cloudsql/{Config.GCLOUD_PROJECT_ID}:{Config.GCLOUD_INSTANCE_REGION}:{Config.GCLOUD_INSTANCE_ID}"
    POSTGRES_USER = CloudSecrets.get_cloud_secret(
        Config.GCLOUD_PROJECT_ID, "POSTGRES_USER")
    POSTGRES_PASSWORD = CloudSecrets.get_cloud_secret(
        Config.GCLOUD_PROJECT_ID, "POSTGRES_PASSWORD")
    POSTGRES_PORT = 5432

    """CONTACT FORM"""
    CONTACT_EMAIL_ADDR = CloudSecrets.get_cloud_secret(
        Config.GCLOUD_PROJECT_ID, "CONTACT_EMAIL_ADDR")
    CONTACT_EMAIL_PASS = CloudSecrets.get_cloud_secret(
        Config.GCLOUD_PROJECT_ID, "CONTACT_EMAIL_PASS")

    """SECURITY"""
    # SSL_REDIRECT = True
    SECRET_KEY = CloudSecrets.get_cloud_secret(
        Config.GCLOUD_PROJECT_ID, "SECRET_KEY")
    RECAPTCHA_PUBLIC_KEY = CloudSecrets.get_cloud_secret(
        Config.GCLOUD_PROJECT_ID, "RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = CloudSecrets.get_cloud_secret(
        Config.GCLOUD_PROJECT_ID, "RECAPTCHA_PRIVATE_KEY")
    TESTING = False  # True to turn off ReCAPTCHA for testing

class DevelopmentConfig(Config):

    DEBUG_STATUS = True

    """POSTGRES DATABASE CONNECTION"""
    POSTGRES_HOST = "localhost"
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
    TESTING = False # True to turn off ReCAPTCHA for testing
