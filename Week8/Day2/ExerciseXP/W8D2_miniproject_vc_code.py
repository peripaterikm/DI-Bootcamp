import time
import csv
import pandas as pd
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Automatically install ChromeDriver matching the installed Chrome version
chromedriver_autoinstaller.install()

# Chrome options (headless is disabled to allow full JS rendering)
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # <- Do NOT use headless for this site
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Start Chrome browser
driver = webdriver.Chrome(options=options)

# Open target URL
driver.get("https://www.inmotionhosting.com/web-hosting/")

# Wait for hosting cards to appear
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "imh-rostrum-card"))
    )
    print("✅ Hosting plans loaded.")
except:
    print("❌ Hosting plans not found.")
    driver.quit()
    exit()

# Locate all cards
cards = driver.find_elements(By.CLASS_NAME, "imh-rostrum-card")

data = []

for i, card in enumerate(cards):
    try:
        name = card.find_element(By.CLASS_NAME, "imh-rostrum-card-title").text.strip()
    except:
        name = f"Card #{i+1}"

    try:
        price_element = card.find_element(By.CLASS_NAME, "imh-rostrum-starting-at-price-discounted")
        price = driver.execute_script("return arguments[0].innerText;", price_element).strip().split("\n")[0]
    except:
        price = "N/A"

    try:
        features = card.find_elements(By.CSS_SELECTOR, "ul.imh-rostrum-details-list li")
        features_list = [f.text.strip() for f in features if f.text.strip()]
    except:
        features_list = []

    print(f"▶️ Parsed card #{i+1}: name='{name}', price='{price}'")

    data.append({
        "Plan Name": name,
        "Price": price,
        "Features": ", ".join(features_list)
    })


# Save to CSV
csv_filename = "inmotion_plans.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Plan Name", "Price", "Features"])
    writer.writeheader()
    for row in data:
        writer.writerow(row)

# Close browser
driver.quit()

# Load and show CSV preview
df = pd.read_csv(csv_filename)
print(df.head())
