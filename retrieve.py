from db import get_conn

def retrieve(query_vec,k=3,max_distance=0.9):
    vec=str(query_vec.tolist())
    conn=get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute('''select documents.filename,chunks.chunk_index,chunks.chunk_text,
            chunks.embedding<=>%s::vector as distance from chunks join documents on documents.id=chunks.document_id
            where chunks.embedding<=>%s::vector<%s
            order by distance limit %s''',(vec,vec,max_distance,k))
            return cur.fetchall()
    finally:
        conn.close()
# <=> = Cosine distance: measures how dissimilar two vectors are based on the angle smaller distance mean more similar meaning.
#The above sql query  calculates up to k document chunks whose embedding
# is closer than max_distance to the query embedding.
# Results are ordered from most similar to least similar