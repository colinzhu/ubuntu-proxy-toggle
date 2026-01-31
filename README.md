# Ubuntu Proxy Toggle

A simple GUI app to quickly toggle system proxy on Ubuntu without going through Settings → Network.

## Features

- Toggle proxy on/off with a single click
- Real-time status display
- Works with Ubuntu's built-in proxy settings (gsettings)
- Default proxy: 127.0.0.1:8080 (adjust in code if needed)

## Requirements

- Ubuntu with GNOME desktop
- Python 3
- tkinter (usually pre-installed)

## Installation

```bash
# Make executable
chmod +x proxy-toggle.py

# Run directly
./proxy-toggle.py

# Or add to your PATH for quick access
sudo cp proxy-toggle.py /usr/local/bin/proxy-toggle
sudo chmod +x /usr/local/bin/proxy-toggle
```

## Usage

```bash
# Run the app
./proxy-toggle.py

# Or from anywhere if installed to PATH
proxy-toggle
```

## Customization

Edit `proxy-toggle.py` to change:
- Default proxy host/port (lines 68-76)
- Window size (line 18)
- Colors and styling

## Desktop Integration

Create a desktop shortcut for even faster access:

```bash
cat > ~/.local/share/applications/proxy-toggle.desktop << EOF
[Desktop Entry]
Name=Proxy Toggle
Comment=Quick toggle system proxy
Exec=/path/to/proxy-toggle.py
Icon=network-workgroup
Terminal=false
Type=Application
Categories=Utility;Network;
EOF
```
