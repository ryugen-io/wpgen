#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== wpgen Installation ===${NC}"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"

# Target directories
BIN_DIR="$HOME/.local/bin"
BINARY="$BIN_DIR/wpgen"
BUILD_DIR="$PROJECT_DIR/build"
DIST_DIR="$PROJECT_DIR/dist"

echo -e "${BLUE}Building standalone binary...${NC}"
echo ""

# Create temporary venv for building
TEMP_VENV="$PROJECT_DIR/.build-venv"
if [ ! -d "$TEMP_VENV" ]; then
    echo -e "${GREEN}Creating build environment...${NC}"
    python3 -m venv "$TEMP_VENV"
fi

# Install dependencies and PyInstaller
echo -e "${GREEN}Installing dependencies...${NC}"
"$TEMP_VENV/bin/pip" install --upgrade pip -q
"$TEMP_VENV/bin/pip" install -r "$PROJECT_DIR/requirements.txt" -q

# Build with PyInstaller
echo -e "${GREEN}Compiling to single binary...${NC}"
echo -e "${YELLOW}This may take a few minutes...${NC}"
"$TEMP_VENV/bin/pyinstaller" \
    --onefile \
    --name wpgen \
    --clean \
    --noconfirm \
    "$PROJECT_DIR/tui.py" > /dev/null 2>&1

# Install binary
echo -e "${GREEN}Installing binary...${NC}"
mkdir -p "$BIN_DIR"
cp "$DIST_DIR/wpgen" "$BINARY"
chmod +x "$BINARY"

# Cleanup
echo -e "${GREEN}Cleaning up...${NC}"
rm -rf "$BUILD_DIR" "$DIST_DIR" "$TEMP_VENV" wpgen.spec

echo ""
echo -e "${GREEN}✓ Installation complete!${NC}"
echo ""
echo -e "  Binary installed: ${BLUE}$BINARY${NC}"
echo ""
echo "Run 'wpgen' to start the Wallpaper Generator TUI"
echo ""
echo -e "${BLUE}Note:${NC} Make sure ~/.local/bin is in your PATH"
echo "  Add to your shell config: export PATH=\"\$HOME/.local/bin:\$PATH\""
