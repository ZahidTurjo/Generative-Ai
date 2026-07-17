from langchain_community.document_loaders import PyPDFLoader
data=PyPDFLoader("document_loaders/gru.pdf")

docs=data.load()
for i in range(15):
    print("="*50)
    print(docs[i].page_content)