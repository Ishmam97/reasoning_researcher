import os
from dotenv import load_dotenv
from openai import OpenAI 
from langchain.memory import ConversationBufferMemory  

class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.memory = ConversationBufferMemory()  # Ensure compatibility with LangChain's migration guide
        self.initialize_openai_client()

    def initialize_openai_client(self):
        """Load environment variables and set OpenAI API key"""
        load_dotenv()  # Load environment variables from the .env file
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is missing in the environment variables")
        base_url= os.getenv("AI_ML_API")
        if not base_url:
            raise ValueError("AI_ML API key is missing in the environment variables")
        self.api = OpenAI(api_key=api_key, base_url=base_url)

    def save_memory(self, input_data, output_data):
        """Saves the input and output to agent's memory."""
        self.memory.save_context({"input": input_data}, {"output": output_data})

    def retrieve_memory(self):
        """Retrieves all memory."""
        return self.memory.load_memory_variables({})

    def use_tool(self, tool, query):
        """Simulates using a tool (e.g., arXiv API)."""
        return tool.search(query)
