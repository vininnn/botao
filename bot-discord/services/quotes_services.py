import aiohttp

ZEN_QUOTES_URL = "https://zenquotes.io/api/random"
   
async def get_inspirational_quote() -> str:
    """Fetches a random inspirational quote from the ZenQuotes API.

    Returns:
        str: A formatted string containing the quote and the author.
             Returns a fallback message if no quote is found.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(ZEN_QUOTES_URL) as resp:
            data = await resp.json()

            quote_data = data[0]
            quote = quote_data.get("q", "No quote found")
            author = quote_data.get("a") or "Unknown"

            return quote, author
