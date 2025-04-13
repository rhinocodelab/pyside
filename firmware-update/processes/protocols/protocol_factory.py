from typing import Optional
from .base_protocol import NetworkProtocolHandler
from .http_handler import HTTPHandler
from .ftp_handler import FTPHandler

class ProtocolFactory:
    """Factory class for creating protocol handlers"""
    
    @staticmethod
    def get_handler(method_text: str) -> Optional[NetworkProtocolHandler]:
        """
        Get the appropriate protocol handler based on method text
        
        Args:
            method_text: Text of the selected method
                "HTTP"
                "HTTPS"
                "FTP"
                "FTPS"
                
        Returns:
            NetworkProtocolHandler or None if method is not supported
        """
        method_text = method_text.upper()
        
        if method_text == "HTTP":
            return HTTPHandler(is_secure=False)
        elif method_text == "HTTPS":
            return HTTPHandler(is_secure=True)
        elif method_text == "FTP":
            return FTPHandler(is_secure=False)
        elif method_text == "FTPS":
            return FTPHandler(is_secure=True)
        else:
            return None 