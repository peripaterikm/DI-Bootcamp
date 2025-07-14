import time
import csv
import pandas as pd
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Automatically install ChromeDriver matching the installed Chrome version
chromedriver_autoinstaller.install()

# Set Chrome options (no headless mode to ensure full rendering)
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Disable for full JS rendering
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Start the Chrome browser
driver = webdriver.Chrome(options=options)

# Open the hosting plans page
driver.get("https://www.inmotionhosting.com/web-hosting/")

# Wait for the hosting cards to load in the DOM
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "imh-rostrum-card"))
    )
    print("✅ Hosting plans loaded.")
except:
    print("❌ Hosting plans not found.")
    driver.quit()
    exit()

# Get the full rendered HTML after JS execution
html = driver.page_source

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")
cards = soup.select(".imh-rostrum-card")

data = []

for i, card in enumerate(cards):
    # Plan name
    name_tag = card.select_one(".imh-rostrum-card-title")
    name = name_tag.text.strip() if name_tag else f"Card #{i+1}"

    # Price (via JavaScript-rendered content — fallback via Selenium)
    try:
        # Re-find the original element in Selenium DOM to access JS-rendered text
        sel_card = driver.find_elements(By.CLASS_NAME, "imh-rostrum-card")[i]
        price_element = sel_card.find_element(By.CLASS_NAME, "imh-rostrum-starting-at-price-discounted")
        price = driver.execute_script("return arguments[0].innerText;", price_element).strip().split("\n")[0]
    except:
        price = "N/A"

    # Features list
    features = [li.text.strip() for li in card.select("ul.imh-rostrum-details-list li") if li.text.strip()]

    print(f"▶️ Parsed card #{i+1}: name='{name}', price='{price}'")

    data.append({
        "Plan Name": name,
        "Price": price,
        "Features": ", ".join(features)
    })

# Save results to CSV file
csv_filename = "inmotion_plans.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Plan Name", "Price", "Features"])
    writer.writeheader()
    writer.writerows(data)

# Close the browser
driver.quit()

# Load and preview the saved CSV
df = pd.read_csv(csv_filename)
print(df.head())
