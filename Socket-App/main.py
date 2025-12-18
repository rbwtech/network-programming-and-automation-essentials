import sys
from PySide6.QtWidgets import QApplication
from ui.chat_window import ChatWindow

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("UDP Chat")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("RBW Room")
    
    # Create and show main window
    window = ChatWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()