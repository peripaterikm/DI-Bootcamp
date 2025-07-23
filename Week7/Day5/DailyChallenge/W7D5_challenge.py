import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://github.com/topics"
response = requests.get(URL)

print("Status Code:", response.status_code)
if response.status_code != 200:
    raise Exception("Request failed.")

print("First 100 characters of HTML:\n", response.text[:100])

with open("webpage.html", "w", encoding="utf-8") as f:
    f.write(response.text)
print("HTML saved to webpage.html")

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# ✅ Updated selectors
titles = [tag.text.strip() for tag in soup.select("h3 a")]
descriptions = [tag.text.strip() for tag in soup.select("p.f5.color-fg-muted.mb-0.mt-1")]

print(f"Titles extracted: {len(titles)}")
print(f"Descriptions extracted: {len(descriptions)}")
print("Sample Titles:", titles[:5])
print("Sample Descriptions:", descriptions[:5])

# Align lengths
min_len = min(len(titles), len(descriptions))
titles = titles[:min_len]
descriptions = descriptions[:min_len]

# Create DataFrame
df = pd.DataFrame({"title": titles, "description": descriptions})
print("\n--- Final DataFrame ---")
print(df.head())

df.to_csv("github_topics.csv", index=False, encoding="utf-8")
print("\nData saved to github_topics.csv")
