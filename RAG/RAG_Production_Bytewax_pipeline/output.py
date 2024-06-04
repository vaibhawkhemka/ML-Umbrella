from rag.embeddings import EmbeddingModelSingleton, CrossEncoderModelSingleton
from rag.pinecone_vs import build_pinecone_client
from rag.retrieve import PineconeVectorDBRetriever


embedding_model = EmbeddingModelSingleton()
cross_encoder_model = CrossEncoderModelSingleton()
pinecone_client = build_pinecone_client()

vector_db_retriever = PineconeVectorDBRetriever(
    embedding_model=embedding_model,
    vector_db_client=pinecone_client,
    cross_encoder_model=cross_encoder_model,
)

query_question = "Who is Eric Berne?"
retrieved_results = vector_db_retriever.search(query=query_question, limit=3, return_all=True)
for post in retrieved_results["posts"]:
    vector_db_retriever.render_as_text(post)
    #print(post)
