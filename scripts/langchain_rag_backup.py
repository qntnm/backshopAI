import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_community.document_loaders import PyPDFLoader, PDFMinerLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma


def getDocument_chunks(
        path: str = r'data\manuals\GOVPUB-D101-PURL-LPS37172.pdf',
        chunk_size: int = 512,
        chunk_overlap: int = 50
    ) -> list[str]:
    try:
        pdf = PyPDFLoader(file_path=path)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            add_start_index=True,
        )
        chunks = pdf.load_and_split(text_splitter=text_splitter)
    except Exception as e:
        print(f"Error in {getDocument_chunks.__name__}: {e}")
        return []
    return chunks

def conversation():
    template = """
    Answer the question below carefully.

    Here is the conversation history: {context}

    Question: {question}

    Answer:

    """

    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model="llama3.1")
    chain = prompt | model
    context = ""

    while True:
        user_query = input("[You]: ")
        if user_query.lower() == "exit":
            break

        start_time = time.time()
        res = chain.invoke(
            {
                "context": context,
                "question": user_query
                }
            )
        end_time = time.time()
        print(f"[{end_time - start_time:.2f} s][BOT]: ", res)

        context += f"\n[User]: {user_query}\n[BOT]: {res}\n"

def get_embeddings(text: str) -> list[float]:
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
    )
    return embeddings(text)


def add_to_chromadb(chunks: list[Document]):
    db = Chroma(
        persist_directory="data/chroma",
        embedding_function=get_embeddings,
    )
    db.add_documents(chunks)
    db.persist()


if __name__ == "__main__":
    chunks = getDocument_chunks()
    print(chunks)
    breakpoint()
    pass






