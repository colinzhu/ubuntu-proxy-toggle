#!/bin/bash
# Enable auto-start for proxy-toggle-tray on login

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/proxy-toggle-tray.py"

# Check if the script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: proxy-toggle-tray.py not found at $SCRIPT_PATH"
    exit 1
fi

# Create autostart directory if it doesn't exist
mkdir -p ~/.config/autostart

# Create desktop entry for auto-start
cat > ~/.config/autostart/proxy-toggle.desktop << EOF
[Desktop Entry]
Name=Proxy Toggle
Comment=System tray proxy toggle
Exec=$SCRIPT_PATH
Icon=network-workgroup
Terminal=false
Type=Application
Categories=Utility;Network;
EOF

echo "Auto-start enabled!"
echo ""
echo "The proxy toggle will now start automatically when you log in."
echo ""
echo "To disable auto-start, run:"
echo "  rm ~/.config/autostart/proxy-toggle.desktop"
echo ""
echo "To test it now:"
echo "  $SCRIPT_PATH"
