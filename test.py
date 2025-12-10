# test.py

# LiteLLM to access any LLM quickly
from litellm import completion
import os
from dotenv import load_dotenv
load_dotenv()

# Loading API Keys
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")


response = completion(
    model="groq/llama-3.1-8b-instant", 
    messages=[{ "content": "Hello, there! ", "role": "user" }]
)

print("\n>>> RESPONSE:")
print(response.choices[0].message.content)

