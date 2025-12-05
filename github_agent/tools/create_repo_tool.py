from google.adk.tools import FunctionTool
from dotenv import load_dotenv
import requests
import os
load_dotenv()


def create_repository_tool( name: str, description: str, private: bool = False) -> str:
    """
    Creates a new repository with the given name and description
    
    Args:
        name: str - The name of the repository
        description: str - The description of the repository
        private: bool - Whether the repository is private

    Returns:
        str - A message indicating that the repository was created successfully
    """


    headers = {
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github+json",
    }
    #Always add agent-{name} to the repository name
    name = f"agent-{name}"
    
    # 1) Check if repo exists for the authenticated user
    me = requests.get("https://api.github.com/user", headers=headers)
    me.raise_for_status()
    owner = me.json()["login"]

    check = requests.get(f"https://api.github.com/repos/{owner}/{name}", headers=headers)

    if check.status_code == 200:
        raise RuntimeError(f"Repository '{owner}/{name}' already exists")

    # 2) Create repo (will still fail if race condition)
    payload = {"name": name, "private": private}
    resp = requests.post("https://api.github.com/user/repos", json=payload, headers=headers)
    resp.raise_for_status()

    return resp.json()



create_repository_tool = FunctionTool(create_repository_tool)