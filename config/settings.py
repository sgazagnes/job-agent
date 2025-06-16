# # config/settings.py
# """
# Configuration settings for the Job Search System
# """

# # User Configuration
# USER_INTERESTS = [
#     "Scientific Computing",
#     # "Energy",
#     # "Research", 
#     # "Quantum computing",
#     # "Climate Science",
#     # "Health"
# ]

# # Institution types to research
# INSTITUTION_TYPES = [
#     "universities",
#     "companies", 
#     "startups",
#     "research_institutes",
#     "government_agencies",
# ]

# # User-provided companies to research
# USER_PROVIDED_COMPANIES = [
#     "TNO",
#     "SURF",
#     "Netherlands eScience Center"
# ]

# # Companies to exclude from results
# USER_PROVIDED_COMPANIES_NO = [
#     "Amazon",
#     "Meta", 
#     "Eindhoven University",
#     "ASML",
# ]

# # Geographic focus
# GEOGRAPHIC_FOCUS = ["Netherlands"]

# # Search configuration
# SEARCH_CONFIG = {
#     "location": "Europe",
#     "locale": "en-GB", 
#     "n_results": 10
# }

# # Output configuration
# OUTPUT_CONFIG = {
#     "csv_filename": "institutions_job_research.csv",
#     "verbose": False
# }
# config/settings.py
"""
Configuration settings for the Job Search System
Loads user configuration from user_config.txt
"""

from .config_parser import get_user_configuration, print_configuration_summary

# Load user configuration
try:
    _user_config = get_user_configuration()
    
    # Personal Information
    CV_FILE_PATH = _user_config['CV_FILE_PATH']
    LINKEDIN_PROFILE = _user_config['LINKEDIN_PROFILE']
    EMAIL = _user_config['EMAIL']
    
    # Job Search Configuration
    USER_INTERESTS = _user_config['USER_INTERESTS']
    GEOGRAPHIC_FOCUS = _user_config['GEOGRAPHIC_FOCUS']
    INSTITUTION_TYPES = _user_config['INSTITUTION_TYPES']
    
    # Company Preferences
    USER_PROVIDED_COMPANIES = _user_config['USER_PROVIDED_COMPANIES']
    USER_PROVIDED_COMPANIES_NO = _user_config['USER_PROVIDED_COMPANIES_NO']
    
    # Search and Output Configuration
    SEARCH_CONFIG = _user_config['SEARCH_CONFIG']
    OUTPUT_CONFIG = _user_config['OUTPUT_CONFIG']
    
    # Print configuration summary when loaded
    print_configuration_summary(_user_config)
    
except FileNotFoundError as e:
    print("❌ Configuration Error:")
    print(e)
    print("\n📝 Please create and fill the config/user_config.txt file.")
    print("You can use the template provided in config/user_config.txt")
    raise
    
except Exception as e:
    print(f"❌ Error loading user configuration: {e}")
    raise

def get_full_config():
    """Return the full user configuration dictionary."""
    return _user_config