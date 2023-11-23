from azure.storage.blob import BlobServiceClient
import os
from json import load

with open('config.json', 'r') as file:
    config = load(file)


def upload_to_blob(file_name_info, blob_name):
    CONNECTION_STRING = config.get('CONNECTION_STRING')
    CONTAINER_NAME = config.get('CONTAINER_NAME')

    # Init BlobServiceClient with connection string
    blob_service_client = BlobServiceClient.from_connection_string(
        CONNECTION_STRING)

    # Get BlobClient
    blob_client = blob_service_client.get_blob_client(
        CONTAINER_NAME, blob=blob_name)

    # open and read file
    with open(file_name_info, 'r') as file:
        data = file.read()

    # upload data
    blob_client.upload_blob(data)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(parent_dir, 'data')
    file = os.listdir(data_dir)[-1]
    file_name_info = os.path.join(parent_dir, 'data', file)
    blob_name = 'info.json'
    upload_to_blob(file_name_info, blob_name)


if __name__ == '__main__':
    main()
