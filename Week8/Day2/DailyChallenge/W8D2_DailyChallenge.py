# 📦 Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from zipfile import ZipFile
from sklearn.preprocessing import MinMaxScaler
from IPython.display import display, Markdown

# 📥 Step 1: Load from ZIP
zip_path = "C:/DI-Bootcamp/Week8/Day2/DailyChallenge/Global Terrorism Database.zip"
csv_filename = "Global Terrorism Database/Global Terrorism Database/globalterrorismdb_0718dist.csv"

with ZipFile(zip_path) as z:
    with z.open(csv_filename) as f:
        df = pd.read_csv(f, encoding="ISO-8859-1", nrows=1000, usecols=[
            "eventid", "iyear", "imonth", "iday",
            "country_txt", "region_txt", "city",
            "attacktype1_txt", "target1", "nkill", "nwound",
            "weaptype1_txt", "gname"
        ], low_memory=False)

# 🧼 Step 2: Cleaning
df["imonth"] = df["imonth"].replace(0, 1)
df["iday"] = df["iday"].replace(0, 1)
df["date"] = pd.to_datetime(dict(year=df["iyear"], month=df["imonth"], day=df["iday"]), errors="coerce")

df["nkill"] = df["nkill"].fillna(0).astype(int)
df["nwound"] = df["nwound"].fillna(0).astype(int)
df["city"] = df["city"].fillna("Unknown")
df["target1"] = df["target1"].fillna("Unknown")
df["gname"] = df["gname"].fillna("Unknown")

# ➕ Step 3: Derived fields
df["ncasualties"] = df["nkill"] + df["nwound"]
df["ncasualties_norm"] = MinMaxScaler().fit_transform(df[["ncasualties"]])
df = pd.get_dummies(df, columns=["attacktype1_txt"], prefix="attack")

# 📊 Step 4: Country Summary
display(Markdown("### 🌍 Top 10 Countries by Number of Attacks"))
country_summary = pd.DataFrame({
    "Attacks": df["country_txt"].value_counts(),
    "Total Casualties": df.groupby("country_txt")["ncasualties"].sum()
}).dropna().sort_values(by="Attacks", ascending=False).head(10)
display(country_summary)

plt.figure(figsize=(10, 6))
sns.barplot(x=country_summary.index, y=country_summary["Attacks"])
plt.title("Top 10 Countries by Number of Attacks")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 📈 Step 5: Yearly Dynamics
display(Markdown("### 📅 Number of Attacks by Year"))
yearly_dynamics = df["iyear"].value_counts().sort_index()
display(yearly_dynamics.to_frame(name="Attacks"))

plt.figure(figsize=(10, 6))
sns.lineplot(x=yearly_dynamics.index, y=yearly_dynamics.values)
plt.title("Number of Attacks by Year")
plt.xlabel("Year")
plt.ylabel("Attacks")
plt.tight_layout()
plt.show()

# 🎯 Step 6: Attack Type Distribution
display(Markdown("### 💣 Distribution of Attack Types"))
attack_types = df[[col for col in df.columns if col.startswith("attack_")]].sum().sort_values(ascending=False)
display(attack_types.to_frame(name="Occurrences"))

plt.figure(figsize=(10, 6))
sns.barplot(x=attack_types.index, y=attack_types.values)
plt.title("Distribution of Attack Types")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 🧨 Step 7: Top Terrorist Groups
display(Markdown("### 🔫 Top 10 Terrorist Groups (Excluding 'Unknown')"))
group_counts = df["gname"].value_counts()
top_groups = group_counts[group_counts.index != "Unknown"].head(10)
display(top_groups.to_frame(name="Incidents"))

plt.figure(figsize=(10, 6))
sns.barplot(x=top_groups.index, y=top_groups.values)
plt.title("Top 10 Terrorist Groups")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 💾 Save cleaned version
df.to_csv("global_terrorism_sample_cleaned.csv", index=False, encoding="utf-8-sig")
print("✅ Cleaned sample saved and visualizations displayed.")
