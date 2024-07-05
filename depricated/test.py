import ollama
import chromadb
import sys

print(chromadb.__version__)

PROMPT = 'bully who says "Ha-ha!"'
MODEL = 'snowflake-arctic-embed:latest'


response = ollama.embeddings(
  prompt=PROMPT,
  model=MODEL
)


print(response)
print(len(response['embedding']))
