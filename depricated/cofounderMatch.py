import re


import ollama
import chromadb


MODEL = 'snowflake-arctic-embed:latest'
#CHUNK_SIZE = 250
#OVERLAP_SIZE = CHUNK_SIZE // 2



def split_by_timestamp(file_path):
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
'''
TO CREATE: 
'''

file_path = './cofounder.txt'
chunks = split_by_timestamp(file_path)
chunks = chunks[:-1]
embed(MODEL, chunks, collection)

'''
TO RUN
'''


#collection = client.get_collection(name="docs")


# Example usage




prompt = "i love jeff bezos"
N_RESULTS = 2

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