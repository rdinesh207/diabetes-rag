import os
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

PAPERS_DIR = os.path.join(os.path.dirname(__file__), "papers")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "diabetes-papers")
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
EMBEDDING_DIM = 384

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Check if index exists and has correct dimension, else recreate
index_exists = INDEX_NAME in pc.list_indexes().names()
if index_exists:
    desc = pc.describe_index(INDEX_NAME)
    current_dim = desc.dimension if hasattr(desc, 'dimension') else desc['dimension']
    if current_dim != EMBEDDING_DIM:
        print(f"Index '{INDEX_NAME}' has dimension {current_dim}, expected {EMBEDDING_DIM}. Deleting and recreating.")
        pc.delete_index(INDEX_NAME)
        index_exists = False

if not index_exists:
    pc.create_index(
        name=INDEX_NAME,
        dimension=EMBEDDING_DIM,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",  # or "gcp" if that's your deployment
            region=PINECONE_ENV or "us-west-2"
        )
    )
index = pc.Index(INDEX_NAME)

# Initialize embedding model
embedder = SentenceTransformer(EMBEDDING_MODEL)


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text


def chunk_text_with_overlap(text, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    # splitter expects a list of documents, but we have a single string
    docs = splitter.create_documents([text])
    return [doc.page_content for doc in docs]


def extract_metadata_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    meta = doc.metadata or {}
    # Title: Prefer PDF metadata, fallback to filename
    title = meta.get('title') or os.path.splitext(os.path.basename(pdf_path))[0]
    # Journal: Try PDF metadata, else try to heuristically extract from first page
    journal = meta.get('journal')
    if not journal:
        first_page_text = doc[0].get_text() if doc.page_count > 0 else ""
        # Heuristic: look for lines with 'journal' or similar
        for line in first_page_text.split('\n'):
            if 'journal' in line.lower():
                journal = line.strip()
                break
        if not journal:
            journal = "Unknown Journal"
    # URL: Not available, so set to '#'
    url = meta.get('url', '#')
    doc.close()
    return title, journal, url


def upsert_pdf_to_pinecone(pdf_path, index):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text_with_overlap(text)
    title, journal, url = extract_metadata_from_pdf(pdf_path)
    vectors = []
    for i, chunk in enumerate(chunks):
        embedding = embedder.encode(chunk).tolist()
        vector_id = f"{os.path.basename(pdf_path)}-chunk-{i}"
        vectors.append((vector_id, embedding, {
            "text": chunk,
            "title": title,
            "journal": journal,
            "url": url
        }))
    if vectors:
        index.upsert(vectors)
        print(f"Upserted {len(vectors)} chunks from {os.path.basename(pdf_path)} to Pinecone.")


def ingest_local_pdfs(papers_dir, index):
    pdf_files = [f for f in os.listdir(papers_dir) if f.lower().endswith('.pdf')]
    for pdf_file in pdf_files:
        pdf_path = os.path.join(papers_dir, pdf_file)
        upsert_pdf_to_pinecone(pdf_path, index)


if __name__ == "__main__":
    ingest_local_pdfs(PAPERS_DIR, index)
