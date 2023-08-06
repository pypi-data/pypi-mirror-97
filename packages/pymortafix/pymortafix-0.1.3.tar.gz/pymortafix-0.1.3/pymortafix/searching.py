from googleapiclient.discovery import build
from requests import get

GOOGLE_URL = "https://google.it/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,it;q=0.8,la;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


def google_search(query, api_key, cse_id, results=10, **kwargs):
    """Google search with API and CSE (official method)"""
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, num=results, **kwargs).execute()
    return res.get("items")


async def google_search_pirate_async(session, query):
    """Async Google search via scraping and fake header (pirate method)"""
    async with session.get(
        GOOGLE_URL, headers=HEADERS, params={"q": query}
    ) as response:
        google_content = await response.read()
    return google_content


def google_search_pirate(query):
    """Google search via scraping and fake header (pirate method)"""
    return get(GOOGLE_URL, headers=HEADERS, params={"q": query}).text
