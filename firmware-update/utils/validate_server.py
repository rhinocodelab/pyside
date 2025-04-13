import re

class ValidateServer:
    """Single source of validation for server-related fields"""
    
    def validate_server(self, server_address: str) -> tuple[bool, str]:
        """
        Validate if the server field contains a valid:
        - IP address (IPv4 or IPv6)
        - IP address with port number
        - Fully Qualified Domain Name (FQDN)
        - Simple hostname
        
        Args:
            server_address: The server address to validate
            
        Returns:
        - (True, None) if valid
        - (False, error_message) if invalid
        """
        print(f"Validating server address: {server_address}")
        # Check if the server address is empty
        if not server_address:
            return False, "Server address is required"
        
        # Check for invalid characters that shouldn't be in a server address
        if '@' in server_address:
            return False, "Server address cannot contain '@' symbol"
        
        # IPv4 with optional port regex
        ipv4_regex = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::(\d{1,5}))?$'

        # IPv6 with optional port regex
        ipv6_regex = r'^(\[([0-9a-fA-F:]+)\])?(?::(\d{1,5}))?$'

        # FQDN regex - must start with alphanumeric, no @ symbol allowed
        fqdn_regex = r'^([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}(?::\d{1,5})?$'
        
        # Simple hostname regex - must start with alphanumeric
        hostname_regex = r'^([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)(?::\d{1,5})?$'

        # Check if it's an IPv4 address with optional port
        ipv4_match = re.match(ipv4_regex, server_address)
        if ipv4_match:
            ip = ipv4_match.group(1)
            port = ipv4_match.group(2)
            
            # Validate IP address components
            octets = ip.split('.')
            for octet in octets:
                # Check for invalid leading zeros
                if len(octet) > 1 and octet[0] == '0':
                    return False, f"Invalid IPv4 address: leading zeros not allowed in {ip}"
                try:
                    value = int(octet)
                    if value < 0 or value > 255:
                        return False, f"Invalid IPv4 address: each octet must be between 0 and 255 in {ip}"
                except ValueError:
                    return False, f"Invalid IPv4 address: non-numeric octet in {ip}"
            
            # Validate port if present
            if port:
                try:
                    port_num = int(port)
                    if port_num < 1 or port_num > 65535:
                        return False, f"Invalid port number: {port}"
                except ValueError:
                    return False, f"Invalid port number (must be numeric): {port}"
            
            return True, None
        
        # Check if it's an IPv6 address with optional port
        ipv6_match = re.match(ipv6_regex, server_address)
        if ipv6_match:
            # We won't do deep validation of IPv6 here
            ip = ipv6_match.group(1)
            port = ipv6_match.group(2)
            
            # Validate port if present
            if port:
                try:
                    port_num = int(port)
                    if port_num < 1 or port_num > 65535:
                        return False, f"Invalid port number: {port}"
                except ValueError:
                    return False, f"Invalid port number (must be numeric): {port}"
            
            return True, None
        
        # Check if it's an FQDN with optional port
        fqdn_match = re.match(fqdn_regex, server_address)
        if fqdn_match:
            fqdn = fqdn_match.group(1)
            port = fqdn_match.group(2)
            
            # Validate port if present
            if port:
                try:
                    port_num = int(port)
                    if port_num < 1 or port_num > 65535:
                        return False, f"Invalid port number: {port}"
                except ValueError:
                    return False, f"Invalid port number (must be numeric): {port}"
            
            return True, None
        
        # Check if it's a simple hostname with optional port
        hostname_match = re.match(hostname_regex, server_address)
        if hostname_match:
            hostname = hostname_match.group(1)
            port = hostname_match.group(3)
            
            # Validate port if present
            if port:
                try:
                    port_num = int(port)
                    if port_num < 1 or port_num > 65535:
                        return False, f"Invalid port number: {port}"
                except ValueError:
                    return False, f"Invalid port number (must be numeric): {port}"
            
            return True, None
        
        return False, "Invalid server address format"
    
    def validate_username(self, username: str, password: str = None) -> tuple[bool, str]:
        """
        Validate the username field.
        If either username or password is provided, both must be provided.
        
        Args:
            username: The username to validate
            password: The password to check against (optional)
            
        Returns:
        - (True, None) if valid
        - (False, error_message) if invalid
        """
        # Empty check - username is optional, so empty is valid
        if not username:
            # If password is provided, username is required
            if password and password.strip():
                return False, "Username is required when password is provided"
            return True, None
        
        # Basic validation: no whitespace at the beginning or end
        if username.strip() != username:
            return False, "Username cannot contain leading or trailing whitespace"
        
        # If username is provided, password must also be provided
        if not password or not password.strip():
            return False, "Password is required when username is provided"
        
        return True, None
    
    def validate_password(self, password: str, username: str = None) -> tuple[bool, str]:
        """
        Validate the password field.
        If either username or password is provided, both must be provided.
        
        Args:
            password: The password to validate
            username: The username to check against (optional)
            
        Returns:
        - (True, None) if valid
        - (False, error_message) if invalid
        """
        # Empty check - password is optional, so empty is valid
        if not password:
            # If username is provided, password is required
            if username and username.strip():
                return False, "Password is required when username is provided"
            return True, None
        
        # If password is provided, username must also be provided
        if not username or not username.strip():
            return False, "Username is required when password is provided"
        
        return True, None
    
    def validate_upgrade_path(self, path: str) -> tuple[bool, str]:
        """
        Validate the upgrade file path.
        Can be any filename or path, with or without extension.
        
        Args:
            path: The upgrade file path to validate
            
        Returns:
        - (True, None) if valid
        - (False, error_message) if invalid
        """
        # Empty check
        if not path:
            return False, "Upgrade file path cannot be empty"
        
        # Any non-empty string is valid
        return True, None 
    

