# crews/company_research/workflow.py
"""
Company research workflow orchestrator
"""

from crewai import Crew, Process
from typing import List
from models.data_models import Institution
from config.settings import USER_INTERESTS, USER_PROVIDED_COMPANIES, OUTPUT_CONFIG
from utils.utils import process_research_results, extract_json_block
import json5 as json
import re
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from crewai.flow.flow import Flow, listen, start
from collections import OrderedDict

import csv
import os
from datetime import datetime


from .agents import (
    create_company_finder_agent,
    create_company_scraper_agent,
    create_validator_agent
)
from .tasks import (
    create_company_finding_task,
    create_similar_company_finding_task,
    create_company_detail_finding_task,
    create_validation_task
        )

# Define our models for structured data
class CompanyState(BaseModel):
    names: list = []
    details: list[Institution] = [] 

class Institution(BaseModel):
    """Model for institutional data"""
    name: str
    type: str  # 'university', 'company', 'startup', 'research_institute', 'government', 'ngo'
    website_url: str
    careers_url: str
    location: Optional[str] = None
    size: Optional[str] = None  # 'small', 'medium', 'large', 'enterprise'
    industry: Optional[str] = None
    interest_match: Optional[str] = None  # Which user interest this matches
    description: Optional[str] = None


# Define our flow state

def extract_json_array(text: str):
    """Extract first valid flat JSON array from a block of text."""
    matches = re.findall(r'\[\s*(".*?"\s*(,\s*".*?")*)?\s*\]', text, re.DOTALL)
    for match in re.finditer(r'\[[\s\S]*?\]', text):
        try:
            arr = json.loads(match.group())
            if isinstance(arr, list) and all(isinstance(x, str) for x in arr):
                return arr
        except:
            continue
    return []



class CompanyFinderFlow(Flow[CompanyState]):
    """Flow for creating a comprehensive guide on any topic"""

    @start()
    def run_company_discovery(self):
        agent_discovery = create_company_finder_agent()

        all_names = []

        if  USER_PROVIDED_COMPANIES:
            all_names.extend(USER_PROVIDED_COMPANIES)


        for interest in USER_INTERESTS:
            print(f"\n🔍 Finding companies related to: {interest}")
            task1 = create_company_finding_task(agent_discovery, interest)

            # task2 = create_extend_company_finding_task(agent_discovery, interest)
            # task2.context = [task1]
            company_finder_crew = Crew(
                agents=[agent_discovery],
                tasks=[task1],
                process=Process.sequential,
                verbose=OUTPUT_CONFIG['verbose']
            )

            result = company_finder_crew.kickoff()

            # Extract JSON safely (flat list of names)
            raw_json = extract_json_array(str(result))  # Use improved helper from before
            if not raw_json:
                continue

            print(f"Found {len(raw_json)} companies for {interest}")
            all_names.extend(raw_json)

        # for company in USER_PROVIDED_COMPANIES:
        #     print(f"\n🔍 Finding companies similar to: {company}")
        #     task1 = create_similar_company_finding_task(agent_discovery, company)

        #     # task2 = create_extend_company_finding_task(agent_discovery, interest)
        #     # task2.context = [task1]
        #     company_finder_crew = Crew(
        #         agents=[agent_discovery],
        #         tasks=[task1],
        #         process=Process.sequential,
        #         verbose=OUTPUT_CONFIG['verbose']
        #     )

        #     result = company_finder_crew.kickoff()

        #     # Extract JSON safely (flat list of names)
        #     raw_json = extract_json_array(str(result))  # Use improved helper from before
        #     if not raw_json:
        #         continue

        #     print(f"Found {len(raw_json)} companies similar to {company}")
        #     all_names.extend(raw_json)

        # Deduplicate while preserving order
        deduplicated_names = list(OrderedDict.fromkeys(all_names))
        self.state.names = deduplicated_names

        print(f"\n📦 Total unique institutions found: {len(self.state.names)}")
        return self.state


    @listen(run_company_discovery)
    def get_company_details(self, outline):
        """Find necessary details about a company"""
        agent_detail_finder = create_company_scraper_agent()

        for name in self.state.names:
            print(f"\n🔍 Finding details for: {name}")
            task1 = create_company_detail_finding_task(agent_detail_finder, name)

            task2 = create_validation_task(agent_detail_finder, task1)
            # task2.context = [task1]
            company_detail_finder_crew = Crew(
                agents=[agent_detail_finder],
                tasks=[task1, task2],
                process=Process.sequential,
                verbose=OUTPUT_CONFIG['verbose']
            )

            result = company_detail_finder_crew.kickoff()

            raw_json = extract_json_block(str(result))
            print(raw_json)
            # parsed = json.loads(raw_json)
            # print(parsed)
            try:
                parsed = json.loads(raw_json)

                if parsed == "delete":
                    print(f"🗑 Skipped and removed excluded company: {name}")
                    self.state.names.remove(name)
                    continue

                if isinstance(parsed, dict):
                    institution = Institution(**parsed)
                    self.state.details.append(institution)

                elif isinstance(parsed, list) and len(parsed) == 1 and isinstance(parsed[0], dict):
                    print(f"Wrapped in list — unpacking single institution for: {name}")
                    institution = Institution(**parsed[0])
                    self.state.details.append(institution)

                else:
                    print(f"Unexpected format for {name}: {parsed}")

            except Exception as e:
                print(f"❌ Error processing {name}: {e}")

        return self.state
    
    @listen(get_company_details)
    def deduplicate_institutions(self):
        """Deduplicate self.state.details based on institution name and website_url."""
        print("\n🧹 Deduplicating institution details...")

        seen = set()
        unique_institutions = []

        for inst in self.state.details:
            key = (inst.name.strip().lower(), inst.website_url.strip().lower())
            if key not in seen:
                seen.add(key)
                unique_institutions.append(inst)
            else:
                print(f"Duplicate removed: {inst.name} ({inst.website_url})")

        original_count = len(self.state.details)
        deduped_count = len(unique_institutions)

        self.state.details = unique_institutions

        print(f"Deduplication complete: {original_count - deduped_count} removed, {deduped_count} remaining.")
        return self.state

    @listen(deduplicate_institutions)
    def save_institutions_to_csv(self) -> str:
        """Save all institutions in self.state.details to a CSV file."""
        if not self.state.details:
            print("No institution details to save.")
            return None

        # Filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"institutions_{timestamp}.csv"

        # Define fieldnames based on your Institution model
        fieldnames = [
            "name",
            "type",
            "website_url",
            "careers_url",
            "location",
            "size",
            "industry",
            "interest_match",
            "description",
        ]

        print(f"\nSaving {len(self.state.details)} institutions to {filename}...")

        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for inst in self.state.details:
                        writer.writerow(inst.dict())

        return filename

def plot():
    """Generate a visualization of the flow"""
    flow = CompanyFinderFlow()
    flow.plot("guide_creator_flow")
    print("Flow visualization saved to guide_creator_flow.html")

    
def run_complete_workflow() -> str:
    plot()

    """Run the complete company research workflow."""
    print("🎯 Starting Complete Company Research Workflow")
    print(f"Researching interests: {', '.join(USER_INTERESTS)}")
    if USER_PROVIDED_COMPANIES:
        print(f"Institution similar to: {', '.join(USER_PROVIDED_COMPANIES)}")
    print("="*60)
    
    try:
        fname = CompanyFinderFlow().kickoff()
    except Exception as e:
        print(f"❌ Error in workflow: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def run_company_research() -> str:
    """Convenience function to run the complete company research workflow."""
    return run_complete_workflow()