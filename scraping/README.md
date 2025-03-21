# Pohkim.net Web Scraper

This project contains scripts to scrape product data from pohkim.net, an e-commerce website for DVD retail.

## Project Structure

```
scraping/
├── data/                   # Directory where scraped data is stored
├── scrape_pohkim.py        # Main scraping script
├── analyze_structure.py    # Helper script to analyze website structure
├── import_to_prototype.py  # Script to import data into the prototype
└── README.md               # This file
```

## Setup

1. Make sure you have Python 3.6+ installed
2. Install required packages:
   ```
   python3 -m pip install requests beautifulsoup4
   ```

## Usage

### Analyzing Website Structure

Before running the main scraper, it's recommended to run the structure analyzer to understand the HTML structure of the website:

```
python3 analyze_structure.py
```

This will:
- Save the HTML of the main page to `data/pohkim_html.html` for inspection
- Print information about potential navigation elements and product containers
- Help identify the correct CSS selectors for the main scraper

### Running the Scraper

After adjusting the selectors in `scrape_pohkim.py` based on the analysis:

```
python3 scrape_pohkim.py
```

This will:
- Scrape category information
- Extract product listings from each category
- Fetch detailed information for each product
- Save all data to a JSON file in the `data/` directory with a timestamp

### Importing Data into Prototype

After running the scraper, you can import the data into your prototype:

```
python3 import_to_prototype.py
```

This will:
- Find the most recent scraped data file
- Process the data to fit the prototype's data structure
- Save the processed data to the prototype's data directory
- Create separate files for products and categories

## Important Notes

1. **Rate Limiting**: The scraper includes random delays between requests to avoid overwhelming the server.
2. **CSS Selectors**: The included selectors are placeholders and need to be adjusted based on the actual website structure.
3. **Legal Considerations**: Make sure web scraping is allowed by the website's terms of service.

## Output Data Format

The script outputs a JSON file with the following structure:

```json
[
  {
    "title": "Product Title",
    "price": "Product Price",
    "url": "Product URL",
    "image_url": "Product Image URL",
    "description": "Product Description",
    "specifications": {
      "Spec1": "Value1",
      "Spec2": "Value2"
    },
    "images": [
      "Image URL 1",
      "Image URL 2"
    ]
  },
  ...
]
```

### Prototype Data Format

After processing through `import_to_prototype.py`, the data is transformed into:

**products.json:**
```json
[
  {
    "id": 1234567,
    "title": "Product Title",
    "price": "Product Price",
    "description": "Product Description",
    "category": "Category Name",
    "image": "Main Image URL",
    "additionalImages": ["Image URL 1", "Image URL 2"],
    "specifications": {
      "Spec1": "Value1",
      "Spec2": "Value2"
    },
    "url": "Original Product URL"
  },
  ...
]
```

**categories.json:**
```json
["Category 1", "Category 2", "Category 3", ...]
```

## Customization

To customize the scraper for different parts of the website:

1. Update the CSS selectors in the script based on your analysis
2. Modify the product detail extraction to match the structure of the product pages
3. Add additional fields to the data extraction as needed
4. Adjust the data processing in `import_to_prototype.py` if your prototype requires a different data format 