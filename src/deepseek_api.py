import aiohttp
import os

async def ask_mudrets(question: str) -> str:
    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": question}]
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data
        ) as resp:
            result = await resp.json()
            return result["choices"][0]["message"]["content"]