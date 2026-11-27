import streamlit as st
from main import OllamaChatBot  # Import your main class

st.title("Multiple Document Explainer Chatbot")
st.markdown("Upload PDFs and chat with your documents using local Ollama")

# Initialize the bot (only once)
if "bot" not in st.session_state:
    st.session_state.bot = OllamaChatBot()
bot = st.session_state.bot

# File uploader
uploaded_file = st.file_uploader("Upload PDF document", type="pdf")

if uploaded_file is not None:
    if st.button("Process Document"):
        with st.spinner("Processing..."):
            n=bot.add_document(uploaded_file.name,uploaded_file)
        if n:
            st.success(f"Stored {n} chunks")
        else:
            st.error("Failed to process PDF")
if "pending_delete" not in st.session_state:
    st.session_state.pending_delete = None
with st.sidebar:
    st.header("Stored documents")
    docs = bot.list_docs()
    if not docs:
        st.caption("No documents found")
    for filename, n_chunks in docs:
        st.write(f"{filename} ({n_chunks} chunks)")
        if st.button("Delete", key=f"del_{filename}"):
            st.session_state.pending_delete = filename

    pending = st.session_state.pending_delete
    if pending:
        st.warning(f"Delete {pending} and all its chunks?")
        col1, col2 = st.columns(2)
        if col1.button("Confirm", key="confirm_delete"):
            bot.delete_doc(pending)
            st.session_state.pending_delete = None
            st.rerun()
        if col2.button("Cancel", key="cancel_delete"):
            st.session_state.pending_delete = None
            st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about the document"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response,rows = bot.ask_question(prompt)
            st.markdown(response)
            if rows:
                with st.expander("Sources"):
                    for r in rows:
                        st.write(f"{r[0]}(chunk {r[1]},distance{r[3]:.2f})")
    st.session_state.messages.append({"role": "assistant", "content": response})