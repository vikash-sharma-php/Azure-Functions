import logging
from azure.storage.blob import BlobServiceClient,ContainerClient,ContentSettings


def upload_pickle_to_blob(pkl):

    BLOB_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=automation9e98;AccountKey=lePx6UTRq6nZPFF4Cg3VHDT1m1R5RqAklPRcU6960idIwtsvGr6L5a+iUexLuEegrUmHUij002iT+AStbuIPxA==;EndpointSuffix=core.windows.net"
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
        