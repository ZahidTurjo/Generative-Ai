#load pdf
#split into chunk
#create embeddings
#store into vectore database
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
load_dotenv()

document=TextLoader("document_loaders/notes.txt")

docs=document.load()

splitter=RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)
chunks=splitter.split_documents(docs)

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vector_sore=Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)
