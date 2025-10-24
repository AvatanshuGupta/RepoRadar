from fastmcp import FastMCP
import os
from git import Repo

mcp=FastMCP(name="RepoRadar")

CLONE_DIR = "cloned_repos"


@mcp.tool
def clone_repo(url: str) -> str:
    repo_name = url.split("/")[-1].replace(".git", "")
    path = os.path.join(CLONE_DIR, repo_name)
    if not os.path.exists(path):
        Repo.clone_from(url, path)
    return path




@mcp.tool
def generate_tree(start_path, prefix=""):
    """
    this is a helper function which returns the tree structure of the repository
    """

    items = sorted(os.listdir(start_path))
    for index, item in enumerate(items):
        path = os.path.join(start_path, item)
        connector = "└── " if index == len(items) - 1 else "├── "
        print(prefix + connector + item)
        if os.path.isdir(path):
            extension = "    " if index == len(items) - 1 else "│   "
            generate_tree(path, prefix + extension)




