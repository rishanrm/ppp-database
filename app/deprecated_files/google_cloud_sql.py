from google.oauth2 import service_account
import googleapiclient.discovery

PROJECT_NAME = "ppp-test"
PROJECT_ID = "ppp-test-283923"
SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin']
SERVICE_ACCOUNT_FILE = '.\ppp_dashboard\service_account.json'

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
sqladmin_service = googleapiclient.discovery.build('sqladmin', 'v1beta4', credentials=credentials)
req = sqladmin_service.instances().list(project=PROJECT_ID, filter=("name=ppp-test-instance-2"))
instance = req.execute()

print(instance)
print("Instance name: " + instance["items"][0]["name"])


"""
import json
import requests
import urllib.parse


def explicit():
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        '.\ppp_dashboard\service_account.json')

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)
    return storage_client
""" 

#client = explicit()

# #import json
# #import requests
# #from urllib.parse import urlparse

# project_id = "ppp-test"
# r = requests.get('https://xkcd.com/353/')
# g = requests.post(f'https://www.googleapis.com/sql/v1beta4/projects/{project_id}/instances')
# print(g)

# #list = client.aggregatedList()
# print(dir(client))

# """
# Create an instance
# https://cloud.google.com/sql/docs/postgres/create-instance
# """

#    print(instance["items"][0]["name"])
#response = json.dumps(resp, indent=2)
#response = json.loads(resp, indent=2)
#print(type(response))
#req = sqladmin_service.instances().insert(project=PROJECT_ID, zone="us-central1-f", name="ppp-test-10")



#gcloud compute instances create example-instance-1 example-instance-2 example-instance-3 --zone=us-central1-a

"""
sql_json = {
      "kind": "sql#instance",
      "state": "RUNNABLE",
      "databaseVersion": "POSTGRES_12",
      "settings": {
        "authorizedGaeApplications": [],
        "tier": "db-custom-1-3840",
        "kind": "sql#settings",
        "availabilityType": "ZONAL",
        "pricingPlan": "PER_USE",
        "replicationType": "SYNCHRONOUS",
        "activationPolicy": "ALWAYS",
        "ipConfiguration": {
          "authorizedNetworks": [],
          "ipv4Enabled": True
        },
        "locationPreference": {
          "zone": "us-central1-a",
          "kind": "sql#locationPreference"
        },
        "dataDiskType": "PD_SSD",
        "maintenanceWindow": {
          "kind": "sql#maintenanceWindow",
          "hour": 0,
          "day": 0
        },
        "backupConfiguration": {
          "startTime": "05:00",
          "kind": "sql#backupConfiguration",
          "location": "us",
          "enabled": True,
          "replicationLogArchivingEnabled": True,
          "pointInTimeRecoveryEnabled": True
        },
        "settingsVersion": "1",
        "storageAutoResizeLimit": "0",
        "storageAutoResize": True,
        "dataDiskSizeGb": "10"
      },
      "etag": "131aee0d1b7bbf054d5ba1bb09d7a1c197ad21bd8443208de6cc0f90820a131b",
      "ipAddresses": [
        {
          "type": "PRIMARY",
          "ipAddress": "34.72.111.112"
        }
      ],
      "serverCaCert": {
        "kind": "sql#sslCert",
        "certSerialNumber": "0",
        "cert": "-----BEGIN CERTIFICATE-----\nMIIDfzCCAmegAwIBAgIBADANBgkqhkiG9w0BAQsFADB3MS0wKwYDVQQuEyQwMWU3\nMzEyNS0yNDM3LTQwNWEtYjBmYi0wNzQyNWIzODkwMjQxIzAhBgNVBAMTGkdvb2ds\nZSBDbG91ZCBTUUwgU2VydmVyIENBMRQwEgYDVQQKEwtHb29nbGUsIEluYzELMAkG\nA1UEBhMCVVMwHhcNMjAwNzIyMDIwMzA1WhcNMzAwNzIwMDIwNDA1WjB3MS0wKwYD\nVQQuEyQwMWU3MzEyNS0yNDM3LTQwNWEtYjBmYi0wNzQyNWIzODkwMjQxIzAhBgNV\nBAMTGkdvb2dsZSBDbG91ZCBTUUwgU2VydmVyIENBMRQwEgYDVQQKEwtHb29nbGUs\nIEluYzELMAkGA1UEBhMCVVMwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIB\nAQCntNxShvSRHQHOaDg5Rna+9bE+MZC4HnCCzecNkzaIvl1//VtMyBaSMP6O4toI\n6tHTlFQTk7jaQZJRKnUFqamolYCjppQoKQsU7qNEFGWpNWlLrmxnM+RxgeUUihws\nR5MphnqwZCVmhPO8M1AZOfU85PZlldEF4gz/1INf93oZnCB/EYhbZqd6pLRjO9ic\nJbce2AibkrW8RVn16UjPnpSXV8nalhHLUPDNyP02fCH72BDqsXtD0T+xjydM0JnN\ngN448t/gyOSTDYdAAT5oRYVUeUp7kAD4itRjKMUieDHjYxlcbnJquaZJNJhTfeWx\naXaYJFDxHkrEjQmfo2TmBDfnAgMBAAGjFjAUMBIGA1UdEwEB/wQIMAYBAf8CAQAw\nDQYJKoZIhvcNAQELBQADggEBABrdxhl6JHT0YZHHbNUbXg32A8c1sNpepDLfJDgQ\n77WXQROAE01Eitzbh0Op4vyj/zkUMI02nBOJ5tdoR6dUNGEjDcZ4fO87PClaUFsn\nYvjCelIkdCfyvCBH/3pFCr5eHgwoHq9nD6XRgLYTiynTACyAsOm2Ug1eFYmp6YS0\nIdGriIOgxhzGzrU2OfSP+dET8DT8qgKfFBKFJKmKoIepDehjTAkM6tnB6BsOwo/S\nhBEcAZIrkyK3yWPp6ePUvCpOTZmmOdhCN1wySAubQn9KH3czYSN7u/BXhDmqi7z/\njtYt6mtcahDCZpvdIjhkBNQzgSTt4TzTLhAutt0KRTX3cHM=\n-----END CERTIFICATE-----",
        "commonName": "C=US,O=Google\\, Inc,CN=Google Cloud SQL Server CA,dnQualifier=01e73125-2437-405a-b0fb-07425b389024",
        "sha1Fingerprint": "a82bc9380e40750d7c6ddd6c05c227c05dfd2058",
        "instance": "ppp-test-instance-2",
        "createTime": "2020-07-22T02:03:05.608Z",
        "expirationTime": "2030-07-20T02:04:05.608Z"
      },
      "instanceType": "CLOUD_SQL_INSTANCE",
      "project": "ppp-test-283923",
      "serviceAccountEmailAddress": "p355491811298-gq2xhk@gcp-sa-cloud-sql.iam.gserviceaccount.com",
      "backendType": "SECOND_GEN",
      "selfLink": "https://www.googleapis.com/sql/v1beta4/projects/ppp-test-283923/instances/ppp-test-instance-2",
      "connectionName": "ppp-test-283923:us-central1:ppp-test-instance-2",
      "name": "ppp-test-instance-2",
      "region": "us-central1",
      "gceZone": "us-central1-a"
    }
"""
"""
req = sqladmin_service.instances().insert(project=PROJECT_ID)
instances = req.execute()
print(instances)
"""

