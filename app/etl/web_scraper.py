import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_recursively(base_url, visited_urls=None, tags_to_extract=None, url_filter=None, max_visits=10000):
    """
    Generalized web scraper that recursively scrapes web pages with a max visits limit.

    Args:
        base_url (str): The starting URL for web scraping.
        visited_urls (set): Tracks visited URLs to avoid duplicates.
        tags_to_extract (list): HTML tags to extract.
        url_filter (function): A filtering function to keep relevant URLs.
        max_visits (int): The maximum number of pages to visit.

    Returns:
        list: A list of scraped documents.
    """

    if visited_urls is None:
        visited_urls = set()

    if tags_to_extract is None:
        tags_to_extract = ["h1", "h2", "p", "pre", "code"]

    docs = []

    # Stop if we've reached the max visits limit
    if len(visited_urls) >= max_visits:
        print(f"⚠️ Max visits limit of {max_visits} reached. Stopping.")
        return docs

    try:
        print(f"🔍 Scraping: {base_url} | Visited: {len(visited_urls)}")

        if base_url in visited_urls:
            print(f"🔄 Already visited {base_url}, skipping.")
            return docs

        response = requests.get(base_url, timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to fetch {base_url} (Status Code: {response.status_code})")
            return docs

        soup = BeautifulSoup(response.text, "html.parser")
        extracted_content = []

        # Extract content from specified tags
        for tag in tags_to_extract:
            elements = soup.find_all(tag)
            for element in elements:
                extracted_content.append(element.get_text(strip=True))

        if extracted_content:
            docs.append({
                "url": base_url,
                "title": soup.title.get_text(strip=True) if soup.title else "No Title",
                "content": "\n".join(extracted_content)
            })
            print(f"✅ Scraped: {base_url} | Found {len(extracted_content)} elements.")

        # Mark as visited
        visited_urls.add(base_url)

        # Follow internal links
        for link in soup.find_all("a", href=True):
            href = link["href"]
            next_url = urljoin(base_url, href)

            # Use the custom filtering function
            if url_filter and url_filter(base_url, next_url, visited_urls):
                print(f"🔗 Found internal link: {next_url}")
                docs.extend(scrape_recursively(next_url, visited_urls, tags_to_extract, url_filter, max_visits))

    except Exception as e:
        print(f"❌ Error scraping {base_url}: {e}")

    return docs
