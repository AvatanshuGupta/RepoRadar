# RepoRadar - Git Repository Manager with FastMCP

**RepoRadar** is an AI-assisted Git repository manager built using **FastMCP**. It allows you to clone Git repositories, read and edit files, stage/unstage changes, commit, push, and visualize the repository tree structure — all programmatically through MCP tools. This project is ideal for automating repository management and experimentation with Git operations.

---
https://RepoRadar.fastmcp.app/mcp  RepoRadar mcp server is live on this link
---


## **Table of Contents**

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [MCP Tools Overview](#mcp-tools-overview)
7. [Deployment on FastMCP Cloud](#deployment-on-fastmcp-cloud)
8. [Directory Structure](#directory-structure)
9. [Contributing](#contributing)


---

## **Project Overview**

RepoRadar is a Python-based MCP server that provides programmatic access to Git repositories. Using FastMCP, you can perform Git operations like clone, read, edit, commit, push, and manage staged changes without directly using the terminal.

It is built for:

* Automating Git workflows
* Repository monitoring
* Learning and experimenting with MCP tool creation
* Integration with other MCP-based systems or agents

---

## **Features**

* Clone GitHub repositories into a local directory
* Read file content (with character limit support)
* Edit or add new files to repositories
* Stage and unstage files individually or all at once
* Commit changes with custom messages
* Push commits to remote repositories
* Generate a tree-like structure of the repository
* Fully compatible with FastMCP cloud deployment (Linux-based)

---

## **Requirements**

* Python 3.12+
* FastMCP >= 2.12.5
* GitPython
* Internet connection for cloning and pushing to repositories

**Python Dependencies (from `requirements.txt`):**

```
fastmcp==2.12.5
gitpython==3.1.45
mcp==1.16.0
uvicorn==0.38.0
requests==2.32.5
pydantic==2.12.3
python-multipart==0.0.20
rich==14.2.0
...
```

> ⚠ **Note:** `pywin32` is removed because it is Windows-specific and will fail on FastMCP cloud (Linux).

---

## **Installation**

1. Clone this repository locally:

```bash
git clone https://github.com/AvatanshuGupta/RepoRadar.git
cd RepoRadar
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies using `uv`:

```bash
uv pip install -r requirements.txt
```

4. Make sure Git is installed and accessible from your terminal.

---

## **Usage**

Run the MCP server locally:

```bash
python main.py
```

This starts the FastMCP server in **development mode**. You can now call MCP tools either:

* Through the MCP Inspector
* Or via another MCP client

---

## **MCP Tools Overview**

| Tool                                                                          | Description                                      |
| ----------------------------------------------------------------------------- | ------------------------------------------------ |
| `clone_repo(url: str)`                                                        | Clone a GitHub repository locally                |
| `read_file(repo_name: str, relative_path: str, max_chars: int=5000)`          | Read a file’s content (truncated)                |
| `edit_or_add_file(repo_name: str, relative_path: str, content: str)`          | Add or edit a file without committing            |
| `commit_changes(repo_name: str, file_paths: list, commit_message: str)`       | Commit staged files                              |
| `push_changes(repo_name: str, remote_name: str="origin", branch: str="main")` | Push commits to remote                           |
| `destage_files(repo_name: str, file_paths: list)`                             | Unstage specific files                           |
| `destage_all(repo_name: str)`                                                 | Unstage all staged changes                       |
| `generate_tree_initiation()`                                                  | Generate a tree-like structure of the repository |

> **Important:** File paths in `commit_changes`, `destage_files`, and similar tools should be **relative to the repository root**.

---

## **Deployment on FastMCP Cloud**

To deploy `RepoRadar` to FastMCP Cloud:

1. Make sure your repository is on GitHub.
2. Update `requirements.txt` with Linux-compatible dependencies (remove `pywin32`).
3. Go to FastMCP Cloud and create a new MCP server.
4. Connect it to your GitHub repo.
5. Set the **entrypoint** to `main.py`.
6. Optionally, set environment variables if needed.
7. Deploy. The server will start automatically in the cloud.

> **Tip:** If deployment fails due to `pywin32`, remove it from `requirements.txt`. MCP cloud uses Linux containers.

---

## **Directory Structure**

```
RepoRadar/
├── cloned_repos/          # Local clone directory
├── main.py                # MCP server entrypoint
├── requirements.txt       # Python dependencies
├── README.md
└── .gitignore
```

* `cloned_repos/` is created automatically if it doesn’t exist.
* All cloned repositories are stored here.

---

## **Contributing**

1. Fork the repository
2. Create a branch for your feature
3. Implement your feature or fix
4. Submit a pull request

---



## **Notes & Best Practices**

* Always use relative file paths in Git operations.
* Use `destage_all` to safely unstage everything before new changes.
* Avoid Windows-specific packages for cloud deployment.
* Use `generate_tree_initiation()` to visualize repository structure before co
