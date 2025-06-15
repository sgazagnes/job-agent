# crews/company_research/tasks.py
"""
Tasks for company research crew
"""

from crewai import Task
from config.settings import GEOGRAPHIC_FOCUS, USER_PROVIDED_COMPANIES, USER_PROVIDED_COMPANIES_NO

def create_interest_research_task(agent, interest: str):
    """Create task for researching institutions by interest."""
    return Task(
        description=f"""
        Research institutions and companies specifically related to "{interest}" in {', '.join(GEOGRAPHIC_FOCUS)}.
        
        Find:
        1. Universities with strong programs in {interest}
        2. Companies that specialize in {interest}
        3. Research institutes focused on {interest}
        4. Government agencies working in {interest}
        5. Startups in the {interest} space
        
        For each institution found, gather:
        - Official name
        - Main website URL
        - Careers page URL where jobs are listed!
        - Location (city, country)
        - Brief description of their work in {interest}
        - Institution type
        - Estimated size/scale
        
        Make sure you return the proper JSON list with at least 5 results.
        """,
        expected_output="""
        A JSON list of institutions with career page information added:
        [
          {
            "name": "Institution Name",
            "type": "university/company/startup/research_institute/government/ngo",
            "website_url": "https://website.com",
            "careers_url": "https://careers-page.com",
            "location": "City, Country",
            "size": "small/medium/large/enterprise",
            "industry": "Primary industry/field",
            "interest_match": "Interest area specified by user",
            "description": "Description",
            "notes": "Career page details, application process notes"
          }
        ]
        """,
        agent=agent
    )

def create_user_defined_companies_task(agent):
    """Create task for researching user-defined companies."""
    return Task(
        description=f"""
        Research the details of companies and institutions in {USER_PROVIDED_COMPANIES}
        
        Use directories, rankings, and specialized lists.
        
        Gather comprehensive information for each organization. The careers url is where job openings are listed. Make sure you return the proper JSON list.
        """,
        expected_output="""
        A JSON list of institutions with career page information added:
        [
          {
            "name": "Institution Name",
            "type": "university/company/startup/research_institute/government/ngo",
            "website_url": "https://website.com",
            "careers_url": "https://careers-page.com",
            "location": "City, Country",
            "size": "small/medium/large/enterprise",
            "industry": "Primary industry/field",
            "interest_match": "User defined company",
            "description": "Description",
            "notes": "Career page details, application process notes"
          }
        ]
        """,
        agent=agent
    )

def create_similar_institutions_task(agent, company: str):
    """Create task for finding institutions similar to user-provided companies."""
    return Task(
        description=f"""
        Research companies and institutions in {', '.join(GEOGRAPHIC_FOCUS)} that are similar to {company}
        
        Use directories, rankings, and specialized lists.
        
        Gather comprehensive information for each organization found.
        Make sure you return the proper JSON list.
        """,
        expected_output="""
        A JSON list of institutions with career page information added:
        [
          {
            "name": "Institution Name",
            "type": "university/company/startup/research_institute/government/ngo",
            "website_url": "https://website.com",
            "careers_url": "https://careers-page.com",
            "location": "City, Country",
            "size": "small/medium/large/enterprise",
            "industry": "Primary industry/field",
            "interest_match": "Similar to company specified by user",
            "description": "Description",
            "notes": "Career page details, application process notes"
          }
        ]
        """,
        agent=agent
    )

def create_validation_task(agent, previous_tasks):
    """Create task for validating and consolidating results."""
    return Task(
        description=f"""
        Validate the institution information from previous research.
        
        Tasks:
        1. Remove duplicates (same institution found multiple times)
        2. Remove companies provided if they match the user removing list: {USER_PROVIDED_COMPANIES_NO}
        3. Verify all career page URLs are working. If not specified, find them.
        4. Standardize formats
        5. Add any missing critical information
        6. Propagate information from previous tasks
        
        Create a final, clean list of all institutions you checked. Make sure you return the proper JSON list.
        """,
        expected_output="""
        A final JSON list of validated, deduplicated institutions:
        [
          {
            "name": "Institution Name",
            "type": "university/company/startup/research_institute/government/ngo",
            "website_url": "https://website.com",
            "careers_url": "https://careers-page.com",
            "location": "City, Country",
            "size": "small/medium/large/enterprise",
            "industry": "Primary industry/field",
            "interest_match": "previously reported matching interest.",
            "description": "comprehensive description",
            "notes": "additional notes"
          }
        ]
        """,
        agent=agent,
        context=previous_tasks
    )