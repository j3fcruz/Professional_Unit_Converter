# dialogs/Donate_Dialog.py

"""
Donate dialog for supporting the project
"""

import os
import webbrowser
from io import BytesIO
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFrame, QGroupBox, QMessageBox, QApplication
)
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QFile, QIODevice

import qrcode
from cryptography.fernet import Fernet
from app_config.app_config import (
    APP_NAME, MAYA_QR_KEY, MAYA_QR_FILE, PAYPAL_ID, KOFI_ID,
    BTC_ID, ETH_ID, GITHUB_ID
)
from core.crypto_utils import decrypt_fernet
from themes.apply_themes import get_dark_qss, get_light_qss
import resources_rc


def read_qrc_file(path: str) -> bytes:
    """Reads a binary resource file from Qt Resource System."""
    file = QFile(path)
    if not file.open(QIODevice.ReadOnly):
        raise FileNotFoundError(f"Failed to open resource: {path}")
    return bytes(file.readAll())


class DonateDialog(QDialog):
    """Donate dialog for supporting the project."""

    def __init__(self, parent=None, dark_mode=True):
        super().__init__(parent)
        self.dark_mode = dark_mode
        self.setWindowTitle(f"Support {APP_NAME}")
        self.setFixedSize(450, 520)
        self.setModal(True)
        self.setWindowIcon(QIcon(":/assets/icons/donate_icon.png"))

        # Apply theme dynamically
        self.apply_theme()
        self._setup_ui()

    def apply_theme(self):
        style = get_dark_qss() if self.dark_mode else get_light_qss()
        self.setStyleSheet(style)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        header = QLabel(f"<h2 style='margin:0;'>Support {APP_NAME}</h2>")
        header.setAlignment(Qt.AlignCenter)
        header.setTextFormat(Qt.RichText)
        layout.addWidget(header)
        layout.addWidget(self._separator())
        layout.addWidget(self._description_widget())
        layout.addWidget(self._donation_options())

        thanks = QLabel(
            f"Thank you for considering supporting {APP_NAME}! "
            "Every contribution helps us continue development."
        )
        thanks.setWordWrap(True)
        thanks.setStyleSheet("font-style: italic; padding: 10px;")
        layout.addWidget(thanks)
        layout.addLayout(self._footer_buttons())

    def _separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def _description_widget(self):
        desc = QTextEdit()
        desc.setReadOnly(True)
        desc.setMaximumHeight(140)

        bg_color = "#2b2b2b" if self.dark_mode else "#ffffff"
        text_color = "white" if self.dark_mode else "#2b2b2b"

        desc.setHtml(f"""
            <h3>Help Us Improve</h3>
            <p>{APP_NAME} is developed with passion. Your support helps us:</p>
            <ul>
                <li>Continue developing new features</li>
                <li>Maintain compatibility with latest Python versions</li>
                <li>Provide better documentation and support</li>
                <li>Keep the software free and open source</li>
            </ul>
        """)
        desc.setStyleSheet(f"""
            QTextEdit {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid #88c0d0;
                padding: 8px;
                border-radius: 6px;
            }}
        """)
        return desc

    def _donation_options(self):
        group = QGroupBox("Ways to Support")
        layout = QVBoxLayout(group)

        options = [
            ("⭐ Star us on GitHub", "Visit GitHub", lambda: webbrowser.open(GITHUB_ID)),
            ("💰 Donate via PayPal", "Donate", lambda: webbrowser.open(PAYPAL_ID)),
            ("☕ Buy us a coffee", "Ko-fi", lambda: webbrowser.open(KOFI_ID)),
            ("🪙 Cryptocurrency", "Addresses", self._show_crypto_addresses),
            ("📱 Donate via Maya", "Open QR", self._show_maya_qr)
        ]

        for label, btn_text, callback in options:
            layout.addLayout(self._donation_row(label, btn_text, callback))

        return group

    def _donation_row(self, label_text, btn_text, callback):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        label_color = "#88c0d0" if self.dark_mode else "#0078D4"
        label.setStyleSheet(f"font-weight: bold; color: {label_color};")
        button = QPushButton(btn_text)
        button.clicked.connect(callback)
        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(button)
        return layout

    def _footer_buttons(self):
        layout = QHBoxLayout()
        share_btn = QPushButton("Share with Friends")
        share_btn.clicked.connect(self._share_application)
        close_btn = QPushButton("Close")
        close_btn.setFixedWidth(80)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(share_btn)
        layout.addStretch()
        layout.addWidget(close_btn)
        return layout

    def _show_crypto_addresses(self):
        addresses = f"Bitcoin (BTC): {BTC_ID}\nEthereum (ETH): {ETH_ID}"
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Cryptocurrency Addresses")
        msg_box.setText(addresses)
        msg_box.setIcon(QMessageBox.Information)
        copy_btn = QPushButton("Copy All")
        msg_box.addButton(copy_btn, QMessageBox.ActionRole)
        msg_box.addButton(QMessageBox.Ok)
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(addresses))
        msg_box.exec_()

    def _share_application(self):
        share_text = (
            f"Help spread the word about {APP_NAME}!\n"
            "Share on social media, Reddit, Discord, and LinkedIn."
        )
        box = QMessageBox(self)
        box.setWindowTitle(f"Share {APP_NAME}")
        box.setText(share_text)
        box.setIcon(QMessageBox.Information)
        copy_btn = QPushButton("Copy")
        box.addButton(copy_btn, QMessageBox.ActionRole)
        box.addButton(QMessageBox.Ok)
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(share_text))
        box.exec_()

    def _show_maya_qr(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Donate via Maya")
        dialog.setFixedSize(300, 400)
        layout = QVBoxLayout(dialog)

        try:
            encrypted = read_qrc_file(MAYA_QR_FILE)
            link = decrypt_fernet(encrypted, MAYA_QR_KEY)
        except Exception as e:
            layout.addWidget(QLabel(f"Failed to load QR code: {e}"))
            dialog.exec_()
            return

        pixmap = self._generate_qr_pixmap(link, 250)
        label = QLabel()
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        info_label = QLabel(f"Thank you for considering supporting {APP_NAME}.\nEvery contribution helps us continue development.")
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(close_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        dialog.exec_()

    @staticmethod
    def _generate_qr_pixmap(data: str, size: int) -> QPixmap:
        qr = qrcode.QRCode(
            version=1, error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10, border=2
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qimage = QImage.fromData(buffer.getvalue())
        return QPixmap.fromImage(qimage).scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
