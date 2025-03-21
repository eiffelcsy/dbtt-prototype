#!/usr/bin/env python3
"""
Pohkim.net Web Scraper

This script scrapes product information from pohkim.net, an e-commerce website
for DVD retail.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
import random
import re
from datetime import datetime
from urllib.parse import urljoin

# Constants
BASE_URL = "https://pohkim.net"
SHOP_URL = "https://pohkim.net/shop/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
VIDEOS_JSON_PATH = "/Users/eiffelcsy/Projects/dbtt-prototype/pohkim/public/videos.json"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_page(url):
    """Get page content with error handling and random delay to be respectful to the server"""
    try:
        # Random delay between 1-3 seconds to avoid overwhelming the server
        time.sleep(random.uniform(1, 3))
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_price(price_text):
    """Extract numeric price from price text"""
    if not price_text or price_text == "Price not available":
        return 0.0
    
    # Use regex to find the price pattern
    price_match = re.search(r'[\$£€]?\s*(\d+(?:\.\d+)?)', price_text)
    if price_match:
        return float(price_match.group(1))
    return 0.0

def scrape_product_listing_page(url):
    """Scrape a product listing page and extract basic product info"""
    html = get_page(url)
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    products = []
    
    # Find product elements on the page - based on analysis
    product_elements = soup.select('.wd-products-element .product')
    
    if not product_elements:
        # Try alternative selectors
        product_elements = soup.select('.product-grid-item')
    
    if not product_elements:
        # Last attempt with a more generic selector
        product_elements = soup.select('li.product')
    
    print(f"Found {len(product_elements)} products on page {url}")
    
    for product in product_elements:
        try:
            # Extract product data using the observed structure
            product_link = product.select_one('a.product-image-link, a.product-title-link, h3.wd-entities-title a')
            
            if not product_link:
                continue
                
            product_url = product_link['href']
            if not product_url.startswith('http'):
                product_url = urljoin(BASE_URL, product_url)
                
            title_element = product.select_one('.product-title, .wd-entities-title')
            title = title_element.text.strip() if title_element else "Unknown Title"
            
            # Improved price extraction
            price_element = product.select_one('.price .woocommerce-Price-amount')
            price_text = price_element.text.strip() if price_element else "Price not available"
            price = extract_price(price_text)
            
            image_element = product.select_one('img.attachment-woocommerce_thumbnail, img.wp-post-image')
            image_url = ""
            if image_element:
                image_url = image_element.get('src') or image_element.get('data-src', '')
                if not image_url.startswith('http'):
                    image_url = urljoin(BASE_URL, image_url)
            
            products.append({
                'title': title,
                'price': price,
                'url': product_url,
                'image_url': image_url,
            })
        except (AttributeError, KeyError) as e:
            print(f"Error extracting product data: {e}")
            continue
    
    # Look for pagination
    next_page = soup.select_one('a.next.page-numbers')
    next_page_url = None
    if next_page:
        next_page_url = next_page['href']
        if not next_page_url.startswith('http'):
            next_page_url = urljoin(BASE_URL, next_page_url)
    
    return {
        'products': products,
        'next_page': next_page_url
    }

def scrape_product_details(url):
    """Scrape detailed product information from a product page"""
    html = get_page(url)
    if not html:
        return {}
    
    soup = BeautifulSoup(html, 'html.parser')
    product_details = {}
    
    try:
        # Extract detailed product information based on observed structure
        title_element = soup.select_one('.product_title, .product-title')
        product_details['title'] = title_element.text.strip() if title_element else "Unknown Title"
        
        # Improved price extraction
        price_element = soup.select_one('.price .woocommerce-Price-amount')
        price_text = price_element.text.strip() if price_element else "Price not available"
        product_details['price'] = extract_price(price_text)
        
        description_element = soup.select_one('.woocommerce-product-details__short-description, .product-short-description, .woocommerce-Tabs-panel--description, #tab-description')
        product_details['description'] = description_element.text.strip() if description_element else ""
        
        # Extract specifications/attributes
        specs = {}
        spec_table = soup.select_one('.woocommerce-product-attributes, .shop_attributes')
        if spec_table:
            rows = spec_table.select('tr')
            for row in rows:
                key_element = row.select_one('th')
                value_element = row.select_one('td, .woocommerce-product-attributes-item__value')
                
                if key_element and value_element:
                    key = key_element.text.strip()
                    value = value_element.text.strip()
                    specs[key] = value
        
        product_details['specifications'] = specs
        
        # Extract release date for videos.json format
        release_date = "2023-01-01"  # Default
        if 'Release Date' in specs:
            try:
                date_text = specs['Release Date']
                # Try to parse DD/MM/YYYY format
                if '/' in date_text:
                    day, month, year = date_text.split('/')
                    release_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            except:
                pass
        
        product_details['releaseDate'] = release_date
        
        # Extract categories
        categories = []
        category_elements = soup.select('.posted_in a')
        for category in category_elements:
            categories.append(category.text.strip())
        
        product_details['categories'] = categories
        # Get primary genre
        product_details['genre'] = categories[0] if categories else "DVD"
        
        # Extract duration
        duration = "2h 00m"  # Default
        if 'Running Time' in specs:
            duration_text = specs['Running Time']
            # Extract minutes and convert to hours and minutes format
            minutes_match = re.search(r'(\d+)\s*min', duration_text)
            if minutes_match:
                total_minutes = int(minutes_match.group(1))
                hours = total_minutes // 60
                minutes = total_minutes % 60
                duration = f"{hours}h {minutes}m"
        
        product_details['duration'] = duration
        
        # Extract additional images
        images = []
        # Try the product gallery
        gallery_elements = soup.select('.woocommerce-product-gallery__image a')
        if gallery_elements:
            for img in gallery_elements:
                img_url = img.get('href')
                if img_url and img_url not in images:
                    images.append(img_url)
        else:
            # Try alternative image selectors
            image_elements = soup.select('.product-images img')
            for img in image_elements:
                img_url = img.get('src') or img.get('data-src', '')
                if img_url and img_url not in images:
                    if not img_url.startswith('http'):
                        img_url = urljoin(BASE_URL, img_url)
                    images.append(img_url)
        
        product_details['images'] = images
        
        # Set thumbnail for videos.json format
        product_details['thumbnail'] = images[0] if images else ""
        
    except (AttributeError, KeyError) as e:
        print(f"Error extracting product details: {e}")
    
    return product_details

def scrape_categories():
    """Scrape the main categories from the website"""
    html = get_page(BASE_URL)
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    categories = []
    
    # Find main navigation categories - based on analysis
    category_elements = soup.select('.wd-nav-main li.menu-item, .woodmart-navigation li.menu-item')
    
    # Filter out the home and shop links
    filtered_categories = []
    for category in category_elements:
        try:
            category_link = category.select_one('a')
            if category_link:
                name = category_link.text.strip()
                url = category_link['href']
                
                # Skip the Home and Shop pages
                if name.lower() in ['home', 'shop']:
                    continue
                    
                if not url.startswith('http'):
                    url = urljoin(BASE_URL, url)
                
                filtered_categories.append({
                    'name': name,
                    'url': url
                })
        except (AttributeError, KeyError) as e:
            print(f"Error extracting category: {e}")
    
    # If we didn't find categories in the main nav, try from the shop page
    if not filtered_categories:
        print("Trying to extract categories from the shop page...")
        html = get_page(SHOP_URL)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            shop_categories = soup.select('.widget_product_categories a, .product-categories a')
            
            for category in shop_categories:
                name = category.text.strip()
                url = category['href']
                if not url.startswith('http'):
                    url = urljoin(BASE_URL, url)
                
                filtered_categories.append({
                    'name': name,
                    'url': url
                })
    
    # If we still don't have categories, use the shop page as a fallback
    if not filtered_categories:
        filtered_categories.append({
            'name': 'All Products',
            'url': SHOP_URL
        })
    
    return filtered_categories

def convert_to_videos_json_format(products):
    """Convert scraped products to videos.json format"""
    videos = []
    
    # Get the next available ID
    try:
        # Read existing videos.json to get the last ID
        with open(VIDEOS_JSON_PATH, 'r', encoding='utf-8') as f:
            existing_videos = json.load(f)
            # Sort existing videos by ID to make sure we get the right max
            existing_videos.sort(key=lambda video: video['id'])
            last_id = max(video['id'] for video in existing_videos) if existing_videos else 0
    except (FileNotFoundError, json.JSONDecodeError):
        last_id = 0
    
    # Convert each product to videos.json format
    for idx, product in enumerate(products, 1):
        # Extract format from specifications
        dvd_format = "DVD"
        if 'specifications' in product:
            specs = product['specifications']
            if 'Number of Disc' in specs:
                num_discs = specs.get('Number of Disc', '').strip()
                if num_discs:
                    dvd_format = f"DVD Box Set ({num_discs})"
            elif 'No. of Disc' in specs:
                num_discs = specs.get('No. of Disc', '').strip()
                if num_discs:
                    dvd_format = f"DVD Box Set ({num_discs})"
        
        # Format price as string with 2 decimal places
        price_value = product.get('price', 0)
        price_str = f"{price_value:.2f}"
        
        video = {
            "id": last_id + idx,
            "title": product['title'],
            "description": product.get('description', ''),
            "releaseDate": product.get('releaseDate', '2023-01-01'),
            "genre": product.get('genre', 'DVD'),
            "thumbnail": product.get('thumbnail', product.get('image_url', '/images/default.jpg')),
            "duration": product.get('duration', '2h 00m'),
            "rating": 4.5,  # Default rating
            "price": price_str,
            "inStock": True,
            "format": dvd_format
        }
        videos.append(video)
    
    return videos

def save_to_videos_json(videos, update_existing=True):
    """Save videos to videos.json file"""
    if update_existing:
        try:
            # Read existing videos.json
            with open(VIDEOS_JSON_PATH, 'r', encoding='utf-8') as f:
                existing_videos = json.load(f)
            
            # Append new videos to existing ones
            all_videos = existing_videos + videos
            
            # Sort videos by ID
            all_videos.sort(key=lambda video: video['id'])
            
            # Reassign IDs sequentially
            for i, video in enumerate(all_videos, 1):
                video['id'] = i
            
            # Save combined list
            with open(VIDEOS_JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump(all_videos, f, ensure_ascii=False, indent=2)
            
            print(f"Added {len(videos)} videos to existing {len(existing_videos)} videos in {VIDEOS_JSON_PATH}")
            print(f"Reassigned IDs for {len(all_videos)} videos")
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is invalid, create new
            # Start IDs from 1
            for i, video in enumerate(videos, 1):
                video['id'] = i
                
            with open(VIDEOS_JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump(videos, f, ensure_ascii=False, indent=2)
            
            print(f"Created new videos.json file with {len(videos)} videos")
    else:
        # Replace existing file
        # Start IDs from 1
        for i, video in enumerate(videos, 1):
            video['id'] = i
            
        with open(VIDEOS_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(videos, f, ensure_ascii=False, indent=2)
        
        print(f"Replaced videos.json file with {len(videos)} videos")

def main():
    """Main function to coordinate the scraping process"""
    print(f"Starting scraping of {BASE_URL} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Scraping limits
    max_pages_per_category = 3  # Limit to first 3 pages
    max_products_per_page = None   # Limit to 5 products per page (set to None for all products)
    save_intermediate = True    # Save intermediate results
    
    # Generate timestamp for this run
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(OUTPUT_DIR, f"pohkim_data_{timestamp}.json")
    intermediate_file = os.path.join(OUTPUT_DIR, f"pohkim_data_{timestamp}_intermediate.json")
    
    # Scrape categories
    categories = scrape_categories()
    print(f"Found {len(categories)} categories")
    
    all_products = []
    categories_processed = 0
    
    # Process each category
    for category in categories:
        categories_processed += 1
        print(f"Processing category: {category['name']} ({categories_processed}/{len(categories)})")
        
        # Starting with the category URL
        page_url = category['url']
        page_count = 1
        
        # Scrape all paginated results (up to max_pages)
        while page_url and page_count <= max_pages_per_category:
            print(f"  Scraping page {page_count} of category: {category['name']} (max: {max_pages_per_category})")
            result = scrape_product_listing_page(page_url)
            products = result['products']
            
            # Limit number of products per page if specified
            if max_products_per_page and len(products) > max_products_per_page:
                print(f"    Limiting from {len(products)} to {max_products_per_page} products on this page")
                products = products[:max_products_per_page]
            
            print(f"    Processing {len(products)} products on this page")
            
            # Get detailed information for each product
            for product in products:
                print(f"    Scraping details for: {product['title']}")
                details = scrape_product_details(product['url'])
                
                # Add category to the product if not already in specifications
                if 'specifications' not in details:
                    details['specifications'] = {}
                
                if 'Category' not in details['specifications']:
                    details['specifications']['Category'] = category['name']
                
                # Merge basic product info with details
                product.update(details)
                all_products.append(product)
            
            # Move to next page if available and within page limit
            page_url = result['next_page']
            page_count += 1
            
            if page_count > max_pages_per_category and result['next_page']:
                print(f"  Reached maximum page limit ({max_pages_per_category}) for category: {category['name']}")
            
            # Save intermediate results if enabled
            if save_intermediate and all_products:
                try:
                    with open(intermediate_file, 'w', encoding='utf-8') as f:
                        json.dump(all_products, f, ensure_ascii=False, indent=2)
                    print(f"  Saved {len(all_products)} products to intermediate file")
                except Exception as e:
                    print(f"  Warning: Failed to save intermediate results: {e}")
    
    # Save final results in original format
    if all_products:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_products, f, ensure_ascii=False, indent=2)
        
        # Convert to videos.json format and save
        videos = convert_to_videos_json_format(all_products)
        save_to_videos_json(videos, update_existing=True)
        
        # Remove intermediate file if it exists
        if save_intermediate and os.path.exists(intermediate_file):
            try:
                os.remove(intermediate_file)
            except Exception:
                pass
    
        print(f"Scraping completed. Data saved to {output_file}")
        print(f"Products also imported to videos.json")
    else:
        print("No products were scraped.")
    
    print(f"Total products scraped: {len(all_products)}")

if __name__ == "__main__":
    main() 