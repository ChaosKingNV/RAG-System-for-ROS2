from github import Github

def fetch_ros2_middleware_docs():
    # Set your GitHub token here
    github_token = "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"
    
    # Initialize the GitHub client
    g = Github(github_token)
    
    # Fetch the specific repository - ROS2 Documentation
    repo = g.get_repo("ros2/ros2_documentation")
    
    docs = []
    try:
        contents = repo.get_contents("")  # Get contents of the root directory
        print("Fetching GitHub Contents...")
        while contents:
            content = contents.pop(0)
            #print(f"Content: {content.name}, Type: {content.type}")  # Debug line
            
            # Filtering criteria: look for files related to middleware
            if content.type == "file" and content.name.endswith(".md"):
                docs.append({
                    "file_name": content.name,
                    "url": content.download_url
                })
                # Check if the file path contains 'middleware', 'dds', 'communication', or any related terms
                    # if 'middleware' in content.path.lower() or 'dds' in content.path.lower() or 'communication' in content.path.lower():
                    #     docs.append(content.download_url)  # Add the download URL of the middleware-related docs
            
            elif content.type == "dir":  # Recurse into directories
                contents.extend(repo.get_contents(content.path))

    except Exception as e:
        print(f"Error fetching GitHub documentation: {e}")
    
    return docs

# # Call the function to get middleware docs URLs
# middleware_docs = fetch_ros2_middleware_docs()
# print("Fetched Middleware Docs:", middleware_docs)
