import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load dataset
df = pd.read_csv("owid-covid-data.csv")

# View columns and data
print(df.columns)
print(df.head())
print(df.info())
print(df.isnull().sum().sort_values(ascending=False))

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Filter specific countries
countries = ['Kenya', 'India', 'United States']
df = df[df['location'].isin(countries)]

# Drop rows missing critical fields
df = df.dropna(subset=['total_cases', 'total_deaths'])

# Fill or interpolate missing numeric data
df = df.fillna(method='ffill')

# Set style
sns.set(style="whitegrid")

# Total cases over time
plt.figure(figsize=(10,6))
sns.lineplot(data=df, x="date", y="total_cases", hue="location")
plt.title("Total COVID-19 Cases Over Time")
plt.xlabel("Date")
plt.ylabel("Total Cases")
plt.show()

# New cases comparison
plt.figure(figsize=(10,6))
sns.lineplot(data=df, x="date", y="new_cases", hue="location")
plt.title("Daily New COVID-19 Cases")
plt.xlabel("Date")
plt.ylabel("New Cases")
plt.show()

# Death rate
df["death_rate"] = df["total_deaths"] / df["total_cases"]

# Vaccination over time
plt.figure(figsize=(10,6))
sns.lineplot(data=df, x="date", y="total_vaccinations", hue="location")
plt.title("Cumulative Vaccinations Over Time")
plt.xlabel("Date")
plt.ylabel("Total Vaccinations")
plt.show()

# Percentage vaccinated (assuming people_fully_vaccinated & population exist)
df["percent_vaccinated"] = (df["people_fully_vaccinated"] / df["population"]) * 100

# Prepare latest data
latest_data = df[df["date"] == df["date"].max()]
latest_data = latest_data.dropna(subset=["iso_code", "total_cases"])

fig = px.choropleth(
    latest_data,
    locations="iso_code",
    color="total_cases",
    hover_name="location",
    color_continuous_scale="Reds",
    title="Global Total COVID-19 Cases"
)
fig.show()