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
        """Use the arXiv tool to get results, analyze them, and then conduct further research."""
        if self.should_use_arxiv(self.topic):
            print(f"Using arXiv tool for topic: {self.topic}")
            raw_results = self.arxiv_tool.run(self.topic)
            structured_analysis = self.analyze_arxiv_results(raw_results)  # Step 2: Analyze results

            # Save both raw results and structured analysis in memory
            self.save_memory("arxiv_raw_results", raw_results)
            self.save_memory("arxiv_analysis", structured_analysis)

            # Save the raw results and analysis to files
            self.save_tool_results("ArxivResults_Raw", raw_results, output_dir)
            self.save_tool_results("ArxivResults_Analysis", structured_analysis, output_dir)

            # Perform further research using both the arXiv results and analysis
            extended_research = self.perform_further_research(raw_results, structured_analysis)
        else:
            extended_research = self.generic_research(self.topic)

        self.save_memory(self.topic, extended_research)
        return extended_research

    def analyze_arxiv_results(self, results):
        """Analyze arXiv results and provide a structured summary."""
        try:
            response = self.api.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a research assistant analyzing papers."},
                    {"role": "user", "content": f"Analyze the following papers and provide research gaps and future directions:\n\n{results}"}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()  # Access the content correctly
        except Exception as e:
            return f"Error in analyzing arXiv results: {str(e)}"

    def perform_further_research(self, raw_results, analysis):
        """Perform further research by leveraging both arXiv results and the analysis."""
        try:
            response = self.api.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a research assistant conducting further research."},
                    {"role": "user", "content": f"Using the following papers and analysis, conduct further research on {self.topic}:\n\nPapers:\n{raw_results}\n\nAnalysis:\n{analysis}"}
                ],
                max_tokens=1000,
                temperature=0.8
            )
            return response.choices[0].message.content.strip()  # Access the content correctly
        except Exception as e:
            return f"Error in performing further research: {str(e)}"

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
            response = self.api.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",  # Update to use GPT-4o mini
                messages=[
                    {"role": "system", "content": "You are a research assistant."},
                    {"role": "user", "content": self.generate_prompt()}
                ],
                max_tokens=1000,
                temperature=0.8
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"
        
    def generate_prompt(self):
        """Load prompt template from file and insert the topic"""
        with open('prompts/researcher_prompt.txt', 'r') as file:
            prompt_template = file.read()
        return prompt_template.format(topic=self.topic)
    