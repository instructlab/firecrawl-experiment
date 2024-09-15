# Firecrawl Experiment

This project is an experiment using the Firecrawl API to map and scrape websites. It maps a given website to get all subpage links, allows the user to choose a URL, and scrapes the content, saving it in markdown format.

## Features

- Map a website to retrieve all subpage links.
- Interactive CLI to select a URL for scraping.
- Save scraped content as a Markdown file.

## Prerequisites

- Python 3.x
- Firecrawl API Key
    -   To obtain an API key, visit https://www.firecrawl.dev and sign up for an account.
## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/instructlab/firecrawl-experiment.git
   
   cd firecrawl-experiment
   ```

2. Create a `.env` file in the root directory:
   ```bash
   touch .env
   ```
   Add your Firecrawl API key to the `.env` file:
   ```
   FIRECRAWL_API_KEY=your_api_key_here
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```bash
   python scrape_website.py
   ```
2. Enter the base URL of the website you want to scrape.
3. Select a URL from the list of available links.
4. The content will be scraped and saved as `scraped_content.md`.

## Example

```bash
Enter the website URL: https://www.example.com
Mapping https://www.example.com for available links...
Found 20 links.
Available URLs:
--------------------
1. https://www.example.com
2. https://www.example.com/about
3. https://www.example.com/contact
...

Options:
- Enter a number to select a URL
- Type 'more' to see the next 5 links
- Type 'all' to see all links
- Type 'exit' to quit

Your choice: 2
Scraping content from https://www.example.com/about...
Markdown content saved to scraped_content.md
```