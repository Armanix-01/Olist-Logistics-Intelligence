import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()



api_key = os.getenv("OPENAI_API_KEY")
query_llm = ChatOpenAI(
    model="gpt-6.1-sol",
    api_key=api_key,
    reasoning_effort="medium",
    max_tokens=700
)
general_llm = ChatOpenAI(
    model="gpt-6.1-sol",
    api_key=api_key,
    reasoning_effort="low",
    max_tokens=500,
)