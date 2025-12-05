# GitHub Agent

A simple AI agent built with Google ADK (Agent Development Kit) that can create, delete, and list GitHub repositories using the Gemini 2.0 Flash model.

## Features

- Create GitHub repositories
- Delete GitHub repositories
- List repositories

## Prerequisites

- Python 3.x
- Google API Key
- GitHub Personal Access Token

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root (you can use `github_agent/sample_env` as a template):
```bash
GOOGLE_API_KEY="your_google_api_key_here"
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GITHUB_TOKEN="your_github_token_here"
```

## Usage

Import and use the agent in your Python code:

```python
from github_agent.agent import root_agent

# The agent is ready to use with the configured tools
```

## Project Structure

```
starter_agents/
├── github_agent/
│   ├── __init__.py
│   ├── agent.py              # Main agent configuration
│   ├── tools/
│   │   ├── create_repo_tool.py
│   │   └── delete_repo_tool.py
│   └── sample_env            # Environment variables template
├── requirements.txt
└── README.md
```

## Tools

The agent has access to the following tools:

- **create_repository**: Creates a new GitHub repository with name, description, and privacy settings
- **delete_repository**: Deletes a repository by name
- **list_repositories**: Lists all repositories

## Configuration

The agent is configured with:
- Model: `gemini-2.0-flash`
- Temperature: `0.2` (for more deterministic output)
- Max output tokens: `250`

