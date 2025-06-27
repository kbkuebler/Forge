#!/usr/bin/env bash
set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}[*] Installing Python, pip, and virtual environment...${NC}"

# Ensure apt is up to date
sudo apt-get update

# Install Python 3, pip, and venv support
sudo apt-get install -y python3 python3-pip python3-venv

# Create the virtual environment if it doesn't already exist
if [ ! -d ".venv" ]; then
    echo -e "${GREEN}[*] Creating Python virtual environment in .venv...${NC}"
    python3 -m venv .venv
else
    echo -e "${GREEN}[✓] .venv already exists, skipping creation.${NC}"
fi

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip
echo -e "${GREEN}[*] Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}[*] Installing Python dependencies from requirements.txt...${NC}"
    pip install -r requirements.txt
else
    echo -e "${GREEN}[!] requirements.txt not found, skipping Python package installation.${NC}"
fi

# Add .venv to .gitignore if not already present
if [ ! -f ".gitignore" ]; then
    touch .gitignore
fi

if ! grep -qxF ".venv/" .gitignore; then
    echo ".venv/" >> .gitignore
    echo -e "${GREEN}[*] Added '.venv/' to .gitignore.${NC}"
else
    echo -e "${GREEN}[✓] .venv/ already in .gitignore.${NC}"
fi

echo -e "${GREEN}[✓] Python environment setup complete.${NC}"

