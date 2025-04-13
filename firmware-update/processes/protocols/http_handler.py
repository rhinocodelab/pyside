from .base_protocol import NetworkProtocolHandler, NetworkSettings
from urllib.parse import quote
from processes.verification.network_verifier import NetworkVerifier
from processes.verification.metadata_patchcx_verifier import MetadataPatchCXVerifier
from utils.logger import Logger
import subprocess
import os
import shutil

class HTTPHandler(NetworkProtocolHandler):
    """Handler for HTTP/HTTPS protocols"""
    
    def __init__(self, is_secure: bool = False):
        """
        Initialize HTTP handler
        
        Args:
            is_secure: Whether to use HTTPS (True) or HTTP (False)
        """
        super().__init__()
        self.is_secure = is_secure
        self.verifier = NetworkVerifier()
        self.metadata_verifier = MetadataPatchCXVerifier()
        self.logger = Logger()
    
    def execute_update(self, settings: NetworkSettings):
        """
        Execute HTTP/HTTPS update process
        
        Args:
            settings: NetworkSettings object containing all required fields
            
        Raises:
            ValueError: If validation fails
        """
        # First validate all fields
        is_valid, error_message = self.validate_settings(settings)
        if not is_valid:
            raise ValueError(error_message)
            
        # Set protocol based on security setting
        protocol = "https" if self.is_secure else "http"
        
        # Construct full URL with credentials if provided
        server_url = settings.server_url
        if not server_url.startswith(f"{protocol}://"):
            # Add credentials if both username and password are provided
            if settings.username and settings.password:
                # URL encode username and password to handle special characters
                encoded_username = quote(settings.username, safe='')
                encoded_password = quote(settings.password, safe='')
                
                # Extract host and port if present
                if ":" in server_url:
                    host, port = server_url.split(":", 1)
                    server_url = f"{protocol}://{encoded_username}:{encoded_password}@{host}:{port}"
                else:
                    server_url = f"{protocol}://{encoded_username}:{encoded_password}@{server_url}"
            else:
                server_url = f"{protocol}://{server_url}"
            
        
        # Final URL
        final_url = f"{server_url}/{settings.firmware_path}"
        
        # Verify connection and SSL certificate in case of HTTPS
        if self.is_secure:
            is_valid, error_message = self.verifier.verify_ssl_certificate(final_url)
            if not is_valid:
                raise ValueError(error_message)
            is_valid, error_message = self.verifier.verify_connection(final_url, settings.username, settings.password)
            if not is_valid:
                raise ValueError(error_message)
            self.logger.info(f"Connected to {final_url}")
        else:
            is_valid, error_message = self.verifier.verify_connection(final_url, settings.username, settings.password)
            if not is_valid:
                raise ValueError(error_message)
            self.logger.info(f"Connected to {final_url}")
        
        # Verify metadata
        is_valid, error_message = self.metadata_verifier.verify_metadata(final_url, settings.username, settings.password)
        if not is_valid:
            raise ValueError(error_message)
    
    def copy_update_files(self) -> bool:
        """
            Copy the update files to the target directory
            1. Mount /sda1 in read-write mode
            2. Create required directories
            3. Copy the update files to the target directory
            4. Unmount /sda1
        """
        PATCH_DIR = "/sda1/data/cxfw/patch"
        ROLLBACK_DIR = "/sda1/data/cxfw/rollback"

        try:
            # Mount /sda1 in read-write mode
            self.logger.info("Mounting /sda1 in read-write mode")
            mount_cmd = ["mount", "-o", "remount,rw", "/sda1"]
            result = subprocess.run(mount_cmd, check=True, capture_output=True, text=True)
            if result.returncode != 0:
                self.logger.error(f"Failed to mount /sda1 in read-write mode: {result.stderr}")
                return False
            
        except subprocess.SubprocessError as e:
            self.logger.error(f"Failed to mount /sda1 in read-write mode: {e}")
            return False
        
        try:
            # Create required directories
            for directory in [PATCH_DIR, ROLLBACK_DIR]:
                if not os.path.exists(directory):
                    self.logger.info(f"Creating directory: {directory}")
                    os.makedirs(directory, exist_ok=True)
                else:
                    self.logger.info(f"Clearing directory: {directory}")
                    for item in os.listdir(directory):
                        item_path = os.path.join(directory, item)
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
        except Exception as e:
            self.logger.error(f"Failed to create required directories: {e}")
            return False
        
        try:
            # Copy the update files to the target directory
            shutil.copy("/tmp/metadata.json", os.path.join(PATCH_DIR, "metadata.json"))
            self.logger.info("Metadata file copied to the target directory")
        except Exception as e:
            self.logger.error(f"Failed to copy metadata file to the target directory: {e}")
            return False
        
    
    def _uncorrupt_patchcx(self, patchcx_path: str) -> bool:
        """
            Un-corrupt the patchcx file
        """
        pass