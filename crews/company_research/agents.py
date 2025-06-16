# crews/company_research/agents.py
"""
Agents for company research crew
"""

from crewai import Agent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from crewai_tools import FirecrawlScrapeWebsiteTool
search_tool =  SerperDevTool(
    # search_url="https://google.serper.dev/search",
    # country="NL",  # Change to your preferred EU country
    location="Europe",
    locale="en-GB",
    n_results=10
)
scrape_tool = FirecrawlScrapeWebsiteTool()
def create_company_finder_agent():
    """Agent specialized in finding institutions and companies by interest areas or similarity with other companies."""
    return Agent(
        role="Company finder",
        goal="Find institutions and companies base on user interest or companies of interest. ",
        backstory="""You are an expert at finding companies and organizations that match the interests, locations, and companies of interets of the user. You have deep knowledge of academic institutions, 
        companies, and research organizations across different domains.""",
        verbose=True,
        tools=[search_tool, FirecrawlScrapeWebsiteTool()],
        allow_delegation=False
    )

def create_company_scraper_agent():
    """Agent specialized in finding all the relevant details for a company."""
    return Agent(
        role="Company Scraper Specialist",
        goal="Find all the relevant details for a company or institution provided by the user. ",
        backstory="""You are an expert at scraping all the relevant information about a company. You have deep knowledge of academic institutions, 
        companies, and research organizations across different domains.""",
        verbose=True,
        tools=[search_tool, FirecrawlScrapeWebsiteTool()],
        allow_delegation=False
    )

def create_validator_agent():
    """Agent specialized in validating and merging institution information."""
    return Agent(
        role="Institution Information Validator",
        goal="Validate and merge institution information",
        backstory="""You are meticulous at verifying information about institutions. 
        You are able to find duplicates and remove them. You combine the data from different sources into a single JSON list.""",
        verbose=True,
        tools=[],
        allow_delegation=False
    )