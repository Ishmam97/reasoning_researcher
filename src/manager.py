from agents.researcher_agent import ResearcherAgent
from agents.analyst_agent import AnalystAgent

class AgentManager:
    def __init__(self, topic):
        self.topic = topic
        self.researcher_agent = ResearcherAgent(topic)
        self.analyst_agent = AnalystAgent()

    def orchestrate_agents(self):
        """Orchestrate agent actions in sequence."""
        print(f"Researching topic: {self.topic}")

        # Researcher agent gathers research material
        research_results = self.researcher_agent.search_papers()
        print("Researcher Agent Results:\n", research_results)

        # Analyst agent analyzes the research and finds gaps
        analysis = self.analyst_agent.analyze_papers(research_results)
        print("Analyst Agent Results:\n", analysis)

        return research_results, analysis

