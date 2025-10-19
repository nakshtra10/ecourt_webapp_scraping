#!/usr/bin/env python3
"""
eCourts Professional Scraper Launcher - Updated Version
Easy-to-use launcher for the complete eCourts scraper system
"""

import sys
import os
import subprocess
import platform
from datetime import datetime

def print_banner():
    print("="*70)
    print("🏛️  eCOURTS PROFESSIONAL SCRAPER - UPDATED VERSION")
    print("="*70)
    print("Real-time Case Search & Cause List Fetcher")
    print("✅ Fixed: No Duplicate UI • Shows All Cases • Dynamic Data")
    print(f"📅 Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*70)

def check_requirements():
    """Check if required files exist"""
    required_files = [
        'ecourts_scraper.py',
        'ecourts_web_interface.py',
        'requirements.txt'
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False

    print("✅ All required files found")
    return True

def install_dependencies():
    """Install required dependencies"""
    try:
        print("\n📦 Installing dependencies...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def run_web_interface():
    """Launch the web interface"""
    try:
        print("\n🌐 Starting web interface...")
        print("📱 Open http://localhost:5000 in your browser")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)

        subprocess.run([sys.executable, 'ecourts_web_interface.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Web server stopped")
    except Exception as e:
        print(f"\n❌ Error starting web interface: {e}")

def run_cli_help():
    """Show CLI help"""
    try:
        subprocess.run([sys.executable, 'ecourts_scraper.py', '--help'])
    except Exception as e:
        print(f"❌ Error showing CLI help: {e}")

def run_quick_cnr_search():
    """Quick CNR search"""
    print("\n🔍 Quick CNR Search")
    print("-" * 30)

    while True:
        cnr = input("Enter CNR number (16 digits) or 'back' to return: ").strip()

        if cnr.lower() == 'back':
            return

        if len(cnr) != 16 or not cnr.isalnum():
            print("❌ Invalid CNR. Must be exactly 16 alphanumeric characters.")
            continue

        check_today = input("Check today's listing? (y/n): ").strip().lower() == 'y'
        check_tomorrow = input("Check tomorrow's listing? (y/n): ").strip().lower() == 'y'

        try:
            print(f"\n🔍 Searching CNR: {cnr}")

            cmd = [sys.executable, 'ecourts_scraper.py', '--cnr', cnr]
            if check_today:
                cmd.append('--today')
            if check_tomorrow:
                cmd.append('--tomorrow')

            subprocess.run(cmd)

            break
        except Exception as e:
            print(f"❌ Error in CNR search: {e}")
            break

def run_quick_cause_list():
    """Quick cause list fetch"""
    print("\n📊 Quick Cause List Fetch")
    print("-" * 30)

    # Get user input
    state = input("Enter state (default: Delhi): ").strip() or "Delhi"
    district = input("Enter district (default: New Delhi): ").strip() or "New Delhi"
    complex_name = input("Enter court complex (default: Patiala House Court Comp): ").strip() or "Patiala House Court Comp"

    date = input("Enter date (DD/MM/YYYY) or press Enter for today: ").strip()
    if not date:
        date = datetime.now().strftime("%d/%m/%Y")

    output_format = input("Output format (console/json/csv, default: console): ").strip() or "console"

    try:
        print(f"\n📊 Fetching cause list...")
        print(f"📍 {state} → {district} → {complex_name}")
        print(f"📅 Date: {date}")

        cmd = [
            sys.executable, 'ecourts_scraper.py',
            '--causelist',
            '--state', state,
            '--district', district,
            '--complex', complex_name,
            '--date', date,
            '--output', output_format
        ]

        subprocess.run(cmd)

    except Exception as e:
        print(f"❌ Error fetching cause list: {e}")

def run_system_info():
    """Show system information"""
    print("\n💻 System Information")
    print("-" * 30)
    print(f"🐍 Python Version: {platform.python_version()}")
    print(f"💻 Platform: {platform.system()} {platform.release()}")
    print(f"🏗️  Architecture: {platform.architecture()[0]}")

    # Check Chrome
    try:
        if platform.system() == "Windows":
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
        else:
            chrome_paths = ["/usr/bin/google-chrome", "/usr/bin/chromium-browser"]

        chrome_found = any(os.path.exists(path) for path in chrome_paths)
        print(f"🌐 Chrome Browser: {'✅ Found' if chrome_found else '❌ Not Found'}")
    except:
        print("🌐 Chrome Browser: ❓ Unknown")

    # Check pip packages
    try:
        import selenium, flask, requests, bs4
        print("📦 Required Packages: ✅ Installed")
    except ImportError as e:
        print(f"📦 Required Packages: ❌ Missing - {e}")

def main():
    """Main launcher function"""
    print_banner()

    # Check requirements
    if not check_requirements():
        print("\n🛠️  Please ensure all required files are present")
        input("\nPress Enter to exit...")
        return

    while True:
        print("\n📋 Select an option:")
        print("1. 🌐 Launch Web Interface (Recommended)")
        print("2. 🖥️  Command Line Help")
        print("3. 🔍 Quick CNR Search")
        print("4. 📊 Quick Cause List")
        print("5. 📦 Install Dependencies")
        print("6. 💻 System Information")
        print("7. 📖 View Documentation")
        print("0. 👋 Exit")

        try:
            choice = input("\nEnter your choice (0-7): ").strip()

            if choice == "1":
                run_web_interface()

            elif choice == "2":
                print("\n🖥️  Command Line Interface Help:")
                print("-" * 40)
                run_cli_help()

            elif choice == "3":
                run_quick_cnr_search()

            elif choice == "4":
                run_quick_cause_list()

            elif choice == "5":
                install_dependencies()

            elif choice == "6":
                run_system_info()

            elif choice == "7":
                if os.path.exists("README.md"):
                    print("\n📖 Documentation:")
                    print("-" * 40)
                    with open("README.md", "r", encoding='utf-8') as f:
                        content = f.read()
                        # Show first 2000 characters
                        print(content[:2000])
                        if len(content) > 2000:
                            print("\n... (truncated)")
                else:
                    print("\n❌ README.md not found")

            elif choice == "0":
                print("\n👋 Thank you for using eCourts Professional Scraper!")
                print("🎊 Perfect for internship submissions and production use!")
                break

            else:
                print("\n❌ Invalid choice. Please try again.")

            if choice != "0" and choice != "1":
                input("\nPress Enter to continue...")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
