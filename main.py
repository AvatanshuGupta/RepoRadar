from fastmcp import FastMCP
import os
from git import Repo
import sys


sys.stdout.reconfigure(encoding='utf-8')

mcp=FastMCP(name="RepoRadar")

CLONE_DIR = "cloned_repos"


@mcp.tool
def clone_repo(url: str) -> str:
    """
    this is a helper function used to clone a github repository from it's url and save the repository
    locally.
    """
    repo_name = url.split("/")[-1].replace(".git", "")
    path = os.path.join(CLONE_DIR, repo_name)
    if not os.path.exists(path):
        Repo.clone_from(url, path)
    return path


@mcp.tool
def read_file(repo_name: str, relative_path: str, max_chars: int = 5000):
    """Return contents of a single file, truncated"""
    path = os.path.join(CLONE_DIR, repo_name, relative_path)
    if not os.path.isfile(path):
        return {"error": "file not found"}
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read(max_chars)
    return content




@mcp.tool
def generate_tree_initiation():
    """
    Returns the tree structure of the repository as a string
    """
    result = []

    def generate_tree(start_path, prefix=""):
        items = sorted(os.listdir(start_path))
        for index, item in enumerate(items):
            path = os.path.join(start_path, item)
            connector = "└── " if index == len(items) - 1 else "├── "
            result.append(prefix + connector + item)
            if os.path.isdir(path):
                extension = "    " if index == len(items) - 1 else "│   "
                generate_tree(path, prefix + extension)

    generate_tree(CLONE_DIR)
    return "\n".join(result)


if __name__=="__main__":
    mcp.run()
