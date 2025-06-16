# crews/company_research/tasks.py
"""
Tasks for company research crew
"""

from crewai import Task
from config.settings import GEOGRAPHIC_FOCUS, USER_PROVIDED_COMPANIES, USER_PROVIDED_COMPANIES_NO

def create_company_finding_task(agent, interest: str):
    """Create task for researching institutions by interest."""
    return Task(
        description=f"""
        Research and identify institutions that are strongly associated with "{interest}" in the following regions: {', '.join(GEOGRAPHIC_FOCUS)}.

        You should the following:
        - Universities with notable programs in {interest}
        - Companies that specialize in {interest}
        - Start-ups that specialize in {interest}
        - Research institutes focused on {interest}
        - Government or public sector institutions engaged in {interest}

        Guidelines:
        - Make a separate search for each different type of organization
        - Focus on well-known or active institutions in the field. Do not include irrelevant companies
        - Return the most relevant companies 
        - DO NOT include duplicates.
        - ONLY return the JSON array of names. Do not explain or format in markdown.

        Example:
        [
          "Institution 1",
          "Institution 2",
          "Institution 3"
        ]
        """,
        expected_output="""
        A flat JSON array of institution names as strings, with no surrounding markdown or explanation. The list must contain all the entries you found.
        """,
        agent=agent
    )

#the maximum of entries you find. 
def create_extend_company_finding_task(agent, interest: str):
    """Create task for expanding institution search, avoiding duplicates."""
    return Task(
        description=f"""
        You previously found institutions related to "{interest}" in {', '.join(GEOGRAPHIC_FOCUS)}.
        
        Now, find **additional institutions** that fit the same topic and were NOT previously listed. These might include:
        - Smaller or less well-known organizations
        - Regional research labs
        - Emerging startups

        Guidelines:
        - Append the new names you found to the previous list of institutions.
        - ONLY return a flat JSON list of institution names — no explanations, markdown, or formatting.

        Example:
        [
          "Institution 1",
          "Institution 2",
          "Institution 3"
        ]
        """,
        expected_output="""
        A JSON array of institution names as strings. 
        """,
        agent=agent
    )



def create_similar_company_finding_task(agent, company: str):
    """Create task for finding institutions similar to user-provided companies."""
    return Task(
        description=f"""
        Companies, start-ups and universities in {', '.join(GEOGRAPHIC_FOCUS)} that are similar to this institution: {company}
        
        Guidelines:
        - Find details about the company
        - If {company} is a company, focus on companies that are similar to it.
        - If {company} is a start-up, focus on start-ups that are similar to it.    
        - If {company} is a university, focus on universities that are similar to it.
        - Focus on well-known or active institutions in the field.
        - Return the maximum of entries you can find.
        - DO NOT include duplicates.
        - ONLY return the JSON array of names. Do not explain or format in markdown.

        Example:
        [
          "Institution 1",
          "Institution 2",
          "Institution 3"
        ]
        """,
        expected_output="""
        A flat JSON array of institution names as strings, with no surrounding markdown or explanation. The list must contain all the entries you found.
        """,
        agent=agent
    )



def create_company_detail_finding_task(agent, company):
    """Create task for researching all the important details about a company."""
    return Task(
        description=f"""
        Research the company: "{company}"

        If the company is in this list of excluded companies: {USER_PROVIDED_COMPANIES_NO}
        - Return only the string: `"delete"` and nothing else.

        Otherwise, return a single JSON object with the following fields:
        - `name`: Exact institution name
        - `type`: One of university, company, startup, research_institute, government
        - `website_url`: Must be a valid and working URL (status 200)
        - `careers_url`: A valid working URL where jobs are listed
        - `location`: City and Country
        - `size`: One of small, medium, large, enterprise
        - `industry`: Main industry or domain
        - `description`: Concise, meaningful summary of what this institution does

        Output rules:
        - DO NOT return a list or array
        - DO NOT return markdown or explanation
        - Only return a single JSON object exactly like the one below

        Example:
        {{
          "name": "ACME Robotics",
          "type": "startup",
          "website_url": "https://acmerobotics.com",
          "careers_url": "https://acmerobotics.com/careers",
          "location": "Berlin, Germany",
          "size": "small",
          "industry": "Robotics",
          "description": "ACME Robotics develops autonomous drone systems for industrial use."
        }}
        """,
        expected_output="A single valid JSON object, or the string 'delete'.",
        agent=agent,
    )

def create_validation_task(agent, previous_task):
    """Create task for validating and consolidating institution results."""
    return Task(
        description=f"""
        You are validating the details returned from the previous task.

        - If the previous output was `"delete"`, return `"delete"` and stop. Do NOT return any list or explanation.
        
        Otherwise, review the data and ensure it is correct and complete. For each institution:

        Validation Instructions:
        - Double-check that `website_url` and `careers_url` are both working (status 200 and not redirecting to error pages).
        - Improve or correct the `description` if vague or incorrect.
        - Fix any formatting issues.

        Output Format:
        - Return a **JSON array** of validated institution objects.
        - No markdown. No explanation. No surrounding text.

        Example:
        [
          {{
            "name": "ACME Robotics",
            "type": "startup",
            "website_url": "https://acmerobotics.com",
            "careers_url": "https://acmerobotics.com/careers",
            "location": "Berlin, Germany",
            "size": "small",
            "industry": "Robotics",
            "interest_match": "matched robotics and automation interest",
            "description": "ACME Robotics develops autonomous drone solutions for logistics and surveillance."
          }}
        ]
        """,
        expected_output="Either a valid JSON array as described, or the string 'delete'.",
        agent=agent,
        context=[previous_task]
    )
