#!/usr/bin/env bash
set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== wpgen Installation ===${NC}"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# XDG-compliant directories
INSTALL_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/wpgen"
BIN_DIR="$HOME/.local/bin"

echo -e "${BLUE}Installing to $INSTALL_DIR${NC}"

# Create installation directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"

# Copy source files
echo -e "${GREEN}Copying source files...${NC}"
cp -v "$SCRIPT_DIR"/*.py "$INSTALL_DIR/"

# Create virtual environment
echo -e "${GREEN}Creating virtual environment...${NC}"
python3 -m venv "$INSTALL_DIR/venv"

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip -q
"$INSTALL_DIR/venv/bin/pip" install -r "$SCRIPT_DIR/requirements.txt" -q

# Create wrapper script
echo -e "${GREEN}Creating wrapper script...${NC}"
cat > "$BIN_DIR/wpgen" << 'EOF'
#!/usr/bin/env bash
WPGEN_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/wpgen"
exec "$WPGEN_DIR/venv/bin/python" "$WPGEN_DIR/tui.py" "$@"
EOF

chmod +x "$BIN_DIR/wpgen"

echo ""
echo -e "${GREEN}✓ Installation complete!${NC}"
echo ""
echo -e "  Application: ${BLUE}$INSTALL_DIR${NC}"
echo -e "  Command:     ${BLUE}$BIN_DIR/wpgen${NC}"
echo ""
echo "Run 'wpgen' to start the Wallpaper Generator TUI"
echo ""
echo -e "${BLUE}Note:${NC} Make sure ~/.local/bin is in your PATH"
echo "  Add to your shell config: export PATH=\"\$HOME/.local/bin:\$PATH\""
