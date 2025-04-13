import requests
from typing import Optional, Tuple


class NetworkVerifier:
    """Class for network verification operations"""
    
    def __init__(self):
        """Initialize the NetworkVerifier"""
        pass
    
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
            response = requests.head(url, auth=(username, password) if username and password else None,
                                  timeout=5, verify=False)
            response.raise_for_status()
            return True, f"Connected to {url}"
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return False, f"File not found at {url}. Please check the file path."
            elif e.response.status_code == 401:
                return False, f"Authentication failed for {url}. Please check your credentials."
            elif e.response.status_code == 403:
                return False, f"Access forbidden to {url}. Please check your permissions."
            else:
                return False, f"HTTP error: {e.response.status_code} - {e.response.reason}"
        except requests.exceptions.ConnectionError:
            return False, f"Could not connect to server at {url}. Please check if the server is running and accessible."
        except requests.exceptions.Timeout:
            return False, f"Connection to {url} timed out. Please check your network connection."
        except requests.exceptions.RequestException as e:
            return False, f"Could not connect to {url}: {str(e)}"
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
            # Make a HEAD request with SSL verification enabled
            response = requests.head(url, timeout=5, verify=True)
            response.raise_for_status()
            return True, f"SSL certificate verified for {url}"
            
        except requests.exceptions.SSLError as e:
            return False, f"SSL certificate verification failed: {str(e)}"
        except requests.exceptions.RequestException as e:
            return False, f"Could not verify SSL certificate: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error during SSL certificate verification: {str(e)}" 