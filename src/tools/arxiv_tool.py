import requests

class ArxivTool:
    BASE_URL = "http://export.arxiv.org/api/query?"

    def search(self, query):
        """Search arXiv for papers using the provided query."""
        params = {'search_query': f'all:{query}', 'start': 0, 'max_results': 5}
        response = requests.get(self.BASE_URL, params=params)
        # Simulating a parsed response
        return response.text  # Here, parsing the XML would be necessary.
