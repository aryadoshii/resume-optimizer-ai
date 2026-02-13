import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Try platform.qubrid.com instead
client = OpenAI(
    base_url="https://platform.qubrid.com/v1",  # Try this URL
    api_key=os.getenv("QUBRID_API_KEY"),
)

response = client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.3",
    messages=[{"role": "user", "content": "Say hello"}],
    max_tokens=100,
)

print(response.choices[0].message.content)