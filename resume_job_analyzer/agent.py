# resume_jd_multi_agent.py
#
# Single-file setup of:
# - analyze_resume_agent
# - analyze_jd_agent
# - job_fit_agent
# - resume_enhancer_agent
# - root_agent (uses others as AgentTool)
#
# Run pattern (pseudo):
# from google.adk.runtime import run_agent
# response = run_agent(root_agent, user_message)

import json
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import FunctionTool
from google.adk.agents import SequentialAgent
import logging


logging.basicConfig(level=logging.INFO)

logging.info("Loading resume_jd_multi_agent agents...")

# -----------------------------
# Specialist agents
# -----------------------------

analyze_resume_agent = Agent(
    name="analyze_resume_agent",
    model="gemini-2.5-flash",
    description="Extracts structured information and insights from resumes.",
    instruction=(
       """# Role
You are an expert Resume Parser. 

# Task
Analyze the provided resume text and extract the following into a structured summary:
1. **Key Skills:** Technical and Soft skills.
2. **Experience Highlights:** Years of experience, major roles, and key industries.
3. **Education:** Degrees and certifications.
4. **Weaknesses:** Identify vague bullet points, formatting issues, or missing metrics (ROI).

# Output
You MUST Return a clean, structured JSON summary of the candidate's profile.
# Example Output
{
    "key_skills": ["Python", "SQL", "Machine Learning"],
    "experience_highlights": ["5 years of experience in data analysis", "2 years of experience in machine learning"],
    "education": ["Bachelor of Science in Computer Science", "Master of Business Administration"],
    "weaknesses": ["Lacks experience in cloud computing", "Needs to improve communication skills"]
}


       """
    ),
    output_key="analyze_resume_agent_output",
)


jd_summarize_agent = Agent(
    name="jd_summarize_agent",
    model="gemini-2.5-flash",
    description="Extracts structured information and core requirements from job descriptions.",
    instruction=(
        """# Role
You are an expert Job Description (JD) Parser.


# Task
Analyze the provided job description text and extract the following into a structured summary:
1. **Role Title**: The main job title.
2. **Seniority Level**: e.g., Junior, Mid, Senior, Lead, Principal.
3. **Location Type**: Onsite, Hybrid, Remote if mentioned.
4. **Core Responsibilities**: 5–10 bullet-style responsibility statements.
5. **Must-Have Skills**: Explicitly required skills, technologies, or certifications.
6. **Nice-to-Have Skills**: Preferred or bonus skills.
7. **Experience Requirements**: Years of experience and any domain/industry focus.
8. **Keywords for ATS**: Important keywords a candidate should include in their resume.


# Output
You MUST return a clean, structured JSON summary of the job description.

# Example Output
{
    "role_title": "Senior Data Scientist",
    "seniority_level": "Senior",
    "location_type": "Hybrid",
    "core_responsibilities": [
        "Lead end-to-end development of data science projects",
        "Collaborate with product and engineering to define data-driven solutions"
    ],
    "must_have_skills": [
        "Python",
        "SQL",
        "Machine Learning",
        "Statistics"
    ],
    "nice_to_have_skills": [
        "Cloud platforms (GCP, AWS, or Azure)",
        "Experience with MLOps tools"
    ],
    "experience_requirements": [
        "5+ years of experience in data science or related field",
        "Experience working in a product-focused environment"
    ],
    "keywords_for_ats": [
        "Data Science",
        "Machine Learning",
        "Python",
        "SQL",
        "A/B Testing"
    ]
}
"""
    ),
    output_key="jd_summarize_agent_output",
)



job_fit_analyst_agent = Agent(
    name="job_fit_analyst_agent",
    model="gemini-2.5-flash",
    description="Analyzes how well a candidate's resume matches a target job description.",
    instruction=(
        """# Role
You are an expert Job Fit Analyst.

# Inputs
You receive two structured JSON objects:
1. `resume_profile`  → output of analyze_resume_agent
   {
     "key_skills": [...],
     "experience_highlights": [...],
     "education": [...],
     "weaknesses": [...]
   }

2. `jd_profile`  → output of jd_summarize_agent
   {
     "role_title": "",
     "seniority_level": "",
     "location_type": "",
     "core_responsibilities": [],
     "must_have_skills": [],
     "nice_to_have_skills": [],
     "experience_requirements": [],
     "keywords_for_ats": []
   }

# Task
Compare `resume_profile` and `jd_profile` and evaluate job fit.

You MUST:
1. Compute numeric scores (0–100) for:
   - overall_fit
   - technical_fit
   - domain_fit
   - seniority_fit
2. Identify:
   - matched_skills: skills that clearly appear in both resume and JD.
   - missing_must_have_skills: required skills in the JD that the resume does not demonstrate.
   - missing_nice_to_have_skills: preferred skills in the JD that the resume does not demonstrate.
3. Provide:
   - strengths_summary: 2–5 short bullet-style strings highlighting why the candidate is a good fit.
   - gaps_summary: 2–5 short bullet-style strings highlighting the main gaps.
   - recommendations: 3–7 short, action-oriented suggestions (e.g., what to learn, what to emphasize).

# Output
Return ONLY a clean JSON object with the following keys:
{
  "overall_fit": 0,
  "technical_fit": 0,
  "domain_fit": 0,
  "seniority_fit": 0,
  "matched_skills": [],
  "missing_must_have_skills": [],
  "missing_nice_to_have_skills": [],
  "strengths_summary": [],
  "gaps_summary": [],
  "recommendations": []
}

- All scores must be integers between 0 and 100.
- Bullet-style text should be short, clear sentences or phrases.
- Do NOT include any explanation outside the JSON.
"""
    ),
    output_key="job_fit_analyst_agent_output",
)



