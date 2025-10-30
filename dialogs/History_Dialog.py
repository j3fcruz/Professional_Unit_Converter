from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import json
from datetime import datetime


class HistoryDialog(QDialog):
    """Dialog to show conversion history"""

    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.history = history
        self.setWindowTitle("Conversion History")
        self.setFixedSize(600, 500)
        self.setModal(True)

        layout = QVBoxLayout()
        layout.addWidget(self._create_title())
        layout.addWidget(self._create_history_list())
        layout.addLayout(self._create_buttons())
        self.setLayout(layout)

    def _create_title(self):
        title = QLabel("Conversion History")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        return title

    def _create_history_list(self):
        self.history_list = QListWidget()
        self._populate_history()
        return self.history_list

    def _create_buttons(self):
        layout = QHBoxLayout()

        export_btn = QPushButton("Export to File")
        export_btn.clicked.connect(self._export_history)
        layout.addWidget(export_btn)

        clear_btn = QPushButton("Clear History")
        clear_btn.clicked.connect(self._clear_history)
        layout.addWidget(clear_btn)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        return layout

    def _populate_history(self):
        """Populate the history list"""
        self.history_list.clear()
        for item in self.history:
            timestamp = item.get("timestamp", "Unknown")
            conversion = item.get("formatted", "Unknown conversion")
            conv_type = item.get("type", "Unknown")
            entry = f"[{timestamp}] {conv_type}: {conversion}"
            self.history_list.addItem(QListWidgetItem(entry))

    def _export_history(self):
        """Export history to a JSON file"""
        if not self.history:
            QMessageBox.warning(self, "Warning", "No history to export!")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export History",
            f"conversion_history_{datetime.now().strftime('%Y%m%d')}.json",
            "JSON Files (*.json)"
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.history, f, indent=2, default=str)
                QMessageBox.information(self, "Success", f"History exported to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export history:\n{str(e)}")

    def _clear_history(self):
        """Clear conversion history"""
        confirm = QMessageBox.question(
            self,
            "Clear History",
            "Are you sure you want to clear all conversion history?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.history.clear()
            self._populate_history()
            QMessageBox.information(self, "Success", "History cleared successfully!")