"""
import requests
import json
url = f"https://sqladmin.googleapis.com/sql/v1beta4/projects/{PROJECT_ID}/instances"
res = requests.put(url, json=sql_json)

print(res.status_code)
print(res.raise_for_status())
"""


"""
#JSON representation that I tried to create as a template
instance_json = {
    "kind": "sql#instance",
    "state": "RUNNABLE",
    "databaseVersion": "POSTGRES_12",
    "settings": {
    "authorizedGaeApplications": [],
    "tier": "db-custom-1-3840",
    "kind": "sql#settings",
    "availabilityType": "ZONAL",
    "pricingPlan": "PER_USE",
    "replicationType": "SYNCHRONOUS",
    "activationPolicy": "ALWAYS",
    "ipConfiguration": {
        "authorizedNetworks": [],
        "ipv4Enabled": true
    },
    }
    "etag": "131aee0d1b7bbf054d5ba1bb09d7a1c197ad21bd8443208de6cc0f90820a131b",
    "ipAddresses": [
    {
        "type": "PRIMARY",
        "ipAddress": "34.72.111.112"
    }
    ],
    "serverCaCert": {
    "kind": "sql#sslCert",
    "certSerialNumber": "0",
    "cert": "-----BEGIN CERTIFICATE-----\nMIIDfzCCAmegAwIBAgIBADANBgkqhkiG9w0BAQsFADB3MS0wKwYDVQQuEyQwMWU3\nMzEyNS0yNDM3LTQwNWEtYjBmYi0wNzQyNWIzODkwMjQxIzAhBgNVBAMTGkdvb2ds\nZSBDbG91ZCBTUUwgU2VydmVyIENBMRQwEgYDVQQKEwtHb29nbGUsIEluYzELMAkG\nA1UEBhMCVVMwHhcNMjAwNzIyMDIwMzA1WhcNMzAwNzIwMDIwNDA1WjB3MS0wKwYD\nVQQuEyQwMWU3MzEyNS0yNDM3LTQwNWEtYjBmYi0wNzQyNWIzODkwMjQxIzAhBgNV\nBAMTGkdvb2dsZSBDbG91ZCBTUUwgU2VydmVyIENBMRQwEgYDVQQKEwtHb29nbGUs\nIEluYzELMAkGA1UEBhMCVVMwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIB\nAQCntNxShvSRHQHOaDg5Rna+9bE+MZC4HnCCzecNkzaIvl1//VtMyBaSMP6O4toI\n6tHTlFQTk7jaQZJRKnUFqamolYCjppQoKQsU7qNEFGWpNWlLrmxnM+RxgeUUihws\nR5MphnqwZCVmhPO8M1AZOfU85PZlldEF4gz/1INf93oZnCB/EYhbZqd6pLRjO9ic\nJbce2AibkrW8RVn16UjPnpSXV8nalhHLUPDNyP02fCH72BDqsXtD0T+xjydM0JnN\ngN448t/gyOSTDYdAAT5oRYVUeUp7kAD4itRjKMUieDHjYxlcbnJquaZJNJhTfeWx\naXaYJFDxHkrEjQmfo2TmBDfnAgMBAAGjFjAUMBIGA1UdEwEB/wQIMAYBAf8CAQAw\nDQYJKoZIhvcNAQELBQADggEBABrdxhl6JHT0YZHHbNUbXg32A8c1sNpepDLfJDgQ\n77WXQROAE01Eitzbh0Op4vyj/zkUMI02nBOJ5tdoR6dUNGEjDcZ4fO87PClaUFsn\nYvjCelIkdCfyvCBH/3pFCr5eHgwoHq9nD6XRgLYTiynTACyAsOm2Ug1eFYmp6YS0\nIdGriIOgxhzGzrU2OfSP+dET8DT8qgKfFBKFJKmKoIepDehjTAkM6tnB6BsOwo/S\nhBEcAZIrkyK3yWPp6ePUvCpOTZmmOdhCN1wySAubQn9KH3czYSN7u/BXhDmqi7z/\njtYt6mtcahDCZpvdIjhkBNQzgSTt4TzTLhAutt0KRTX3cHM=\n-----END CERTIFICATE-----",
    "commonName": "C=US,O=Google\\, Inc,CN=Google Cloud SQL Server CA,dnQualifier=01e73125-2437-405a-b0fb-07425b389024",
    "sha1Fingerprint": "a82bc9380e40750d7c6ddd6c05c227c05dfd2058",
    "instance": "ppp-test-instance-10",
    "createTime": "2020-07-22T02:03:05.608Z",
    "expirationTime": "2030-07-20T02:04:05.608Z"
    },
    "instanceType": "CLOUD_SQL_INSTANCE",
    "project": "ppp-test-283923",
    "serviceAccountEmailAddress": "p355491811298-gq2xhk@gcp-sa-cloud-sql.iam.gserviceaccount.com",
    "replicaConfiguration": {
        "backendType": "SECOND_GEN",
        "selfLink": "https://www.googleapis.com/sql/v1beta4/projects/ppp-test-283923/instances/ppp-test-instance-10",
        "connectionName": "ppp-test-283923:us-central1:ppp-test-instance-10",
        "name": "ppp-test-instance-10",
        "region": "us-central1",
        "gceZone": "us-central1-a",
    "rootPassword": "postgres"
    }
    }
"""



