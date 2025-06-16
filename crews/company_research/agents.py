# crews/company_research/agents.py
"""
Agents for company research crew
"""

from crewai import Agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

search_tool =  SerperDevTool(
    # search_url="https://google.serper.dev/search",
    # country="NL",  # Change to your preferred EU country
    location="Europe",
    locale="en-GB",
    n_results=10
)

def create_interest_researcher_agent():
    """Agent specialized in researching institutions by interest areas."""
    return Agent(
        role="Interest-Specific Research Specialist",
        goal="Research institutions that match specific user interests",
        backstory="""You are an expert researcher who specializes in finding organizations 
        that work in specific fields. You have deep knowledge of academic institutions, 
        companies, and research organizations across different domains. You're particularly 
        good at identifying lesser-known but relevant organizations.""",
        verbose=True,
        tools=[search_tool, ScrapeWebsiteTool()],
        allow_delegation=False
    )

def create_institution_type_researcher_agent():
    """Agent specialized in researching specific types of institutions."""
    return Agent(
        role="Institution Type Specialist",
        goal="Research specific types of institutions (universities, companies, startups, etc.)",
        backstory="""You are an expert at finding and researching different types of 
        institutions. You understand the landscape of universities, corporations, startups, 
        research institutes, government agencies, and NGOs. You know how to find comprehensive 
        lists and directories for each type.""",
        verbose=True,
        tools=[search_tool, ScrapeWebsiteTool()],
        allow_delegation=False
    )

def create_institution_validator_agent():
    """Agent specialized in validating and enriching institution information."""
    return Agent(
        role="Institution Information Validator",
        goal="Validate and enrich institution information",
        backstory="""You are meticulous at verifying information about institutions. 
        You check websites, validate URLs, extract additional details like size, 
        location, and industry focus. You ensure all information is accurate and complete.""",
        verbose=True,
        tools=[ScrapeWebsiteTool()],
        allow_delegation=False
    )