from langchain.vectorstores import Chroma
from langchain.embeddings import CohereEmbeddings
import os

COHERE_API_KEY=os.environ['COHERE_API_KEY']

def query_vectorstore(query: str, k=5):
    db = Chroma(
        persist_directory="../vectorstore",
        embedding_function=CohereEmbeddings(cohere_api_key=COHERE_API_KEY)
    )

    results = db.similarity_search(query, k=k)
    return [r.page_content for r in results]

if __name__ == "__main__":
    query = "backend developer experience with AWS and Docker"
    examples = query_vectorstore(query)
    for ex in examples:
        print("---------")
        print(ex)
