
from .tools import Tool

class ImageAnalysisTool(Tool):
    def __init__(self, text, url):
        self.text = text
        self.url = url

    def use(self, agent):
        completion = agent.model_instance.client.chat.completions.create(
            model=agent.llm,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self.text},
                        {"type": "image_url", "image_url": {"url": self.url}}
                    ]
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message
