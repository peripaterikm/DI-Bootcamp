from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Set up headless Chrome browser options
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Launch the browser
driver = webdriver.Chrome(options=options)
url = "https://www.rottentomatoes.com/browse/movies_at_home/affiliates:netflix~critics:certified_fresh"
driver.get(url)

# Wait until at least one movie card is loaded
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-qa="discovery-media-list-item"]'))
)
time.sleep(2)  # Additional wait to ensure everything is fully loaded

# Get the page HTML
soup = BeautifulSoup(driver.page_source, 'html.parser')
movies = soup.find_all(attrs={"data-qa": "discovery-media-list-item"})

# Extract data for each movie
for movie in movies[:10]:  # Example: Only first 10 movies
    # Movie title
    title_tag = movie.find('span', class_='p--small')
    title = title_tag.get_text(strip=True) if title_tag else "No Title"

    # Release date
    date_tag = movie.find('span', class_='smaller')
    date = date_tag.get_text(strip=True) if date_tag else "No Date"

    # Tomatometer Score
    score = None
    score_pairs = movie.find('score-pairs-deprecated')
    if score_pairs:
        critics_score = score_pairs.find('rt-text', {'slot': 'criticsScore'})
        if critics_score:
            score = critics_score.get_text(strip=True)
    score = score if score else "No Score"

    print(f"Title: {title}")
    print(f"Tomatometer: {score}")
    print(f"Release Date: {date}")
    print("-" * 40)

driver.quit()