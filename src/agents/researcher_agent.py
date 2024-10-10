from langchain_community.tools import ArxivQueryRun  # Updated as per deprecation warning
from .base_agent import BaseAgent
import os

class ResearcherAgent(BaseAgent):
    def __init__(self, topic):
        super().__init__("ResearcherAgent")
        self.topic = topic
        self.arxiv_tool = ArxivQueryRun()

    def should_use_arxiv(self, topic):
        """Determine if the arXiv tool is needed based on the topic."""
        return any(keyword in topic.lower() for keyword in ['research', 'paper', 'study', 'academic'])

    def search_papers(self, output_dir):
        """Use the arXiv tool if needed or fetch research using OpenAI otherwise."""
        if self.should_use_arxiv(self.topic):
            print(f"Using arXiv tool for topic: {self.topic}")
            results = self.arxiv_tool.run(self.topic)
            self.save_tool_results("ArxivResults", results, output_dir)  # Pass output_dir here
        else:
            results = self.generic_research(self.topic)
        self.save_memory(self.topic, results)
        return results

    def save_tool_results(self, tool_name, results, output_dir):
        """Save the tool call results to a separate file in the same output directory."""
        file_path = os.path.join(output_dir, f"{tool_name}_{self.topic}.md")
        with open(file_path, "w") as file:
            file.write(f"# Results from {tool_name}\n\n")
            file.write(results)
        print(f"Results saved to {file_path}")
        
    def generic_research(self, topic):
        """Fetch general research information via OpenAI using the new Chat API"""
        try:
            # Correcting the API call by providing 'model' and 'messages'
            response = self.api.chat.completions.create(model="gpt-4o-mini-2024-07-18",  # Update to use GPT-4o mini
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
    