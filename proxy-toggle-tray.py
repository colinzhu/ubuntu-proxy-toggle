#!/usr/bin/env python3
"""
System tray app to toggle system proxy on Ubuntu
Requires: gir1.2-ayatanaappindicator3-0.1 python3-gi python3-gi-cairo gir1.2-gtk-3.0
"""
import subprocess
import pystray
from PIL import Image, ImageDraw
import threading

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
        
        # Also update the http/https/ftp/socks modes
        if new_mode == 'manual':
            # Set default proxy settings if enabling
            subprocess.run([
                'gsettings', 'set', 'org.gnome.system.proxy.http', 'host', "'127.0.0.1'"
            ], check=True)
            subprocess.run([
                'gsettings', 'set', 'org.gnome.system.proxy.http', 'port', '8080'
            ], check=True)
            subprocess.run([
                'gsettings', 'set', 'org.gnome.system.proxy.https', 'host', "'127.0.0.1'"
            ], check=True)
            subprocess.run([
                'gsettings', 'set', 'org.gnome.system.proxy.https', 'port', '8080'
            ], check=True)
        
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

def create_menu():
    """Create the menu with current status"""
    enabled = get_proxy_status()
    status = "ON" if enabled else "OFF"
    
    return pystray.Menu(
        pystray.MenuItem(f"Proxy: {status}", lambda: None, enabled=False),
        pystray.MenuItem("Toggle Proxy", on_clicked),
        pystray.MenuItem("Exit", lambda icon, item: icon.stop())
    )

def main():
    # Initial status
    enabled = get_proxy_status()
    
    # Create icon
    icon = pystray.Icon("proxy-toggle", create_icon(enabled), "Proxy Toggle", create_menu())
    
    # Run in a separate thread to avoid blocking
    threading.Thread(target=icon.run, daemon=True).start()
    
    # Keep main thread alive
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        icon.stop()

if __name__ == "__main__":
    main()
