
import os
import asyncio
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

async def list_models():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found in .env")
        return

    client = AsyncGroq(api_key=api_key)
    
    try:
        models = await client.models.list()
        with open("models_clean.txt", "w", encoding="utf-8") as f:
            f.write(f"Found {len(models.data)} models:\n")
            for model in models.data:
                f.write(f"- {model.id} (Owner: {model.owned_by})\n")
        print("Models written to models_clean.txt")
    except Exception as e:
        print(f"Error checking models: {e}")

if __name__ == "__main__":
    asyncio.run(list_models())
