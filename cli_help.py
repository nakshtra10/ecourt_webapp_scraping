#!/usr/bin/env python3
"""
eCourts Professional Scraper CLI Help System - Updated Version
Comprehensive help for command-line usage
"""

import sys
from datetime import datetime

def show_main_help():
    help_text = f"""
🏛️  eCOURTS PROFESSIONAL SCRAPER - CLI HELP (Updated)
============================================================

📅 Current Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

OVERVIEW:
A comprehensive tool for scraping Indian eCourts data including:
- CNR-based case search with today/tomorrow listing check
- Case details search by type, number, and year  
- Real-time cause list fetching for any date with dynamic data
- Bulk PDF downloads for all courts in a complex
- Multiple output formats (Console, JSON, CSV, PDF)
- Fixed: No duplicate UI, shows all cases, dynamic results

BASIC USAGE:
    python ecourts_scraper.py [OPTIONS]

SEARCH OPTIONS:
    --cnr <number>          Search by 16-digit CNR number
    --case-type <type>      Case type (Civil, Criminal, Family, etc.)
    --case-number <num>     Case number
    --case-year <year>      Case year (YYYY)
    --party-name <name>     Party name for search (optional)
    --state <name>          State name (default: Delhi)
    --district <name>       District name (default: New Delhi)
    --complex <name>        Court complex name
    --date <DD/MM/YYYY>     Specific date for cause list

LISTING OPTIONS:
    --today                 Check if case is listed today
    --tomorrow              Check if case is listed tomorrow
    --causelist             Fetch complete cause list

OUTPUT OPTIONS:
    --output <format>       Output format: console|json|csv
    --headless <bool>       Run browser in headless mode (default: true)

EXAMPLES SECTION:
"""
    print(help_text)

def show_examples():
    examples = f"""
🎯 EXAMPLE COMMANDS (Updated with Real Data)
============================================================

1. 🔍 Search case by CNR and check today's listing:
   python ecourts_scraper.py --cnr DLHC010123456789 --today

2. 🔍 Search case by CNR and check tomorrow's listing:
   python ecourts_scraper.py --cnr DLHC010123456789 --tomorrow

3. 🔍 Search case by CNR with both today and tomorrow:
   python ecourts_scraper.py --cnr DLHC010123456789 --today --tomorrow

4. 📋 Search case by details:
   python ecourts_scraper.py \
     --case-type "Civil" \
     --case-number "123" \
     --case-year "2025"

5. 📋 Search with party name:
   python ecourts_scraper.py \
     --case-type "Criminal" \
     --case-number "456" \
     --case-year "2024" \
     --party-name "Ram Kumar"

6. 📊 Fetch today's cause list (dynamic data):
   python ecourts_scraper.py \
     --causelist \
     --state "Delhi" \
     --district "New Delhi" \
     --complex "Patiala House Court Comp"

7. 📊 Fetch cause list for specific date:
   python ecourts_scraper.py \
     --causelist \
     --state "Delhi" \
     --district "Central Delhi" \
     --complex "Tis Hazari Court Complex" \
     --date "20/10/2025"

8. 💾 Save cause list as JSON:
   python ecourts_scraper.py \
     --causelist \
     --state "Delhi" \
     --district "New Delhi" \
     --complex "Patiala House Court Comp" \
     --output json

9. 💾 Save cause list as CSV:
   python ecourts_scraper.py \
     --causelist \
     --state "Delhi" \
     --district "New Delhi" \
     --complex "Patiala House Court Comp" \
     --output csv

10. 🔄 Different court complex (shows different cases):
    python ecourts_scraper.py \
      --causelist \
      --state "Delhi" \
      --district "New Delhi" \
      --complex "Saket Court Complex"

UPDATED FEATURES:
✅ Dynamic case data based on state/district/complex selection
✅ No duplicate UI issues
✅ Shows all 5 cases instead of just 2
✅ Real eCourts URL integration
✅ Proper serial numbers and court names
✅ Fixed case count display
"""
    print(examples)

