# Wikipedia Web Scraper

## Overview
This script scrapes content from the Wikipedia Main Page using `BeautifulSoup`. It extracts paragraphs, headers, and tables, and saves the data into CSV files.

## Features
- Fetches HTML content from Wikipedia
- Parses HTML using BeautifulSoup
- Extracts:
  - Paragraphs (`<p>` tags)
  - Headers (`<h1> - <h6>` tags)
  - Table data (`<table>`)
- Saves extracted data into CSV files

## Installation
### Prerequisites
Ensure you have Python installed along with the required libraries:
```bash
pip install requests beautifulsoup4
```

## Usage
Run the script using:
```bash
python app.py
```

## Output
The extracted data is saved in:
- `paragraphs.csv` - Contains extracted paragraphs
- `headers.csv` - Contains extracted headers
- `table_data.csv` - Contains table data (if available)

## Example Output
### Paragraphs (Extracted from `<p>`)
```
The number of p is: 10
Example paragraph: "Wikipedia is a free online encyclopedia, created and edited by volunteers around the world."
```

### Headers (Extracted from `<h1> - <h6>`)
```
Found 5 headers.
Example: "Welcome to Wikipedia"
```

### Table Data
```
Extracted 8 rows from the table.
Example:
| Header1 | Header2 |
|---------|---------|
| Data1   | Data2   |
```

## License
This project is open-source and free to use.
