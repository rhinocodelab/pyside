from .base_protocol import NetworkProtocolHandler, NetworkSettings

class FTPHandler(NetworkProtocolHandler):
    """Handler for FTP/FTPS protocols"""
    
    def __init__(self, is_secure: bool = False):
        super().__init__()
        self.is_secure = is_secure
    
    def execute_update(self, settings: NetworkSettings):
        """
        Execute FTP/FTPS update process
        
        Args:
            settings: NetworkSettings object containing all required fields
        """
        # First validate all fields
        is_valid, error_message = self.validate_common_fields(settings)
        if not is_valid:
            raise ValueError(error_message)
            
        # Set protocol based on security setting
        protocol = "ftps" if self.is_secure else "ftp"
        
        # Construct full URL
        server_url = settings.server_url
        if not server_url.startswith(f"{protocol}://"):
            server_url = f"{protocol}://{server_url}"
            
        print(f"Starting {protocol.upper()} update process...")
        print(f"Server URL: {server_url}")
        print(f"Firmware path: {settings.firmware_path}")
        if settings.username:
            print(f"Username: {settings.username}")
        if settings.password:
            print("Password: [HIDDEN]") 