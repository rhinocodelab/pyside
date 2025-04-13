import json
import pycurl
from io import BytesIO
from typing import Optional, Tuple
from utils.logger import Logger
import tarfile
import hashlib
class MetadataPatchCXVerifier:
    def __init__(self):
        self.logger = Logger()
    
    def verify_metadata(self, url: str, username: Optional[str] = None, password: Optional[str] = None) -> Tuple[bool, str]:
        """
            The metadata.json file is expected to be at the root of the Upgrade file which will be always a tar.bz2 file with or without extention.
            Try to extact only the metadata.json file from the tar.bz2 file
        """
        try:
            self.logger.info(f"Verifying metadata for {url}")
            # Initialize pycurl
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, url)
            curl.setopt(pycurl.FOLLOWLOCATION, 1)
            curl.setopt(pycurl.MAXREDIRS, 5)
            # Create a buffer to store the response
            response_buffer = BytesIO()
            curl.setopt(pycurl.WRITEDATA, response_buffer)
            # Set authentication if provided
            if username and password:
                curl.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
                curl.setopt(pycurl.USERPWD, f"{username}:{password}")
            # Perform the request
            self.logger.info(f"Downloading metadata from {url}")
            curl.perform()
            # Get the response code
            response_code = curl.getinfo(pycurl.RESPONSE_CODE)
            self.logger.info(f"Response code: {response_code}")
            # Close the connection
            curl.close()
            # Check if the response code is 200
            if response_code not in [200, 201, 206]:
                self.logger.error(f"Failed to download metadata from {url}")
                return False, f"Failed to download metadata from {url}"
            # Extract the metadata.json file from the tar.bz2 file
            response_buffer.seek(0)
            with tarfile.open(fileobj=response_buffer, mode='r:bz2') as tar:
                file_list = tar.getnames()
                if 'metadata.json' not in file_list:
                    self.logger.error(f"metadata.json file not found in {url}")
                    return False, f"metadata.json file not found in {url}"
                # Extract the metadata.json file
                metadata_file = tar.extractfile('metadata.json')
                # Read the metadata.json file
                if metadata_file:
                    try:
                        metadata_content = metadata_file.read().decode('utf-8')
                        metadata_json = json.loads(metadata_content)
                        # Check for required keys
                        required_keys = ['patch_version', 'patch_name', 'checksum', 'description', 'status']
                        missing_keys = [key for key in required_keys if key not in metadata_json]
                        if missing_keys:
                            self.logger.error(f"Missing required keys in metadata: {missing_keys}")
                            return False, f"Missing required keys in metadata: {missing_keys}"
                        ## Check if the checksum exists in the database
                        
                        # Extract the metadata.json file to /tmp/metadata.json
                        tmp_path = "/tmp/metadata.json"
                        with open(tmp_path, 'w') as f:
                            f.write(metadata_content)
                        self.logger.info(f"metadata.json file extracted to {tmp_path}")
                        
                        # Verify the patchcx file
                        is_valid, error_message = self._verify_patchcx(tar, metadata_json['checksum'])
                        if not is_valid:
                            return False, error_message
                        self.logger.info(f"Patchcx file verified successfully")
                        return True, "Metadata verification successful"
                    except json.JSONDecodeError:
                        self.logger.error(f"Failed to parse metadata from {url}")
                        return False, f"Failed to parse metadata from {url}"
                else:
                    self.logger.error(f"metadata.json file not found in {url}")
                    return False, f"metadata.json file not found in {url}"
        except (pycurl.error, tarfile.error, json.JSONDecodeError, IOError) as e:
            return False, f"Error verifying metadata: {e}"
        

    def _verify_patchcx(self, tar: tarfile.TarFile, expected_checksum: str) -> Tuple[bool, str]:
        """
            Verify the patchcx file
        """
        # Check if patch.cx exists in the archive
        patchcx_path = None
        for member in tar.getmembers():
            if member.name == 'patch.cx' or member.name.endswith('/patchcx'):
                patchcx_path = member.name
                break
        if not patchcx_path:
            return False, "patch.cx file not found in the archive"
        # Extract the patchcx file
        try:
            patchcx_file = tar.extractfile(patchcx_path)
            if patchcx_file:
                destination_path = "/tmp/patch.cx"
                calculated_checksum = hashlib.sha256()

                # Read the patchcx file in chunks
                chunk_size = 65536
                with open(destination_path, 'wb') as f:
                    while True:
                        chunk = patchcx_file.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        calculated_checksum.update(chunk)
                # Verify the checksum
                if calculated_checksum.hexdigest() != expected_checksum:
                    return False, "Checksum verification failed"
                return True, "Checksum verification successful"
        except Exception as e:
            return False, f"Error extracting patch.cx file: {e}"                