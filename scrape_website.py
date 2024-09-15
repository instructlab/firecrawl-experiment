import os
import io
from dotenv import load_dotenv
from contextlib import redirect_stdout
from firecrawl import FirecrawlApp

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('FIRECRAWL_API_KEY')
if not api_key:
    raise ValueError("API key not found. Please set the FIRECRAWL_API_KEY environment variable.")

app = FirecrawlApp(api_key=api_key)

def map_website(base_url):
    print(f"Mapping {base_url} for available links...")
    try:
        # Capture and suppress the output from app.map_url
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            response = app.map_url(base_url)
        
        # Check if the response was successful and contains links
        if isinstance(response, dict) and response.get('success') and 'links' in response:
            links = response['links']
        elif isinstance(response, list):
            links = response
        else:
            print("API call was not successful or didn't return links in the expected format.")
            return []
        
        if links:
            print(f"Found {len(links)} links.")
            return links
        else:
            print("No links found in the response.")
            return []
    except Exception as e:
        print(f"An error occurred during mapping: {str(e)}")
        return []

# Step 2: Allow user to select which URL they want to scrape
def choose_url(links):
    if not links:
        print("No links available to choose from.")
        return None
    
    def display_links(start, end):
        print("\nAvailable URLs:")
        print("--------------------")
        for idx, link in enumerate(links[start:end], start=start+1):
            print(f"{idx:3}. {link}")
        print("--------------------")

    start = 0
    page_size = 5
    total_links = len(links)

    while True:
        display_links(start, start + page_size)
        
        if start + page_size < total_links:
            print("\nOptions:")
            print("- Enter a number to select a URL")
            print("- Type 'more' to see the next 5 links")
            print("- Type 'all' to see all links")
            print("- Type 'exit' to quit")
        else:
            print("\nOptions:")
            print("- Enter a number to select a URL")
            print("- Type 'exit' to quit")

        choice = input("\nYour choice: ").lower().strip()

        if choice == 'exit':
            print("Exiting.")
            return None
        elif choice == 'more' and start + page_size < total_links:
            start += page_size
        elif choice == 'all':
            display_links(0, total_links)
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < total_links:
                    return links[index]
                else:
                    print(f"Invalid choice. Please choose a number between 1 and {total_links}.")
            except ValueError:
                print("Invalid input. Please enter a valid option.")

        print()  # Add a blank line for better readability

# Step 3: Scrape the chosen URL for markdown content
def scrape_url(url):
    print(f"Scraping content from {url}...")
    try:
        response = app.scrape_url(url=url, params={
            'formats': ['markdown'],
        })
        
        if isinstance(response, dict) and 'markdown' in response:
            # Extract the markdown content
            markdown_content = response['markdown']
            # Save the markdown content to a new file
            output_path = 'scraped_content.md'
            with open(output_path, 'w', encoding='utf-8') as markdown_file:
                markdown_file.write(markdown_content)
            print(f"Markdown content saved to {output_path}")
        else:
            print("Scraping failed or markdown content is not present.")
    except Exception as e:
        print(f"An error occurred during scraping: {str(e)}")

# Main process
if __name__ == "__main__":
    # Step 1: Input the base URL to map the website
    base_url = input("Enter the website URL: ")
    
    # Step 2: Map the website and get the list of available links
    links = map_website(base_url)
    
    # Step 3: If links are available, allow the user to choose one to scrape
    if links:
        selected_url = choose_url(links)
        # Step 4: Scrape the selected URL for markdown content
        if selected_url:
            scrape_url(selected_url)
    else:
        print("No links found or available to scrape.")
