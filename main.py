from Building_Model import answer_with_rag, build_prompt
from Document_work import extract_chunks
from retrieve import retrieve
from Embeddings_work import embed_user_query, embed_file_chunks
from store import store_document,list_documents,delete_document

class OllamaChatBot:
    def __init__(self,model="llama3.2"):
        self.model=model
    def ask_question(self, question):
        """Ask a question about the document"""
        q_emb= embed_user_query(question)[0]#embeds user query  into a vector
        print("q_emb:",q_emb)
        rows=retrieve(q_emb,k=5)#rows contains the most similar parts that could lead to the answer to the most dissimilar ones
        print("rows:",rows)
        if len(rows)==0:
            return "I don't have info on that in the uploaded documents",[]
        #the above row is in this order:filename,chunk_index,chunk_text,distance,below we only take actual chunk text
        words=[row[2] for row in rows]
        print("words:",words)
        context_string='\n'.join(words)
        print("context_string:",context_string)
        prompt=build_prompt(question,context_string)
        return answer_with_rag(prompt,self.model),rows
    def add_document(self,filename,source):
        chunks=extract_chunks(source)
        if not chunks:
            return 0
        chunk_embeds=embed_file_chunks(chunks)
        store_document(filename,chunks,chunk_embeds)
        return len(chunks)
    def list_docs(self):
        return list_documents()
    def delete_doc(self,filename):
        return delete_document(filename)