from github import Github

def fetch_github_docs():
    g = Github("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")  # Use your actual GitHub token
    repo = g.get_repo("ros2/ros2_documentation")
    contents = repo.get_contents("")
    
    docs = []
    for content in contents:
        if content.type == "file" and content.name.endswith(".md"):  # Only markdown files
            docs.append(content.download_url)
    return docs
