from .base_agent import BaseAgent

class AnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__("AnalystAgent")

    def analyze_papers(self, papers):
        """Analyze papers and find research gaps."""
        analysis_result = f"After reviewing The research, These are the gaps identified: \n"
        self.save_memory(papers, analysis_result)
        return analysis_result
