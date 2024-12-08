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

# Base URL for Web Scraping
#ROS_DOCS_BASE_URL = "https://docs.ros.org/en/rolling"
TEST_COLLECTION = "test_site_docs"
TEST_SITE_BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"


# Custom URL Filter for the ROS2 Docs Website
# def ros2_url_filter(base_url, next_url, visited_urls):
#     """
#     Custom filter function for validating URLs within ROS2 docs.

#     Args:
#         base_url (str): The root/base URL to compare with.
#         next_url (str): The next URL to validate.
#         visited_urls (set): A set of already visited URLs.

#     Returns:
#         bool: True if the next_url is valid and should be visited.
#     """
#     return (
#         next_url.startswith(base_url) and  # Must start with the base URL
#         next_url not in visited_urls and  # Avoid revisiting pages
#         "/en/rolling/" in next_url  # Ensure it's within the docs site
#     )
def test_site_url_filter(base_url, next_url, visited_urls):
    return (
        next_url.startswith(base_url) and
        next_url not in visited_urls
    )


@app.post("/run_etl")
def trigger_etl():
    """
    Triggers the ETL pipeline for all subdomains.
    """
    try:
        # Step 1: Clear all collections at once
        print(f"✅ Cleared collection '{TEST_COLLECTION}'.")
        collections_to_clear = list(SUBDOMAINS.keys())
        for collection_name in collections_to_clear:
            clear_collection(collection_name)
            print(f"✅ Cleared collection '{collection_name}'.")

        # Step 2: Scrape ROS Official Docs Using Web Scraper
        scraped_docs = scrape_recursively(
            #ROS_DOCS_BASE_URL, url_filter=ros2_url_filter
            TEST_SITE_BASE_URL, url_filter=test_site_url_filter
            
        )
        for doc in scraped_docs:
            doc["source"] = "test_site_scraping"
        store_data_in_mongo(scraped_docs, TEST_COLLECTION)
        print(f"✅ Scraped and stored {len(scraped_docs)} documents from the test site.")

        # # Add a "source" field to distinguish this data
        # for doc in scraped_docs:
        #     doc["source"] = "web_scraping"
        # store_data_in_mongo(scraped_docs, "ros2_docs")
        # print(f"✅ Scraped and stored {len(scraped_docs)} ROS2 docs from official site.")

        # Step 3: Fetch GitHub Repositories
        for collection_name, repo_name in SUBDOMAINS.items():
            if collection_name == "ros2_docs":
                # Fetch only the GitHub part for ros2_docs
                github_docs = fetch_github_docs(repo_name, "")
                # Add a "source" field to distinguish this data
                for doc in github_docs:
                    doc["source"] = "github_fetching"
                store_data_in_mongo(github_docs, "ros2_docs")
                print(f"✅ Fetched and stored {len(github_docs)} GitHub docs in 'ros2_docs'.")
            else:
                # Handle other repositories normally
                github_docs = fetch_github_docs(repo_name, "")
                store_data_in_mongo(github_docs, collection_name)
                print(f"✅ Fetched and stored {len(github_docs)} docs in '{collection_name}'.")

        return {"message": "✅ ETL pipeline executed successfully for all subdomains!"}

    except Exception as e:
        print(f"❌ ETL pipeline failed: {e}")
        return {"message": f"❌ ETL pipeline failed: {e}"}


# Start the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
