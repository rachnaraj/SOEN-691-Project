import requests
import subprocess
import datetime
import os
import re

# GitHub API URL
GITHUB_API = "https://api.github.com/search/repositories"

# Authentication token
TOKEN = "your_github_token"

# Search GitHub for repositories
def search_github_repositories(keywords, language="Python", min_stars=10, min_forks=10, max_repos=10):
    headers = {'Authorization': f'token {TOKEN}'} if TOKEN else {}
    
    # Get the date for one year ago
    one_year_ago = datetime.date.today() - datetime.timedelta(days=365)
    one_year_ago_str = one_year_ago.isoformat()

    # Combine keywords with 'OR' and add qualifiers for stars, forks, and created date
    query = ' '.join([f"{keyword}+language:{language}" for keyword in keywords])
    query += f" stars:>{min_stars} forks:>{min_forks} created:>{one_year_ago_str}"

    params = {"q": query, "sort": "stars", "order": "desc"}
    response = requests.get(GITHUB_API, headers=headers, params=params)
    response.raise_for_status()
    items = response.json().get("items", [])
    return items[:max_repos]

# Clone a repository
def clone_repository(repo_url, local_path):
    subprocess.run(["git", "clone", repo_url, local_path], check=True)

# Find SADTs in code
def find_sadts_in_code(repo_path):
    sadts = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        if re.search(r'\b(TODO|FIXME|HACK|XXX)\b', line):
                            sadts.append((file_path, line_num, line.strip()))
    return sadts

# Main process
def main():
    # Step 1: Search for ML repositories
    keywords = ["machine learning", "deep learning", "neural network"]
    ml_repositories = search_github_repositories(keywords)

    # Step 2 & 3: Clone repositories and analyze them
    for repo in ml_repositories:
        repo_url = repo['clone_url']
        local_path = os.path.join("SADTs-Repos", repo['name'])
        clone_repository(repo_url, local_path)
        sadts = find_sadts_in_code(local_path)
        print(f"SADTs in {repo['name']}:", sadts)

if __name__ == "__main__":
    main()
