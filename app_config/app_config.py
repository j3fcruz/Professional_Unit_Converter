from PyQt5.QtGui import QIcon
from dotenv import load_dotenv
import os, sys
import resources_rc  # PyQt5 resources

# Load .env
load_dotenv()

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# Paths / Icons

ICON_PATH = os.getenv("ICON_PATH", "")
ABOUT_ICON_PATH = os.getenv("ABOUT_ICON_PATH", "")
DONATE_ICON_PATH = os.getenv("DONATE_ICON_PATH", "")
HELP_ICON_PATH = os.getenv("HELP_ICON_PATH", "")

APP_NAME = "Professional Unit Converter"
ABOUT_APP = "Professional UI, Fast, and accurate unit conversions"
AUTHOR = "Marco Polo"
APP_DEVELOPER  = "PatronHub"
APP_VERSION = "1.0.0"

MAYA_QR_FILE = os.getenv("MAYA_QR_FILE", "")
COPYRIGHT = f"© 2025 {APP_NAME}. All rights reserved."

# Default donation/GitHub links
MAYA_QR_KEY = os.getenv("MAYA_QR_KEY", "").encode()
GITHUB_ID = os.getenv("GITHUB_ID", "")
KOFI_ID = os.getenv("KOFI_ID", "")
PAYPAL_ID = os.getenv("PAYPAL_ID", "")
BTC_NAME = os.getenv("BTC_NAME", "")
ETH_NAME = os.getenv("ETH_NAME", "")
BTC_ID = os.getenv("BTC_ID", "")
ETH_ID = os.getenv("ETH_ID", "")

DESCRIPTION = f"""{APP_NAME} by {AUTHOR} is a comprehensive desktop utility
designed to make unit conversions fast, accurate, and effortless. 
It combines a professional interface with real-time calculation for 
both casual and advanced users.

Features:

• Convert units across multiple categories: Distance, Time, Temperature, Mass, Volume, Power, Pressure, Energy, and Storage  
• Real-time conversion as you type with numeric precision  
• Multi-unit selection with quick swap between "From" and "To" units  
• Conversion history tracking and export functionality  
• Dark and Light themes for comfortable viewing  
• Minimal, modern interface with menu bar, toolbar, and status bar  
• Save conversion results to JSON files for record keeping  
• Keyboard shortcuts for faster operation  
• Designed for efficiency, accuracy, and professional use
"""
