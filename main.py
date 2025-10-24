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
def edit_or_add_file(repo_name: str, relative_path: str, content: str) -> str:
    """
    Add or edit a file in the cloned repo without committing.
    """
    repo_path = os.path.join(CLONE_DIR, repo_name)
    if not os.path.exists(repo_path):
        return f"Repository '{repo_name}' not found."

    # Full path to the file
    file_path = os.path.join(repo_path, relative_path)

    # Ensure parent directories exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Write content to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"File '{relative_path}' added/edited successfully. Commit separately."

@mcp.tool
def commit_changes(repo_name: str, file_paths: list, commit_message: str) -> str:
    """
    Commit staged files in a repository. File paths must be relative to repo root.
    """
    repo_path = os.path.join(CLONE_DIR, repo_name)
    if not os.path.exists(repo_path):
        return f"Repository '{repo_name}' not found."

    repo = Repo(repo_path)

    # Stage files using paths **relative to repo root**
    repo.index.add(file_paths)

    # Commit
    repo.index.commit(commit_message)

    return f"Committed {len(file_paths)} file(s) with message: '{commit_message}'"





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


@mcp.tool
def push_changes(repo_name: str, remote_name: str = "origin", branch: str = "main") -> str:
    """
    Push commits to the remote repository.
    """
    repo_path = os.path.join(CLONE_DIR, repo_name)
    if not os.path.exists(repo_path):
        return f"Repository '{repo_name}' not found."

    repo = Repo(repo_path)
    origin = repo.remote(name=remote_name)
    origin.push(refspec=f"{branch}:{branch}")

    return f"Pushed changes to {remote_name}/{branch}"


@mcp.tool
def destage_files(repo_name: str, file_paths: list) -> str:
    """
    Unstage specified files in a repository (remove from Git staging area).
    
    repo_name: Name of the cloned repo inside CLONE_DIR
    file_paths: List of file paths relative to repo root
    """
    repo_path = os.path.join(CLONE_DIR, repo_name)
    if not os.path.exists(repo_path):
        return f"Repository '{repo_name}' not found."

    repo = Repo(repo_path)

    # Convert to absolute paths
    abs_paths = [os.path.join(repo_path, f) for f in file_paths]

    # Unstage each file
    try:
        repo.index.reset(abs_paths, working_tree=False)
        return f"Unstaged {len(file_paths)} file(s) successfully."
    except Exception as e:
        return f"Error destaging files: {str(e)}"

@mcp.tool
def destage_all(repo_name: str) -> str:
    """
    Unstage all staged changes in the repository.
    Equivalent to `git reset` with no arguments.
    """
    repo_path = os.path.join(CLONE_DIR, repo_name)
    if not os.path.exists(repo_path):
        return f"Repository '{repo_name}' not found."

    repo = Repo(repo_path)

    try:
        repo.git.reset()  # Reset staging area only
        return "All staged changes have been unstaged."
    except Exception as e:
        return f"Error destaging all files: {str(e)}"




if __name__=="__main__":
    mcp.run()
