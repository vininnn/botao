import aiohttp

ZEN_QUOTES_URL = "https://zenquotes.io/api/random"

# Get a inspirational quote to send (API zenquotes)        
async def get_inspirational_quote() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(ZEN_QUOTES_URL) as resp:
            data = await resp.json()

            quote_data = data[0]
            quote = quote_data.get("q", "No quote found")
            author = quote_data.get("a") or "Unknown"

            return f"{quote} - {author}"
