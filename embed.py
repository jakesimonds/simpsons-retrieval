import ollama
import chromadb
import re

MODEL = 'snowflake-arctic-embed:latest'
file_path = './simpsons_opt.txt'

def simpsons_chunks_opt(file_path):
    with open(file_path, 'r') as file:
        content = file.read()    
    chunks = content.split('\n')
    return chunks

def embed(MODEL, chunks, collection):
    for i, d in enumerate(chunks):
        response = ollama.embeddings(model=MODEL, prompt=d)
        embedding = response["embedding"]
        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[d]
        )

client = chromadb.PersistentClient(path="./db")
collection = client.create_collection(name="docs")

chunks = simpsons_chunks_opt(file_path)
#chunks = chunks[1:] # simpsons

embed(MODEL, chunks, collection)




prompt = "STEM professional"
N_RESULTS = 3

response = ollama.embeddings(
  prompt=prompt,
  model=MODEL
)
results = collection.query(
  query_embeddings=[response["embedding"]],
  n_results=N_RESULTS
)
data = results['documents']

#print(data)

flat_list = [item for sublist in data for item in sublist]

# Print each item on a new line
for item in flat_list:
    print(item)