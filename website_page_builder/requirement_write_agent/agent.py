import os
import sys
from typing import List, Dict

import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.genai import types

# Add website_page_builder directory to path for imports
_current_file = os.path.abspath(__file__)
_agent_dir = os.path.dirname(_current_file)
_website_builder_dir = os.path.dirname(_agent_dir)
if _website_builder_dir not in sys.path:
    sys.path.insert(0, _website_builder_dir)

# Import utils with proper path handling
# Since website_page_builder is added to sys.path, use direct import
try:
    from utils.file_loader import load_text_file
except ImportError:
    # Fallback: try full path if direct import doesn't work
    from website_page_builder.utils.file_loader import load_text_file



load_dotenv()


# Path to instruction.txt relative to this file
BASE_DIR = os.path.dirname(__file__)
instruction_path = os.path.join(BASE_DIR, "instructions.txt")

instruction_text = load_text_file(instruction_path)

requirement_write_agent = Agent(
    name="requirement_write_agent",
    model="gemini-2.0-flash",
    description=""" You are a helpful assistant that can write website requirements
                You will translate users ideas into blueprints. User will you what kind of website they need,
                 and you will generate a detailed specification document covering design, layout,
                  and functionality for the design team to build.
            """,
    instruction= instruction_text,
    
    output_key="requirement_write_agent_output"
)

# ADK web expects root_agent
root_agent = requirement_write_agent