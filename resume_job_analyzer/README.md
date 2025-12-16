# Resume & Job Description Analyzer

An intelligent multi-agent system built with Google ADK that analyzes resumes, parses job descriptions, evaluates job fit, and provides resume enhancement recommendations.

## Overview

This project uses a multi-agent architecture to help job seekers:
- **Analyze resumes** and extract structured insights
- **Parse job descriptions** to identify key requirements
- **Evaluate job fit** by comparing resumes against job descriptions
- **Enhance resumes** with tailored recommendations to improve ATS compatibility

## Agents

The system consists of four specialized agents orchestrated by a root agent:

### 1. `analyze_resume_agent`
- **Model**: `gemini-2.5-flash`
- **Purpose**: Extracts structured information from resumes
- **Output**: JSON with:
  - Key skills (technical and soft)
  - Experience highlights
  - Education and certifications
  - Weaknesses and improvement areas

### 2. `jd_summarize_agent`
- **Model**: `gemini-2.5-flash`
- **Purpose**: Parses job descriptions and extracts requirements
- **Output**: JSON with:
  - Role title and seniority level
  - Location type (Onsite/Hybrid/Remote)
  - Core responsibilities
  - Must-have and nice-to-have skills
  - Experience requirements
  - Keywords for ATS optimization

### 3. `job_fit_analyst_agent`
- **Model**: `gemini-2.5-flash`
- **Purpose**: Computes job fit scores between resume and job description
- **Output**: JSON with:
  - Fit scores (overall, technical, domain, seniority) - 0-100 scale
  - Matched skills
  - Missing must-have and nice-to-have skills
  - Strengths and gaps summary
  - Actionable recommendations

### 4. `analyze_resume_enhancer_agent`
- **Model**: `gemini-2.5-pro`
- **Purpose**: Enhances resume wording to better match target job descriptions
- **Output**: JSON with:
  - Improved summary section
  - Enhanced experience sections (with before/after bullets)
  - Improved skills section
  - Tailoring notes for the candidate

### 5. `root_agent`
- **Model**: `gemini-2.5-flash`
- **Purpose**: Orchestrates the workflow and coordinates tool usage
- **Capabilities**: 
  - Detects user intent (resume analysis, JD analysis, job fit, resume enhancement)
  - Calls appropriate agents in the correct sequence
  - Combines outputs into user-friendly responses

## Requirements

- Python 3.10+
- Google ADK dependencies
- Google API Key with access to Gemini models

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file in the project root with:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. **Verify the agent file**:
   The main agent file is located at: `resume_job_analyzer/agent.py`

## How to Run

### Option 1: Using ADK Web (Recommended)

1. **Load the agent in ADK Web**:
   - Navigate to ADK Web interface
   - Load the module: `resume_job_analyzer.agent`
   - The `root_agent` will be automatically detected

2. **Provide input**:
   - Enter your request in natural language
   - Examples:
     - "Take a look at my Resume: 10 years experience in Distributed systems. Can code in Python, C. Can you review my resume"
     - "Analyze this job description: [paste JD text]"
     - "Compare my resume with this job description: [resume] and [JD]"
     - "Help me tailor my resume for this job: [resume] and [JD]"

3. **Get results**:
   - The agent will automatically determine which tools to use
   - Results will be presented in a clear, structured format

### Option 2: Using Python Terminal

**Note**: The current implementation uses `google.adk.runtime.run_agent` which may not be available in all environments. For direct Python usage, you can:

```python
from resume_job_analyzer.agent import root_agent

# Run a single query
result = root_agent.run("Take a look at my Resume: 10 years experience in Distributed systems. Can code in Python, C. Can you review my resume")
print(result.text)
```

Or create a simple script:

```python
# test_agent.py
from resume_job_analyzer.agent import root_agent

user_input = input("Enter your request: ")
result = root_agent.run(user_input)
print("\n" + "="*50)
print("RESULT:")
print("="*50)
print(result.text)
```

Then run:
```bash
python test_agent.py
```

## Usage Examples

### Example 1: Resume Analysis Only
```
User: "Take a look at my Resume: 10 years experience in Distributed systems. 
       Can code in Python, C. Can you review my resume"

Agent Action: Calls analyze_resume_agent
Output: Structured JSON with skills, experience, education, and weaknesses
```

### Example 2: Job Description Analysis
```
User: "Analyze this job description: [paste JD text]"

Agent Action: Calls jd_summarize_agent
Output: Structured JSON with role details, skills, and requirements
```

### Example 3: Job Fit Analysis
```
User: "Compare my resume with this job description: 
       Resume: [resume text]
       JD: [job description text]"

Agent Action: 
1. Calls analyze_resume_agent
2. Calls jd_summarize_agent
3. Calls job_fit_analyst_agent with both outputs
Output: Fit scores, matched/missing skills, recommendations
```

### Example 4: Resume Enhancement
```
User: "Help me tailor my resume for this job: 
       Resume: [resume text]
       JD: [job description text]"

Agent Action:
1. Calls analyze_resume_agent
2. Calls jd_summarize_agent
3. Calls job_fit_analyst_agent
4. Calls analyze_resume_enhancer_agent
Output: Enhanced resume sections with before/after comparisons
```

## Workflow Logic

The `root_agent` intelligently determines which agents to call based on user input:

1. **Resume Only** → `analyze_resume_agent`
2. **JD Only** → `jd_summarize_agent`
3. **Resume + JD (Analysis)** → `analyze_resume_agent` → `jd_summarize_agent` → `job_fit_analyst_agent`
4. **Resume + JD (Enhancement)** → All agents in sequence, ending with `analyze_resume_enhancer_agent`

## Output Format

All agents return structured JSON data that can be:
- Parsed programmatically
- Displayed in user-friendly formats
- Used for further processing or analysis

## Important Notes

- **Dependencies**: The `job_fit_analyst_agent` requires outputs from both `analyze_resume_agent` and `jd_summarize_agent`
- **Context Passing**: Downstream agents receive structured outputs from previous agents, not raw text
- **Truthfulness**: The resume enhancer agent does NOT fabricate experience or skills - it only rephrases and reorganizes existing content
- **ATS Optimization**: All outputs include keywords and formatting suggestions for Applicant Tracking Systems

## Troubleshooting

### "Object of type bytes is not JSON serializable" Error
If you encounter this error in ADK Web, ensure that:
- All agents have `output_key` parameters set
- File uploads are converted to text before processing

### Module Import Errors
- Ensure you're in the correct directory
- Verify that `requirements.txt` dependencies are installed
- Check that your Python path includes the project root

## Architecture

```
User Input
    ↓
root_agent (Orchestrator)
    ↓
    ├──→ analyze_resume_agent (if resume provided)
    ├──→ jd_summarize_agent (if JD provided)
    ├──→ job_fit_analyst_agent (if both provided)
    └──→ analyze_resume_enhancer_agent (if enhancement requested)
    ↓
Combined Results → User
```

## License

This project is part of the starter_agents collection.

