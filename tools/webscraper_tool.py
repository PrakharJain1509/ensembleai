
import requests
from bs4 import BeautifulSoup
from .tools import Tool

class WebScrapingTool(Tool):
    def __init__(self, url):
        self.url = url

    def use(self, agent):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.title.string.strip() if soup.title else 'No title found'
            meta = soup.find('meta', attrs={'name': 'description'})
            meta_description = meta['content'] if meta and 'content' in meta.attrs else 'No description found'

            headings = {}
            for tag in ['h1', 'h2', 'h3']:
                elements = soup.find_all(tag)
                if elements:
                    headings[tag] = [h.get_text(strip=True) for h in elements]

            paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]

            result = f"Title: {title}\n"
            result += f"Meta Description: {meta_description}\n"
            result += "Headings:\n"
            for level, texts in headings.items():
                result += f"  {level.upper()}: {', '.join(texts)}\n"
            result += "Paragraphs:\n"
            result += "\n".join(paragraphs)

            insights = agent.model_instance.generate(
                name=agent.name,
                llm=agent.llm,
                work=agent.work,
                role=agent.role,
                context=result
            )
            return insights

        except requests.exceptions.RequestException as e:
            return f"Error during the request: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"
