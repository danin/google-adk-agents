from google.adk.tools import FunctionTool
from dotenv import load_dotenv
import os
import requests

load_dotenv()


from google.adk.tools import FunctionTool
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def delete_repository_tool(name: str) -> str:
    """
    Deletes a repository with the given name.

    Args:
        name: The name of the repository.

    Returns:
        A message indicating the result.
    """
    headers = {
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github+json",
    }

    # 1) Get username (owner) from token
    me = requests.get("https://api.github.com/user", headers=headers)
    me.raise_for_status()
    owner = me.json()["login"]

    # 2) Delete repo under that owner
    url = f"https://api.github.com/repos/{owner}/{name}"
    resp = requests.delete(url, headers=headers)

    if resp.status_code == 204:
        return f"Repository '{owner}/{name}' deleted successfully."
    if resp.status_code == 404:
        raise RuntimeError(f"Repository '{owner}/{name}' does not exist or you lack access.")
    resp.raise_for_status()
    return f"Unexpected status {resp.status_code} when deleting repository."

#add the tool to the agent
delete_repository_tool = FunctionTool(delete_repository_tool)
