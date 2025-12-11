import os
import sys
from typing import List, Dict
from google.adk.agents import SequentialAgent
from dotenv import load_dotenv

# Add the starter_agents directory to path to enable proper imports
_current_file = os.path.abspath(__file__)
_agent_dir = os.path.dirname(_current_file)
_website_builder_dir = os.path.dirname(_agent_dir)
_starter_agents_dir = os.path.dirname(_website_builder_dir)

# Add to path if not already there
if _starter_agents_dir not in sys.path:
    sys.path.insert(0, _starter_agents_dir)
if _website_builder_dir not in sys.path:
    sys.path.insert(0, _website_builder_dir)

# Import utils with proper path handling
try:
    from utils.file_loader import load_text_file
except ImportError:
    from website_page_builder.utils.file_loader import load_text_file

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Path to instructions.txt relative to this file
BASE_DIR = os.path.dirname(__file__)
instruction_path = os.path.join(BASE_DIR, "instructions.txt")

instruction_text = load_text_file(instruction_path)

# Import sub-agents directly from their agent modules
# Since we've added website_page_builder to sys.path, we can use the shorter import path
from requirement_write_agent.agent import requirement_write_agent
from page_designer_agent.agent import page_designer_agent
from code_write_agent.agent import code_write_agent

# SequentialAgent only accepts name and sub_agents parameters
# It orchestrates the workflow automatically between sub-agents
sequential_manager_agent = SequentialAgent(
    name="sequential_manager_agent",
    sub_agents=[requirement_write_agent, page_designer_agent, code_write_agent],
)

root_agent = sequential_manager_agent