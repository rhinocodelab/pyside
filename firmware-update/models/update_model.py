import os
import sqlite3
from models.database import DatabaseManager

class UpdateModel:
    def __init__(self):
        """Initialize the model with database connection"""
        self.db_manager = DatabaseManager()
    
    def get_settings(self):
        """Get all settings from the database"""
        return self.db_manager.get_settings()
    
    def get_update_on_boot(self):
        """Get the UpdateOnBoot setting from the database"""
        settings = self.db_manager.get_settings()
        if settings:
            return settings.get('UpdateOnBoot', False)
        return False
    
    def get_auto_update(self):
        """Get the AutoUpdate setting from the database"""
        settings = self.db_manager.get_settings()
        if settings:
            return settings.get('AutoUpdate', True)
        return True
    
    def get_update_method(self):
        """Get the UpdateMethod setting from the database"""
        settings = self.db_manager.get_settings()
        if settings:
            return settings.get('Method', 0)  # Default to 0 (DHCP)
        return 0  # Default to 0 (DHCP)
    
    def get_server_url(self):
        """Get the server URL from the database"""
        settings = self.db_manager.get_settings()
        if settings:
            return settings.get('IP', '')
        return ''
    
    def get_username(self):
        """Get the username from the database"""
        settings = self.db_manager.get_settings()
        if settings:
            return settings.get('Username', '')
        return ''
    
    def get_password(self):
        """Get the password from the database"""
        settings = self.db_manager.get_settings()
        if settings:
            return settings.get('Password', '')
        return ''
    
    def get_upgrade_filepath(self):
        """Get the upgrade file path from the database"""
        settings = self.db_manager.get_settings()
        if settings:
            return settings.get('UpgFilepath', '')
        return ''
    
    def get_md5sum(self, checksum: str):
        """Get the MD5SUM for a given checksum"""
        settings = self.db_manager.get_md5sum(checksum)
        if settings:
            return settings.get('md5sum', '')
        return ''
    

    def save_update_on_boot(self, update_on_boot):
        """Save the UpdateOnBoot setting to the database"""
        return self.db_manager.save_update_settings({'update_on_boot': update_on_boot})
    
    def save_auto_update(self, auto_update):
        """Save the AutoUpdate setting to the database"""
        return self.db_manager.save_update_settings({'auto_update': auto_update})
    
    def save_update_method(self, method):
        """Save the UpdateMethod setting to the database"""
        return self.db_manager.save_update_settings({'update_method': method})
    
    def save_server_url(self, server_url):
        """Save the server URL to the database"""
        return self.db_manager.save_update_settings({'server_url': server_url})
    
    def save_username(self, username):
        """Save the username to the database"""
        return self.db_manager.save_update_settings({'Username': username})
    
    def save_password(self, password):
        """Save the password to the database"""
        return self.db_manager.save_update_settings({'Password': password})
    
    def save_upgrade_filepath(self, filepath):
        """Save the upgrade file path to the database"""
        return self.db_manager.save_update_settings({'UpgFilepath': filepath}) 