# main.py
"""
Main entry point for the Job Search System
"""

import os
from crews import run_company_research

def setup_environment():
    """Set up environment variables and validate configuration."""
    # Check for required environment variables
    required_vars = ['OPENAI_API_KEY', 'SERPER_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these environment variables before running the system.")
        return False
    
    return True

def main():
    """Main function to orchestrate the job search system."""
    print("🚀 Job Search System")
    print("="*50)
    
    # Validate environment setup
    if not setup_environment():
        return
    
    try:
        # Import here to trigger configuration loading
        from crews import run_company_research
        
        print("\nStarting Company Research...")
        institutions, csv_file = run_company_research()
        
        if institutions and csv_file:
            print(f"\n🎉 Success! Found {len(institutions)} institutions")
            print(f"📄 Results saved to: {csv_file}")
        else:
            print("\n❌ Company research failed")
            
    except FileNotFoundError as e:
        print("\n❌ Configuration file missing!")
        print("Please run the setup first:")
        print("  python setup_config.py")
        print("\nOr manually create config/user_config.txt using the template.")
    except KeyboardInterrupt:
        print("\n\n⏹️  Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()