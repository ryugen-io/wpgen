#!/usr/bin/env bash
set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== wpgen Installation ===${NC}"
echo ""

# Check if pipx is installed
if ! command -v pipx &> /dev/null; then
    echo -e "${RED}Error: pipx is not installed${NC}"
    echo ""
    echo "Install pipx first:"
    echo "  Arch/CachyOS: sudo pacman -S python-pipx"
    echo "  Debian/Ubuntu: sudo apt install pipx"
    echo "  Fedora: sudo dnf install pipx"
    echo ""
    echo "Or via pip: python3 -m pip install --user pipx"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${GREEN}Installing wpgen via pipx...${NC}"
pipx install "$SCRIPT_DIR" --force

echo ""
echo -e "${GREEN}✓ Installation complete!${NC}"
echo ""
echo "Run 'wpgen' to start the Wallpaper Generator TUI"
