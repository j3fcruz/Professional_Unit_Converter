# Professional_Unit_Converter.py

"""
Professional Unit Converter Desktop Application
A comprehensive desktop unit converter with PyQt5 GUI
"""

import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QLineEdit, QLabel, QPushButton, QCheckBox, QGroupBox,
    QSplitter, QListWidget, QScrollArea,
    QFileDialog, QStatusBar, QAction, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QIcon, QDoubleValidator, QKeySequence
from PyQt5.QtCore import Qt, QTimer, QSettings

from core.unit_conversion import UnitConverterCore
from dialogs.About_Dialog import AboutDialog
from dialogs.Help_Dialog import HelpDialog
from dialogs.Donate_Dialog import DonateDialog
from dialogs.History_Dialog import HistoryDialog
from themes.apply_themes import get_dark_qss, get_light_qss
from app_config.app_config import APP_NAME, APP_VERSION, ICON_PATH


class ProfessionalUnitConverter(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()

        # Core converter
        self.converter = UnitConverterCore()
        self.setWindowIcon(QIcon(ICON_PATH))
        # Settings
        self.settings = QSettings("ProfessionalConverter", "UnitConverter")
        self.conversion_history = []

        # UI state
        self.dark_mode = True
        self.current_conversion_type = "Distance"
        self.last_result = None

        # Initialize UI
        self.init_ui()
        self.load_settings()

        # Auto-conversion timer
        self.auto_convert_timer = QTimer()
        self.auto_convert_timer.timeout.connect(self.convert_units)
        self.auto_convert_timer.setSingleShot(True)

        # Load units
        self.populate_units()
        self.input_value.setFocus()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")
        self.resize(900, 700)

        self.create_menu_bar()
        self.create_toolbar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        splitter = QSplitter(Qt.Horizontal)
        self.left_panel = self.create_converter_panel()
        self.right_panel = self.create_info_panel()

        splitter.addWidget(self.left_panel)
        splitter.addWidget(self.right_panel)
        splitter.setSizes([600, 320])

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)

        self.create_status_bar()
        self.apply_theme()

    # -------------------- Menu & Toolbar -------------------- #
    def create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        new_action = QAction("New Conversion", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self.new_conversion)
        file_menu.addAction(new_action)

        save_action = QAction("Save Result", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self.save_result)
        file_menu.addAction(save_action)

        open_history_action = QAction("Open History", self)
        open_history_action.setShortcut(QKeySequence.Open)
        open_history_action.triggered.connect(self.open_history)
        file_menu.addAction(open_history_action)

        export_action = QAction("Export History", self)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        export_action.triggered.connect(self.export_history)
        file_menu.addAction(export_action)

        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("Edit")
        clear_action = QAction("Clear Input", self)
        clear_action.setShortcut(QKeySequence("Escape"))
        clear_action.triggered.connect(self.clear_input)
        edit_menu.addAction(clear_action)

        view_menu = menubar.addMenu("View")
        self.dark_mode_action = QAction("Indigo Dark", self, checkable=True)
        self.dark_mode_action.triggered.connect(lambda: self.toggle_dark_mode(True))
        view_menu.addAction(self.dark_mode_action)

        self.light_mode_action = QAction("Professional Blue", self, checkable=True)
        self.light_mode_action.triggered.connect(lambda: self.toggle_dark_mode(False))
        view_menu.addAction(self.light_mode_action)

        help_menu = menubar.addMenu("Help")
        help_action = QAction("Help", self)
        help_action.setShortcut(QKeySequence.HelpContents)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        donate_action = QAction("Donate", self)
        donate_action.triggered.connect(self.show_donate)
        help_menu.addAction(donate_action)

    def create_toolbar(self):
        toolbar = self.addToolBar("Main")
        toolbar.setMovable(False)

        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.setToolTip("New Conversion")
        new_action.triggered.connect(self.new_conversion)
        toolbar.addAction(new_action)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.setToolTip("Save Result (Ctrl+S)")
        save_action.triggered.connect(self.save_result)
        toolbar.addAction(save_action)

        toolbar.addSeparator()

        convert_action = QAction("Convert", self)
        convert_action.setToolTip("Convert Units (Enter)")
        convert_action.triggered.connect(self.convert_units)
        toolbar.addAction(convert_action)

        toolbar.addSeparator()

        toggle_panel_action = QAction("Info Panel", self, checkable=True)
        toggle_panel_action.setToolTip("Show/Hide Info Panel")
        toggle_panel_action.setChecked(True)
        toggle_panel_action.triggered.connect(self.toggle_right_panel)
        self.toolbar_panel_action = toggle_panel_action
        toolbar.addAction(toggle_panel_action)
        toolbar.addSeparator()

        dark_action = QAction("Switch Theme", self, checkable=True)
        dark_action.setToolTip("Switch Theme")
        dark_action.triggered.connect(self.toggle_dark_mode)
        self.dark_mode_toolbar_action = dark_action
        toolbar.addAction(dark_action)

    # -------------------- Panels -------------------- #
    def create_converter_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        group = QGroupBox("Unit Conversion")
        group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        group.setMaximumHeight(300)
        form_layout = QVBoxLayout()

        self.conversion_type_combo = QComboBox()
        self.conversion_type_combo.addItems(sorted(self.converter.unit_mappings.keys()))
        self.conversion_type_combo.currentTextChanged.connect(self.on_conversion_type_changed)
        form_layout.addWidget(QLabel("Conversion Type:"))
        form_layout.addWidget(self.conversion_type_combo)

        self.input_value = QLineEdit()
        self.input_value.setPlaceholderText("Enter value")
        validator = QDoubleValidator(bottom=-1e308, top=1e308, decimals=10)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.input_value.setValidator(validator)
        self.input_value.textChanged.connect(self.on_input_changed)
        self.input_value.returnPressed.connect(self.convert_units)
        form_layout.addWidget(QLabel("From:"))
        form_layout.addWidget(self.input_value)

        self.from_unit_combo = QComboBox()
        self.from_unit_combo.currentTextChanged.connect(self.on_unit_changed)
        form_layout.addWidget(self.from_unit_combo)

        self.to_unit_combo = QComboBox()
        self.to_unit_combo.currentTextChanged.connect(self.on_unit_changed)
        form_layout.addWidget(QLabel("To:"))
        form_layout.addWidget(self.to_unit_combo)

        self.result_label = QLabel("0")
        self.result_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.result_label)

        group.setLayout(form_layout)
        layout.addWidget(group)

        btn_layout = QHBoxLayout()
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_input)
        save_btn = QPushButton("Save Result")
        save_btn.clicked.connect(self.save_result)
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

        return panel

    def create_info_panel(self):
        panel = QWidget()
        panel.setFixedWidth(320)
        layout = QVBoxLayout(panel)

        recent_group = QGroupBox("Recent Conversions")
        recent_layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.recent_list = QListWidget()
        scroll_area.setWidget(self.recent_list)
        recent_layout.addWidget(scroll_area)
        recent_group.setLayout(recent_layout)
        layout.addWidget(recent_group)

        settings_group = QGroupBox("Settings")
        settings_layout = QVBoxLayout()
        self.dark_mode_check = QCheckBox("Switch Theme")
        self.dark_mode_check.toggled.connect(self.toggle_dark_mode)
        self.auto_convert_check = QCheckBox("Auto Convert")
        self.auto_convert_check.setChecked(True)
        settings_layout.addWidget(self.dark_mode_check)
        settings_layout.addWidget(self.auto_convert_check)
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        layout.addStretch()
        return panel

    # -------------------- Right Panel Toggle -------------------- #
    def toggle_right_panel(self, visible=None):
        if visible is None:
            visible = not self.right_panel.isVisible()
        self.right_panel.setVisible(visible)
        self.toolbar_panel_action.setText("Hide Panel" if visible else "Show Panel")

    # -------------------- Status Bar -------------------- #
    def create_status_bar(self):
        """Initialize dynamic status bar with live status and clock"""
        status_bar = self.statusBar()

        # Left: dynamic status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        status_bar.addWidget(self.status_label, 1)

        # Right: live clock
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        status_bar.addPermanentWidget(self.time_label)

        # Timer to update clock every second
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)
        self.update_status()

    def update_status(self):
        """Update only the clock part of the status bar"""
        self.time_label.setText(datetime.now().strftime("%H:%M:%S"))

    def set_status(self, message: str):
        """Update the left status message dynamically"""
        self.status_label.setText(message)

        # -------------------- Unit Conversion -------------------- #

    def populate_units(self):
        units = self.converter.get_units_for_type(self.current_conversion_type)
        self.from_unit_combo.clear()
        self.to_unit_combo.clear()
        self.from_unit_combo.addItems(units)
        self.to_unit_combo.addItems(units)
        if len(units) > 1:
            self.from_unit_combo.setCurrentIndex(0)
            self.to_unit_combo.setCurrentIndex(1)

    def on_conversion_type_changed(self, conversion_type):
        self.current_conversion_type = conversion_type
        self.populate_units()
        self.clear_result()
        self.set_status(f"[Status] Conversion type changed to {conversion_type}...")

    def on_input_changed(self, text):
        self.set_status("[Status] Typing input...")
        if self.auto_convert_check.isChecked() and text.strip():
            self.auto_convert_timer.start(500)

    def on_unit_changed(self):
        self.set_status("[Status] Unit changed...")
        if self.auto_convert_check.isChecked():
            self.auto_convert_timer.start(300)

    def convert_units(self):
        value = self.input_value.text().strip()
        from_unit = self.from_unit_combo.currentText()
        to_unit = self.to_unit_combo.currentText()
        if not value or not from_unit or not to_unit:
            self.result_label.setText("0")
            self.set_status("[Status] Waiting for input...")
            return
        try:
            self.set_status("[Status] Converting...")
            numeric_value = float(value)
            result = self.converter.convert_units(numeric_value, from_unit, to_unit, self.current_conversion_type)
            numeric_result = float(result.get('result', 0))
            self.result_label.setText(f"{numeric_result:,.4f}")
            self.last_result = result
            self.add_to_history(result)
            self.set_status(f"[Status] Conversion complete: {result['formatted']}")
        except Exception as e:
            self.result_label.setText("0")
            self.set_status(f"[Status] Error: {str(e)}")

    def add_to_history(self, result):
        item = {
            'formatted': result['formatted'],
            'type': self.current_conversion_type,
            'timestamp': datetime.now().strftime("%H:%M:%S"),
        }
        self.conversion_history.insert(0, item)
        if len(self.conversion_history) > 20:
            self.conversion_history = self.conversion_history[:20]
        self.update_recent_list()

    def update_recent_list(self):
        self.recent_list.clear()
        for item in self.conversion_history[:5]:
            self.recent_list.addItem(f"[{item['timestamp']}] {item['formatted']}")

    def clear_result(self):
        self.result_label.setText("Enter values to see result")
        self.set_status("[Status] Result cleared...")

        # -------------------- Actions -------------------- #

    def new_conversion(self):
        self.input_value.clear()
        self.clear_result()
        self.set_status("[Status] New conversion started...")

    def clear_input(self):
        self.input_value.clear()
        self.clear_result()
        self.set_status("[Status] Input cleared...")

    def save_result(self):
        if not self.last_result:
            QMessageBox.warning(self, "Warning", "No result to save!")
            self.set_status("[Status] Save failed: no result")
            return
        os.makedirs('results', exist_ok=True)
        filename = f"results/conversion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump({'timestamp': datetime.now().isoformat(),
                       'conversion_type': self.current_conversion_type,
                       'result': self.last_result}, f, indent=2)
        QMessageBox.information(self, "Success", f"Result saved to {filename}")
        self.set_status(f"[Status] Result saved to {filename}")

    def open_history(self):
        HistoryDialog(self.conversion_history, self).exec_()
        self.set_status("[Status] History dialog opened...")

    def export_history(self):
        if not self.conversion_history:
            QMessageBox.warning(self, "Warning", "No history to export!")
            self.set_status("[Status] Export failed: no history")
            return
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export History",
            f"conversion_history_{datetime.now().strftime('%Y%m%d')}.json",
            "JSON Files (*.json)"
        )
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.conversion_history, f, indent=2, default=str)
            QMessageBox.information(self, "Success", f"History exported to {filename}")
            self.set_status(f"[Status] History exported to {filename}")

    def swap_units(self):
        from_index = self.from_unit_combo.currentIndex()
        to_index = self.to_unit_combo.currentIndex()
        self.from_unit_combo.setCurrentIndex(to_index)
        self.to_unit_combo.setCurrentIndex(from_index)
        self.set_status("[Status] Units swapped...")

        # -------------------- Themes -------------------- #

    def toggle_dark_mode(self, theme=None):
        if theme is None:
            self.dark_mode = not self.dark_mode
        else:
            self.dark_mode = theme

        self.dark_mode_check.setChecked(self.dark_mode)
        self.dark_mode_action.setChecked(self.dark_mode)
        self.light_mode_action.setChecked(not self.dark_mode)
        self.dark_mode_toolbar_action.setChecked(self.dark_mode)

        # Update toolbar label dynamically
        if self.dark_mode:
            self.dark_mode_toolbar_action.setText("Indigo Dark")  # or "Dark Blue"
            self.dark_mode_check.setText("Indigo Dark")  # or "Dark Blue"
        else:
            self.dark_mode_toolbar_action.setText("Indigo Blue")  # optional for clarity
            self.dark_mode_check.setText("Indigo Blue")  # or "Dark Blue"

        style = get_dark_qss() if self.dark_mode else get_light_qss()
        self.setStyleSheet(style)
        self.set_status(f"[Status] Theme set to {'Indigo Dark' if self.dark_mode else 'Indigo Blue'}")

    def apply_theme(self):
        style = get_dark_qss() if self.dark_mode else get_light_qss()
        self.setStyleSheet(style)

        # -------------------- Dialogs -------------------- #

    def show_help(self):
        HelpDialog(parent=self, dark_mode=self.dark_mode).exec_()
        self.set_status("[Status] Help dialog opened...")

    def show_about(self):
        AboutDialog(parent=self, dark_mode=self.dark_mode).exec_()
        self.set_status("[Status] About dialog opened...")

    def show_donate(self):
        DonateDialog(parent=self, dark_mode=self.dark_mode).exec_()
        self.set_status("[Status] Donate dialog opened...")

        # -------------------- Settings -------------------- #

    def load_settings(self):
        self.dark_mode = self.settings.value("dark_mode", False, type=bool)
        self.toggle_dark_mode(self.dark_mode)
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        history_data = self.settings.value("conversion_history", [])
        if history_data:
            self.conversion_history = history_data
            self.update_recent_list()

    def save_settings(self):
        self.settings.setValue("dark_mode", self.dark_mode)
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("conversion_history", self.conversion_history)

        # -------------------- Close Event -------------------- #

    def closeEvent(self, event):
        self.save_settings()
        reply = QMessageBox.question(self, "Confirm Exit",
                                     "Do you really want to quit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
