from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_file_chunks(input_list):
    #the model takes in the documented chunks  and turns each chunk into a list of numbers called an vector.That vector represents the overall meaning of the chunk.
    embedded_contents = model.encode(input_list)
    return embedded_contents
def embed_user_query(user_query):
    embedded_user_query = model.encode([user_query])
    return embedded_user_query

