from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                              QTextEdit, QLineEdit, QPushButton, 
                              QLabel, QDialog, QFormLayout, QSpinBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
import random

class ConnectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Connect to Chat")
        self.setModal(True)
        self.setFixedSize(350, 250)
        
        layout = QFormLayout()
        
        # Title
        title = QLabel("UDP Chat Connection")
        title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        layout.addRow(title)
        
        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        layout.addRow("Username:", self.username_input)
        
        # Port input (same port = same chat room)
        self.port_input = QSpinBox()
        self.port_input.setRange(1024, 65535)
        self.port_input.setValue(12345)
        layout.addRow("Chat Room Port:", self.port_input)
        
        # Info label
        info_label = QLabel("Note: Users with the same port number will be in the same chat room.")
        info_label.setStyleSheet("color: #666; font-size: 10px;")
        info_label.setWordWrap(True)
        layout.addRow(info_label)
        
        # Preset chat rooms
        preset_layout = QHBoxLayout()
        self.general_btn = QPushButton("General (12345)")
        self.random_btn = QPushButton("Random Room")
        
        self.general_btn.clicked.connect(lambda: self.port_input.setValue(12345))
        self.random_btn.clicked.connect(lambda: self.port_input.setValue(random.randint(10000, 20000)))
        
        preset_layout.addWidget(self.general_btn)
        preset_layout.addWidget(self.random_btn)
        layout.addRow("Quick Select:", preset_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.connect_btn = QPushButton("Connect")
        self.cancel_btn = QPushButton("Cancel")
        
        self.connect_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.connect_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addRow(button_layout)
        self.setLayout(layout)
        
        # Set focus to username input
        self.username_input.setFocus()
    
    def get_connection_info(self):
        """Get connection information"""
        return {
            "username": self.username_input.text().strip(),
            "host": "localhost",  # Always localhost for UDP broadcast
            "port": self.port_input.value()
        }

class ChatWidget(QWidget):
    message_sent = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Consolas", 10))
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #0a0a0a;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.chat_display)
        
        # Message input area
        input_layout = QHBoxLayout()
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.returnPressed.connect(self.send_message)
        self.message_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 3px;
                padding: 5px;
                font-size: 12px;
            }
        """)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_btn)
        
        layout.addLayout(input_layout)
        self.setLayout(layout)
    
    def send_message(self):
        """Send message"""
        message = self.message_input.text().strip()
        if message:
            self.message_sent.emit(message)
            self.message_input.clear()
    
    def add_message(self, username: str, message: str, timestamp: str):
        """Add message to chat display"""
        if username == "System":
            formatted_msg = f"<span style='color: #666; font-style: italic;'>[{timestamp}] {message}</span>"
        elif username == "You":
            formatted_msg = f"<span style='color: #007acc;'>[{timestamp}] <b>You:</b></span> {message}"
        else:
            formatted_msg = f"<span style='color: #2d8f2d;'>[{timestamp}] <b>{username}:</b></span> {message}"
        
        self.chat_display.append(formatted_msg)
        
        # Auto scroll to bottom
        scrollbar = self.chat_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.clear()
    
    def set_input_enabled(self, enabled: bool):
        """Enable/disable message input"""
        self.message_input.setEnabled(enabled)
        self.send_btn.setEnabled(enabled)