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

ICON_PATH = ":/assets/icons/icon.png"

APP_NAME = "Professional Unit Converter"
ABOUT_APP = "Professional UI, Fast, and accurate unit conversions"
AUTHOR = "Marco Polo"
APP_DEVELOPER  = "PatronHub"
APP_VERSION = "1.0.0"

MAYA_QR_FILE = ":/assets/resources/maya_qr.bin"
COPYRIGHT = f"© 2025 {APP_NAME}. All rights reserved."

# Default donation/GitHub links
MAYA_QR_KEY = b'KqTen1MmkOycHJp5HqBkcaCWZ7Be8p-ClzSf9srKm3c='
GITHUB_ID = "https://github.com/j3fcruz"
KOFI_ID = "https://ko-fi.com/marcopolo55681"
PAYPAL_ID = "https://paypal.me/jofreydelacruz13"
BTC_NAME = "Bitcoin (BTC) Address"
ETH_NAME = "Ethereum (ETH) Address"
BTC_ID = "1BcWJT8gBdZSPwS8UY39X9u4Afu1nZSzqk"
ETH_ID = "0xcd5eef32ff4854e4cefa13cb308b727433505bf4"

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