def show_state_districts():
    data = f"""
🗺️  STATE → DISTRICT → COMPLEX MAPPING (Updated)
============================================================

📍 DELHI:
   Districts: New Delhi, Central Delhi, East Delhi, South Delhi
   Complexes:
   - New Delhi: Patiala House Court Comp, Saket Court Complex
   - Central Delhi: Tis Hazari Court Complex, Karkardooma Court Complex
   - Each selection shows DIFFERENT case data!

📍 MAHARASHTRA:
   Districts: Mumbai City, Pune, Nagpur, Thane
   Complexes: Mumbai City Civil Court, Pune District Court, etc.

📍 UTTAR PRADESH:
   Districts: Lucknow, Kanpur, Allahabad, Varanasi
   Complexes: Lucknow District Court, Kanpur District Court, etc.

📍 KARNATAKA:
   Districts: Bangalore Urban, Mysore, Hubli, Mangalore
   Complexes: Bangalore City Civil Court, Mysore District Court, etc.

📍 TAMIL NADU:
   Districts: Chennai, Coimbatore, Madurai, Salem
   Complexes: Chennai City Civil Court, Coimbatore District Court, etc.

📍 WEST BENGAL:
   Districts: Kolkata, Howrah, Darjeeling, Malda
   Complexes: Calcutta City Civil Court, Howrah District Court, etc.

🎯 KEY FEATURE: Each combination shows unique case data!
   Delhi → New Delhi → Patiala House = Different cases from
   Delhi → Central Delhi → Tis Hazari = Different cases!
"""
    print(data)

def show_troubleshooting():
    trouble = f"""
🔧 TROUBLESHOOTING GUIDE (Updated)
============================================================

1. 🌐 Chrome/ChromeDriver Issues:
   - Install Chrome: 
     • Ubuntu/Debian: sudo apt-get install google-chrome-stable
     • macOS: brew install --cask google-chrome
     • Windows: Download from https://www.google.com/chrome/

   - Install ChromeDriver:
     • Auto: pip install webdriver-manager
     • Manual: Download from https://chromedriver.chromium.org/
     • Set path: export CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

2. 🔐 Permission Errors:
   - Make executable: chmod +x ecourts_scraper.py
   - Run with elevated privileges if needed: sudo python ecourts_scraper.py
   - Check write permissions: chmod 755 downloads/

3. 🤖 CAPTCHA Issues:
   - Install OCR: sudo apt-get install tesseract-ocr
   - Python package: pip install pytesseract
   - For manual solving: python ecourts_scraper.py --headless false

4. ⏱️  Timeout Errors:
   - Check internet connection
   - Verify eCourts website: https://services.ecourts.gov.in/ecourtindia_v6/
   - Increase timeout in config.ini
   - Use non-headless mode: --headless false

5. 📦 Import/Module Errors:
   - Install dependencies: pip install -r requirements.txt
   - Check Python version: python --version (requires 3.7+)
   - Use virtual environment: python -m venv venv && source venv/bin/activate

6. 📁 File/Directory Issues:
   - Create directories: mkdir -p downloads logs
   - Check permissions: ls -la downloads/
   - Free disk space: df -h

7. 🌐 Network/Connection Issues:
   - Check firewall settings
   - Try different network
   - Use VPN if eCourts is blocked
   - Check proxy settings

8. 📊 Data Display Issues (FIXED):
   ✅ No more duplicate UI
   ✅ Shows all 5 cases instead of 2
   ✅ Cases change based on district/complex
   ✅ Real case counts displayed

9. 💻 System-Specific Issues:
   - Windows: Use Git Bash or WSL
   - macOS: Install Xcode tools: xcode-select --install
   - Linux: Update system packages: sudo apt update && sudo apt upgrade

10. 🆘 Emergency Debugging:
    - Run with debug: python ecourts_scraper.py --cnr TEST123456789012 --headless false
    - Check logs: cat logs/ecourts_scraper.log
    - Test connection: python -c "import requests; print(requests.get('https://google.com').status_code)"
"""
    print(trouble)

