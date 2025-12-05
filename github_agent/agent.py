#import the agent from google.adk.agents
from google.adk.agents import Agent
from google.genai import types # For further configuration controls
from dotenv import load_dotenv
from google.adk.tools import FunctionTool
from .tools.create_repo_tool import create_repository_tool
from .tools.delete_repo_tool import delete_repository_tool



load_dotenv() 




def list_repositories_tool() -> list[str]:
    return ["repository1", "repository2", "repository3"]


list_repositories_tool = FunctionTool(list_repositories_tool)


#create a new agent
root_agent = Agent(
    name="github_agent",
    model="gemini-2.0-flash",
    description="A helpful assistant that can create create and delete github repositories",
    instruction="""
    You are a helpful assistant that can create create and delete github repositories.
    You are also able to create and delete github repositories.
    You will have access to the following tools:
    - create_repository(name: str, description: str, private: bool) -> str: Creates a new repository with the given name and description
    - delete_repository(name: str) -> str: Deletes the repository with the given name
    - list_repositories() -> list[str]: Lists all repositories
    """,
    generate_content_config = types.GenerateContentConfig(
        temperature=0.2, # More deterministic output, closer to 0 more deterministic it is
        max_output_tokens=250
    ),

    tools=[create_repository_tool, delete_repository_tool, list_repositories_tool]
    
)




