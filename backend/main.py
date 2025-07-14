from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from embed import get_relevant_docs, build_prompt, query_llm

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str
    model: str = "llm"  # Optional, defaults to 'llm'. Accepts 'llm' or 'gemini'

class AnswerResponse(BaseModel):
    answer: str
    citations: list

@app.post("/api/ask", response_model=AnswerResponse)
def ask(query: Query):
    relevant_docs = get_relevant_docs(query.question, n_results=5)
    context = "\n\n".join([doc["document"] for doc in relevant_docs["documents"][0]])
    prompt = build_prompt(context, query.question)
    if hasattr(query, 'model') and query.model == "gemini":
        from embed import query_gemini
        answer = query_gemini(prompt)
    else:
        answer = query_llm(prompt)
    # print(f"Answer: {llm_answer}")
    # print(f"Citations: {relevant_docs['metadatas'][0]}")
    return AnswerResponse(answer=answer, citations=relevant_docs["metadatas"][0]) 

