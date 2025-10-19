#!/bin/bash
# eCourts Professional Scraper - Complete Setup Script
# Updated version with all fixes and improvements

echo "🚀 eCourts Professional Scraper - Complete Setup"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running on supported OS
check_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        print_info "Detected OS: Linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        print_info "Detected OS: macOS"
    elif [[ "$OSTYPE" == "msys" ]]; then
        OS="windows"
        print_info "Detected OS: Windows (Git Bash)"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
}

# Check Python version
check_python() {
    print_info "Checking Python installation..."

    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python is not installed or not in PATH"
        exit 1
    fi

    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
        print_error "Python 3.7+ is required. Current version: $PYTHON_VERSION"
        exit 1
    fi

    print_status "Python $PYTHON_VERSION found"
}

# Create virtual environment
create_venv() {
    print_info "Creating virtual environment..."

    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists"
        read -p "Do you want to recreate it? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf venv
        else
            return 0
        fi
    fi

    $PYTHON_CMD -m venv venv

    if [ $? -eq 0 ]; then
        print_status "Virtual environment created"
    else
        print_error "Failed to create virtual environment"
        exit 1
    fi
}

# Activate virtual environment
activate_venv() {
    print_info "Activating virtual environment..."

    if [[ "$OS" == "windows" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi

    if [ $? -eq 0 ]; then
        print_status "Virtual environment activated"
    else
        print_error "Failed to activate virtual environment"
        exit 1
    fi
}

# Install Python dependencies
install_python_deps() {
    print_info "Installing Python dependencies..."

    # Upgrade pip first
    pip install --upgrade pip

    # Install requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt

        if [ $? -eq 0 ]; then
            print_status "Python dependencies installed"
        else
            print_error "Failed to install some Python dependencies"
            print_warning "You may need to install some packages manually"
        fi
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Install system dependencies
install_system_deps() {
    print_info "Installing system dependencies..."

    case $OS in
        "linux")
            # Detect package manager
            if command -v apt-get &> /dev/null; then
                print_info "Using apt package manager..."
                sudo apt-get update
                sudo apt-get install -y wget curl unzip

                # Install Chrome
                wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
                echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google.list
                sudo apt-get update
                sudo apt-get install -y google-chrome-stable

                # Install ChromeDriver
                CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
                wget -N http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip
                unzip -o chromedriver_linux64.zip
                sudo mv chromedriver /usr/local/bin/
                sudo chmod +x /usr/local/bin/chromedriver
                rm chromedriver_linux64.zip

                # Install tesseract for CAPTCHA
                sudo apt-get install -y tesseract-ocr tesseract-ocr-eng

            elif command -v yum &> /dev/null; then
                print_info "Using yum package manager..."
                sudo yum update -y
                sudo yum install -y wget curl unzip

                # Install Chrome on CentOS/RHEL
                cat << EOF | sudo tee /etc/yum.repos.d/google-chrome.repo
[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
EOF
                sudo yum install -y google-chrome-stable

                # Install tesseract
                sudo yum install -y tesseract tesseract-langpack-eng

            else
                print_warning "Unknown package manager. Please install Chrome and ChromeDriver manually."
            fi
            ;;

        "macos")
            print_info "Installing dependencies for macOS..."

            # Check if Homebrew is installed
            if ! command -v brew &> /dev/null; then
                print_warning "Homebrew not found. Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi

            # Install Chrome and ChromeDriver
            brew install --cask google-chrome
            brew install chromedriver

            # Install tesseract
            brew install tesseract
            ;;

        "windows")
            print_warning "Please install the following manually on Windows:"
            echo "1. Google Chrome: https://www.google.com/chrome/"
            echo "2. ChromeDriver: https://chromedriver.chromium.org/"
            echo "3. Add ChromeDriver to your PATH"
            ;;
    esac

    print_status "System dependencies installation completed"
}

# Create directories
create_directories() {
    print_info "Creating required directories..."

    mkdir -p downloads
    mkdir -p logs
    mkdir -p data
    mkdir -p exports

    print_status "Directories created"
}

# Set permissions
set_permissions() {
    print_info "Setting file permissions..."

    chmod +x launcher.py
    chmod +x ecourts_scraper.py

    if [[ "$OS" != "windows" ]]; then
        chmod +x setup.sh
    fi

    print_status "Permissions set"
}

# Verify installation
verify_installation() {
    print_info "Verifying installation..."

    # Test Python imports
    $PYTHON_CMD -c "import selenium, flask, requests, bs4; print('✅ Required packages imported successfully')" 2>/dev/null

    if [ $? -eq 0 ]; then
        print_status "Python packages verification passed"
    else
        print_error "Some Python packages failed to import"
    fi

    # Test Chrome installation
    if command -v google-chrome &> /dev/null || command -v chrome &> /dev/null || command -v chromium-browser &> /dev/null; then
        print_status "Chrome browser found"
    else
        print_warning "Chrome browser not found in PATH"
    fi

    # Test ChromeDriver
    if command -v chromedriver &> /dev/null; then
        print_status "ChromeDriver found"
    else
        print_warning "ChromeDriver not found in PATH"
    fi
}

# Main setup function
main() {
    echo
    print_info "Starting eCourts Professional Scraper setup..."
    echo

    check_os
    check_python
    create_venv
    activate_venv
    install_python_deps
    install_system_deps
    create_directories
    set_permissions
    verify_installation

    echo
    echo "=================================================="
    print_status "Setup completed successfully!"
    echo "=================================================="
    echo
    echo "🎯 Quick Start Commands:"
    echo "  1. Web Interface:  python launcher.py"
    echo "  2. CLI Help:       python ecourts_scraper.py --help"
    echo "  3. CNR Search:     python ecourts_scraper.py --cnr DLHC010123456789 --today"
    echo "  4. Cause List:     python ecourts_scraper.py --causelist --state Delhi"
    echo
    echo "📱 Web Interface: http://localhost:5000"
    echo "📁 Downloads:     ./downloads/"
    echo "📋 Logs:          ./logs/"
    echo
    echo "🎊 Ready for internship submission and production use!"
    echo
}

# Run main function
main
