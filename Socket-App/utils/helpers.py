import time
import re

def get_timestamp():
    """Get current timestamp string"""
    return time.strftime("%H:%M:%S")

def validate_username(username):
    """Validate username format"""
    if not username or len(username.strip()) == 0:
        return False, "Username cannot be empty"
    
    if len(username) > 20:
        return False, "Username too long (max 20 characters)"
    
    if not re.match("^[a-zA-Z0-9_-]+$", username):
        return False, "Username can only contain letters, numbers, underscore, and dash"
    
    return True, "Valid username"

def validate_host(host):
    """Basic host validation"""
    if not host or len(host.strip()) == 0:
        return False, "Host cannot be empty"
    
    return True, "Valid host"

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"