#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "beautifulsoup4",
#     "feedparser",
#     "requests",
# ]
# ///
from pathlib import Path

import feedparser
import requests
from bs4 import BeautifulSoup


def main():
    chunks = []
    chunks.extend(get_bio())
    chunks.append('')
    chunks.extend(get_latest_posts())

    readme = Path(__file__).parent / "README.md"
    readme.write_text("\n".join(chunks))


def get_bio():
    # Get bio from my website to avoid duplication
    response = requests.get("https://adamj.eu")
    if response.status_code != 200:
        raise ValueError("Unexpected response status code {response.status_code}")
    soup = BeautifulSoup(response.content.decode(), "html.parser")
    heading = soup.body.find("div", id="me").find("h2")
    for elem in heading.next_siblings:
        if elem.name == "h2":
            break
        if elem.name != "img" and str(elem).strip():
            yield str(elem).replace("welcome to my site", "welcome to my GitHub bio")


def get_latest_posts():
    chunks = ["## Latest blog posts\n"]
    posts = feedparser.parse("https://adamj.eu/tech/atom.xml")["entries"][:5]
    chunks.extend(
        [
            f'* [{post["title"]}]({post["link"]}) ({post["updated"].split("T")[0]})'
            for post in posts
        ]
    )
    return chunks


if __name__ == "__main__":
    main()
