#!/usr/bin/env python3
"""
Pohkim.net Data Importer

This script imports scraped product data from pohkim.net into the prototype project.
"""

import json
import os
import glob
import shutil
from datetime import datetime

# Constants
SCRAPING_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
PROTOTYPE_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pohkim", "public", "data")
IMAGES_DIR = os.path.join(PROTOTYPE_DATA_DIR, "images")

def ensure_directories():
    """Ensure the necessary directories exist"""
    os.makedirs(PROTOTYPE_DATA_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

def get_latest_data_file():
    """Find the most recent data file in the scraping/data directory"""
    data_files = glob.glob(os.path.join(SCRAPING_DATA_DIR, "pohkim_data_*.json"))
    if not data_files:
        print("No data files found. Please run the scraper first.")
        return None
    
    # Sort by modification time, newest first
    data_files.sort(key=os.path.getmtime, reverse=True)
    return data_files[0]

def process_for_prototype(data):
    """Process the data to fit the prototype's requirements"""
    processed_data = {
        "products": [],
        "categories": set()
    }
    
    for product in data:
        # Extract categories from specifications
        category = "Uncategorized"
        if 'specifications' in product and 'Category' in product['specifications']:
            category = product['specifications']['Category']
        
        processed_data['categories'].add(category)
        
        # Create a clean product record
        processed_product = {
            "id": hash(product['url']) % 10000000,  # Generate a numeric ID
            "title": product.get('title', 'Untitled Product'),
            "price": product.get('price', 'N/A'),
            "description": product.get('description', ''),
            "category": category,
            "image": product.get('image_url', ''),
            "additionalImages": product.get('images', []),
            "specifications": product.get('specifications', {}),
            "url": product.get('url', '')
        }
        
        processed_data['products'].append(processed_product)
    
    # Convert categories from set to list
    processed_data['categories'] = list(processed_data['categories'])
    
    return processed_data

def save_to_prototype(processed_data):
    """Save the processed data to the prototype directory"""
    # Save the main data file
    products_file = os.path.join(PROTOTYPE_DATA_DIR, "products.json")
    with open(products_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data['products'], f, ensure_ascii=False, indent=2)
    
    # Save categories
    categories_file = os.path.join(PROTOTYPE_DATA_DIR, "categories.json")
    with open(categories_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data['categories'], f, ensure_ascii=False, indent=2)
    
    return {
        "products_file": products_file,
        "categories_file": categories_file
    }

def main():
    """Main function to coordinate the data import process"""
    print(f"Starting import process at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ensure directories exist
    ensure_directories()
    
    # Get the latest data file
    data_file = get_latest_data_file()
    if not data_file:
        return
    
    print(f"Using data file: {data_file}")
    
    # Load the data
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Loaded {len(data)} products")
    
    # Process the data for the prototype
    processed_data = process_for_prototype(data)
    print(f"Processed {len(processed_data['products'])} products across {len(processed_data['categories'])} categories")
    
    # Save to the prototype
    saved_files = save_to_prototype(processed_data)
    
    print("Import completed successfully!")
    print(f"Products saved to: {saved_files['products_file']}")
    print(f"Categories saved to: {saved_files['categories_file']}")

if __name__ == "__main__":
    main() 