# config/config_parser.py
"""
Configuration parser for user settings
"""
import os
from typing import List, Dict, Any
from pathlib import Path

def parse_list_value(value: str) -> List[str]:
    """Parse a comma-separated string into a list of stripped strings."""
    if not value.strip():
        return []
    return [item.strip() for item in value.split(',') if item.strip()]

def parse_boolean_value(value: str) -> bool:
    """Parse a string into a boolean value."""
    return value.lower().strip() in ('true', 'yes', '1', 'on')

def load_user_config(config_file: str = "config/user_config.txt") -> Dict[str, Any]:
    """
    Load user configuration from a text file.
    
    Args:
        config_file: Path to the user configuration file
        
    Returns:
        Dictionary containing parsed configuration values
    """
    config_path = Path(config_file)
    
    if not config_path.exists():
        raise FileNotFoundError(
            f"User configuration file not found: {config_file}\n"
            f"Please create this file using the template and fill in your information."
        )
    
    config = {}
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse key=value pairs
                if '=' not in line:
                    print(f"Warning: Invalid line {line_num} in {config_file}: {line}")
                    continue
                
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Skip empty values
                if not value:
                    continue
                
                config[key] = value
                
    except Exception as e:
        raise Exception(f"Error reading configuration file {config_file}: {e}")
    
    return config

def get_user_configuration() -> Dict[str, Any]:
    """
    Get processed user configuration with defaults and validation.
    
    Returns:
        Dictionary with all configuration values needed by the system
    """
    # Load raw configuration
    raw_config = load_user_config()
    
    # Process and validate configuration
    processed_config = {
        # Personal information
        'CV_FILE_PATH': raw_config.get('CV_FILE_PATH', ''),
        'LINKEDIN_PROFILE': raw_config.get('LINKEDIN_PROFILE', ''),
        'EMAIL': raw_config.get('EMAIL', ''),
        
        # Job search preferences
        'USER_INTERESTS': parse_list_value(raw_config.get('USER_INTERESTS', '')),
        'GEOGRAPHIC_FOCUS': parse_list_value(raw_config.get('GEOGRAPHIC_FOCUS', 'Netherlands')),
        
        # Company preferences
        'USER_PROVIDED_COMPANIES': parse_list_value(raw_config.get('COMPANIES_OF_INTEREST', '')),
        'USER_PROVIDED_COMPANIES_NO': parse_list_value(raw_config.get('COMPANIES_TO_EXCLUDE', '')),
        
        # Search preferences
        'INSTITUTION_TYPES': parse_list_value(raw_config.get('INSTITUTION_TYPES', 
            'universities, companies, startups, research_institutes, government_agencies')),
        
        # Search configuration
        'SEARCH_CONFIG': {
            'location': raw_config.get('SEARCH_LOCATION', 'Europe'),
            'locale': raw_config.get('SEARCH_LOCALE', 'en-GB'),
            'n_results': int(raw_config.get('MAX_RESULTS_PER_SEARCH', '10'))
        },
        
        # Output configuration
        'OUTPUT_CONFIG': {
            'csv_filename': raw_config.get('OUTPUT_FILENAME', 'institutions_job_research.csv'),
            'verbose': parse_boolean_value(raw_config.get('VERBOSE_OUTPUT', 'false'))
        }
    }
    
    # Validation
    if not processed_config['USER_INTERESTS']:
        raise ValueError("USER_INTERESTS cannot be empty. Please specify at least one interest.")
    
    if not processed_config['GEOGRAPHIC_FOCUS']:
        print("Warning: No geographic focus specified. Using default: Netherlands")
        processed_config['GEOGRAPHIC_FOCUS'] = ['Netherlands']
    
    return processed_config

def print_configuration_summary(config: Dict[str, Any]):
    """Print a summary of the loaded configuration."""
    print("📋 User Configuration Loaded:")
    print("-" * 40)
    
    if config['CV_FILE_PATH']:
        cv_exists = os.path.exists(config['CV_FILE_PATH'])
        status = "✅" if cv_exists else "❌ (file not found)"
        print(f"CV File: {config['CV_FILE_PATH']} {status}")
    
    if config['LINKEDIN_PROFILE']:
        print(f"LinkedIn: {config['LINKEDIN_PROFILE']}")
    
    print(f"Interests: {', '.join(config['USER_INTERESTS'])}")
    print(f"Geographic Focus: {', '.join(config['GEOGRAPHIC_FOCUS'])}")
    
    if config['USER_PROVIDED_COMPANIES']:
        print(f"Companies of Interest: {', '.join(config['USER_PROVIDED_COMPANIES'])}")
    
    if config['USER_PROVIDED_COMPANIES_NO']:
        print(f"Companies to Exclude: {', '.join(config['USER_PROVIDED_COMPANIES_NO'])}")
    
    print(f"Search Location: {config['SEARCH_CONFIG']['location']}")
    print(f"Output File: {config['OUTPUT_CONFIG']['csv_filename']}")
    print("-" * 40)