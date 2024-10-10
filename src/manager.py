from agents.researcher_agent import ResearcherAgent
from agents.analyst_agent import AnalystAgent

class AgentManager:
    def __init__(self, topic):
        self.topic = topic
        self.researcher_agent = ResearcherAgent(topic)
        self.analyst_agent = AnalystAgent()

    def orchestrate_agents(self, output_dir):
        """Orchestrate agent actions in sequence."""
        research_results = self.researcher_agent.search_papers(output_dir)
        analysis = self.analyst_agent.analyze_papers(research_results)
        return research_results, analysis


