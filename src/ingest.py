import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():

    if not PDF_PATH:
        print("PDF_PATH não está definido no arquivo .env")
        return

    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)
    if not chunks:
        raise ValueError("Nenhum texto foi extraído do PDF.")
    
    print(f"Número de chunks criados: {len(chunks)}")

    enriched =[
        Document(
            page_content=document.page_content,
            metadata={k: v for k, v in document.metadata.items() if v not in ("", None)},
        )
        for document in chunks
    ]

    ids = [f"doc-{i}" for i in range(len(enriched))]
    
    embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001"))
    pgvector = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )
    pgvector.add_documents(enriched, ids=ids)
    print("Ingestão concluída com sucesso.")
if __name__ == "__main__":
    ingest_pdf()