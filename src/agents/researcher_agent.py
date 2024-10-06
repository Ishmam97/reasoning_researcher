from langchain_community.tools import ArxivQueryRun  # Updated as per deprecation warning
from .base_agent import BaseAgent
import openai  # Ensure openai is imported

class ResearcherAgent(BaseAgent):
    def __init__(self, topic):
        super().__init__("ResearcherAgent")
        self.topic = topic
        self.arxiv_tool = ArxivQueryRun()

    def should_use_arxiv(self, topic):
        """Determine if the arXiv tool is needed based on the topic."""
        return any(keyword in topic.lower() for keyword in ['research', 'paper', 'study', 'academic'])

    def search_papers(self):
        """Use the arXiv tool if needed or fetch research using OpenAI otherwise."""
        if self.should_use_arxiv(self.topic):
            print(f"Using arXiv tool for topic: {self.topic}")
            results = self.use_tool(self.arxiv_tool, self.topic)
        else:
            results = self.generic_research(self.topic)
        self.save_memory(self.topic, results)
        return results

    def generic_research(self, topic):
        """Fetch general research information via OpenAI using the new Chat API"""
        try:
            # Correcting the API call by providing 'model' and 'messages'
            response = openai.chat.completions.create(model="gpt-4o-mini",  # Update to use GPT-4o mini
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
    