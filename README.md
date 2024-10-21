# Auction Viewer and Scraper

A Python-based tool for scraping auction data from bidfta.com and a web-based viewer for easy deal searching.

## Features

- Scrapes auction data based on location, condition, and keywords
- Web-based interface for viewing and searching auction deals
- Customizable search parameters

## Prerequisites

- Python 3.x
- Windows (for batch script execution)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/auction-viewer-and-scraper.git
   cd auction-viewer-and-scraper
   ```
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Scraping Data

1. Run the scraper:
   ```
   python backend/auction_scraper.py
   ```
2. Follow the prompts to enter search criteria
3. The script will save the data to `data/auction_data.csv`

### Viewing Data

1. Launch the viewer:
   ```
   scripts/launch_auction_viewer.bat
   ```
2. Your default browser will open to the auction viewer
3. Use the search bar and filters to explore the data

## Project Structure

- `frontend/`: HTML and CSS for the auction viewer
- `backend/`: Python scraper script
- `scripts/`: Utility scripts
- `data/`: Scraped auction data (CSV)

### Open an Issue When:

- You've found a bug in the existing code
- You have a feature request or idea for improvement
- You're experiencing unexpected behavior
- You have questions about how to use the project
- You want to discuss a change before investing time in a pull request

To open an issue:
1. Go to the [Issues tab](https://github.com/jnjustice/bidfta-auction-scraper/issues) in this repository
2. Click on "New Issue"
3. Choose the appropriate issue template if available, or start with a blank issue
4. Provide as much detail as possible, including steps to reproduce for bugs


## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
