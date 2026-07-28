class GitHubEngine:
    def analyze_repo(self, repo_name: str) -> dict:
        return {"repo": repo_name, "issues_count": 0, "prs_open": 0, "status": "HEALTHY"}

    def prepare_pull_request(self, branch: str, title: str) -> dict:
        return {"branch": branch, "title": title, "ready_to_merge": True}
