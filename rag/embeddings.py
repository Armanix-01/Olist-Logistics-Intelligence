import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings


load_dotenv()


def set_up_embedder():

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set in environment variables."
        )

    return OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=api_key
    )