# src/main.py
from agents.researcher_agent import ResearcherAgent

def main():
    topic = input("Enter the research topic: ")
    
    # Initialize the Researcher Agent
    researcher_agent = ResearcherAgent(topic)
    
    # Get research on the topic
    research_summary = researcher_agent.get_research()
    
    print("\nResearch Overview:\n")
    print(research_summary)

if __name__ == "__main__":
    main()
