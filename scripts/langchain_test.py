from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
# from langchain.prompts import PromptTemplate
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain
import sys


def get_pdf_doc(path: str):
    # Load and split PDF pages
    pdf_loader = PyPDFLoader(path)
    pages = pdf_loader.load_and_split()

    # Reduce chunk size and overlap to improve memory efficiency
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,  # Reduced size
        chunk_overlap=50,  # Reduced overlap
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(pages)
    print(f"Split {len(pages)} documents into {len(chunks)} chunks.")

    # Embedding setup
    embedding = FastEmbedEmbeddings()

    # Batch processing to avoid memory overload
    batch_size = 25  # Adjust batch size based on your machine's capacity
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]

        # Extract content from documents to pass to embed_documents
        batch_contents = [chunk.page_content for chunk in batch]

        # Embed only a batch at a time
        try:
            batch_embeddings = embedding.embed_documents(batch_contents)
        except TypeError as e:
            print(f"Error embedding batch {i} to {i + batch_size}: {e}")
            continue

        # Store embeddings incrementally using Chroma
        Chroma.from_documents(documents=batch, embedding=batch_embeddings, persist_directory="./sql_chroma_db")


    print("Embeddings and vector store creation complete.")


def main():
    get_pdf_doc(r'C:\Users\16025\Documents\Code\appRepairAssist\data\manuals\GOVPUB-D101-PURL-LPS37172.pdf')



if __name__ == "__main__":
    main()