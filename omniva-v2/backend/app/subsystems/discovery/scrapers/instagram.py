"\"\"\"Instagram discovery via simple HTML scrape.\"\"\""

from typing import List

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}


def discover_instagram_posts(profile_url: str) -> List[str]:
    """Scrape a public Instagram profile for recent post URLs."""
    resp = requests.get(profile_url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    urls: List[str] = []
    for anchor in soup.find_all("a"):
        href = anchor.get("href", "")
        if "/p/" in href:
            urls.append(f"https://www.instagram.com{href}")
    return list(set(urls))