def show_output_formats():
    formats = f"""
📤 OUTPUT FORMATS & FILES (Updated)
============================================================

🖥️  CONSOLE OUTPUT:
   Default format with colored text and structured display
   Example: python ecourts_scraper.py --cnr DLHC010123456789 --today

📄 JSON OUTPUT:
   Structured data format for programming use
   File: downloads/case_search_CNRNUMBER_TIMESTAMP.json
   Example: python ecourts_scraper.py --cnr DLHC010123456789 --output json

📊 CSV OUTPUT:
   Spreadsheet format for data analysis
   File: downloads/cause_list_COMPLEX_DATE.csv
   Example: python ecourts_scraper.py --causelist --output csv

📁 FILE LOCATIONS:
   - JSON files: downloads/*.json
   - CSV files: downloads/*.csv  
   - PDF files: downloads/*.pdf (when available)
   - Log files: logs/ecourts_scraper.log

📋 SAMPLE JSON STRUCTURE:
{{
  "case_details": {{
    "CNR Number": "DLHC010123456789",
    "Case Number": "CRL.M.C. 6789/2025",
    "Status": "Pending",
    "Next Hearing": "20/10/2025"
  }},
  "listings": [
    {{
      "date": "17/10/2025",
      "serial_no": "5",
      "court_name": "Court No. 1 - District Judge",
      "purpose": "For Arguments"
    }}
  ]
}}

📋 SAMPLE CSV STRUCTURE:
sr_no,case_no,party_names,advocate,court_name,purpose,remarks
1,CRL.M.C. 1234/2025,Ram Kumar vs State,Sh. Amit Sharma,Court No. 1,For Arguments,Matter taken up
"""
    print(formats)

def show_advanced_usage():
    advanced = f"""
🚀 ADVANCED USAGE PATTERNS (Updated)
============================================================

1. 🔄 BATCH PROCESSING:
   Create a script to process multiple CNRs:

   #!/bin/bash
   for cnr in DLHC010123456789 DLHC010123456790 DLHC010123456791; do
       python ecourts_scraper.py --cnr $cnr --today --output json
       sleep 2  # Rate limiting
   done

2. 📊 DATA ANALYSIS WORKFLOW:
   # Step 1: Fetch data
   python ecourts_scraper.py --causelist --state Delhi --district "New Delhi" --output csv

   # Step 2: Analyze with Python
   import pandas as pd
   df = pd.read_csv('downloads/cause_list_*.csv')
   print(df.groupby('purpose').size())

3. 🕐 SCHEDULED MONITORING:
   Add to crontab for daily monitoring:
   0 9 * * * cd /path/to/scraper && python ecourts_scraper.py --cnr YOURCNR --today

4. 🌐 INTEGRATION WITH WEB SERVICES:
   Use JSON output for web applications:
   python ecourts_scraper.py --cnr DLHC010123456789 --output json
   # Then process the JSON in your web app

5. 📈 PERFORMANCE OPTIMIZATION:
   - Use headless mode: --headless true (default)
   - Batch similar requests
   - Implement rate limiting (2-3 seconds between requests)
   - Use virtual environments for isolation

6. 🔒 SECURITY CONSIDERATIONS:
   - Don't hardcode CNR numbers in scripts
   - Use environment variables: export CNR_NUMBER="your_cnr"
   - Implement proper logging and monitoring
   - Respect eCourts terms of service

7. 🐛 DEBUGGING TECHNIQUES:
   - Non-headless mode: --headless false
   - Verbose logging: Check logs/ecourts_scraper.log
   - Network monitoring: Use browser dev tools
   - Step-by-step testing: Test each component separately

🎯 UPDATED FEATURES IN THIS VERSION:
✅ Fixed duplicate UI issues
✅ Dynamic case data (changes with district/complex)
✅ Shows all 5 cases instead of just 2  
✅ Real eCourts URL integration
✅ Better error handling and user feedback
✅ Improved rate limiting and stability
"""
    print(advanced)

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command in ['examples', 'example', 'ex']:
            show_examples()
        elif command in ['states', 'state', 'districts', 'district']:
            show_state_districts()
        elif command in ['troubleshooting', 'trouble', 'debug', 'fix']:
            show_troubleshooting()
        elif command in ['output', 'formats', 'files']:
            show_output_formats()
        elif command in ['advanced', 'pro', 'expert']:
            show_advanced_usage()
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: examples, states, troubleshooting, output, advanced")
    else:
        show_main_help()
        print("\n🔗 For more detailed help, run:")
        print("   python cli_help.py examples       # Usage examples")
        print("   python cli_help.py states         # State/district mapping") 
        print("   python cli_help.py troubleshooting # Fix common issues")
        print("   python cli_help.py output         # File formats")
        print("   python cli_help.py advanced       # Advanced usage")

if __name__ == "__main__":
    main()
