import requests
from github import Github


def fetch_github_docs(repo_name, subdomain_folder):
    """
    Fetches GitHub documents from the specified repository and folder.

    Args:
        repo_name (str): The GitHub repository name (e.g., 'ros2/ros2_documentation').
        subdomain_folder (str): The subdomain folder to fetch files from (e.g., 'nav2').

    Returns:
        list: A list of dictionaries containing file metadata and content.
    """
    # Set your GitHub token here
    github_token = "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"

    # Initialize the GitHub client
    g = Github(github_token)

    # Fetch the specified repository
    repo = g.get_repo(repo_name)

    docs = []
    try:
        # Fetch root directory contents
        contents = repo.get_contents(subdomain_folder)
        print(f"Fetching GitHub Contents from {subdomain_folder}...")

        # Process files and folders recursively
        while contents:
            content = contents.pop(0)
            print(f"Content: {content.name}, Type: {content.type}")  # Debug line

            # Filter Markdown files
            if content.type == "file" and content.name.endswith(".md"):
                # Download file content
                file_content = fetch_file_content(content.download_url)

                # Store file metadata
                docs.append({
                    "file_name": content.name,
                    "url": content.download_url,
                    "content": file_content,
                    "path": content.path
                })

            # Recurse into directories
            elif content.type == "dir":
                contents.extend(repo.get_contents(content.path))

        print(f"✅ Fetched {len(docs)} docs from {subdomain_folder}.")

    except Exception as e:
        print(f"Error fetching GitHub documentation from {subdomain_folder}: {e}")

    return docs


def fetch_file_content(url):
    """
    Downloads file content from the provided URL.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"✅ Fetched content from {url}")
            return response.text
        else:
            print(f"❌ Failed to fetch content from {url}")
            return "Content fetch failed"
    except Exception as e:
        print(f"❌ Error downloading content: {e}")
        return "Content fetch failed"
