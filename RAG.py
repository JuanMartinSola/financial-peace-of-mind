from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.llms.gemini import Gemini
from llama_index.llms.openai_like import OpenAILike
import asyncio
from dotenv import load_dotenv
import os

# Create a RAG tool using LlamaIndex
load_dotenv()
openai_token = os.getenv("openai_API_KEY")
apertus80B_token = os.getenv("apertus80B_API_KEY")

def load_and_chunk(path: str, chunk_size: int = 1000, chunk_overlap: int = 100):
    raw_docs = SimpleDirectoryReader(path).load_data()
    splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    nodes = splitter.get_nodes_from_documents(raw_docs)
    return nodes  # return Node objects directly

documents = SimpleDirectoryReader(r"C:\Users\jmsal\FinancialPeaceOfMind\financial-peace-of-mind\OCR_texts").load_data(show_progress=True)
#index = VectorStoreIndex.from_documents(documents_short)
#documents_short = load_and_chunk(r"C:\Users\jmsal\FinancialPeaceOfMind\financial-peace-of-mind\OCR_texts_shorts")
documents_short = SimpleDirectoryReader(r"C:\Users\jmsal\FinancialPeaceOfMind\financial-peace-of-mind\OCR_texts_shorts").load_data(show_progress=True)
#index = VectorStoreIndex.from_documents(documents_short)
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()


async def search_documents(query: str) -> str:
    """Useful for answering natural language questions about UBS knowledge."""
    response = await query_engine.aquery(query)
    return str(response)


# Create an enhanced workflow with tool
agent = FunctionAgent(
    tools=[search_documents],
    #llm = OpenAILike(model="swiss-ai/Apertus-70B",
    #                 api_base="https://api.swisscom.com/layer/swiss-ai-weeks/apertus-70b/v1",
    #                    api_key=apertus80B_token,
    #                    context_window=128000,
    #                    is_chat_model=True,
    #                    is_function_calling_model=True
    #),
    #llm = Gemini(model="models/gemini-ultra", api_key="YOUR_API_KEY"),
    llm=OpenAI(model="gpt-4o",openai_client=openai_token),
    system_prompt="""You are an expert UBS advisor with deep understanding of the market
    and capable of searching through documents to answer questions. Maintain a professional, kind tone. 
    Share your precise market insights based on the users risk-tolerance and current investment portfolio positions, 
    as well as the knowledge provided in the documents you can read. Fundament your answer quoting the documents you have access to. Do so in a concise paragraph.""",
)


# Now we can ask questions about the documents or do calculations
async def main():
    response = await agent.run(
        """Being a conservative investor with low risk affinity and having a large percentage of my 
        portfolio invested in commodities, give me a brief yet meaningful overview of the market 
        trends and possible future actions to guarantee high yield whilst maintaining a low risk profile."""
    )
    print(response)


# Run the agent
if __name__ == "__main__":
    asyncio.run(main())