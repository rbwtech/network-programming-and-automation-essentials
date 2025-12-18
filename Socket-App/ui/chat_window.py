from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                              QWidget, QPushButton, QLabel, QStatusBar,
                              QMenuBar, QMessageBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction
import time

from ui.components import ChatWidget, ConnectionDialog
from network.udp_client import UDPClient
from network.message_handler import MessageHandler

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.udp_client = UDPClient()
        self.message_handler = MessageHandler()
        self.setup_ui()
        self.setup_connections()
        
        # Connection state
        self.is_connected = False
        self.current_username = ""
    
    def setup_ui(self):
        """Setup main UI"""
        self.setWindowTitle("UDP Chat - RBW Room")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Status bar at top
        self.status_label = QLabel("Not connected")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        layout.addWidget(self.status_label)
        
        # Chat widget
        self.chat_widget = ChatWidget()
        self.chat_widget.set_input_enabled(False)
        layout.addWidget(self.chat_widget)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.connect_btn = QPushButton("Connect")
        self.disconnect_btn = QPushButton("Disconnect")
        self.clear_btn = QPushButton("Clear Chat")
        
        self.disconnect_btn.setEnabled(False)
        
        button_layout.addWidget(self.connect_btn)
        button_layout.addWidget(self.disconnect_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        central_widget.setLayout(layout)
        
        # Setup menu bar
        self.setup_menu()
        
        # Setup status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Chat menu
        chat_menu = menubar.addMenu("Chat")
        
        connect_action = QAction("Connect", self)
        connect_action.triggered.connect(self.show_connection_dialog)
        chat_menu.addAction(connect_action)
        
        disconnect_action = QAction("Disconnect", self)
        disconnect_action.triggered.connect(self.disconnect_from_chat)
        chat_menu.addAction(disconnect_action)
        
        clear_action = QAction("Clear Chat", self)
        clear_action.triggered.connect(self.clear_chat)
        chat_menu.addAction(clear_action)
    
    def setup_connections(self):
        """Setup signal connections"""
        # Button connections
        self.connect_btn.clicked.connect(self.show_connection_dialog)
        self.disconnect_btn.clicked.connect(self.disconnect_from_chat)
        self.clear_btn.clicked.connect(self.clear_chat)
        
        # Chat widget connections
        self.chat_widget.message_sent.connect(self.send_message)
        
        # UDP client connections
        self.udp_client.message_received.connect(self.on_message_received)
        self.udp_client.connection_status.connect(self.on_connection_status)
    
    def show_connection_dialog(self):
        """Show connection dialog"""
        if self.is_connected:
            return
        
        dialog = ConnectionDialog(self)
        if dialog.exec() == ConnectionDialog.Accepted:
            conn_info = dialog.get_connection_info()
            
            if not conn_info["username"]:
                QMessageBox.warning(self, "Error", "Username cannot be empty!")
                return
            
            self.connect_to_chat(conn_info)
    
    def connect_to_chat(self, conn_info):
        """Connect to chat"""
        self.current_username = conn_info["username"]
        
        success = self.udp_client.start_client(
            conn_info["username"],
            conn_info["host"],
            conn_info["port"]
        )
        
        if success:
            self.status_bar.showMessage(f"Connecting as {conn_info['username']}...")
    
    def disconnect_from_chat(self):
        """Disconnect from chat"""
        if self.is_connected:
            self.udp_client.stop_client()
    
    def send_message(self, message):
        """Send message via UDP"""
        if self.is_connected:
            success = self.udp_client.send_message(message)
            if success:
                # Add own message to display
                timestamp = time.strftime("%H:%M:%S")
                self.chat_widget.add_message("You", message, timestamp)
                self.message_handler.add_message("You", message, timestamp)
            else:
                self.status_bar.showMessage("Failed to send message", 3000)
    
    def on_message_received(self, username, message, timestamp):
        """Handle received message"""
        self.chat_widget.add_message(username, message, timestamp)
        self.message_handler.add_message(username, message, timestamp, username == "System")
    
    def on_connection_status(self, connected, status_message):
        """Handle connection status change"""
        self.is_connected = connected
        
        if connected:
            self.status_label.setText(f"Connected: {status_message}")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
            self.chat_widget.set_input_enabled(True)
            self.status_bar.showMessage("Connected and ready to chat")
        else:
            self.status_label.setText("Not connected")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
            self.chat_widget.set_input_enabled(False)
            self.status_bar.showMessage(status_message)
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_widget.clear_chat()
        self.message_handler.clear_messages()
        self.status_bar.showMessage("Chat cleared")
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.is_connected:
            self.udp_client.stop_client()
        event.accept()