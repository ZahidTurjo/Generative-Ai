from langchain_groq import ChatGroq
from langchain_core.tools import tool

from langchain.agents import create_agent

import requests
from dotenv import load_dotenv
import os


# =========================
# Environment
# =========================

load_dotenv()

os.environ["LANGCHAIN_PROJECT"] = "Agent"


# =========================
# Search Tool
# =========================
from ddgs import DDGS


@tool
def duckduckgo_search(query: str) -> str:
    """Search the web using DuckDuckGo."""
    
    results = DDGS().text(query, max_results=5)

    if not results:
        return "No search results found."

    return "\n\n".join(
        f"Title: {r['title']}\n"
        f"URL: {r['href']}\n"
        f"Snippet: {r['body']}"
        for r in results
    )


# =========================
# Weather Tool
# =========================

@tool
def get_weather_data(city: str) -> str:
  """
  This function fetches the current weather data for a given city
  """
  url = f'https://api.weatherstack.com/current?access_key={YourApiKEY}&query={city}'

  response = requests.get(url)

  return response.json()

# =========================
# LLM
# =========================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# =========================
# Agent
# =========================

agent = create_agent(
    model=llm,
    tools=[
        duckduckgo_search,
        get_weather_data
    ]
)


# =========================
# Run
# =========================

response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "tell about Bangladesh Politics"
        }
    ]
})


print(response)
