from pinecone import Pinecone
from typing import Optional
import os

pc = Pinecone(api_key='1c4787e9-eb8c-4252-8b8c-f0a03a77ab8a')


from pinecone import ServerlessSpec

cloud =  'aws'
region = 'us-east-1'

spec = ServerlessSpec(cloud=cloud, region=region)
index_name = 'veritusrag'
# check if index already exists (it shouldn't if this is first time)
if index_name not in pc.list_indexes().names():
    # if does not exist, create index
    pc.create_index(
        index_name,
        dimension=384,  # dimensionality of text-embedding-ada-002
        metric='cosine',
        spec=spec
    )
    
# connect to index
index = pc.Index(index_name)
# pc.delete_index(index_name)
# view index stats
print(index.describe_index_stats())

# for ids in index.list():
#     print(ids)

#print(index.fetch(ids=["00c579fb1d20275752acbcd6f6772d94", "3f5b9f793331ebe2b60aa5aab5169abc"]))

# index_description = pc.describe_index("pdfsdev")




def build_pinecone_client(url: Optional[str] = None, api_key: Optional[str] = None):
    """
    Builds a PineconeClient object with the given URL and API key.

    Args:
        url (Optional[str]): The URL of the Qdrant server. If not provided,
            it will be read from the QDRANT_URL environment variable.
        api_key (Optional[str]): The API key to use for authentication. If not provided,
            it will be read from the QDRANT_API_KEY environment variable.

    Raises:
        KeyError: If the QDRANT_URL or QDRANT_API_KEY environment variables are not set
            and no values are provided as arguments.

    Returns:
        QdrantClient: A QdrantClient object connected to the specified Qdrant server.
    """

    client_kwargs = {}
    if url is None:
        try:
            url = os.environ["PINECONE_URL"]
        except KeyError:
            raise KeyError(
                "PINECONE_URL must be set as environment variable or manually passed as an argument."
            )
    client_kwargs["url"] = url

    if api_key is None:
        api_key = os.environ.get("PINECONE_API_KEY")
    if api_key:
        client_kwargs["url"] = url

    client = Pinecone(**client_kwargs)

    return client

