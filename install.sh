#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== wpgen Installation ===${NC}"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"

# Target directories
DEPLOY_DIR="$HOME/.local/share/wpgen"
BIN_DIR="$HOME/.local/bin"
LAUNCHER="$BIN_DIR/wpgen"

echo -e "${BLUE}Project directory: ${NC}$PROJECT_DIR"
echo -e "${BLUE}Deploy directory:  ${NC}$DEPLOY_DIR"
echo -e "${BLUE}Launcher:          ${NC}$LAUNCHER"
echo ""

# Create directories
echo -e "${GREEN}Creating directories...${NC}"
mkdir -p "$DEPLOY_DIR"
mkdir -p "$BIN_DIR"

# Copy Python files
echo -e "${GREEN}Copying Python files...${NC}"
for file in ai_generator.py generate_examples.py generator.py kitchn_bridge.py tui.py; do
    if [ -f "$PROJECT_DIR/$file" ]; then
        cp "$PROJECT_DIR/$file" "$DEPLOY_DIR/$file"
        echo "  Copied: $file"
    fi
done

# Copy static files
echo -e "${GREEN}Copying static files...${NC}"
if [ -d "$PROJECT_DIR/examples" ]; then
    cp -r "$PROJECT_DIR/examples" "$DEPLOY_DIR/" 2>/dev/null || true
    echo "  Copied: examples/"
fi

for file in README.md requirements.txt; do
    if [ -f "$PROJECT_DIR/$file" ]; then
        cp "$PROJECT_DIR/$file" "$DEPLOY_DIR/"
        echo "  Copied: $file"
    fi
done

# Create virtual environment
echo -e "${GREEN}Setting up virtual environment...${NC}"
if [ ! -d "$DEPLOY_DIR/.venv" ]; then
    python3 -m venv "$DEPLOY_DIR/.venv"
    echo "  Created virtual environment"
fi

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
"$DEPLOY_DIR/.venv/bin/pip" install --upgrade pip > /dev/null
"$DEPLOY_DIR/.venv/bin/pip" install -r "$DEPLOY_DIR/requirements.txt" > /dev/null
echo "  Dependencies installed"

# Create launcher script
echo -e "${GREEN}Creating launcher script...${NC}"
cat > "$LAUNCHER" << 'EOF'
#!/bin/bash
# Wrapper for the Wallpaper Generator TUI
PROJECT_DIR="$HOME/.local/share/wpgen"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python3"

if [ -f "$VENV_PYTHON" ]; then
    exec "$VENV_PYTHON" "$PROJECT_DIR/tui.py" "$@"
else
    echo "Error: Virtual environment not found at $VENV_PYTHON"
    exit 1
fi
EOF

chmod +x "$LAUNCHER"
echo "  Created: $LAUNCHER"

echo ""
echo -e "${GREEN}✓ Installation complete!${NC}"
echo ""
echo "Run 'wpgen' to start the Wallpaper Generator TUI"
echo ""
echo -e "${BLUE}Note:${NC} Make sure ~/.local/bin is in your PATH"
echo "  Add to your shell config: export PATH=\"\$HOME/.local/bin:\$PATH\""
