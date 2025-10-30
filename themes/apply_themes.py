# themes/apply_themes.py

from PyQt5.QtCore import QFile, QTextStream
import resources_rc  # compiled from your .qrc

def load_qss_from_rc(path_in_rc):
    """Load QSS from Qt Resource file"""
    file = QFile(path_in_rc)
    if not file.open(QFile.ReadOnly | QFile.Text):
        raise FileNotFoundError(f"Cannot load QSS: {path_in_rc}")
    stream = QTextStream(file)
    return stream.readAll()

def get_dark_qss():
    return load_qss_from_rc(":/assets/themes/get_dark.qss")

def get_light_qss():
    return load_qss_from_rc(":/assets/themes/get_light.qss")
