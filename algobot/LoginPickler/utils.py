from azure.storage.blob import BlobServiceClient,ContainerClient


def upload_pickle_to_blob(pkl):
    BLOB_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=automation9e98;AccountKey=lePx6UTRq6nZPFF4Cg3VHDT1m1R5RqAklPRcU6960idIwtsvGr6L5a+iUexLuEegrUmHUij002iT+AStbuIPxA==;EndpointSuffix=core.windows.net"
    try:
        bsc = BlobServiceClient.from_connection_string(BLOB_STORAGE_CONNECTION_STRING)
    except:
        pass

    if bsc:
        # get Container Client cc
        try:
            cc = BlobServiceClient.get_container_client('data')
        except:
            pass
    
    if cc:
        cc.upload_blob(pkl)