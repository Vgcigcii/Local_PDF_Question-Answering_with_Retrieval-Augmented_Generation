import ollama#its a open source software platform that lets you download,run and manage llm direclty on your pc
def build_prompt(query, relevant_context=""):# this functions tells the model as to how to respond to the context and the question
    return f"""You are a careful assistant answering questions about a document.
                Rules:
                - Use ONLY the context below. Do not use outside knowledge.
                - If the question asks for a list, include only items that appear in the context, exactly as written. Never add items that are not there.
                - If the context does not contain the answer, reply exactly: I don't know based on the provided documents.
                
                Context:
                {relevant_context}
        
                Question: {query}
                Answer:"""
# Context:
# {relevant_context}#this is the information that it receives from which it has to answer.
# Question: {query}#This is the question we ask.
#                 Answer:"""
def answer_with_rag(prompt,model="llama3.2"):
    try:
        response=ollama.chat(
            model=model,
            messages = [{"role":"user","content":prompt}],# this line sends our prompt to Ollama as a chat msg
            options={
             "temperature":0,#Temperature controls the randomness and creativity of the model's output.
              "top_k":40,#The model picks ups the top 40 most likely tokens
            }
        )
        return response["message"]["content"]
    except Exception as e:
        print(e)
