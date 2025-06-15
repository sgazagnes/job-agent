# utils/file_utils.py
"""
Utility functions for file operations and data processing
"""

import re
import json5 as json
import pandas as pd
from typing import List
from models.data_models import Institution

def extract_json_block(text: str) -> str:
    """Extract JSON code block from text."""
    # Try multiple patterns to find JSON
    patterns = [
        r"```(?:json)?\s*(\[.*?\])\s*```",  # JSON array in code block
        r"```(?:json)?\s*(\{.*?\})\s*```",  # JSON object in code block
        r'(\[.*?\])',  # JSON array without code block
        r'(\{.*?\})'   # JSON object without code block
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1)
    
    raise ValueError("No valid JSON block found in the output.")

def save_institutions_to_csv(institutions: List[Institution], filename: str = None) -> str:
    """Save institutions to CSV file."""
    if filename is None:
        filename = "institutions_job_research.csv"
    
    df = pd.DataFrame([inst.dict() for inst in institutions])
    df.to_csv(filename, index=False)
    print(f"Institutions saved to {filename}")
    return filename

def load_institutions_from_csv(filename: str) -> List[Institution]:
    """Load institutions from CSV file."""
    try:
        df = pd.read_csv(filename)
        return [Institution(**row.to_dict()) for _, row in df.iterrows()]
    except Exception as e:
        print(f"Error loading from CSV: {e}")
        return []

def print_research_summary(institutions: List[Institution]):
    """Print a summary of research results."""
    print(f"\nResearch Summary:")
    print(f"Total institutions found: {len(institutions)}")
    
    # Count by type
    type_counts = {}
    for inst in institutions:
        type_counts[inst.type] = type_counts.get(inst.type, 0) + 1
    
    print("\nInstitutions by type:")
    for inst_type, count in sorted(type_counts.items()):
        print(f"  {inst_type}: {count}")
    
    # Count by interest
    interest_counts = {}
    for inst in institutions:
        interest = inst.interest_match
        interest_counts[interest] = interest_counts.get(interest, 0) + 1
        
    print("\nInstitutions by interest match:")
    for interest, count in sorted(interest_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {interest}: {count}")

def process_research_results(raw_output) -> tuple[List[Institution], str]:
    """Process and save the final research results."""
    try:
        print("Processing final results...")
        
        # Extract JSON and create Institution objects
        raw_json = extract_json_block(str(raw_output))
        final_list = json.loads(raw_json)
        institutions = [Institution(**inst_data) for inst_data in final_list]
                
        # Save to CSV
        filename = save_institutions_to_csv(institutions)
        
        # Print summary
        print_research_summary(institutions)
        
        return institutions, filename
        
    except Exception as e:
        print(f"Error processing results: {e}")
        print("Raw output:")
        print(raw_output)
        return None, None