# dialogs/Help_Dialog.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextBrowser, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from app_config.app_config import APP_NAME
from themes.apply_themes import get_dark_qss, get_light_qss
import resources_rc  # your resource file

class HelpDialog(QDialog):
    """Help dialog for Professional Unit Converter"""

    def __init__(self, parent=None, dark_mode=True):
        super().__init__(parent)
        self.dark_mode = dark_mode

        self.setWindowTitle(f"Help – {APP_NAME}")
        self.setFixedSize(460, 360)
        self.setModal(True)
        self.setWindowIcon(QIcon(":/assets/icons/help_icon.png"))

        # Apply theme dynamically
        self.apply_theme()

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        layout.addWidget(self._create_title_label())
        layout.addWidget(self._create_help_text())
        layout.addWidget(self._create_close_button(), alignment=Qt.AlignRight)

        self.setLayout(layout)

    def apply_theme(self):
        """Apply dark or light theme to the dialog"""
        style = get_dark_qss() if self.dark_mode else get_light_qss()
        self.setStyleSheet(style)

    def _create_title_label(self):
        label = QLabel(f"<b>{APP_NAME} – Help Guide</b>")
        label.setAlignment(Qt.AlignCenter)
        label.setTextFormat(Qt.RichText)
        label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        return label

    def _create_help_text(self):
        text = QTextBrowser()
        text.setFont(QFont("Segoe UI", 10))
        text.setOpenExternalLinks(True)
        text.setHtml(f"""
            <html>
            <head>
            <style>
                body {{
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 10pt;
                    color: {'#e0e0e0' if self.dark_mode else '#2b2b2b'};
                    background-color: {'#2b2b2b' if self.dark_mode else '#ffffff'};
                    line-height: 1.5;
                }}
                h2 {{
                    color: {'#88c0d0' if self.dark_mode else '#0055aa'};
                    margin-bottom: 6px;
                }}
                h3 {{
                    color: {'#81a1c1' if self.dark_mode else '#0077cc'};
                    margin-bottom: 4px;
                }}
                p, li {{
                    margin: 4px 0;
                }}
                ul {{
                    margin: 4px 0 8px 20px;
                }}
                .section-title {{
                    font-weight: bold;
                    color: {'#8fbcbb' if self.dark_mode else '#003366'};
                    margin-top: 8px;
                }}
            </style>
            </head>
            <body>
                <h2>{APP_NAME} – Help Guide</h2>

                <h3>Quick Start Guide</h3>
                <ol>
                    <li>Select a conversion type from the dropdown.</li>
                    <li>Enter the value you want to convert.</li>
                    <li>Choose the "From" unit.</li>
                    <li>Choose the "To" unit.</li>
                    <li>Click "Convert" or press Enter.</li>
                </ol>

                <h3>Keyboard Shortcuts</h3>
                <ul>
                    <li><b>Ctrl+N</b> – New Conversion</li>
                    <li><b>Ctrl+S</b> – Save Result</li>
                    <li><b>Ctrl+O</b> – Open History</li>
                    <li><b>Ctrl+E</b> – Export History</li>
                    <li><b>Ctrl+Q</b> – Exit Application</li>
                    <li><b>F1</b> – Help (This dialog)</li>
                    <li><b>Enter</b> – Convert</li>
                    <li><b>Escape</b> – Clear Input / Close Dialog</li>
                </ul>

                <h3>Features</h3>
                <ul>
                    <li>Real-time conversion as you type</li>
                    <li>Dark/Light mode toggle</li>
                    <li>Conversion history tracking</li>
                    <li>Export results to file</li>
                    <li>Professional menu system</li>
                    <li>Status bar with real-time updates</li>
                </ul>

                <h3>Supported Conversions</h3>
                <ul>
                    <li><b>Distance:</b> mm, cm, m, km, miles, yards, feet, inch</li>
                    <li><b>Time:</b> seconds, minutes, hours, days, years, decades, centuries</li>
                    <li><b>Temperature:</b> Celsius, Fahrenheit, Kelvin</li>
                    <li><b>Mass:</b> grams, kilograms, milligrams, pounds, ounces, ton</li>
                    <li><b>Volume:</b> milliliters, centiliters, deciliters, liters, gallons, cups, quarts, pints</li>
                    <li><b>Computer Storage:</b> bytes, kilobytes, megabytes, gigabytes, terabytes</li>
                    <li><b>Power:</b> watts, kilowatts, horsepower, megawatts</li>
                    <li><b>Pressure:</b> pascals, bar, atm, psi, torr</li>
                    <li><b>Energy:</b> joules, kilojoules, calories, kilocalories, watt-hours, kilowatt-hours</li>
                </ul>

                <h3>Tips</h3>
                <ul>
                    <li>Use decimal points for precise conversions</li>
                    <li>Save important results using Ctrl+S</li>
                    <li>Export history for record keeping</li>
                    <li>Switch themes for better visibility</li>
                </ul>
            </body>
            </html>
        """)
        text.setMinimumHeight(200)
        return text

    def _create_close_button(self):
        btn = QPushButton("✖ Close")
        btn.setFixedWidth(100)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setShortcut("Esc")
        btn.clicked.connect(self.accept)
        return btn

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)