"""Full instance object JSON

{
  "items": [
    {
      "kind": "sql#instance",
      "state": "RUNNABLE",
      "databaseVersion": "POSTGRES_12",
      "settings": {
        "authorizedGaeApplications": [],
        "tier": "db-custom-1-3840",
        "kind": "sql#settings",
        "availabilityType": "ZONAL",
        "pricingPlan": "PER_USE",
        "replicationType": "SYNCHRONOUS",
        "activationPolicy": "ALWAYS",
        "ipConfiguration": {
          "authorizedNetworks": [],
          "ipv4Enabled": true
        },
        "locationPreference": {
          "zone": "us-central1-a",
          "kind": "sql#locationPreference"
        },
        "dataDiskType": "PD_SSD",
        "maintenanceWindow": {
          "kind": "sql#maintenanceWindow",
          "hour": 0,
          "day": 0
        },
        "backupConfiguration": {
          "startTime": "05:00",
          "kind": "sql#backupConfiguration",
          "location": "us",
          "enabled": true,
          "replicationLogArchivingEnabled": true,
          "pointInTimeRecoveryEnabled": true
        },
        "settingsVersion": "1",
        "storageAutoResizeLimit": "0",
        "storageAutoResize": true,
        "dataDiskSizeGb": "10"
      },
      "etag": "131aee0d1b7bbf054d5ba1bb09d7a1c197ad21bd8443208de6cc0f90820a131b",
      "ipAddresses": [
        {
          "type": "PRIMARY",
          "ipAddress": "34.72.111.112"
        }
      ],
      "serverCaCert": {
        "kind": "sql#sslCert",
        "certSerialNumber": "0",
        "cert": "-----BEGIN CERTIFICATE-----\nMIIDfzCCAmegAwIBAgIBADANBgkqhkiG9w0BAQsFADB3MS0wKwYDVQQuEyQwMWU3\nMzEyNS0yNDM3LTQwNWEtYjBmYi0wNzQyNWIzODkwMjQxIzAhBgNVBAMTGkdvb2ds\nZSBDbG91ZCBTUUwgU2VydmVyIENBMRQwEgYDVQQKEwtHb29nbGUsIEluYzELMAkG\nA1UEBhMCVVMwHhcNMjAwNzIyMDIwMzA1WhcNMzAwNzIwMDIwNDA1WjB3MS0wKwYD\nVQQuEyQwMWU3MzEyNS0yNDM3LTQwNWEtYjBmYi0wNzQyNWIzODkwMjQxIzAhBgNV\nBAMTGkdvb2dsZSBDbG91ZCBTUUwgU2VydmVyIENBMRQwEgYDVQQKEwtHb29nbGUs\nIEluYzELMAkGA1UEBhMCVVMwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIB\nAQCntNxShvSRHQHOaDg5Rna+9bE+MZC4HnCCzecNkzaIvl1//VtMyBaSMP6O4toI\n6tHTlFQTk7jaQZJRKnUFqamolYCjppQoKQsU7qNEFGWpNWlLrmxnM+RxgeUUihws\nR5MphnqwZCVmhPO8M1AZOfU85PZlldEF4gz/1INf93oZnCB/EYhbZqd6pLRjO9ic\nJbce2AibkrW8RVn16UjPnpSXV8nalhHLUPDNyP02fCH72BDqsXtD0T+xjydM0JnN\ngN448t/gyOSTDYdAAT5oRYVUeUp7kAD4itRjKMUieDHjYxlcbnJquaZJNJhTfeWx\naXaYJFDxHkrEjQmfo2TmBDfnAgMBAAGjFjAUMBIGA1UdEwEB/wQIMAYBAf8CAQAw\nDQYJKoZIhvcNAQELBQADggEBABrdxhl6JHT0YZHHbNUbXg32A8c1sNpepDLfJDgQ\n77WXQROAE01Eitzbh0Op4vyj/zkUMI02nBOJ5tdoR6dUNGEjDcZ4fO87PClaUFsn\nYvjCelIkdCfyvCBH/3pFCr5eHgwoHq9nD6XRgLYTiynTACyAsOm2Ug1eFYmp6YS0\nIdGriIOgxhzGzrU2OfSP+dET8DT8qgKfFBKFJKmKoIepDehjTAkM6tnB6BsOwo/S\nhBEcAZIrkyK3yWPp6ePUvCpOTZmmOdhCN1wySAubQn9KH3czYSN7u/BXhDmqi7z/\njtYt6mtcahDCZpvdIjhkBNQzgSTt4TzTLhAutt0KRTX3cHM=\n-----END CERTIFICATE-----",
        "commonName": "C=US,O=Google\\, Inc,CN=Google Cloud SQL Server CA,dnQualifier=01e73125-2437-405a-b0fb-07425b389024",
        "sha1Fingerprint": "a82bc9380e40750d7c6ddd6c05c227c05dfd2058",
        "instance": "ppp-test-instance-2",
        "createTime": "2020-07-22T02:03:05.608Z",
        "expirationTime": "2030-07-20T02:04:05.608Z"
      },
      "instanceType": "CLOUD_SQL_INSTANCE",
      "project": "ppp-test-283923",
      "serviceAccountEmailAddress": "p355491811298-gq2xhk@gcp-sa-cloud-sql.iam.gserviceaccount.com",
      "backendType": "SECOND_GEN",
      "selfLink": "https://www.googleapis.com/sql/v1beta4/projects/ppp-test-283923/instances/ppp-test-instance-2",
      "connectionName": "ppp-test-283923:us-central1:ppp-test-instance-2",
      "name": "ppp-test-instance-2",
      "region": "us-central1",
      "gceZone": "us-central1-a"
    }
  ]
}

"""