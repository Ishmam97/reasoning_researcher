# src/main.py
import os
import datetime
from agents.researcher_agent import ResearcherAgent
from utils.saving import save_output_to_markdown

def main():
    topic = input("Enter the research topic: ")
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.join("output", f"run_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize the Researcher Agent
    researcher_agent = ResearcherAgent(topic)
    
    # Get research on the topic
    research_summary = researcher_agent.get_research()
    
    # Save the research summary to a markdown file
    save_output_to_markdown(research_summary, "researcher", output_dir)
    print(f"Research summary saved to {output_dir}/researcher_output.md")
if __name__ == "__main__":
    main()
