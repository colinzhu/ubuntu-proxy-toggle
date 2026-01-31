#!/usr/bin/env python3
"""
Simple GUI app to toggle system proxy on Ubuntu
Opens a small window that stays on top for quick access
"""
import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class ProxyToggleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proxy Toggle")
        self.root.geometry("200x100")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)  # Keep window on top
        
        # Create UI
        self.status_label = tk.Label(root, text="Checking...", font=("Arial", 14, "bold"))
        self.status_label.pack(pady=10)
        
        self.toggle_btn = tk.Button(root, text="Toggle", command=self.toggle_proxy, 
                                   font=("Arial", 11), bg="#4CAF50", fg="white", height=1)
        self.toggle_btn.pack(pady=5, padx=10, fill=tk.X)
        
        # Check current proxy status
        self.update_status()
        
        # Update status periodically
        self.root.after(1000, self.update_status)
    
    def get_proxy_status(self):
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
    
    def update_status(self):
        """Update the status display"""
        enabled = self.get_proxy_status()
        status = "ON" if enabled else "OFF"
        color = "#4CAF50" if enabled else "#F44336"
        self.status_label.config(text=f"Proxy: {status}", fg=color)
        self.root.after(1000, self.update_status)
    
    def toggle_proxy(self):
        """Toggle proxy on/off"""
        try:
            enabled = self.get_proxy_status()
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
            
            self.update_status()
            
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to toggle proxy: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProxyToggleApp(root)
    root.mainloop()
