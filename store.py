from db import get_conn
def store_document(filename,chunks,embeddings):
    conn=get_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute('''
                insert into documents(filename) values (%s)
                on conflict (filename) do update set uploaded_at=now()
                returning id''',(filename,),)
                doc_id=cur.fetchone()[0]
                cur.execute('''
                delete from chunks where document_id=%s''',(doc_id,))
                for i,(text,vec) in enumerate(zip(chunks,embeddings)):#pairs each chunk
                    # of text with its own vector,so the first chunk gets the first
                    # embedding and so on.
                    cur.execute('''
                        insert into chunks(document_id,chunk_index,chunk_text,embedding) 
                        values (%s,%s,%s,%s::vector)
                ''',(doc_id,i,text,str(vec.tolist())))
        return doc_id
    finally:
        conn.close()
def list_documents():
    conn=get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute('''
            select  documents.filename,count(chunks.id) from documents left join chunks on chunks.document_id=documents.id 
            group by documents.id,documents.filename
            order by documents.uploaded_at desc 
            ''')
            return cur.fetchall()
    finally:
        conn.close()
def delete_document(filename):
    conn=get_conn()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute('''delete from documents where filename=%s returning id
                ''',(filename,))
                return cur.fetchone() is not None
    finally:
        conn.close()