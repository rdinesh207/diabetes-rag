import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch
import requests

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "diabetes-papers")
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)
# Check if index exists, create if not
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,  # EMBEDDING_DIM, hardcoded for now
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",  # or "gcp" if that's your deployment
            region=PINECONE_ENV or "us-west-2"
        )
    )
index = pc.Index(INDEX_NAME)

# Embedding model (biomedical or general)
embedder = SentenceTransformer(EMBEDDING_MODEL)

# LLM pipeline/model (correct for CausalLM)
# model_name = "microsoft/MediPhi-PubMed"
# model = AutoModelForCausalLM.from_pretrained(
#     model_name,
#     device_map="cuda" if torch.cuda.is_available() else "cpu",
#     torch_dtype="auto",
#     trust_remote_code=True,
# )
# tokenizer = AutoTokenizer.from_pretrained(model_name)
#
# llm_pipeline = pipeline(
#     "text-generation",
#     model=model,
#     tokenizer=tokenizer,
# )

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

def ollama_generate(prompt, model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, max_tokens=500):
    url = f"{base_url}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": max_tokens}
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    return data.get("response", "")

# Gemini API setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('models/gemini-2.0-flash')

model = SentenceTransformer(EMBEDDING_MODEL)

def preprocess_and_embed(texts):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.create_documents(texts)
    embeddings = model.encode([chunk.page_content for chunk in chunks])
    return chunks, embeddings

def add_to_chromadb(chunks, embeddings):
    # This function is no longer used as ChromaDB is removed, but kept for now
    # as it might be re-introduced or refactored later.
    pass

def embed_text(text):
    return embedder.encode([text])[0]

def get_relevant_docs(query, n_results=5):
    query_vec = embed_text(query)
    results = index.query(vector=query_vec.tolist(), top_k=n_results, include_metadata=True)
    docs = []
    metadatas = []
    for match in results['matches']:
        docs.append({"document": match['metadata'].get('text', '')})
        metadatas.append({
            "title": match['metadata'].get('title', 'Unknown Title'),
            "journal": match['metadata'].get('journal', 'Unknown Journal'),
            "url": match['metadata'].get('url', '#'),
            "relevance": match.get('score', 0.8)
        })
    return {"documents": [docs], "metadatas": [metadatas]}

def build_prompt(context, question):
    return f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"

def query_llm(prompt):
    raw_answer = ollama_generate(prompt)

    # --- Post-processing for a cleaner answer ---
    # 1. If the model returns multiple Q&A pairs, keep only the first answer.
    # 2. Remove any trailing "Question:" or "Answer:" blocks.
    # 3. Strip leading/trailing whitespace.

    # Find the first occurrence of "Answer:" and take everything after it
    if "Answer:" in raw_answer:
        answer = raw_answer.split("Answer:")[-1]
    else:
        answer = raw_answer

    # Remove any subsequent "Question:" or "Answer:" blocks
    for marker in ["Question:", "Answer:"]:
        if marker in answer:
            answer = answer.split(marker)[0]

    # Clean up whitespace
    answer = answer.strip()

    return answer

def query_gemini(prompt):
    # Use Gemini model to generate a response
    response = gemini_model.generate_content(prompt)
    raw_answer = response.text if hasattr(response, 'text') else str(response)

    # --- Post-processing for a cleaner answer ---
    # 1. If the model returns multiple Q&A pairs, keep only the first answer.
    # 2. Remove any trailing "Question:" or "Answer:" blocks.
    # 3. Strip leading/trailing whitespace.

    # Find the first occurrence of "Answer:" and take everything after it
    if "Answer:" in raw_answer:
        answer = raw_answer.split("Answer:")[-1]
    else:
        answer = raw_answer

    # Remove any subsequent "Question:" or "Answer:" blocks
    for marker in ["Question:", "Answer:"]:
        if marker in answer:
            answer = answer.split(marker)[0]

    # Clean up whitespace
    answer = answer.strip()

    return answer

def main():
    # Example: ingest and embed a sample text
    texts = ["Sample diabetes research text for embedding."]
    chunks, embeddings = preprocess_and_embed(texts)
    add_to_chromadb(chunks, embeddings)
    print(f"Added {len(chunks)} chunks to ChromaDB.")

if __name__ == "__main__":
    main() 