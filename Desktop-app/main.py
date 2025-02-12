import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from login import LoginWindow


#========== main function==========#
def main():
    app = QApplication(sys.argv)
    style_file = os.path.join(os.path.dirname(__file__), "style.qss")
    if os.path.exists(style_file):
        with open(style_file, "r") as file:
            app.setStyleSheet(file.read())
    
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

#========== run main function==========#
if __name__ == '__main__':
    main()  