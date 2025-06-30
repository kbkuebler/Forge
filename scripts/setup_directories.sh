#!/usr/bin/env bash
set -euo pipefail

GREEN='\033[0;32m'
NC='\033[0m'




echo -e "${GREEN}[*] Creating SE Toolkit project structure...${NC}"

# Ensure .local/bin exists
if [ ! -d "$HOME/.local/bin" ]; then
    mkdir -p "$HOME/.local/bin"
    echo -e "${GREEN}[*] Created .local/bin directory.${NC}"
fi

# Add .local/bin to PATH"
if ! grep -q "export PATH=\$HOME/.local/bin:\$PATH" "$HOME/.bashrc"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> $HOME/.bashrc
fi

# Create starter .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo ".venv/" > .gitignore
    echo -e "${GREEN}[*] Created .gitignore with .venv/${NC}"
elif ! grep -qxF ".venv/" .gitignore; then
    echo ".venv/" >> .gitignore
    echo -e "${GREEN}[*] Appended .venv/ to .gitignore${NC}"
fi

echo -e "${GREEN} Directory structure created.${NC}"

