import requests

# Define the endpoints
MAP_URL = "http://localhost:3002/v1/map"
CRAWL_URL = "http://localhost:3002/v1/scrape"

def map_website(base_url):
    print(f"Mapping {base_url} for available links...")
    try:
        response = requests.post(MAP_URL, json={'url': base_url})
        response.raise_for_status()  # Check for request errors
        result = response.json()
        links = result.get('links', [])
        if links:
            print(f"Found {len(links)} links.")
            return links
        else:
            print("No links found in the response.")
            return []
    except Exception as e:
        print(f"An error occurred during mapping: {str(e)}")
        return []

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

def scrape_url(url):
    print(f"Scraping content from {url}...")
    try:
        response = requests.post(CRAWL_URL, json={'url': url, 'formats': ['markdown']})
        response.raise_for_status()  # Check for request errors
        result = response.json()
        markdown_content = result.get('data', {}).get('markdown', '')
        if markdown_content:
            output_path = 'scraped_content.md'
            with open(output_path, 'w', encoding='utf-8') as markdown_file:
                markdown_file.write(markdown_content)
            print(f"Markdown content saved to {output_path}")
        else:
            print("No markdown content found.")
    except Exception as e:
        print(f"An error occurred during scraping: {str(e)}")

# Main process
if __name__ == "__main__":
    base_url = input("Enter the website URL: ")
    links = map_website(base_url)
    
    if links:
        selected_url = choose_url(links)
        if selected_url:
            scrape_url(selected_url)
    else:
        print("No links found or available to scrape.")
