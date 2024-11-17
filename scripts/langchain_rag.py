import argparse
import time
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import OllamaEmbeddings
from .prompt_templates import SYSTEM_TEMPLATE, HUMAN_TEMPLATE


embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)

CHROMA_PATH = "data\chroma"

system_message_prompt = SystemMessagePromptTemplate.from_template(SYSTEM_TEMPLATE)
human_message_prompt = HumanMessagePromptTemplate.from_template(HUMAN_TEMPLATE)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("--query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str):
    # Prepare the DB.
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=6)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    messages = chat_prompt.format_messages(user_input=query_text, knowledge=context_text)
    prompt_string = "\n".join([message.content for message in messages])

    # print(prompt_string)
    print(query_text)


    model = OllamaLLM(model="llama3.2:1b")
    s = time.time()
    response_text = model.invoke(prompt_string)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    sources = ", ".join(sources) # temp delete late


    formatted_response = {
        "response": response_text,
        "sources": sources
    }
    # print(response_text)

    t = time.time()
    print(f"[Time taken: ] {(t - s):.2f} s")
    return formatted_response


if __name__ == "__main__":
    main()