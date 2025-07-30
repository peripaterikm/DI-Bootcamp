from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta
import time

# Set up Chrome browser options for headless mode
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# Open the news page
url = "https://www.bbc.com/news/technology"
driver.get(url)
time.sleep(2)  # Wait for the page to load

# Get the HTML of the page
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Find all news cards on the page
cards = soup.find_all('div', attrs={"data-testid": "dundee-card"})

# Create a dictionary to save articles by month
articles_by_month = {}

for card in cards:
    # Find the title and link
    title_tag = card.find('a', attrs={"data-testid": "internal-link"})
    title = title_tag.text.strip() if title_tag else None
    link = title_tag['href'] if title_tag and title_tag.has_attr('href') else None

    # Find the date
    date_tag = card.find('span', attrs={"data-testid": "card-metadata-lastupdated"})
    date_text = date_tag.text.strip() if date_tag else None

    # Skip if no title or no date
    if not title or not date_text:
        continue

    # Change "days ago" or "hours ago" to real date
    date_real = datetime.now()
    if "day" in date_text:
        num = int(date_text.split()[0])
        date_real = datetime.now() - timedelta(days=num)
    elif "hour" in date_text:
        num = int(date_text.split()[0])
        date_real = datetime.now() - timedelta(hours=num)

    # Get the month name (for example, July)
    month_name = date_real.strftime("%B")
    if month_name not in articles_by_month:
        articles_by_month[month_name] = []
    if link:
        full_link = f"https://www.bbc.com{link}" if link.startswith("/") else link
        articles_by_month[month_name].append(f"{title} ({date_real.strftime('%Y-%m-%d')}) [{full_link}]")
    else:
        articles_by_month[month_name].append(f"{title} ({date_real.strftime('%Y-%m-%d')})")

# Print articles grouped by month
for month, articles in sorted(articles_by_month.items()):
    print(f"\n{month}")
    print("-" * 30)
    for article in articles:
        # Take only title and date
        parts = article.split(' (')
        if len(parts) >= 2:
            title_and_desc = parts[0]
            date = parts[1].split(')')[0]
            title = title_and_desc.split('|')[0].strip() if '|' in title_and_desc else title_and_desc.strip()
            short_title = (title[:57] + '...') if len(title) > 60 else title
            print(f"Title: {short_title}\nDate: {date}\n")
        else:
            print(article + "\n")