from fastapi import FastAPI
from etl.github_fetcher import fetch_github_docs
from etl.mongodb_loader import store_data_in_mongo
from etl.clear_collection import clear_collection
from etl.web_scraper import scrape_recursively


# Initialize FastAPI
app = FastAPI()

# Define Repositories for GitHub Fetching
SUBDOMAINS = {
    "ros2_docs": "ros2/ros2_documentation",
    "nav2_docs": "ros-navigation/docs.nav2.org",
    "moveit2_docs": "moveit/moveit2_tutorials",
    "gazebo_docs": "gazebosim/docs"
}

# Base URLs for Web Scraping
WEB_SITES = {
    "ros2_docs": "https://docs.ros.org/en/rolling",
    "nav2_docs": "https://docs.nav2.org/",
    "moveit2_docs": "https://moveit.picknik.ai/main/",
    "gazebo_docs": "https://gazebosim.org/libs/"
}


# Custom URL Filter for General Web Scraping
def web_scraper_filter(base_url, next_url, visited_urls):
    """
    Custom filter function for validating URLs within the target websites.

    Args:
        base_url (str): The root/base URL to compare with.
        next_url (str): The next URL to validate.
        visited_urls (set): A set of already visited URLs.

    Returns:
        bool: True if the next_url is valid and should be visited.
    """
    return (
        next_url.startswith(base_url) and  # Must start with the base URL
        next_url not in visited_urls  # Avoid revisiting pages
    )


@app.post("/run_etl")
def trigger_etl():
    """
    Triggers the ETL pipeline for all subdomains and web docs.
    """
    try:
        # Step 1: Clear all collections
        collections_to_clear = list(SUBDOMAINS.keys())
        for collection_name in collections_to_clear:
            clear_collection(collection_name)
            print(f"✅ Cleared collection '{collection_name}'.")

        # Step 2: Scrape Official Docs from Websites
        for collection_name, base_url in WEB_SITES.items():
            scraped_docs = scrape_recursively(base_url, url_filter=web_scraper_filter)

            # Add a "source" field to distinguish this data
            for doc in scraped_docs:
                doc["source"] = "web_scraping"
            store_data_in_mongo(scraped_docs, collection_name)
            print(f"✅ Scraped and stored {len(scraped_docs)} docs from '{collection_name}'.")

        # Step 3: Fetch GitHub Repositories
        for collection_name, repo_name in SUBDOMAINS.items():
            github_docs = fetch_github_docs(repo_name, "")

            # Add a "source" field to distinguish this data
            for doc in github_docs:
                doc["source"] = "github_fetching"
            store_data_in_mongo(github_docs, collection_name)
            print(f"✅ Fetched and stored {len(github_docs)} GitHub docs in '{collection_name}'.")

        return {"message": "✅ ETL pipeline executed successfully for all subdomains!"}

    except Exception as e:
        print(f"❌ ETL pipeline failed: {e}")
        return {"message": f"❌ ETL pipeline failed: {e}"}


# Start the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
