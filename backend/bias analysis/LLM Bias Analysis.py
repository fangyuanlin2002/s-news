import requests
import json
import os
from together import Together
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Access environment variables
debug = os.getenv('DEBUG')
api_key = os.getenv('TOGETHER_AI_API_KEY')

# Replace with your actual article content
article_text = """
[INSERT YOUR NEWS ARTICLE HERE]
"""

# Prompt to analyze the article for political bias
analysis_prompt = f"""
Analyze the following news article for political bias. Specifically, identify whether the article leans pro-democracy, pro-communism, or is neutral. Provide evidence from the text to support your conclusion.

Article:
\"\"\"
{article_text}
\"\"\"
"""

client = Together(api_key=api_key)

response = client.chat.completions.create(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    messages=[
      {
        "role": "user",
        "content": "What are some fun things to do in New York?"
      }
    ]
)
print(response.choices[0].message.content)