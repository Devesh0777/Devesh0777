import requests
from bs4 import BeautifulSoup
import json
import os
import sys

# Replace this with your actual GitHub username
USERNAME = "Devesh0777" 

def fetch_github_contributions(username):
    url = f"https://github.com/users/{username}/contributions"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch contributions for {username}. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Github heatmap is stored in table cells with class 'ContributionCalendar-day'
    # Or in newer GitHub UI, it's stored in <tool-tip> elements and path nodes
    # We can also scrape standard GitHub graph APIs if the HTML changes, but the blog post uses scraping.
    
    days = []
    
    # Modern GitHub HTML structure for the contribution graph:
    # A bunch of <td class="ContributionCalendar-day" data-date="2023-01-01" data-level="1">
    cells = soup.find_all('td', class_='ContributionCalendar-day')
    
    for cell in cells:
        date = cell.get('data-date')
        level = cell.get('data-level')
        
        # In newer versions of github, the text inside contains the count (e.g. "5 contributions on Jan 1")
        # Or it might be in a tooltip.
        if date and level:
            days.append({
                "date": date,
                "level": int(level)
            })

    if not days:
        print("Warning: Could not parse contribution days. GitHub's HTML may have changed.")
        
    return {
        "username": username,
        "days": days
    }

def main():
    print(f"Fetching contributions for {USERNAME}...")
    data = fetch_github_contributions(USERNAME)
    
    if data:
        os.makedirs("data", exist_ok=True)
        out_path = os.path.join("data", "contributions.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data['days'])} days of contributions to {out_path}")

if __name__ == "__main__":
    main()
