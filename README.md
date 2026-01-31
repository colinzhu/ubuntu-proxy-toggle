# Ubuntu Proxy Toggle

A simple GUI app to quickly toggle system proxy on Ubuntu without going through Settings → Network.

## Features

- Toggle proxy on/off with a single click
- Real-time status display
- Works with Ubuntu's built-in proxy settings (gsettings)

## Versions

### 1. Window Version (`proxy-toggle.py`)
- Simple GUI window that stays on top
- No additional packages required
- Works out of the box

### 2. System Tray Version (`proxy-toggle-tray.py`)
- Runs in the Ubuntu status bar
- Click icon in tray to toggle
- Requires additional system packages (see setup-tray.sh)

## Requirements

- Ubuntu with GNOME desktop
- Python 3
- tkinter (usually pre-installed)

## Installation

### Window Version (Recommended - works immediately)
```bash
chmod +x proxy-toggle.py
./proxy-toggle.py
```

### System Tray Version (Requires setup)
```bash
# Run the setup script
./setup-tray.sh

# Then run the tray version
./proxy-toggle-tray.py
```

## Usage

```bash
# Window version (stays on top)
./proxy-toggle.py

# System tray version (in status bar)
./proxy-toggle-tray.py
```

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

For system tray version, replace the Exec path with `proxy-toggle-tray.py`.

## Auto-start on Login

```bash
./enable-autostart.sh
```

This will create a desktop entry that auto-starts the tray version when you log in.

To disable auto-start:
```bash
rm ~/.config/autostart/proxy-toggle.desktop
```
