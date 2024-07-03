# https://blog.bawolf.com/p/embeddings-are-a-good-starting-point
# https://github.com/chroma-core/chroma

import ollama
import chromadb
import re

MODEL = 'snowflake-arctic-embed:latest'
#CHUNK_SIZE = 250
#OVERLAP_SIZE = CHUNK_SIZE // 2
#file_path = './cofounder.txt'
file_path = './simpsons_opt.txt'


# Create chunks from the text with specified chunk size and overlap
def generic_create_chunks(file_path, chunk_size, overlap_size):
    with open(file_path, 'r') as file:
        text = file.read()
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

def cofounder_match_chunks(file_path):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Define the regex pattern to match timestamps
    pattern = re.compile(r'\d{1,2}:\d{2}[ap]m')
    
    # Split the content by the pattern
    chunks = pattern.split(content)
    
    # Add the delimiter (timestamp) back to each chunk
    timestamps = pattern.findall(content)
    
    # Combine the chunks and timestamps
    result = [chunk + (timestamp if i < len(timestamps) else '') 
              for i, (chunk, timestamp) in enumerate(zip(chunks, timestamps + ['']))]
    
    return result


def simpsons_chunks(file_path):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Define the regex pattern to match timestamps
    #pattern = re.compile(r'\d{1,2}.')
    pattern = re.compile(r'\b\d{1,2}\.')
    
    # Split the content by the pattern
    chunks = pattern.split(content)
    
    # Add the delimiter (timestamp) back to each chunk
    timestamps = pattern.findall(content)
    
    # Combine the chunks and timestamps
    result = [chunk + (timestamp if i < len(timestamps) else '') 
              for i, (chunk, timestamp) in enumerate(zip(chunks, timestamps + ['']))]
    
    return result

def simpsons_chunks_opt(file_path):
    # Read the contents of the file
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

#chunks = create_chunks(file_path, CHUNK_SIZE, OVERLAP_SIZE)

#chunks = cofounder_match_chunks(file_path)
#chunks = chunks[:-1] # cofounder hack

#chunks = simpsons_chunks(file_path)
chunks = simpsons_chunks(file_path)
chunks = chunks[1:] # simpsons

print(f"length of chunks: {len(chunks)}")
print(f"first chunk: {chunks[0]}")

# for i in range(len(chunks)):
#     print("\n\n NEW CHUNK \n\n")
#     print(f"chunk {i}: {chunks[i]}")
# print(chunks)

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