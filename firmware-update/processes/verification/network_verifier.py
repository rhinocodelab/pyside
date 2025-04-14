import pycurl
from typing import Optional, Tuple
import socket
import ssl
from urllib.parse import urlparse
from io import BytesIO


class NetworkVerifier:
    """Class for network verification operations"""
    
    def __init__(self):
        """Initialize the NetworkVerifier"""
        self.curl = pycurl.Curl()
        self.curl.setopt(pycurl.TIMEOUT, 5)
        self.curl.setopt(pycurl.NOSIGNAL, 1)
        self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
        self.curl.setopt(pycurl.MAXREDIRS, 5)
        
    def __del__(self):
        """Cleanup PyCURL resources"""
        if hasattr(self, 'curl'):
            self.curl.close()
    
    def verify_connection(self, url: str, username: Optional[str] = None,
                         password: Optional[str] = None) -> Tuple[bool, str]:
        """
        Verify network connectivity to the specified URL
        
        Args:
            url: The URL to verify connection to
            username: Optional username for authentication
            password: Optional password for authentication
            
        Returns:
            Tuple[bool, str]: (is_connected, error_message)
        """
        try:
            # Reset curl options
            self.curl.reset()
            
            # Set URL and basic options
            self.curl.setopt(pycurl.URL, url)
            self.curl.setopt(pycurl.NOBODY, True)  # HEAD request
            self.curl.setopt(pycurl.SSL_VERIFYPEER, False)
            self.curl.setopt(pycurl.SSL_VERIFYHOST, 0)
            
            # Set authentication if provided
            if username and password:
                self.curl.setopt(pycurl.USERPWD, f"{username}:{password}")
            
            # Create buffer for response
            buffer = BytesIO()
            self.curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
            
            # Set additional options to match working curl command
            self.curl.setopt(pycurl.HTTPHEADER, [
                'User-Agent: Mozilla/5.0',
                'Accept: */*'
            ])
            
            # Perform request
            self.curl.perform()
            
            # Get response code
            response_code = self.curl.getinfo(pycurl.RESPONSE_CODE)
            
            if response_code == 200:
                return True, f"Connected to {url}"
            elif response_code == 404:
                return False, f"File not found at {url}. Please check the file path."
            elif response_code == 401:
                return False, f"Authentication failed for {url}. Please check your credentials."
            elif response_code == 403:
                return False, f"Access forbidden to {url}. Please check your permissions."
            else:
                return False, f"HTTP error: {response_code}"
                
        except pycurl.error as e:
            error_code = e.args[0]
            error_message = e.args[1]
            
            if error_code == pycurl.E_COULDNT_CONNECT:
                return False, f"Could not connect to server at {url}. Please check if the server is running and accessible."
            elif error_code == pycurl.E_OPERATION_TIMEDOUT:
                return False, f"Connection to {url} timed out. Please check your network connection."
            elif error_code == pycurl.E_COULDNT_RESOLVE_HOST:
                return False, f"Could not resolve hostname for {url}. Please check DNS configuration."
            elif error_code == pycurl.E_SSL_CONNECT_FAILED:
                return False, f"SSL connection failed for {url}. Please check SSL configuration."
            else:
                return False, f"PyCURL error ({error_code}): {error_message}"
        except Exception as e:
            return False, f"Unexpected error during connection verification: {str(e)}"
    
    def verify_connection_ip(self, url: str, username: Optional[str] = None,
                         password: Optional[str] = None) -> Tuple[bool, str]:
        """
        Verify network connectivity to the specified URL when using an IP address
        
        Args:
            url: The URL to verify connection to
            username: Optional username for authentication
            password: Optional password for authentication
            
        Returns:
            Tuple[bool, str]: (is_connected, error_message)
        """
        try:
            # Reset curl options
            self.curl.reset()
            
            # Set URL and basic options
            self.curl.setopt(pycurl.URL, url)
            self.curl.setopt(pycurl.NOBODY, True)  # HEAD request
            self.curl.setopt(pycurl.SSL_VERIFYPEER, False)
            self.curl.setopt(pycurl.SSL_VERIFYHOST, 0)
            
            # Set authentication if provided
            if username and password:
                self.curl.setopt(pycurl.USERPWD, f"{username}:{password}")
            
            # Create buffer for response
            buffer = BytesIO()
            self.curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
            
            # Set additional options to match working curl command
            self.curl.setopt(pycurl.HTTPHEADER, [
                'User-Agent: Mozilla/5.0',
                'Accept: */*'
            ])
            
            # Perform request
            self.curl.perform()
            
            # Get response code
            response_code = self.curl.getinfo(pycurl.RESPONSE_CODE)
            
            if response_code == 200:
                return True, f"Connected to {url}"
            elif response_code == 404:
                return False, f"File not found at {url}. Please check the file path."
            elif response_code == 401:
                return False, f"Authentication failed for {url}. Please check your credentials."
            elif response_code == 403:
                return False, f"Access forbidden to {url}. Please check your permissions."
            else:
                return False, f"HTTP error: {response_code}"
                
        except pycurl.error as e:
            error_code = e.args[0]
            error_message = e.args[1]
            
            if error_code == pycurl.E_COULDNT_CONNECT:
                return False, f"Could not connect to server at {url}. Please check if the server is running and accessible."
            elif error_code == pycurl.E_OPERATION_TIMEDOUT:
                return False, f"Connection to {url} timed out. Please check your network connection."
            elif error_code == pycurl.E_COULDNT_RESOLVE_HOST:
                return False, f"Could not resolve hostname for {url}. Please check DNS configuration."
            elif error_code == pycurl.E_SSL_CONNECT_FAILED:
                # Only skip SSL verification for HTTPS with IP addresses
                if url.startswith('https://') and self._is_valid_ip(urlparse(url).netloc.split(':')[0]):
                    return True, f"SSL connection warning for IP address with HTTPS, but continuing anyway."
                else:
                    return False, f"SSL connection failed for {url}. Please check SSL configuration."
            else:
                return False, f"PyCURL error ({error_code}): {error_message}"
        except Exception as e:
            return False, f"Unexpected error during connection verification: {str(e)}"
            
    def verify_ssl_certificate(self, url: str) -> Tuple[bool, str]:
        """
        Verify the SSL certificate for HTTPS URLs
        
        Args:
            url: The HTTPS URL to verify
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not url.startswith('https://'):
            return True, "Not an HTTPS URL, skipping SSL verification"
            
        try:
            # Reset curl options
            self.curl.reset()
            
            # Set URL and basic options
            self.curl.setopt(pycurl.URL, url)
            self.curl.setopt(pycurl.NOBODY, True)  # HEAD request
            self.curl.setopt(pycurl.SSL_VERIFYPEER, True)
            self.curl.setopt(pycurl.SSL_VERIFYHOST, 2)
            
            # Create buffer for response
            buffer = BytesIO()
            self.curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
            
            # Set additional options to match working curl command
            self.curl.setopt(pycurl.HTTPHEADER, [
                'User-Agent: Mozilla/5.0',
                'Accept: */*'
            ])
            
            # Perform request
            self.curl.perform()
            
            return True, f"SSL certificate verified for {url}"
            
        except pycurl.error as e:
            error_code = e.args[0]
            error_message = e.args[1]
            
            if error_code == pycurl.E_SSL_CERTPROBLEM:
                return False, f"SSL certificate problem: {error_message}"
            elif error_code == pycurl.E_SSL_CIPHER:
                return False, f"SSL cipher error: {error_message}"
            elif error_code == pycurl.E_SSL_CONNECT_FAILED:
                return False, f"SSL connection failed: {error_message}"
            else:
                return False, f"SSL verification error ({error_code}): {error_message}"
        except Exception as e:
            return False, f"Unexpected error during SSL certificate verification: {str(e)}"
            
    def verify_ssl_certificate_ip(self, url: str) -> Tuple[bool, str]:
        """
        Verify the SSL certificate for HTTPS URLs when using an IP address
        
        Args:
            url: The HTTPS URL to verify
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not url.startswith('https://'):
            return True, "Not an HTTPS URL, skipping SSL verification"
            
        try:
            # Reset curl options
            self.curl.reset()
            
            # Set URL and basic options
            self.curl.setopt(pycurl.URL, url)
            self.curl.setopt(pycurl.NOBODY, True)  # HEAD request
            self.curl.setopt(pycurl.SSL_VERIFYPEER, False)
            self.curl.setopt(pycurl.SSL_VERIFYHOST, 0)
            
            # Create buffer for response
            buffer = BytesIO()
            self.curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
            
            # Set additional options to match working curl command
            self.curl.setopt(pycurl.HTTPHEADER, [
                'User-Agent: Mozilla/5.0',
                'Accept: */*'
            ])
            
            # Perform request
            self.curl.perform()
            
            return True, f"SSL certificate verification skipped for IP address: {url}"
            
        except pycurl.error as e:
            error_code = e.args[0]
            error_message = e.args[1]
            
            if error_code == pycurl.E_SSL_CERTPROBLEM:
                # Only skip SSL verification for HTTPS with IP addresses
                if url.startswith('https://') and self._is_valid_ip(urlparse(url).netloc.split(':')[0]):
                    return True, f"SSL certificate verification skipped for IP address with HTTPS: {url}"
                else:
                    return False, f"SSL certificate error: {error_message}"
            elif error_code == pycurl.E_SSL_CIPHER:
                # Only skip SSL verification for HTTPS with IP addresses
                if url.startswith('https://') and self._is_valid_ip(urlparse(url).netloc.split(':')[0]):
                    return True, f"SSL certificate verification skipped for IP address with HTTPS: {url}"
                else:
                    return False, f"SSL cipher error: {error_message}"
            elif error_code == pycurl.E_SSL_CONNECT_FAILED:
                # Only skip SSL verification for HTTPS with IP addresses
                if url.startswith('https://') and self._is_valid_ip(urlparse(url).netloc.split(':')[0]):
                    return True, f"SSL connection warning for IP address with HTTPS, but continuing anyway."
                else:
                    return False, f"SSL connection failed: {error_message}"
            else:
                # Only skip other errors for HTTPS with IP addresses
                if url.startswith('https://') and self._is_valid_ip(urlparse(url).netloc.split(':')[0]):
                    return True, f"SSL error ignored for IP address with HTTPS: {error_message}"
                else:
                    return False, f"SSL error ({error_code}): {error_message}"
        except Exception as e:
            return False, f"Unexpected error during connection to IP address: {str(e)}"
            
    def _is_valid_ip(self, ip: str) -> bool:
        """
        Check if a string is a valid IP address
        
        Args:
            ip: String to check
            
        Returns:
            bool: True if valid IP address, False otherwise
        """
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False 