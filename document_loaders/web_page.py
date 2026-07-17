from langchain_community.document_loaders import WebBaseLoader
url="https://www.daraz.com.bd/products/apple-decal-i-phone-apple-pride-i421411865-s2062571714.html?pvid=f1e66649-2009-4815-bfc5-692907fd6d7e&search=jfy&scm=1007.51705.413671.0&spm=a2a0e.tm80335411.just4u.d_421411865"

data=WebBaseLoader(url)

docs=data.load()

print(docs[0])