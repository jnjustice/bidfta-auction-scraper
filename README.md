# Auction Viewer and Scraper
This repo is a Python scraper for collecting auction deals from bidfta.com and provides a web-based auction viewer to easily search deals.

## Structure

- `frontend/`: Contains the HTML and CSS for the auction viewer
- `backend/`: Contains the Python scraper script
- `scripts/`: Contains utility scripts

## Setup

1. Clone this repository
2. Navigate to the project directory
3. Run the scraper:
   ```
   python backend/auction_scraper.py
   ```
4. Launch the auction viewer:
   ```
   scripts/launch_auction_viewer.bat
   ```

# Usage

The auction_scraper.py script is a command-line tool that scrapes auction data from the bidfta.io website. It allows you to search for auctions based on location, condition, and keywords, and saves the results to a CSV file.

## Prerequisites

- Python 3.x installed on your system
- Required Python packages: requests

To install the required package, run:
```
pip install requests
```

## Running the Script

1. Open a terminal or command prompt.
2. Navigate to the directory containing auction_scraper.py.
3. Run the script using Python:
   ```
   python auction_scraper.py
   ```

## Input Parameters

The script will prompt you for the following inputs:

1. Zip Code (required): Enter your zip code to search for nearby auctions.
2. Search Radius: Enter the distance in miles to search for auctions from your zip code.
3. Search Keywords (optional): Enter any keywords to filter the auction items. Press Enter to skip.
4. Location Selection: The script will display a list of available locations. Enter the location numbers you want to query, separated by commas, or press Enter to search all locations.
5. Condition Selection: The script will display a list of item conditions. Enter the condition numbers you want to query, separated by commas, or press Enter to search all conditions.

## Output

The script will create a file named auction_data.csv in the same directory. This CSV file will contain the following information for each auction item:

- Auction ID
- Lot Code
- Item details (title, description, etc.)
- Current bid information
- Auction location details
- Item condition
- Pickup dates
- And more...

The script will display progress information in the terminal, showing the current page being processed and the total number of items scraped.

## Example Usage

```
$ python auction_scraper.py
Enter your zip code (required): 12345
Enter the search radius in miles: 50
Enter search keywords (optional, press Enter to skip): furniture

Available locations:
1: Location A - 123 Main St (10 miles)
2: Location B - 456 Elm St (25 miles)
3: Location C - 789 Oak St (40 miles)

Enter the location numbers you want to query (comma-separated, or press Enter for all): 1,2

Available conditions:
5: Brand New
14: Good Condition
6: Working Condition Verified
8: Preview for Condition
15: As Is

Enter the condition numbers you want to query (comma-separated, or press Enter for all): 14,15

Processing page 1 of 10
Items processed: 50 / 500
...
Data collection complete. Results saved to auction_data.csv
```
# Usage Instructions for Auction Viewer

## Using launch_auction_viewer.bat

The `launch_auction_viewer.bat` script is designed to easily start a local web server and open the auction viewer in your default web browser.

### Prerequisites
- Python 3.x installed on your system
- Windows operating system (for .bat file execution)

### Steps to Launch

1. Ensure that `launch_auction_viewer.bat`, `auction_viewer.html`, and `style.css` are in the same directory.
2. Double-click on `launch_auction_viewer.bat` or run it from the command prompt.
3. The script will:
   - Start a Python HTTP server on port 8000
   - Open your default web browser to `http://localhost:8000/auction_viewer.html`
4. The auction viewer should now be visible in your web browser.
5. To stop the server, close the command prompt window that opened when you ran the script.

### Troubleshooting
- If the browser doesn't open automatically, manually navigate to `http://localhost:8000/auction_viewer.html`
- If you see an error about Python not being recognized, ensure that Python is installed and added to your system's PATH.

## Using auction_viewer.html

The `auction_viewer.html` file is the frontend interface for viewing auction data. It's designed to work with data scraped by the `auction_scraper.py` script.

### Features

1. **Search**: Use the search bar at the top to filter auction items.
2. **Filters**: Apply filters for Auction IDs, Lot Codes, Categories, Conditions, and Bid Counts.
3. **Clear**: Reset all search criteria and filters.
4. **Auction Groups**: View auction items grouped by various criteria.

### How to Use

1. Once the page is loaded in your browser:
   - Use the search bar to find specific items.
   - Apply filters to narrow down the displayed auctions.
   - Click on auction groups to expand and view details.
2. The page will display auction items based on your search criteria and filters.
3. Scroll through the results to view different auction items.

### Notes
- The auction viewer requires JavaScript to be enabled in your browser.
- For the best experience, use a modern web browser like Chrome, Firefox, or Edge.
- The viewer is designed to work with data in a specific format. Ensure that your data source (e.g., the output from auction_scraper.py) is compatible.

### Customization
- If you need to modify the appearance of the viewer, edit the `style.css` file.
- For functional changes, you may need to modify the JavaScript code within `auction_viewer.html`.

## Integrating with auction_scraper.py

To use the auction viewer with data from the scraper:

1. Run `auction_scraper.py` to collect auction data.
2. Ensure the resulting CSV file is in the same directory as `auction_viewer.html`.
3. Update `auction_viewer.html` to load data from your CSV file (you may need to modify the JavaScript code for this).
4. Launch the viewer using `launch_auction_viewer.bat`.

By following these steps, you'll be able to view the scraped auction data in a user-friendly interface.

## Note

- The script may take some time to run, depending on the number of items found and the speed of your internet connection.
- Be respectful of the website's resources and avoid running the script too frequently or with very broad search parameters.
- The resulting CSV file can be opened with spreadsheet software like Microsoft Excel or Google Sheets for further analysis.

## Contributing

[Add guidelines for contributing to the project]

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
