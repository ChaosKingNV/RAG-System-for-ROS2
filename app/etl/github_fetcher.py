from github import Github

def fetch_github_docs():
    github_token = "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"
    
    g = Github(github_token)
    repo = g.get_repo("ros2/ros2_documentation")
    
    docs = []
    try:
        contents = repo.get_contents("")  # Fetch the contents of the root directory
        while contents:
            content = contents.pop(0)
            if content.type == "file" and content.name.endswith(".md"):  # Only markdown files
                docs.append(content.download_url)
            elif content.type == "dir":  # Handle directories (recursively fetch files)
                contents.extend(repo.get_contents(content.path))

    except Exception as e:
        print(f"Error fetching GitHub documentation: {e}")
    
    return docs
