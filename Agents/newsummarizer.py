from dotenv import load_dotenv
load_dotenv()

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import  ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

search_tool=TavilySearchResults(max=5)

result_tool=search_tool.run("Give Recent Jobs News that are rapidly increasing for AI")

# print(result_tool)

prompt=ChatPromptTemplate.from_template(
    """
    You are a Helpful Ai News Summarizer
    please summarzie the following news with clear bullet points
    {news}
"""
)
model=ChatMistralAI(
    model= "mistral-small-2506"
)

chain=prompt|model| StrOutputParser()
result=chain.invoke(
    {
        "news":result_tool
    }
)

print(result)