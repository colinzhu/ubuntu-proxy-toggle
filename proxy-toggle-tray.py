#!/usr/bin/env python3
"""
System tray app to toggle system proxy on Ubuntu
Requires: gir1.2-ayatanaappindicator3-0.1 python3-gi python3-gi-cairo gir1.2-gtk-3.0
"""
import subprocess
import pystray
from PIL import Image, ImageDraw
import threading
import sys
import time

def get_proxy_status():
    """Check if proxy is enabled via gsettings"""
    try:
        result = subprocess.run(
            ['gsettings', 'get', 'org.gnome.system.proxy', 'mode'],
            capture_output=True, text=True, check=True
        )
        mode = result.stdout.strip().strip("'")
        return mode == 'manual'
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def toggle_proxy():
    """Toggle proxy on/off"""
    try:
        enabled = get_proxy_status()
        new_mode = 'manual' if not enabled else 'none'
        
        subprocess.run(
            ['gsettings', 'set', 'org.gnome.system.proxy', 'mode', new_mode],
            check=True
        )
        
        return True
    except Exception:
        return False

def create_icon(enabled):
    """Create a tray icon image"""
    # Create a simple 64x64 image
    image = Image.new('RGB', (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Draw a circle indicating status
    color = (0, 200, 0) if enabled else (200, 0, 0)  # Green for ON, Red for OFF
    draw.ellipse([16, 16, 48, 48], fill=color, outline=(0, 0, 0), width=2)
    
    return image

def on_clicked(icon, item):
    """Handle menu item click"""
    if str(item) == "Toggle Proxy":
        toggle_proxy()
        # Update the icon to reflect new status
        enabled = get_proxy_status()
        icon.icon = create_icon(enabled)
        # Update menu to show new status
        icon.menu = create_menu()

def on_exit(icon, item):
    """Handle exit"""
    icon.stop()
    sys.exit(0)

def create_menu():
    """Create the menu with current status"""
    enabled = get_proxy_status()
    status = "ON" if enabled else "OFF"
    
    return pystray.Menu(
        pystray.MenuItem(f"Proxy: {status}", lambda: None, enabled=False),
        pystray.MenuItem("Toggle Proxy", on_clicked),
        pystray.MenuItem("Exit", on_exit)
    )

def status_checker(icon):
    """Background thread to periodically check proxy status"""
    last_status = None
    while True:
        time.sleep(1)  # Check every second
        enabled = get_proxy_status()
        if enabled != last_status:
            last_status = enabled
            # Update icon and menu
            icon.icon = create_icon(enabled)
            icon.menu = create_menu()

def main():
    # Initial status
    enabled = get_proxy_status()
    
    # Create icon
    icon = pystray.Icon("proxy-toggle", create_icon(enabled), "Proxy Toggle", create_menu())
    
    # Start background thread to check status periodically
    checker_thread = threading.Thread(target=status_checker, args=(icon,), daemon=True)
    checker_thread.start()
    
    # Run the icon (this blocks until stopped)
    icon.run()

if __name__ == "__main__":
    main()
