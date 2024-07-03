import ollama
import chromadb
import sys

MODEL = 'snowflake-arctic-embed:latest'
N_RESULTS = 5
#PROMPT = "bully who says 'Ha-ha!'"
if len(sys.argv) < 2:
  PROMPT = "bully who says 'Ha-ha!'"
else:
    PROMPT = sys.argv[1]
print(PROMPT)

client = chromadb.PersistentClient(path="./db")
collection = client.get_collection(name="docs")


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

# Print each item on a new line
for item in flat_list:
    print(item)
    
    
# evil genius
# tom cruise
# the godfather
# STEM professional
