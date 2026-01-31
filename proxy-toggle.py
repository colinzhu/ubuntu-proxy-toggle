#!/usr/bin/env python3
"""
Simple GUI app to toggle system proxy on Ubuntu
"""
import tkinter as tk
from tkinter import messagebox
import subprocess
import os

class ProxyToggleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proxy Toggle")
        self.root.geometry("300x150")
        self.root.resizable(False, False)
        
        # Create UI
        self.label = tk.Label(root, text="System Proxy Status", font=("Arial", 12, "bold"))
        self.label.pack(pady=10)
        
        self.status_label = tk.Label(root, text="Checking...", font=("Arial", 14))
        self.status_label.pack(pady=5)
        
        self.toggle_btn = tk.Button(root, text="Toggle Proxy", command=self.toggle_proxy, 
                                   font=("Arial", 11), bg="#4CAF50", fg="white", height=2)
        self.toggle_btn.pack(pady=10, padx=20, fill=tk.X)
        
        # Check current proxy status and update periodically
        self.update_status()
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
        status = "ENABLED" if enabled else "DISABLED"
        self.status_label.config(text=status, fg="#4CAF50" if enabled else "#F44336")
    
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
