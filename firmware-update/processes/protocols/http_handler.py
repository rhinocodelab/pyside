from .base_protocol import NetworkProtocolHandler, NetworkSettings
from urllib.parse import quote
from processes.verification.network_verifier import NetworkVerifier
from processes.verification.metadata_patchcx_verifier import MetadataPatchCXVerifier
from utils.logger import Logger
from utils.uncorrupt import FileRestorer
from utils.validate_server import ValidateServer
import subprocess
import os
import shutil
import magic
import socket
from typing import Tuple

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
        self.validate_server = ValidateServer()
    
    def execute_update(self, settings: NetworkSettings) -> Tuple[bool, str]:
        """
        Execute HTTP/HTTPS update process
        
        Args:
            settings: NetworkSettings object containing all required fields
            
        Raises:
            ValueError: If validation fails
        """
        # First validate all fields
        # Validate server URL
        is_valid, error_message = self.validate_server.validate_server(settings.server_url)
        if not is_valid:
            return False, error_message
        
        # Validate firmware path
        is_valid, error_message = self.validate_server.validate_upgrade_path(settings.firmware_path)
        if not is_valid:
            return False, error_message
        
        # Validate username and password if provided
        if settings.username and settings.password:
            is_valid, error_message = self.validate_server.validate_username(settings.username, settings.password)
            if not is_valid:
                return False, error_message
        
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
            # Check if we're using an IP address
            is_ip_address, error_message = self.validate_server.validate_server(server_url)
            
            if is_ip_address:
                self.logger.info(f"Using IP address for HTTPS: {server_url}. Disabling hostname verification.")
                # For IP addresses, we need to modify the verification process
                # This will be handled in the NetworkVerifier class
                is_valid, error_message = self.verifier.verify_ssl_certificate_ip(final_url)
            else:
                is_valid, error_message = self.verifier.verify_ssl_certificate(final_url)
                
            if not is_valid:
                return False, error_message
                
            # For connection verification, we'll use the same approach
            if is_ip_address:
                is_valid, error_message = self.verifier.verify_connection_ip(final_url, settings.username, settings.password)
            else:
                is_valid, error_message = self.verifier.verify_connection(final_url, settings.username, settings.password)
                
            if not is_valid:
                return False, error_message
                
            self.logger.info(f"Connected to {final_url}")
        else:
            is_valid, error_message = self.verifier.verify_connection(final_url, settings.username, settings.password)
            if not is_valid:
                return False, error_message
            self.logger.info(f"Connected to {final_url}")
        
        # Verify metadata
        is_valid, error_message = self.metadata_verifier.verify_metadata(final_url, settings.username, settings.password)
        if not is_valid:
            return False, error_message

        # Copy the update files to the target directory
        is_success, error_message = self._copy_update_files()
        if not is_success:
            # Only cleanup if copy fails
            cleanup_success, cleanup_message = self._cleanup()
            if not cleanup_success:
                return False, f"{error_message}. Cleanup also failed: {cleanup_message}"
            return False, error_message
        
        return True, "Update process completed successfully"
        
    def _copy_update_files(self) -> Tuple[bool, str]:
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
                return False, f"Failed to mount /sda1 in read-write mode: {result.stderr}"
        except subprocess.SubprocessError as e:
            self.logger.error(f"Failed to mount /sda1 in read-write mode: {e}")
            return False, f"Failed to mount /sda1 in read-write mode: {e}"
        
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
            return False, f"Failed to create required directories: {e}"
        
        try:
            # Copy the update files to the target directory
            shutil.copy("/tmp/metadata.json", os.path.join(PATCH_DIR, "metadata.json"))
            self.logger.info("Metadata file copied to the target directory")
        except Exception as e:
            self.logger.error(f"Failed to copy metadata file to the target directory: {e}")
            return False, f"Failed to copy metadata file to the target directory: {e}"
        
        try:
            # Check if the patchcx file is available
            if not os.path.exists("/tmp/patch.cx"):
                self.logger.error("Patchcx file not found")
                return False, "Patchcx file not found"
            
            # Un-corrupt the patchcx file
            uncorrupt = FileRestorer("/tmp/patch.cx")
            if not uncorrupt.restore():
                self.logger.error("Failed to restore the patchcx file")
                return False, "Failed to restore the patchcx file"
            self.logger.info("Patchcx restored successfully")
            
            # Verify the patchcx file type using magic
            file_type = magic.from_file("/tmp/patch.cx", mime=True)
            if file_type != 'application/x-bzip2':
                self.logger.error("Patchcx file is not a valid bzip2 file")
                return False, "Patchcx file is not a valid bzip2 file"
            self.logger.info("Patchcx file is a valid bzip2 file")
            
            # Copy the patchcx file to the target directory
            shutil.copy("/tmp/patch.cx", os.path.join(PATCH_DIR, "patch.cx"))
            self.logger.info("Patchcx file copied to the target directory")
            
            # Copy the medatadata.json file to /data/
            shutil.copy("/tmp/metadata.json", os.path.join("/data", "metadata.json"))
            self.logger.info("Metadata file copied to /data")
        except Exception as e:
            self.logger.error(f"Failed to restore the patchcx file: {e}")
            return False, f"Failed to restore the patchcx file: {e}"
        
        return True, "Files copied successfully"
    
    def _cleanup(self) -> Tuple[bool, str]:
        """
        Clean up all the files in case of any errors
        """
        PATCH_DIR = "/sda1/data/cxfw/patch"
        ROLLBACK_DIR = "/sda1/data/cxfw/rollback"

        try:
            # Clean-up temporary files
            if os.path.exists("/tmp/patch.cx"):
                os.remove("/tmp/patch.cx")
            if os.path.exists("/tmp/metadata.json"):
                os.remove("/tmp/metadata.json")
            self.logger.info("Temporary files cleaned-up successfully")
        except Exception as e:
            self.logger.error(f"Failed to clean-up temporary files: {e}")
            return False, f"Failed to clean-up temporary files: {e}"
        
        # Read-Write mount /sda1
        try:
            self.logger.info("Mounting /sda1 in read-only mode")
            mount_cmd = ["mount", "-o", "remount,rw", "/sda1"]
            result = subprocess.run(mount_cmd, check=True, capture_output=True, text=True)
            if result.returncode != 0:
                self.logger.error(f"Failed to mount /sda1 in read-write mode: {result.stderr}")
                return False, f"Failed to mount /sda1 in read-write mode: {result.stderr}"
        except Exception as e:
            self.logger.error(f"Failed to mount /sda1 in read-write mode: {e}")
            return False, f"Failed to mount /sda1 in read-write mode: {e}"
        
        try:
            # Clean-up the target directory
            for directory in [PATCH_DIR, ROLLBACK_DIR]:
                if os.path.exists(directory):
                    for item in os.listdir(directory):
                        item_path = os.path.join(directory, item)
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
            self.logger.info("Target directory cleaned-up successfully")
        except Exception as e:
            self.logger.error(f"Failed to clean-up target directory: {e}")
            return False, f"Failed to clean-up target directory: {e}"
        
        # Clean-up /data    
        try:
            if os.path.exists("/data/metadata.json"):
                os.remove("/data/metadata.json")
            self.logger.info("Metadata file cleaned-up successfully")
        except Exception as e:
            self.logger.error(f"Failed to clean-up metadata file: {e}")
            return False, f"Failed to clean-up metadata file: {e}"
        
        return True, "Cleanup completed successfully"

  
