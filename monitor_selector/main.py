# Main application file for the Monitor App Selector.
# This will contain the Tkinter UI and main logic.

import tkinter as tk
from tkinter import filedialog, messagebox
import screeninfo
import subprocess
import json
import os

# Import the factory function from our os_specific module
from .os_specific import get_window_mover

CONFIG_FILE = 'config.json'

class ConfigManager:
    @staticmethod
    def load_config():
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    @staticmethod
    def save_config(config):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)

def get_monitor_details():
    """
    Retrieves and returns a list of all connected monitors and their details.
    """
    try:
        monitors = screeninfo.get_monitors()
        return monitors
    except screeninfo.common.ScreenInfoError:
        return []

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Program Launch Monitor Selector")
        self.geometry("500x400") # Increased height for new button

        self.window_mover = get_window_mover()
        self.config = ConfigManager.load_config()
        self.monitors = get_monitor_details()
        self.selected_monitor = tk.IntVar(value=0)
        self.program_path = tk.StringVar()
        self.program_path.trace_add("write", self.on_path_change)

        # --- UI Elements ---
        monitor_frame = tk.LabelFrame(self, text="1. Select Monitor", padx=10, pady=10)
        monitor_frame.pack(padx=10, pady=10, fill="x")

        if not self.monitors:
            tk.Label(monitor_frame, text="No monitors detected.").pack()
        else:
            for i, monitor in enumerate(self.monitors):
                text = f"Monitor {i+1}: {monitor.width}x{monitor.height} ({'Primary' if monitor.is_primary else ''})"
                rb = tk.Radiobutton(monitor_frame, text=text, variable=self.selected_monitor, value=i)
                rb.pack(anchor="w")

        program_frame = tk.LabelFrame(self, text="2. Select Program", padx=10, pady=10)
        program_frame.pack(padx=10, pady=5, fill="x")

        tk.Entry(program_frame, textvariable=self.program_path, width=50).pack(side="left", expand=True, fill="x")
        tk.Button(program_frame, text="Browse...", command=self.browse_file).pack(side="left", padx=5)

        # --- Buttons Frame ---
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=5)

        tk.Button(buttons_frame, text="Save as Default", command=self.save_default).pack(side="left", padx=5)
        tk.Button(buttons_frame, text="Launch Program", command=self.launch_program, bg="lightblue").pack(side="left", padx=5, ipadx=10)


    def on_path_change(self, *args):
        path = self.program_path.get()
        if path in self.config and self.monitors:
            monitor_index = self.config[path]
            if 0 <= monitor_index < len(self.monitors):
                self.selected_monitor.set(monitor_index)

    def browse_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.program_path.set(filepath)

    def save_default(self):
        path = self.program_path.get()
        if not path:
            messagebox.showerror("Error", "Please select a program first.")
            return

        self.config[path] = self.selected_monitor.get()
        ConfigManager.save_config(self.config)
        messagebox.showinfo("Success", f"Default monitor saved for '{path.split('/')[-1]}'.")

    def launch_program(self):
        path = self.program_path.get()
        if not path:
            messagebox.showerror("Error", "Please select a program to launch.")
            return

        if not self.monitors:
            messagebox.showerror("Error", "No monitors available to launch the program on.")
            return

        try:
            selected_mon = self.monitors[self.selected_monitor.get()]
            # Use the os-specific mover
            self.window_mover.move_window_to_monitor(path, selected_mon)

            messagebox.showinfo("Success", f"Program '{path.split('/')[-1]}' would be launched on monitor {self.selected_monitor.get() + 1}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch program: {e}")


if __name__ == "__main__":
    print("Tkinter App structure created. Cannot run mainloop in headless environment.")
