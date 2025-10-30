# dialogs/About_Dialog.py

"""
About dialog for Professional Unit Converter
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from app_config.app_config import (
    APP_NAME, APP_VERSION, ABOUT_APP, COPYRIGHT, KOFI_ID, DESCRIPTION
)
from themes.apply_themes import get_dark_qss, get_light_qss
import resources_rc


class AboutDialog(QDialog):
    """About dialog for Professional Unit Converter application."""

    def __init__(self, parent=None, dark_mode=True):
        super().__init__(parent)
        self.dark_mode = dark_mode
        self.setWindowTitle(f"About {APP_NAME}")
        self.setFixedSize(460, 480)
        self.setModal(True)
        self.setWindowIcon(QIcon(":/assets/icons/about_icon.png"))

        # Apply theme dynamically
        self.apply_theme()

        self._setup_ui()

    def apply_theme(self):
        """Apply dark or light theme to the dialog"""
        style = get_dark_qss() if self.dark_mode else get_light_qss()
        self.setStyleSheet(style)

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        layout.addWidget(self._create_title_label())
        layout.addWidget(self._create_subtitle_label())
        layout.addWidget(self._create_version_label())
        layout.addWidget(self._create_description_box())
        layout.addWidget(self._create_dev_info_label())
        layout.addWidget(self._create_close_button(), alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def _create_title_label(self):
        label = QLabel(APP_NAME)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 16, QFont.Bold))
        return label

    def _create_subtitle_label(self):
        label = QLabel(ABOUT_APP)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 11))
        return label

    def _create_version_label(self):
        label = QLabel(f"Version: {APP_VERSION}")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 10))
        return label

    def _create_description_box(self):
        text_box = QTextBrowser()
        text_box.setOpenExternalLinks(True)
        text_box.setFont(QFont("Arial", 10))
        text_box.setHtml(self._format_description_html())
        text_box.setMinimumHeight(200)

        # Dynamic background and text color based on theme
        bg_color = "#2b2b2b" if self.dark_mode else "#ffffff"
        text_color = "white" if self.dark_mode else "#2b2b2b"

        text_box.setStyleSheet(f"""
            QTextBrowser {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid #88c0d0;
                padding: 8px;
                border-radius: 6px;
            }}
        """)
        return text_box

    def _format_description_html(self):
        html_desc = DESCRIPTION.replace("\n", "<br>")
        support_color = "orange" if self.dark_mode else "#ff6600"
        return f"""
            <p>{html_desc}</p>
            <p align="center" style="margin-top: 12px;">
                ❤️ Support us on 
                <a href="{KOFI_ID}" 
                   style="color: {support_color}; font-weight: bold; text-decoration: none;" 
                   target="_blank">
                   Ko-fi
                </a>
            </p>
        """

    def _create_dev_info_label(self):
        label = QLabel(COPYRIGHT)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 9))
        return label

    def _create_close_button(self):
        button = QPushButton("Close")
        button.setFixedWidth(100)
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.accept)
        return button

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.accept()
        else:
            super().keyPressEvent(event)
