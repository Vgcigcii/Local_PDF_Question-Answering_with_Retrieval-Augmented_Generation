from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

def extract_chunks(source):
    if not source:
        return []
    try:
        reader = PdfReader(source)  # accepts a path string or an uploaded file object
        if reader.is_encrypted:#checks if the file is encrypted
            print("The file is encrypted")
            return []
        reader=PdfReader(source)
        full_text=""#stores full text
        #reader.pages holds the entire PDF.It knows metadata,encryption status,and holds a list of all  pages inside reader.pages
        for page_num,page in enumerate(reader.pages,1):
            #reader.pages pulls out one single page at a time from the reader.
            page_text=page.extract_text()#pull the readable words and strings off that specific page.
            if page_text:
                full_text+=f"[Page {page_num}]{page_text}\n\n"
        if not full_text.strip():
            print("Empty text")
            return []
        print(f"Extracted text:{len(full_text)} characters from {len(reader.pages)} pages")
        splitter = RecursiveCharacterTextSplitter(#splitter is the characteristic that will help divide the text
            chunk_size=500,
            chunk_overlap=100,
            length_function=len
        )
        chunks = splitter.split_text(full_text)#the full text is divided using the requirements given above in the splitter
        print(f"Your file has been split into  chunks {len(chunks)}")
        #This code prints a short preview of the first text chunk but only if atleast one chunk exists
        if chunks:
            preview = chunks[0][:200] + "..." if len(chunks[0]) > 200 else chunks[0]
            print(f"first chunk Preview: {preview}")
        return chunks
    except Exception as e:
        print(f"Error: {e}")
        return []
