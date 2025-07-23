"""
Web Scraping Exercises with BeautifulSoup
Compatible with Python 3.9+ (tested in VS Code)
"""

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import random
import json

# ---------- Helper Function ----------
def get_soup(url: str) -> BeautifulSoup:
    """Fetch a webpage and return a BeautifulSoup object."""
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "en-US,en;q=0.9"
        }
    )
    html = urlopen(req).read()
    return BeautifulSoup(html, "html.parser")


# ---------- Exercise 1 ----------
def exercise_1():
    """Parse a static HTML string with BeautifulSoup."""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sports World</title>
    </head>
    <body>
        <p>Your one-stop destination for the latest sports news and videos.</p>
        <a href="#football">Football</a>
        <a href="#basketball">Basketball</a>
        <a href="#tennis">Tennis</a>
    </body>
    </html>
    """

    soup = BeautifulSoup(html, "html.parser")
    print("Page Title:", soup.title.string)
    print("Paragraphs:", [p.text for p in soup.find_all("p")])
    print("Links:", [a["href"] for a in soup.find_all("a", href=True)])


# ---------- Exercise 2 ----------
def exercise_2():
    """Download and display the first 500 characters of Wikipedia robots.txt."""
    txt = urlopen("https://en.wikipedia.org/robots.txt").read().decode("utf-8")
    print(txt[:500])


# ---------- Exercise 3 ----------
def exercise_3():
    """Extract all header tags from Wikipedia Main Page."""
    soup = get_soup("https://en.wikipedia.org/wiki/Main_Page")
    headers = [tag.text.strip() for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]
    print(headers)


# ---------- Exercise 4 ----------
def exercise_4():
    """Check if a page contains a title."""
    soup = get_soup("https://en.wikipedia.org/wiki/Main_Page")
    print("Page Title:", soup.title.string if soup.title else "No title found")


# ---------- Exercise 5 ----------
def exercise_5():
    """Count US-CERT (CISA) security alerts for the current year."""
    soup = get_soup("https://www.cisa.gov/news-events/cybersecurity-advisories")
    current_year = str(datetime.now().year)
    alerts = [a.text.strip() for a in soup.find_all("a")
              if current_year in a.text and ("CSA" in a.text or "ICSA" in a.text)]
    print(f"Security alerts in {current_year}: {len(alerts)}")


# ---------- Exercise 6 ----------
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import random
import json

def get_soup(url: str) -> BeautifulSoup:
    """Fetch a webpage and return a BeautifulSoup object."""
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "en-US,en;q=0.9"
        }
    )
    return BeautifulSoup(urlopen(req).read(), "html.parser")

def exercise_6():
    """Scrape 10 random movies (IMDB IDs + OMDb API for details)."""
    API_KEY = "thewdb"  # Demo OMDb API key
    BASE_OMDB = f"http://www.omdbapi.com/?apikey={API_KEY}&i="

    print("\n--- Exercise 6 ---")

    try:
        # Step 1: parse IMDB IDs from the list page
        soup = get_soup("https://www.imdb.com/list/ls091294718/")
        ids = [a["href"].split("/")[2] for a in soup.select("h3.lister-item-header a")]
        ids = list(set(ids))  # remove duplicates

        if not ids:
            print("IMDB did not return any data. The site might be blocking requests.")
            return

        # Step 2: get details from OMDb API
        for imdb_id in random.sample(ids, min(10, len(ids))):
            with urlopen(BASE_OMDB + imdb_id) as resp:
                data = json.loads(resp.read())
                title = data.get("Title", "Unknown")
                year = data.get("Year", "N/A")
                plot = data.get("Plot", "No description")
                print(f"{title} ({year}): {plot}")

    except Exception as e:
        print(f"Failed to fetch movie details. Reason: {e}")

# Run only Exercise 6 for test
if __name__ == "__main__":
    exercise_6()
