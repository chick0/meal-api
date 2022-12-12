from urllib.request import Request
from urllib.request import urlopen


def fetch(url: str, query: str):
    request = Request(
        url=f"{url}?{query}",
        method="GET",
        headers={
            "User-Agent": "meal-api (https://github.com/chick0/meal-api)"
        }
    )

    return urlopen(request, timeout=5)
