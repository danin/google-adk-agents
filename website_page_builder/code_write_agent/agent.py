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
try:
    from website_page_builder.utils.file_loader import load_text_file
except ImportError:
    # Fallback: try direct import if website_page_builder is already in path
    from utils.file_loader import load_text_file



load_dotenv()


# Path to instructions.txt relative to this file
BASE_DIR = os.path.dirname(__file__)
instruction_path = os.path.join(BASE_DIR, "instructions.txt")

instruction_text = load_text_file(instruction_path)

code_write_agent = Agent(
    name="code_write_agent",
    model="gemini-2.0-flash",
    description=""" The page_designer_agent acts as the creative architect. It consumes high-level requirement documents
    and translates them into a rigorous UI Design Specification. It selects specific color hex codes, defines typography,
    writes marketing copy, and dictates the exact CSS Flexbox/Grid structures and JavaScript logic required. 
    It prepares the detailed 'blueprint' that the code_writer_agent will strictly follow to generate the final single-file HTML.""",
    instruction=instruction_text,
    output_key="code_write_agent_output"
)


# ADK web expects root_agent
root_agent = code_write_agent

