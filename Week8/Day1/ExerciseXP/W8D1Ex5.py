import time
from collections import Counter
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

# Start undetected Chrome browser
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36")

driver = uc.Chrome(options=options)

# Open weather forecast page
url = "https://www.accuweather.com/en/us/attica/30607/weather-forecast/2139413"
driver.get(url)

# Wait for page to load
time.sleep(5)

# Scroll down to make sure all data loads
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

# Get page HTML
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Find daily weather cards
cards = soup.find_all('a', class_="daily-list-item")

max_temps = []
min_temps = []
conditions = []

for card in cards:
    # Find temperatures
    temp_hi = card.find("span", class_="temp-hi")
    temp_lo = card.find("span", class_="temp-lo")
    # Find weather condition
    phrase = card.find("p", class_="no-wrap")
    
    if temp_hi and temp_lo and phrase:
        try:
            max_temps.append(int(temp_hi.text.strip().replace("°", "")))
            min_temps.append(int(temp_lo.text.strip().replace("°", "")))
        except ValueError:
            continue
        conditions.append(phrase.text.strip())

# Analysis
if max_temps and min_temps and conditions:
    avg_max = sum(max_temps) / len(max_temps)
    avg_min = sum(min_temps) / len(min_temps)
    most_common_cond = Counter(conditions).most_common(1)[0][0]
    
    print("Weather analysis for Attica:")
    print("-----------------------------")
    print(f"Average maximum temperature: {avg_max:.1f}°C")
    print(f"Average minimum temperature: {avg_min:.1f}°C")
    print(f"Most common weather condition: {most_common_cond}")
else:
    print("No weather data found! Try again later or check selectors.")