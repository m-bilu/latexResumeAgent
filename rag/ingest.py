import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import CohereEmbeddings
from pylatexenc.latex2text import LatexNodes2Text

import os

COHERE_API_KEY=os.environ['COHERE_API_KEY']

LATEX_FOLDER = "../resume_templates"

def latex_to_text(file_path):
    with open(file_path, "r") as f:
        latex_code = f.read()
    return LatexNodes2Text().latex_to_text(latex_code)

def main():
    texts = []
    metadatas = []

    for filename in os.listdir(LATEX_FOLDER):
        if filename.endswith(".tex"):
            raw_text = latex_to_text(os.path.join(LATEX_FOLDER, filename))
            texts.append(raw_text)
            metadatas.append({"source": filename})

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.create_documents(texts, metadatas=metadatas)

    vectorstore = Chroma.from_documents(
        chunks,
        embedding=CohereEmbeddings(cohere_api_key=COHERE_API_KEY),
        persist_directory="../vectorstore"
    )

    vectorstore.persist()

if __name__ == "__main__":
    main()

