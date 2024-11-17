import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """
Answer the question below carefully.

Here is the conversation history: {context}

Question: {question}

Answer:

"""

prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="llama3.1")
chain = prompt | model

def conversation():
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


if __name__ == "__main__":
    conversation()






