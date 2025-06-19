import os
import openai
from dotenv import load_dotenv

load_dotenv()

from app.code_review import CodeReviewerBase

client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

class OpenAICodeReviewer(CodeReviewerBase):
    def __init__(self, code):
        super().__init__(code)
        self.model = "gpt-4o"

    def call_llm(self, prompt: str, max_tokens: int = 1000, response_format: str = "text") -> str:
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=max_tokens,
            response_format={ "type": response_format }
        )
        return response.choices[0].message.content.strip()