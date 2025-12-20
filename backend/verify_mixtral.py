
import asyncio
import os
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv(dotenv_path="backend/.env")

async def verify():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found")
        return

    client = AsyncGroq(api_key=api_key)
    model = "mixtral-8x7b-32768"
    
    print(f"Testing generation with model: {model}")
    try:
        completion = await client.chat.completions.create(
            messages=[
                {"role": "user", "content": "Hello, are you working?"}
            ],
            model=model,
        )
        print("Response received:")
        print(completion.choices[0].message.content)
        print("SUCCESS")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(verify())
