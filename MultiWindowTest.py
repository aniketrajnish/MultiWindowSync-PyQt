import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow          

def main():
    '''
    Creates the Image Window Manager that can be used to open the image windows.
    '''
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_()) # For clean exit

main()