analyze_resume_enhancer_agent = Agent(
    name="analyze_resume_enhancer_agent",
    model="gemini-2.5-pro",
    description="Enhances resume wording and structure to better match a target job description without fabricating experience.",
    instruction=(
        """# Role
You are an expert Resume Enhancer and Career Coach.

# Inputs
You receive:
1. `original_resume_text`: the raw resume text provided by the candidate.
2. `resume_profile`: the structured JSON output from analyze_resume_agent
   {
     "key_skills": [...],
     "experience_highlights": [...],
     "education": [...],
     "weaknesses": [...]
   }
3. `jd_profile`: the structured JSON output from jd_summarize_agent
   {
     "role_title": "",
     "seniority_level": "",
     "location_type": "",
     "core_responsibilities": [],
     "must_have_skills": [],
     "nice_to_have_skills": [],
     "experience_requirements": [],
     "keywords_for_ats": []
   }
4. (Optional) `job_fit_summary`: the JSON output from job_fit_analyst_agent
   {
     "overall_fit": 0,
     "technical_fit": 0,
     "domain_fit": 0,
     "seniority_fit": 0,
     "matched_skills": [],
     "missing_must_have_skills": [],
     "missing_nice_to_have_skills": [],
     "strengths_summary": [],
     "gaps_summary": [],
     "recommendations": []
   }

# Task
Rewrite and enhance the resume to better match the target JD, while staying truthful.

You MUST:
1. Keep all content factually consistent with the original resume.
   - Do NOT invent roles, companies, dates, or tools that are not supported by the resume.
   - You may rephrase, reorganize, merge, split, and add reasonable metrics ONLY if they are consistent with the described work.
2. Emphasize skills and responsibilities that align with the JD's must-have and nice-to-have skills.
3. Improve clarity, impact, and ATS-friendliness:
   - Use strong action verbs.
   - Keep bullet points concise.
   - Surface the most relevant achievements first.

# Output
Return ONLY a clean JSON object with the following keys:

{
  "improved_summary": "",
  "improved_experience_sections": [
    {
      "role_title": "",
      "company": "",
      "location": "",
      "dates": "",
      "original_bullets": [],
      "enhanced_bullets": []
    }
  ],
  "improved_skills_section": [],
  "education_section": [],
  "tailoring_notes_for_candidate": []
}

Field guidance:
- improved_summary: A 2–4 sentence professional summary tailored to the target role.
- improved_experience_sections: For each role, show original_bullets and enhanced_bullets so the candidate can see changes.
- improved_skills_section: A flat list of skills prioritized for this JD (mix of technical and soft skills).
- education_section: Cleaned-up list of education entries based on the resume (no fabrication).
- tailoring_notes_for_candidate: 3–7 practical tips on how to further tweak the resume or prepare for this role.

Do NOT include any explanation outside the JSON.
"""
    ),
    output_key="analyze_resume_enhancer_agent_output",
)





# -----------------------------
# Tools for root agent
# -----------------------------

# Use AgentTool to wrap the agent - this handles the agent call properly
analyze_resume_tool = AgentTool(agent=analyze_resume_agent)
analyze_job_description_tool = AgentTool(agent=jd_summarize_agent)
analyze_job_fit_agent = AgentTool(agent=job_fit_analyst_agent)
analyze_resume_enhancer_agent = AgentTool(agent=analyze_resume_enhancer_agent)

# -----------------------------
# Root agent (orchestrator)
# -----------------------------
# SequentialAgent only accepts name and sub_agents parameters
# It orchestrates the workflow automatically between sub-agents
root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    
    description="User-facing orchestrator for resume and JD workflows.",
    instruction=("""
        # Role
You are the Career Services Orchestrator. Your goal is to help users with career tasks by coordinating four specialized tools:
1. `analyze_resume_tool`
2. `analyze_job_description_tool
3. `job_fit_analyst`
4. `resume_enhancer`

# Workflow Logic
Analyze the user's request to determine which tools are needed and in what order.

## Case 1: Complex Request (Match & Update)
IF user provides Resume AND JD and asks for a match or update:
1. Call `resume_analyst` to parse the resume.
2. Call `jd_analyst` to parse the job description.
3. Call `job_fit_analyst` using the outputs from steps 1 and 2.
4. (Optional) If user asked to update/tailor the resume, call `resume_enhancer` using the output from step 3.

## Case 2: Resume Review Only
IF user provides only Resume:
1. Call `resume_analyst`.

## Case 3: JD Analysis Only
IF user provides only JD:
1. Call `jd_analyst`.

# Important Rules
*   **Dependency:** You cannot run `job_fit_analyst` until you have the structured data from both the Resume and the JD.
*   **Context Passing:** When calling a downstream agent (like `resume_enhancer`), pass the *results* of the previous agents, not just the raw user text.




}



    """),
    tools=[
        analyze_resume_tool,
        analyze_job_description_tool,
        analyze_job_fit_agent,
        analyze_resume_enhancer_agent,
    ],
    output_key="root_agent_output",
)
logging.info("-----------------------------------------------------------------Root agent wired with tools--------------------------------")


# -----------------------------
# (Optional) simple run helper
# -----------------------------
if __name__ == "__main__":
    from google.adk.runtime import run_agent  # or equivalent helper

    print("Type your message (Ctrl+C to exit):")
    while True:
        user_msg = input("> ")
        result = run_agent(root_agent, user_msg)
        #print 

        print ("--------------------------------")
        print ("--------------------------------")
        print(result.text)
