#!/bin/bash
# Setup script for system tray proxy toggle
# Installs required packages for pystray to work on Ubuntu

set -e

echo "Installing required system packages for system tray support..."

# Update package list
sudo apt update

# Install required packages
sudo apt install -y \
    gir1.2-ayatanaappindicator3-0.1 \
    python3-gi \
    python3-gi-cairo \
    gir1.2-gtk-3.0

# Install Python dependencies
pip3 install --break-system-packages pystray pillow

echo ""
echo "Installation complete!"
echo ""
echo "To run the system tray version:"
echo "  ./proxy-toggle-tray.py"
echo ""
echo "To add to startup (optional):"
echo "  mkdir -p ~/.config/autostart"
echo "  cat > ~/.config/autostart/proxy-toggle.desktop << EOF"
echo "  [Desktop Entry]"
echo "  Name=Proxy Toggle"
echo "  Comment=System tray proxy toggle"
echo "  Exec=$(pwd)/proxy-toggle-tray.py"
echo "  Icon=network-workgroup"
echo "  Terminal=false"
echo "  Type=Application"
echo "  Categories=Utility;Network;"
echo "  EOF"
