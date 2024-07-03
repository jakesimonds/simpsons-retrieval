# https://blog.bawolf.com/p/embeddings-are-a-good-starting-point
# https://github.com/chroma-core/chroma

import ollama
import chromadb


MODEL = 'snowflake-arctic-embed:latest'
CHUNK_SIZE = 50  # Define your chunk size here
OVERLAP_SIZE = CHUNK_SIZE // 2  # Overlap size is half of the chunk size

# Read text from a file
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Create chunks from the text with specified chunk size and overlap
def create_chunks(text, chunk_size, overlap_size):
    chunks = []
    length = len(text)
    
    for i in range(0, length, chunk_size):
        chunk = text[i:i + chunk_size]
        if len(chunk) == chunk_size:
            chunks.append(chunk)

    for i in range(overlap_size, length, chunk_size):
        chunk = text[i:i + chunk_size]
        if len(chunk) == chunk_size:
            chunks.append(chunk)

    return chunks

# Path to your text file
file_path = './employee.txt'
text = read_text_file(file_path)

# Create chunks from the text
chunks = create_chunks(text, CHUNK_SIZE, OVERLAP_SIZE)
client = chromadb.Client()
collection = client.create_collection(name="docs")


for i, d in enumerate(chunks):
  response = ollama.embeddings(model=MODEL, prompt=d)
  embedding = response["embedding"]
  collection.add(
    ids=[str(i)],
    embeddings=[embedding],
    documents=[d]
 )

# an example prompt
prompt = "time off"

# generate an embedding for the prompt and retrieve the most relevant doc
response = ollama.embeddings(
  prompt=prompt,
  model=MODEL
)
results = collection.query(
  query_embeddings=[response["embedding"]],
  n_results=1
)
data = results['documents']

print(data)