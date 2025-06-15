# crews/company_research/workflow.py
"""
Company research workflow orchestrator
"""

from crewai import Crew, Process
from typing import List
from models.data_models import Institution
from config.settings import USER_INTERESTS, USER_PROVIDED_COMPANIES, OUTPUT_CONFIG
from utils.utils import process_research_results

from .agents import (
    create_interest_researcher_agent,
    create_institution_type_researcher_agent,
    create_institution_validator_agent
)
from .tasks import (
    create_interest_research_task,
    create_user_defined_companies_task,
    create_similar_institutions_task,
    create_validation_task
)

class CompanyResearchWorkflow:
    """Orchestrates the company research workflow"""
    
    def __init__(self):
        self.results = []
        self.all_tasks = []
        
    def run_interest_research(self):
        """Research institutions for each user interest."""
        print("🔍 Starting interest-based research...")
        
        agent_research = create_interest_researcher_agent()
        tasks = []
        
        for interest in USER_INTERESTS:
            print(f" Researching: {interest}")
            task = create_interest_research_task(agent_research, interest)
            tasks.append(task)
        
        # Run crew for interest research
        crew = Crew(
            agents=[agent_research],
            tasks=tasks,
            process=Process.sequential,
            verbose=OUTPUT_CONFIG['verbose']
        )
        
        result = crew.kickoff()
        self.all_tasks.extend(tasks)
        return result

    def run_user_institutions_research(self):
        """Find details of institutions provided by the user."""
        print("📋 Finding user provided institutions...")
        
        if not USER_PROVIDED_COMPANIES:
            print("No user provided companies found. Skipping user institutions research.")
            return None
        
        agent_research = create_institution_type_researcher_agent()
        task = create_user_defined_companies_task(agent_research)
        
        crew = Crew(
            agents=[agent_research],
            tasks=[task],
            process=Process.sequential,
            verbose=OUTPUT_CONFIG['verbose']
        )
        
        result = crew.kickoff()
        self.all_tasks.append(task)
        return result
    
    def run_similar_institutions_research(self):
        """Find institutions similar to user-provided company."""
        print("🔗 Finding similar institutions...")
        
        if not USER_PROVIDED_COMPANIES:
            print("No user provided companies found. Skipping similar institutions research.")
            return None
        
        agent_research = create_institution_type_researcher_agent()
        tasks = []
        for company in USER_PROVIDED_COMPANIES:
            print(f" Researching: {company}")
            task = create_similar_institutions_task(agent_research, company)
            tasks.append(task)
                
        crew = Crew(
            agents=[agent_research],
            tasks=[tasks],
            process=Process.sequential,
            verbose=OUTPUT_CONFIG['verbose']
        )
        
        result = crew.kickoff()
        self.all_tasks.append(tasks)
        return result

    def run_validation_and_consolidation(self):
        """Validate and consolidate all results."""
        print("✅ Validating and consolidating results...")
        
        agent = create_institution_validator_agent()
        task = create_validation_task(agent, self.all_tasks)
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=OUTPUT_CONFIG['verbose']
        )
        
        result = crew.kickoff()
        return result
    
    def run_complete_workflow(self) -> tuple[List[Institution], str]:
        """Run the complete company research workflow."""
        print("🎯 Starting Complete Company Research Workflow")
        print(f"Researching interests: {', '.join(USER_INTERESTS)}")
        if USER_PROVIDED_COMPANIES:
            print(f"Institution similar to: {', '.join(USER_PROVIDED_COMPANIES)}")
        print("="*60)
        
        try:
            # Step 1: Research by interests
            print("\nSTEP 1: Interest-based research")
            self.run_interest_research()

            # Step 2: Research user-provided companies  
            print("\nSTEP 2: User-provided companies research")
            self.run_user_institutions_research()

            # Step 3: Research similar institutions  
            print("\nSTEP 3: Similar to user-provided companies research")
            self.run_similar_institutions_research()

            # Step 4: Validation and consolidation
            print("\nSTEP 4: Validation and consolidation")
            validated_results = self.run_validation_and_consolidation()

            # Process final results
            institutions, csv_file = process_research_results(validated_results)
            
            if institutions:
                print(f"\n✅ Company research completed successfully!")
                print(f"Results saved to: {csv_file}")
                print(f"Found {len(institutions)} relevant institutions")
                return institutions, csv_file
            else:
                print("\n❌ Failed to process results")
                return None, None
                
        except Exception as e:
            print(f"❌ Error in workflow: {e}")
            import traceback
            traceback.print_exc()
            return None, None

def run_company_research() -> tuple[List[Institution], str]:
    """Convenience function to run the complete company research workflow."""
    workflow = CompanyResearchWorkflow()
    return workflow.run_complete_workflow()