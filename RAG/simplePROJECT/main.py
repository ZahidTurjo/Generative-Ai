from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_mistralai import ChatMistralAI
load_dotenv()

embedding_model=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vector_store=Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

retriever=vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k":2,
        "fetch_k":3,
        "lambda_mult" :0.5

    }
)

llm=ChatMistralAI(model="mistral-small-2506")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful AI assistant.

Use ONLY the provided context to answer the question.

If the answer is not present in the context,
say: "I could not find the answer in the document."
"""
        ),
        (
            "human",
            """Context:
{context}

Question:
{question}
"""
        )
    ]
)
print("Rag system created ")

print("press 0 to exit ")

while True:
    query=input("You : ")
    if query =="0":
        break

    docs=retriever.invoke(query)

    context="\n\n".join(
        [doc.page_content for doc in docs]
    )
    final_prompt=prompt.invoke(
        {
            "context":context,
            "question":query
        }
    )
    response=llm.invoke(final_prompt)
    print(f'\nAi : {response.content}')