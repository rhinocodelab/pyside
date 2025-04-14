import ctypes
import os
import sys
from ctypes import c_char_p, c_int, POINTER

class FileRestorer:
    """Class to handle restoration of a file damaged by the damage CLI."""
    
    LIB_PATH = "/usr/os-bin/librestore.so"
    
    def __init__(self, filename, swap_size=10):
        """
        Initialize the restorer with the damaged file path and swap size.
        
        Args:
            filename (str): Path to the damaged file to restore.
            swap_size (int): Number of bytes swapped in the damage process (default: 10).
            
        Raises:
            RuntimeError: If the library fails to load or the file does not exist.
        """
        if not os.path.exists(filename):
            raise RuntimeError(f"File not found: {filename}")
        self.filename = filename
        self.swap_size = swap_size
        try:
            self.lib = ctypes.CDLL(self.LIB_PATH)
            self._configure_library()
        except OSError as e:
            raise RuntimeError(f"Failed to load library {self.LIB_PATH}: {e}")

    def _configure_library(self):
        """Set up function signatures for librestore.so."""
        self.lib.Restore.argtypes = [c_char_p, c_int, POINTER(c_char_p)]
        self.lib.Restore.restype = c_int
        self.lib.FreeError.argtypes = [c_char_p]
        self.lib.FreeError.restype = None

    def restore(self):
        """
        Restore the damaged file.
        
        Returns:
            bool: True if restoration succeeded, False otherwise.
        """
        filename_bytes = self.filename.encode('utf-8')
        err_msg = c_char_p()
        result = self.lib.Restore(filename_bytes, c_int(self.swap_size), ctypes.byref(err_msg))
        
        if result == 0:
            return True
        else:
            if err_msg.value:
                error_str = err_msg.value.decode('utf-8')
                self.lib.FreeError(err_msg)
            else:
                return False

