import pandas as pd
import sys
import re

# Настройка UTF-8 для Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Read file
file_path = 'data/dentists_results_final_v2.8.xlsx'
try:
    df = pd.read_excel(file_path)
except Exception as e:
    print(f"Error: {e}")
    sys.exit()

# Print sample addresses to understand format
print("Sample Addresses:")
addresses = df['Address'].dropna().head(10).tolist()
for addr in addresses:
    print(f"- {addr}")

# Try to extract State (usually 2 letters before ZIP or at the end)
# Format often: "123 Main St, City, ST 12345"
# Regex: space + 2 uppercase letters + space + 5 digits (optional)
# Or just look for common US states if it's US data.

print("\nTop Regions (State/City):")

# Simple extraction of "City, ST" if present
def extract_state(addr):
    if not isinstance(addr, str): return None
    # Look for "City, ST 12345" -> match "ST"
    # Matches: comma, space, 2 uppercase, space, 5 digits
    match = re.search(r',\s([A-Z]{2})\s\d{5}', addr)
    if match:
        return match.group(1)
    
    # Fallback: Maybe just state name?
    # Let's count occurrences of known states if regex fails.
    return None

df['State'] = df['Address'].apply(extract_state)

if df['State'].notna().sum() > 0:
    print(df['State'].value_counts().head(10))
else:
    print("Could not extract states with standard regex. Printing top occurring words in address:")
    # Tokenize and count (rough approach)
    all_text = " ".join(df['Address'].dropna().astype(str).tolist())
    words = pd.Series(all_text.replace(',', '').split())
    # Filter for common state abbrs or city names manually if needed
    print(words.value_counts().head(20))
