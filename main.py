#main.py

import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import ProfessionalUnitConverter

# -------------------- Main -------------------- #
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Professional Unit Converter")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Professional Converter")
    window = ProfessionalUnitConverter()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()