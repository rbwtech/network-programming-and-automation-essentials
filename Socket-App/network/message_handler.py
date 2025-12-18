from dataclasses import dataclass
from typing import List
import time

@dataclass
class ChatMessage:
    username: str
    message: str
    timestamp: str
    is_system: bool = False

class MessageHandler:
    def __init__(self):
        self.messages: List[ChatMessage] = []
        self.max_messages = 1000
    
    def add_message(self, username: str, message: str, timestamp: str = None, is_system: bool = False):
        """Add message to history"""
        if timestamp is None:
            timestamp = time.strftime("%H:%M:%S")
        
        chat_message = ChatMessage(username, message, timestamp, is_system)
        self.messages.append(chat_message)
        
        # Keep only recent messages
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
        
        return chat_message
    
    def get_messages(self) -> List[ChatMessage]:
        """Get all messages"""
        return self.messages.copy()
    
    def clear_messages(self):
        """Clear all messages"""
        self.messages.clear()
    
    def format_message(self, msg: ChatMessage) -> str:
        """Format message for display"""
        if msg.is_system:
            return f"[{msg.timestamp}] {msg.message}"
        else:
            return f"[{msg.timestamp}] {msg.username}: {msg.message}"