import bytewax.operators as op
from bytewax.connectors.stdio import StdOutSink
from bytewax.dataflow import Dataflow
from bytewax.testing import TestingSource
from rag.json_source import JSONSource
from rag.models import RawPost, ChunkedPost,EmbeddedChunkedPost
from typing import Optional, Tuple, Union
from pydantic import BaseModel
from rag.embeddings import EmbeddingModelSingleton
from rag.pinecone_vs import PineconeVectorOutput
def _build_output(model: EmbeddingModelSingleton, in_memory: bool = False):
    # if in_memory:
    #     return PineconeVectorOutput(
    #         vector_size=model.embedding_size,
    #         client=QdrantClient(":memory:"),
    #     )
    # else:
        # return PineconeVectorOutput(
        #     vector_size=model.embedding_size,
        # )
        return PineconeVectorOutput(
            vector_size=model.embedding_size,
        )

# class RawPost(BaseModel):
#     post_id: str
#     text: str
#     image: Optional[str]

#     @classmethod
#     def from_source(cls, k_v: Tuple[str, dict]) -> "RawPost":
#         k, v = k_v  

#         return cls(post_id=k, text=v["text"], image=v.get("image", None))
embedding_model = EmbeddingModelSingleton()

flow = Dataflow("flow")

stream = op.input("input", flow, JSONSource(["C:/Users/vaibh/OneDrive/Desktop/veritus/Veritus_RAG/rag/data/JSON/Book_TextHeavy.json"]))


stream = op.map("raw_post", stream, RawPost.from_source)

# stream = op.map("cleaned_post", stream, CleanedPost.from_raw_post)
stream = op.flat_map(
        "chunked_post",
        stream,
        lambda raw_post: ChunkedPost.from_cleaned_post(
            raw_post, embedding_model=embedding_model
        ),
    )

stream = op.map(
        "embedded_chunked_post",
        stream,
        lambda chunked_post: EmbeddedChunkedPost.from_chunked_post(
            chunked_post, embedding_model=embedding_model
        ),
    )



op.output(
        "output", stream, _build_output(model=embedding_model, in_memory=False)
    )

op.inspect("inspect", stream, print)




# flow = Dataflow("a_simple_example")

# stream = op.input("input", flow, TestingSource(range(10)))

# op.inspect("inspect", stream, print)

# def times_two(inp: int) -> int:
#     return inp * 2


# double = op.map("double", stream, times_two)

#op.output("out", double, StdOutSink())