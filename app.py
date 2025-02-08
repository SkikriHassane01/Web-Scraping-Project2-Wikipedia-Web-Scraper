# import libraries
import requests #get the url
from bs4 import BeautifulSoup 
import csv
import pandas as pd


# Define base URL
BASE_URL = "https://en.wikipedia.org/wiki/COVID-19_pandemic_deaths"

# step1: get the content from a given url
def fetch_page(url):
    """Fetches the webpage content"""
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        print(f"[SUCCESS] Page fetched successfully: {url}")
        return response.content
    else:
        print(f"[ERROR] Failed to fetch page. Status Code: {response.status_code}")
        return None

# step2: parse the html content using bs4
def parse_html(content):
    """Parses the HTML content using BeautifulSoup"""
    return BeautifulSoup(content, "html.parser")

def extract_paragraphs(soup):
    """Extracts all paragraphs from the page with indexing"""
    paragraphs = [[i+1, p.get_text(strip=True)] for i, p in enumerate(soup.find_all("p"))]
    print(f"[INFO] Found {len(paragraphs)} paragraphs.")
    return paragraphs

def extract_headers(soup):
    """Extracts all headers from the page with indexing"""
    headers = [[i+1, h.get_text(strip=True)] for i, h in enumerate(soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]))]
    print(f"[INFO] Found {len(headers)} headers.")
    return headers

def extract_tables(soup):
    """Extracts all tables from the page, assigning each table the corresponding caption if available."""
    tables = soup.find_all(class_="sticky-table-scroll") # extract all tables 
    if not tables:
        print("[INFO] No tables found on the page.")
        return []

    all_tables = [] # store the content for every table 
    
    for index, table in enumerate(tables):
        
        # Get the caption, if available
        caption_tag = table.find("caption")
        caption = caption_tag.get_text(strip=True) if caption_tag else f"Table_{index+1}"
        rows = table.find_all("tr")
        
        if not rows:
            continue
        
        # Extract headers (from first row)
        headers = [col.get_text(strip=True) for col in rows[0].find_all(["th", "td"])]
        table_data = [["Index"] + headers]

        # Extract table rows
        for i, row in enumerate(rows[1:]):
            cols = row.find_all(["th", "td"])
            table_data.append([i+1] + [col.get_text(strip=True) for col in cols])

        print(f"[INFO] Extracted {len(table_data) - 1} rows from table: {caption}")
        all_tables.append((caption, table_data))
    
    return all_tables

def save_tables_to_csv(tables):
    """Saves each extracted table into a separate CSV file."""
    for caption, table_data in tables:
        df = pd.DataFrame(table_data[1:], columns=table_data[0])
        file_name = f"{caption.replace(' ', '_')}.csv"
        df.to_csv(file_name, index=False, encoding="utf-8")
        print(f"[INFO] Saved table '{caption}' to {file_name}")

def save_to_csv(data, filename, headers):
    """Saves extracted data to a CSV file with headers"""
    if not data:
        print("[WARNING] No data to save.")
        return
    
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
    print(f"[SUCCESS] Data saved to {filename}")

def main():
    """Main function to execute the scraping steps"""
    content = fetch_page(BASE_URL)
    if not content:
        return
    
    soup = parse_html(content)
    
    # Extract different types of content
    paragraphs = extract_paragraphs(soup)
    headers_data = extract_headers(soup)
    tables = extract_tables(soup)
    
    # Save data
    save_to_csv(paragraphs, "paragraphs.csv", ["Index", "Paragraph"])
    save_to_csv(headers_data, "headers.csv", ["Index", "Header"])
    save_tables_to_csv(tables)
    
    print("[INFO] Scraping complete!")

if __name__ == "__main__":
    main()
