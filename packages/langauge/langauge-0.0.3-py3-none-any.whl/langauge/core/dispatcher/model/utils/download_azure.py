# Copyright (c) FlapMX LLC.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import os
import tarfile

from azure.storage.blob import BlobServiceClient

# IMPORTANT: Replace connection string with your storage account connection string
# Usually starts with DefaultEndpointsProtocol=https;...
MY_CONNECTION_STRING = os.environ.get("MY_CONNECTION_STRING")

# Replace with blob container
MY_BLOB_CONTAINER = "ner"

# Replace with the local folder where you want files to be downloaded
LOCAL_BLOB_PATH = "/models"


class AzureBlobFileDownloader:
    def __init__(self):
        print("Intializing AzureBlobFileDownloader")
        # Initialize the connection to Azure storage account
        self.blob_service_client = BlobServiceClient(account_url="https://langauge.blob.core.windows.net")
        self.my_container = self.blob_service_client.get_container_client(MY_BLOB_CONTAINER)

    def save_and_extract_blob(self, file_name, file_content):
        # Get full path to the file
        download_file_path = os.path.join(LOCAL_BLOB_PATH, file_name)
        # for nested blobs, create local path as well!
        os.makedirs(os.path.dirname(download_file_path), exist_ok=True)
        with open(download_file_path, "wb") as file:
            file_content.readinto(file)
        tar = tarfile.open(download_file_path)
        tar.extractall(LOCAL_BLOB_PATH)
        tar.close()
        os.remove(download_file_path)

    def download_blobs_in_container(self, file_name):
        my_blobs = self.my_container.list_blobs(name_starts_with=file_name)
        for blob in my_blobs:
            blob_data = self.my_container.get_blob_client(blob).download_blob()
            self.save_and_extract_blob(blob.name, blob_data)
