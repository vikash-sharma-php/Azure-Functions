import logging
from azure.storage.blob import BlobServiceClient,ContainerClient,ContentSettings,BlobClient

def upload_pickle_to_blob(pkl):

    BLOB_STORAGE_CONNECTION_STRING = "---------------------------------------------------------------------------------------------"
    # BLOB_STORAGE_CONNECTION_STRING = "UseDevelopmentStorage=true;DevelopmentStorageProxyUri=http://azurite"
    try:
        bsc = BlobServiceClient.from_connection_string(BLOB_STORAGE_CONNECTION_STRING)
    except Exception as e:
        logging.error(e)

    if bsc:
        # get Container Client cc
        try:
            cc = bsc.get_container_client(container='data')
        except Exception as e:
            logging.error(e)
    
    content_settings = ContentSettings(content_type='application/octect-stream')
    try:
        if cc is not None:
            cc.upload_blob(data=pkl)
    except Exception as e:
        logging.error(e)
        
