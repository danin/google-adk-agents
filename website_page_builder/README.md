# Website Page Builder

An automated web development pipeline built with Google ADK (Agent Development Kit) that converts natural language requests into fully functional HTML web pages through a sequential workflow of specialized AI agents.

## Overview

This project uses a **SequentialAgent** to orchestrate three specialized sub-agents that work together to:
1. **Analyze** user requirements
2. **Design** the UI specification
3. **Generate** the final HTML code

The system takes a user's natural language description (e.g., "Create a landing page for a coffee shop") and produces a complete, single-file HTML page with embedded CSS and JavaScript.

## Architecture

The system follows a sequential pipeline architecture:

```
User Input
    ↓
[Requirement Write Agent] → requirement_write_agent_output
    ↓
[Page Designer Agent] → page_designer_agent_output
    ↓
[Code Write Agent] → final HTML file
```

### Workflow

1. **Requirement Gathering**: The `requirement_write_agent` analyzes the user's request and generates a detailed Design & Technical Requirement Document.

2. **Visual Specification**: The `page_designer_agent` takes the requirements and creates a comprehensive UI Design Specification with:
   - Color palettes (hex codes)
   - Typography rules
   - Layout structures (Flexbox/Grid)
   - Marketing copy
   - JavaScript interaction logic

3. **Code Generation**: The `code_write_agent` combines both outputs to generate a single-file HTML page with embedded CSS and JavaScript.

## Agents

### 1. Sequential Manager Agent (`sequential_manager_agent`)
- **Type**: `SequentialAgent`
- **Role**: Orchestrates the workflow and manages data flow between sub-agents
- **Location**: `sequential_manager_agent/agent.py`
- **Main Agent**: This is the `root_agent` that should be loaded in ADK web

### 2. Requirement Write Agent (`requirement_write_agent`)
- **Type**: `Agent`
- **Role**: Translates user ideas into detailed website requirements
- **Input**: User's natural language request
- **Output**: `requirement_write_agent_output` - A comprehensive specification document
- **Location**: `requirement_write_agent/agent.py`

### 3. Page Designer Agent (`page_designer_agent`)
- **Type**: `Agent`
- **Role**: Creates the UI Design Specification with exact design details
- **Input**: `requirement_write_agent_output`
- **Output**: `page_designer_agent_output` - Detailed design blueprint
- **Location**: `page_designer_agent/agent.py`

### 4. Code Write Agent (`code_write_agent`)
- **Type**: `Agent`
- **Role**: Generates the final HTML code following the design specification
- **Input**: Both `requirement_write_agent_output` and `page_designer_agent_output`
- **Output**: `code_write_agent_output` - Complete HTML file
- **Location**: `code_write_agent/agent.py`

## Setup

### Prerequisites

- Python 3.8+
- Google ADK installed
- Google API Key

### Installation

1. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file in the root directory (`starter_agents/`) with:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   ```

### Project Structure

```
website_page_builder/
├── sequential_manager_agent/
│   ├── __init__.py
│   ├── agent.py          # Main orchestrator agent
│   └── instructions.txt
├── requirement_write_agent/
│   ├── __init__.py
│   ├── agent.py
│   └── instructions.txt
├── page_designer_agent/
│   ├── __init__.py
│   ├── agent.py
│   └── instructions.txt
├── code_write_agent/
│   ├── __init__.py
│   ├── agent.py
│   └── instructions.txt
├── utils/
│   └── file_loader.py    # Utility for loading instruction files
└── README.md
```

## Running the Agent

### Using ADK Web

1. **Load the agent**:
   - In ADK web, load the module: `sequential_manager_agent`
   - The `root_agent` will be automatically detected

2. **Provide input**:
   - Enter a natural language description of the website you want to create
   - Example: "Create a modern landing page for a tech startup with a hero section, features section, and contact form"

3. **Get output**:
   - The agent will process your request through all three sub-agents
   - The final HTML code will be generated and can be saved

### Running Individual Agents

You can also run individual agents directly in ADK web:
- `requirement_write_agent` - For requirement analysis only
- `page_designer_agent` - For design specification (requires context variables)
- `code_write_agent` - For code generation (requires context variables or user input)

**Note**: When running `code_write_agent` standalone, it will work with direct user input if context variables are not available.

## How It Works

1. **User provides input**: "Create a landing page for a coffee shop"

2. **Requirement Write Agent** processes the input and generates:
   ```
   - Purpose: Coffee shop landing page
   - Target audience: Coffee enthusiasts
   - Key features: Menu display, location, hours, contact form
   - Design style: Warm, inviting, modern
   ```

3. **Page Designer Agent** creates the design spec:
   ```
   - Colors: #8B4513 (brown), #F5DEB3 (wheat), #FFFFFF (white)
   - Typography: 'Playfair Display' for headings, 'Open Sans' for body
   - Layout: Header with nav, hero section, menu grid, contact form
   - Interactions: Smooth scroll, form validation
   ```

4. **Code Write Agent** generates the final HTML:
   ```html
   <!DOCTYPE html>
   <html>
   <!-- Complete single-file HTML with embedded CSS and JS -->
   </html>
   ```

## Features

- **Single-file output**: All CSS and JavaScript embedded in one HTML file
- **Responsive design**: Automatically includes mobile-responsive layouts
- **Semantic HTML**: Uses proper HTML5 semantic tags
- **Modern CSS**: Leverages CSS Variables, Flexbox, and Grid
- **Interactive elements**: Includes JavaScript for forms, navigation, and interactions

## Configuration

### Model Configuration

All agents use `gemini-2.0-flash` by default. You can modify the model in each agent's `agent.py` file:

```python
requirement_write_agent = Agent(
    name="requirement_write_agent",
    model="gemini-2.0-flash",  # Change this if needed
    ...
)
```

### Customizing Instructions

Each agent has its own `instructions.txt` file that defines its behavior. You can modify these to customize:
- Agent personality and style
- Output format requirements
- Specific design preferences
- Code generation patterns

## Troubleshooting

### Import Errors

If you encounter import errors:
- Ensure all `__init__.py` files are present
- Check that `root_agent` is exported in each agent module
- Verify `sys.path` manipulation in `sequential_manager_agent/agent.py`

### Context Variable Errors

If you see errors like `'Context variable not found: page_designer_agent_output'`:
- This means you're running a sub-agent standalone
- Use `sequential_manager_agent` instead, or provide the required context variables

### Module Loading Issues

If ADK web can't load the module:
- Verify the module path is correct
- Check that `root_agent` is defined in `sequential_manager_agent/agent.py`
- Ensure all dependencies are installed

## License

This project is part of the Google ADK starter agents collection.

