#!/usr/bin/env python3
"""
Pohkim.net HTML Structure Analyzer

This script helps identify the HTML selectors for the pohkim.net website
to facilitate web scraping.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin

# Constants
BASE_URL = "https://pohkim.net"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_page(url):
    """Get page content with error handling"""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def analyze_page_structure(url):
    """Analyze the HTML structure of a page and identify key elements"""
    html = get_page(url)
    if not html:
        return
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Output the page title
    print(f"\nPage Title: {soup.title.text if soup.title else 'No title found'}")
    
    # Identify navigation/category elements
    print("\n--- Navigation/Category Elements ---")
    nav_elements = soup.find_all(['nav', 'ul', 'div'], class_=lambda x: x and ('nav' in x or 'menu' in x or 'category' in x))
    
    for i, nav in enumerate(nav_elements[:5]):  # Show only the first 5 to avoid clutter
        print(f"\nPotential Navigation #{i+1}:")
        print(f"Tag: {nav.name}, Classes: {nav.get('class')}, ID: {nav.get('id')}")
        
        # Look for links within navigation
        links = nav.find_all('a', href=True)
        if links:
            print(f"Contains {len(links)} links. First 3 links:")
            for j, link in enumerate(links[:3]):
                print(f"  {j+1}. Text: '{link.text.strip()}', URL: {link['href']}")
    
    # Identify product containers
    print("\n--- Product Containers ---")
    potential_product_containers = []
    
    # Common product container strategies
    container_selectors = [
        soup.find_all('div', class_=lambda x: x and ('product' in x or 'item' in x)),
        soup.find_all('li', class_=lambda x: x and ('product' in x or 'item' in x)),
        soup.find_all('article'),
        soup.find_all('div', class_=lambda x: x and ('card' in x))
    ]
    
    for selectors in container_selectors:
        if selectors:
            potential_product_containers.extend(selectors)
    
    # Deduplicate
    seen = set()
    unique_containers = []
    for container in potential_product_containers:
        if id(container) not in seen:
            seen.add(id(container))
            unique_containers.append(container)
    
    for i, container in enumerate(unique_containers[:5]):  # Show only the first 5
        print(f"\nPotential Product Container #{i+1}:")
        print(f"Tag: {container.name}, Classes: {container.get('class')}, ID: {container.get('id')}")
        
        # Check for common product elements
        title = container.find(text=lambda x: x and len(x.strip()) > 5)
        price = container.find(text=lambda x: x and ('$' in x or '£' in x or '€' in x or 'KRW' in x or '원' in x))
        link = container.find('a', href=True)
        img = container.find('img', src=True)
        
        if title:
            print(f"  Potential Title: {title.strip()[:50]}{'...' if len(title) > 50 else ''}")
        
        if price:
            print(f"  Potential Price: {price.strip()}")
        
        if link:
            link_url = urljoin(BASE_URL, link['href']) if not link['href'].startswith('http') else link['href']
            print(f"  Link: {link_url}")
        
        if img:
            img_url = urljoin(BASE_URL, img['src']) if not img['src'].startswith('http') else img['src']
            print(f"  Image: {img_url}")
    
    # Save HTML for inspection
    output_file = os.path.join(OUTPUT_DIR, "pohkim_html.html")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"\nHTML saved to {output_file} for manual inspection")

def main():
    """Main function"""
    print(f"Analyzing structure of {BASE_URL}")
    analyze_page_structure(BASE_URL)
    
    # You can add more specific pages to analyze, e.g., product or category pages
    # Uncomment and modify these lines as needed
    # print("\n\nAnalyzing a category page")
    # analyze_page_structure(urljoin(BASE_URL, "/category/path"))
    
    # print("\n\nAnalyzing a product page")
    # analyze_page_structure(urljoin(BASE_URL, "/product/path"))

if __name__ == "__main__":
    main() 