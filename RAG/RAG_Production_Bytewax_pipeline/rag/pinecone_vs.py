import os
from typing import Optional

from bytewax.outputs import DynamicSink, StatelessSinkPartition
from rag.settings import settings
from rag.models import EmbeddedChunkedPost
from pinecone import Pinecone
from pinecone import ServerlessSpec

class PineconeVectorOutput(DynamicSink):
    """A class representing a Qdrant vector output.

    This class is used to create a Qdrant vector output, which is a type of dynamic output that supports
    at-least-once processing. Messages from the resume epoch will be duplicated right after resume.

    Args:
        vector_size (int): The size of the vector.
        collection_name (str, optional): The name of the collection.
            Defaults to settings.VECTOR_DB_OUTPUT_COLLECTION_NAME.
        client (Optional[QdrantClient], optional): The Qdrant client. Defaults to None.
    """

    def __init__(
        self,
        vector_size: int,
        #collection_name: str = settings.VECTOR_DB_OUTPUT_COLLECTION_NAME,
        index_name: str = settings.VECTOR_DB_OUTPUT_INDEX_NAME,
        # client: Optional[PineconeClient] = None,
        client = None
    ):
        #self._collection_name = collection_name
        self._index_name = index_name
        self._vector_size = vector_size

        if client:
            self.client = client
        else:
            self.client = build_pinecone_client()

        # try:
        #     self.client.index(index_name=self._index_name)
        # except ValueError:
        #     self.client.create_index(
        #                                 index_name,
        #                                 dimension=self._vector_size,  # dimensionality of text-embedding-ada-002
        #                                 metric='cosine',
        #                                 spec= ServerlessSpec(cloud='aws', region='us-east-1')
        #                             )
        spec = ServerlessSpec(cloud='aws', region='us-east-1')
        if self._index_name not in self.client.list_indexes().names():
                # if does not exist, create index
                self.client.create_index(
                    self._index_name,
                    dimension=self._vector_size,  # dimensionality of text-embedding-ada-002
                    metric='cosine',
                    spec=spec
                )
        print(self.client.Index(self._index_name).describe_index_stats())

        #     # (
            #     collection_name=self._collection_name,
            #     vectors_config=VectorParams(
            #         size=self._vector_size, distance=Distance.COSINE
            #     ),
            # )

    def build(self, step_id, worker_index , worker_count) -> "PineconeVectorSink":
        """Builds a QdrantVectorSink object.

        Args:
            worker_index (int): The index of the worker.
            worker_count (int): The total number of workers.

        Returns:
            PineconeVectorSink: A PineconeVectorSink object.
        """

        return PineconeVectorSink(client=self.client, index_name=self._index_name)


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
    # if url is None:
    #     try:
    #         url = os.environ["PINECONE_URL"]
    #     except KeyError:
    #         raise KeyError(
    #             "PINECONE_URL must be set as environment variable or manually passed as an argument."
    #         )
    # client_kwargs["url"] = url

    # if api_key is None:
    #     api_key = os.environ.get("PINECONE_API_KEY")
    # if api_key:
    #     client_kwargs["url"] = url

    #client = Pinecone(**client_kwargs)

    client = Pinecone(api_key = settings.PINECONE_API_KEY)

    return client

class PineconeVectorSink(StatelessSinkPartition):
    """
    A sink that writes document embeddings to a Qdrant collection.

    Args:
        client (QdrantClient): The Qdrant client to use for writing.
        collection_name (str, optional): The name of the collection to write to.
            Defaults to settings.VECTOR_DB_OUTPUT_COLLECTION_NAME.
    """

    def __init__(
        self,
        client = None,
        #vector_size: int,
        #collection_name: str = settings.VECTOR_DB_OUTPUT_COLLECTION_NAME,
        index_name: str = settings.VECTOR_DB_OUTPUT_INDEX_NAME
    ):
        self._client = build_pinecone_client()
        self._index_name = index_name

    def write_batch(self, chunks: list[EmbeddedChunkedPost]):
        #ids = []
        #embeddings = []
        #metadata = []
        print("Writing Batch")
        vectors = []  ## optimize it
        for chunk in chunks:
            chunk_id, text_embedding, chunk_metadata = chunk.to_payload()
            print(chunk_metadata)
            vector = {"id": "", "values": [],"metadata": {}}
            vector["id"] = chunk_id
            vector["values"] = text_embedding
            vector["metadata"] = chunk_metadata
            #ids.append(chunk_id)
            #embeddings.append(text_embedding)
            vectors.append(vector)
            #metadata.append(chunk_metadata)
        
    #     vectors=[
    # {
    #   "id": "A", 
    #   "values": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], 
    #   "metadata": {"genre": "comedy", "year": 2020}
    # },

        ##vectors = [("id1", [0.1, 0.2, 0.3]), ("id2", [0.4, 0.5, 0.6])]
        ##metadata = [("metadata1",), ("metadata2",)]
        self._client.Index(name= self._index_name).upsert(
            index_name=self._index_name,
            vectors=vectors,
            # metadata=metadata,
            # overwrite=True,
            # routing_key=None,
            # timeout_sec=30,
            # wait=True
            ),
