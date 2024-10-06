# src/main.py
import os
import datetime
from manager import AgentManager
from utils.saving import save_output_to_markdown

def create_output_folder():
    """Create a new folder for each run based on timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.join("output", f"run_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def main():
    topic = input("Enter the research topic: ")

    # Create output directory for this run
    output_dir = create_output_folder()

    # Initialize the manager and orchestrate the agents
    manager = AgentManager(topic)
    research_results, analysis = manager.orchestrate_agents()

    # Save outputs from both agents
    save_output_to_markdown(research_results, "ResearcherAgent", output_dir)
    save_output_to_markdown(analysis, "AnalystAgent", output_dir)

if __name__ == "__main__":
    main()
