import requests
import csv
import time
from datetime import datetime
import json
import re
import os

# Near the top of the file, add:
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
data_dir = os.path.join(project_root, 'data')
os.makedirs(data_dir, exist_ok=True)

# When defining the filename, use:
filename = os.path.join(data_dir, "auction_data.csv")

def get_locations(zip_code, miles):
    url = f"https://auction.bidfta.io/api/location/getLocationsByZipMiles?zipCode={zip_code}&miles={miles}"
    response = requests.get(url)
    return response.json()

def fetch_data(page, locations, conditions, keywords):
    url = "https://auction.bidfta.io/api/search/searchItemList"
    params = {
        "itemSearchKeywords": keywords,
        "locations": locations,
        "itemConditionIds": conditions,
        "pageId": page
    }
    response = requests.get(url, params=params)
    return response.json()

def fetch_item_details(url):
    response = requests.get(url)
    return response.json()

def get_build_id():
    url = "https://www.bidfta.com/"
    response = requests.get(url)
    match = re.search(r'/_next/static/([^/]+)/_buildManifest\.js', response.text)
    if match:
        return match.group(1)
    raise ValueError("Could not find build ID")

def fetch_auction_details(auction_id):
    try:
        build_id = get_build_id()
        url = f"https://www.bidfta.com/_next/data/{build_id}/en-US/auction-detail/{auction_id}/1.json?pageId=1&auctionId={auction_id}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        pickup_dates = data['pageProps']['auction']['auctionPickupDates']
        if pickup_dates:
            pickup_start = min(date['pickupDate'] for date in pickup_dates)
            pickup_end = max(date['pickupDate'] for date in pickup_dates)
            return pickup_start, pickup_end
    except requests.exceptions.RequestException as e:
        print(f"Error fetching auction details for auction {auction_id}: {e}")
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"Error parsing auction details for auction {auction_id}: {e}")
        if isinstance(e, json.JSONDecodeError):
            print(f"Response content: {response.text[:200]}...")  # Print first 200 characters of response
    return None, None

def write_to_csv(items, filename, fieldnames=None):
    mode = 'a' if fieldnames else 'w'
    with open(filename, mode, newline='', encoding='utf-8') as file:
        if not fieldnames:
            fieldnames = set()
            for item in items:
                fieldnames.update(item.keys())
                if 'auctionLocation' in item and isinstance(item['auctionLocation'], dict):
                    fieldnames.update(f"auctionLocation_{k}" for k in item['auctionLocation'].keys())
            
            # Fetch details for the first item to get all possible fields
            first_item = items[0]
            fetch_url = f"https://auction.bidfta.io/api/item/itemDetails/{first_item['auctionId']}/{first_item['id']}"
            first_item_details = fetch_item_details(fetch_url)
            fieldnames.update(first_item_details.keys())
            
            fieldnames = sorted(fieldnames)
            fieldnames.extend(["auctionLocationFull", "fetchItemUrl", "pickupStart", "pickupEnd"])

        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
        
        if mode == 'w':
            writer.writeheader()
        
        auction_pickup_cache = {}
        
        for item in items:
            row = item.copy()
            
            if "auctionLocation" in row and isinstance(row["auctionLocation"], dict):
                location = row["auctionLocation"]
                row["auctionLocationFull"] = json.dumps(location)
                for key, value in location.items():
                    row[f"auctionLocation_{key}"] = value
            
            fetch_url = f"https://auction.bidfta.io/api/item/itemDetails/{item['auctionId']}/{item['id']}"
            row["fetchItemUrl"] = fetch_url
            
            # Fetch additional item details
            item_details = fetch_item_details(fetch_url)
            
            # Add all new fields from item details
            for key, value in item_details.items():
                if key not in row:
                    if isinstance(value, (dict, list)):
                        row[key] = json.dumps(value)
                    else:
                        row[key] = value
            
            # Fetch pickup details if not already cached
            if item['auctionId'] not in auction_pickup_cache:
                pickup_start, pickup_end = fetch_auction_details(item['auctionId'])
                auction_pickup_cache[item['auctionId']] = (pickup_start, pickup_end)
            
            row['pickupStart'], row['pickupEnd'] = auction_pickup_cache[item['auctionId']]
            
            writer.writerow(row)
    
    return fieldnames

def main():
    zip_code = input("Enter your zip code (required): ")
    while not zip_code:
        zip_code = input("Zip code is required. Please enter your zip code: ")
    
    miles = input("Enter the search radius in miles: ")
    
    keywords = input("Enter search keywords (optional, press Enter to skip): ")
    
    locations = get_locations(zip_code, miles)
    print("\nAvailable locations:")
    for location in locations:
        print(f"{location['id']}: {location['nickName']} - {location['address']} ({location['miles']} miles)")
    
    selected_locations = input("\nEnter the location numbers you want to query (comma-separated, or press Enter for all): ")
    location_ids = [loc.strip() for loc in selected_locations.split(',')] if selected_locations else []
    location_slugs = [loc['slug'] for loc in locations if str(loc['id']) in location_ids] if location_ids else ['all']
    
    print("\nAvailable conditions:")
    conditions = {
        "5": "Brand New",
        "14": "Good Condition",
        "6": "Working Condition Verified",
        "8": "Preview for Condition",
        "15": "As Is"
    }
    for key, value in conditions.items():
        print(f"{key}: {value}")
    
    selected_conditions = input("\nEnter the condition numbers you want to query (comma-separated, or press Enter for all): ")
    condition_ids = [cond.strip() for cond in selected_conditions.split(',')] if selected_conditions else []
    
    filename = f"auction_data.csv"
    
    first_page = fetch_data(1, ','.join(location_ids), ','.join(condition_ids), keywords)
    total_pages = first_page["pageCount"]
    total_items = first_page["totalCount"]
    
    print(f"\nTotal pages: {total_pages}")
    print(f"Total items: {total_items}")
    
    items_processed = 0
    fieldnames = None
    
    build_id_cache = None

    for page in range(1, total_pages + 1):
        print(f"Processing page {page} of {total_pages}")
        data = fetch_data(page, ','.join(location_ids), ','.join(condition_ids), keywords)
        
        # Fetch build ID if not cached
        if not build_id_cache:
            try:
                build_id_cache = get_build_id()
                print(f"Fetched build ID: {build_id_cache}")
            except ValueError as e:
                print(f"Error fetching build ID: {e}")
                break

        fieldnames = write_to_csv(data["items"], filename, fieldnames)
        items_processed += len(data["items"])
        print(f"Items processed: {items_processed} / {total_items}")
        
        # Add a small delay to avoid overwhelming the server
        time.sleep(1)
    
    print(f"Data collection complete. Results saved to {filename}")

if __name__ == "__main__":
    main()
