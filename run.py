#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script is the main entry point for the application,
especially for packaging with PyInstaller.
"""

from monitor_selector.main import App

def main():
    """
    Initializes and runs the Tkinter application.
    """
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()
