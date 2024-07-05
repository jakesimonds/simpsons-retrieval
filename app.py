
import chromadb
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import ollama  # Ensure you have the correct import for your model

import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / '.env'  # Adjust the path as necessary
load_dotenv(dotenv_path=env_path)




app = FastAPI()

# NOTE: working right now, am not addressing that I send data to another computer
origins = [
    "http://localhost:3000",  # frontend
    "http://localhost:3001"   # backend
    "http://localhost:5000"   # llama
    "http://localhost:5555"   # ????
    "http://10.244.208.173"
    
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
async def test(request: Request):
    print("HIT /test in fastAPI llama server")
    return {"message": "Hello World"}

@app.post("/query")
async def query(request: Request):
    print("HIT /query in fastAPI llama server")
    data = await request.json()
    print(data)
    PROMPT = data['text']
    #PROMPT = 'STEM professional'

    print(PROMPT)

    client = chromadb.PersistentClient(path="./db")
    collection = client.get_collection(name="docs")

    '''
    TO BE REPLACED WITH API CALL...
    '''
    MODEL = 'snowflake-arctic-embed:latest'
    N_RESULTS = 3
    response = ollama.embeddings(
    prompt=PROMPT,
    model=MODEL
    )
    results = collection.query(
    query_embeddings=[response["embedding"]],
    n_results=N_RESULTS
    )
    data = results['documents']


    flat_list = [item for sublist in data for item in sublist]
    #print(data)
    return {"result": data}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



