from abc import ABC, abstractmethod
from dataclasses import dataclass
from utils.validate_server import ValidateServer

@dataclass
class NetworkSettings:
    """Common settings for network-based protocols"""
    server_url: str = ""
    username: str = ""
    password: str = ""
    firmware_path: str = ""
    is_secure: bool = False  # For HTTPS/FTPS

class NetworkProtocolHandler(ABC):
    """Base class for network protocol handlers"""
    
    def __init__(self):
        self.validator = ValidateServer()
        
    def validate_settings(self, settings: NetworkSettings) -> tuple[bool, str]:
        """
        Validate all settings using ValidateServer
        
        Args:
            settings: NetworkSettings object containing all required fields
            
        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        # Validate server URL
        is_valid, error_message = self.validator.validate_server(settings.server_url)
        if not is_valid:
            return False, error_message
            
        # Validate username and password together
        is_valid, error_message = self.validator.validate_username(settings.username, settings.password)
        if not is_valid:
            return False, error_message
            
        # Validate password and username together
        is_valid, error_message = self.validator.validate_password(settings.password, settings.username)
        if not is_valid:
            return False, error_message
                
        # Validate firmware path
        is_valid, error_message = self.validator.validate_upgrade_path(settings.firmware_path)
        if not is_valid:
            return False, error_message
            
        return True, None
    
    @abstractmethod
    def execute_update(self, settings: NetworkSettings):
        """
        Execute the update process using the provided settings
        
        Args:
            settings: NetworkSettings object containing all required fields
        """
        pass 