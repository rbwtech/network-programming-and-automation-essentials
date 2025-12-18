import socket
import threading
from PySide6.QtCore import QObject, Signal
import json
import time

class UDPClient(QObject):
    message_received = Signal(str, str, str)  # username, message, timestamp
    connection_status = Signal(bool, str)  # connected, status_message
    
    def __init__(self):
        super().__init__()
        self.socket = None
        self.username = ""
        self.local_port = 0
        self.target_host = "localhost"
        self.target_port = 12345
        self.running = False
        self.connected_peers = set()
        
    def start_client(self, username, host="localhost", port=12345):
        """Start UDP client"""
        self.username = username
        self.target_host = host
        self.target_port = port
        
        try:
            # Create UDP socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind to a specific port for this chat room
            # Everyone in the same chat room uses the same port
            self.socket.bind(('', port))
            self.local_port = port
            self.running = True
            
            print(f"UDP Client started on port {port}")
            
            # Start listening thread
            listen_thread = threading.Thread(target=self._listen_for_messages)
            listen_thread.daemon = True
            listen_thread.start()
            
            # Send join announcement
            self.send_system_message("join")
            
            self.connection_status.emit(True, f"Connected as {username} on port {port}")
            return True
            
        except OSError as e:
            error_msg = f"Port {port} already in use. Try a different port or close other instances."
            self.connection_status.emit(False, error_msg)
            return False
        except Exception as e:
            self.connection_status.emit(False, f"Failed to start: {str(e)}")
            return False
    
    def stop_client(self):
        """Stop UDP client"""
        if self.running:
            # Send leave message before stopping
            self.send_system_message("leave")
            time.sleep(0.1)  # Give time for message to be sent
            
            self.running = False
            
            if self.socket:
                self.socket.close()
            
            self.connection_status.emit(False, "Disconnected")
    
    def send_message(self, message):
        """Send chat message"""
        if not self.running or not self.socket:
            return False
        
        try:
            data = {
                "type": "message",
                "username": self.username,
                "message": message,
                "timestamp": time.strftime("%H:%M:%S"),
                "sender_port": self.local_port
            }
            
            self._broadcast_message(data)
            return True
            
        except Exception as e:
            print(f"Send error: {e}")
            return False
    
    def send_system_message(self, msg_type):
        """Send system message (join/leave)"""
        if not self.socket:
            return
        
        try:
            data = {
                "type": msg_type,
                "username": self.username,
                "timestamp": time.strftime("%H:%M:%S"),
                "sender_port": self.local_port
            }
            
            self._broadcast_message(data)
            
        except Exception as e:
            print(f"System message error: {e}")
    
    def _broadcast_message(self, data):
        """Broadcast message to broadcast address"""
        try:
            message = json.dumps(data).encode('utf-8')
            
            # Send to broadcast address
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
            # Calculate broadcast address for local network
            broadcast_addr = '255.255.255.255'  # Limited broadcast
            self.socket.sendto(message, (broadcast_addr, self.target_port))
            
            # Also send to localhost for testing
            if self.target_host != 'localhost':
                self.socket.sendto(message, ('127.0.0.1', self.target_port))
                
        except Exception as e:
            print(f"Broadcast error: {e}")
    
    def _listen_for_messages(self):
        """Listen for incoming UDP messages"""
        self.socket.settimeout(1.0)  # 1 second timeout
        
        while self.running:
            try:
                data, addr = self.socket.recvfrom(1024)
                
                try:
                    message_data = json.loads(data.decode('utf-8'))
                    self._handle_received_message(message_data, addr)
                except json.JSONDecodeError:
                    print(f"Invalid JSON received from {addr}")
                except UnicodeDecodeError:
                    print(f"Invalid encoding received from {addr}")
                    
            except socket.timeout:
                # Timeout is normal, just continue
                continue
            except OSError as e:
                # Socket closed or other OS error
                if self.running:
                    print(f"Socket error: {e}")
                break
            except Exception as e:
                if self.running:
                    print(f"Listen error: {e}")
                break
    
    def _handle_received_message(self, data, addr):
        """Handle received message"""
        msg_type = data.get("type", "")
        username = data.get("username", "Unknown")
        timestamp = data.get("timestamp", time.strftime("%H:%M:%S"))
        sender_port = data.get("sender_port", 0)
        
        # Ignore messages from self (same username and port)
        if username == self.username and sender_port == self.local_port:
            return
        
        if msg_type == "message":
            message = data.get("message", "")
            self.message_received.emit(username, message, timestamp)
            
        elif msg_type == "join":
            self.connected_peers.add(addr)
            self.message_received.emit("System", f"{username} joined the chat", timestamp)
            
        elif msg_type == "leave":
            self.connected_peers.discard(addr)
            self.message_received.emit("System", f"{username} left the chat", timestamp)