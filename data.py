import pandas as pd

# Link CSV dari Google Spreadsheet
url = "https://docs.google.com/spreadsheets/d/1DeB0-8q9D7EFkamjKHMCEp0VBGpzDnby/export?format=csv"

# Baca langsung ke DataFrame
df = pd.read_csv(url)

# Tampilkan isi
print(df.head())

