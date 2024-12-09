from github_fetcher import fetch_github_docs
from mongodb_loader import store_data_in_mongo
from clear_collection import clear_collection
from web_scraper import scrape_recursively


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


# Custom URL Filter for Web Scraping
def web_scraper_filter(base_url, next_url, visited_urls):
    return (
        next_url.startswith(base_url) and  # Must start with the base URL
        next_url not in visited_urls  # Avoid revisiting pages
    )


# The ETL Pipeline Logic
def run_etl_pipeline():
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
