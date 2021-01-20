from google.cloud import secretmanager

class CloudSecrets():

    @staticmethod
    def get_cloud_secret(project_id, secret_name):

        secret_client = secretmanager.SecretManagerServiceClient()
        project_id = project_id
        # Can instead use a numbered version, e.g. 1, 2, 3, etc.
        version = "latest"

        request = {
            "name": f"projects/{project_id}/secrets/{secret_name}/versions/{version}"}
        response = secret_client.access_secret_version(request)
        return response.payload.data.decode("UTF-8")