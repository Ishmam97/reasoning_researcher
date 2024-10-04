# src/agents/researcher_agent.py
from openai import OpenAI
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Get the API key from environment variable

class ResearcherAgent:
    def __init__(self, topic):
        self.topic = topic

    def get_research(self):
        """Fetch research information on the given topic using GPT-4o mini"""
        try:
            # Correcting the API call by providing 'model' and 'messages'
            response = client.chat.completions.create(model="gpt-4o-mini",  # Update to use GPT-4o mini
            messages=[
                {"role": "system", "content": "You are a research assistant."},
                {"role": "user", "content": self.generate_prompt()}
            ],
            max_tokens=500,
            temperature=0.8)
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"

    def generate_prompt(self):
        """Load prompt template from file and insert the topic"""
        with open('prompts/researcher_prompt.txt', 'r') as file:
            prompt_template = file.read()
        return prompt_template.format(topic=self.topic)
