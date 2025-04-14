import sqlite3
from typing import Optional, Dict, Any
import os
import logging

class DatabaseManager:
    """Database manager for handling UpdateSettings table operations"""
    DB_PATH = "/data/sysconf.db"
    TABLE_NAME = "UpdateSettings"
    MD5SUM_TABLE_NAME = "MD5SUM"

    def __init__(self):
        """Initialize the database manager"""
        self.conn = None
        self.cursor = None
        self.initialize_database()
    
    def initialize_database(self):
        """Initialize the database and create tables if they don't exist"""
        try:
            self.connect()
            
            # Create the UpdateSettings table if it doesn't exist
            self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                    id INTEGER PRIMARY KEY,
                    UpdateOnBoot INTEGER DEFAULT 0,
                    Method INTEGER DEFAULT 0,
                    UpgScopeID INTEGER DEFAULT 131,
                    IP TEXT DEFAULT '',
                    UpgFilepath TEXT DEFAULT '',
                    Username TEXT DEFAULT '',
                    Password TEXT DEFAULT '',
                    PromptUser INTEGER DEFAULT 0,
                    AutoUpdate INTEGER DEFAULT 1,
                    Extra1 INTEGER,
                    Extra2 INTEGER,
                    Extra3 TEXT,
                    Extra4 TEXT
                )
            ''')
            
            # Create the MD5SUM table if it doesn't exist
            self.cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {self.MD5SUM_TABLE_NAME} (
                    Filename TEXT NOT NULL,
                    Md5Sum TEXT NOT NULL PRIMARY KEY,
                    PatchVersion TEXT DEFAULT '',
                    PatchName TEXT DEFAULT '',
                    Description TEXT DEFAULT '',
                    Status INTEGER DEFAULT 0,
                    DateString TEXT
                )
            ''')

            # Check if there are any records in the table
            self.cursor.execute(f"SELECT COUNT(*) FROM {self.TABLE_NAME}")
            count = self.cursor.fetchone()[0]
            
            # If no records exist, insert default settings
            if count == 0:
                self.cursor.execute(f'''
                    INSERT INTO {self.TABLE_NAME} (
                        UpdateOnBoot, Method, UpgScopeID, IP, UpgFilepath, 
                        Username, Password, PromptUser, AutoUpdate, 
                        Extra1, Extra2, Extra3, Extra4
                    ) VALUES (
                        0, 0, 131, '', '', 
                        '', '', 0, 1,
                        NULL, NULL, NULL, NULL
                    )
                ''')
                self.conn.commit()
            
            self.disconnect()
        except Exception as e:
            logging.error(f"Database initialization error: {e}")
            self.disconnect()
    
    def get_settings(self):
        """Get all settings from the database"""
        try:
            self.connect()
            
            self.cursor.execute(f"SELECT * FROM {self.TABLE_NAME} WHERE id = 1")
            result = self.cursor.fetchone()
            
            if result:
                settings = {
                    'id': result[0],
                    'UpdateOnBoot': bool(result[1]),
                    'Method': result[2],
                    'UpgScopeID': result[3],
                    'IP': result[4],
                    'UpgFilepath': result[5],
                    'Username': result[6],
                    'Password': result[7],
                    'PromptUser': bool(result[8]),
                    'AutoUpdate': bool(result[9]),
                    'Extra1': result[10],
                    'Extra2': result[11],
                    'Extra3': result[12],
                    'Extra4': result[13]
                }
                return settings
            return None
        except Exception as e:
            logging.error(f"Error getting settings: {e}")
            return None
        finally:
            self.disconnect()
    
    def get_md5sum(self, checksum: str) -> Optional[Dict[str, Any]]:
        """Get the information for a given checksum"""
        try:
            self.connect()
            
            # Query the MD5SUM table for the given checksum
            self.cursor.execute(f"SELECT * FROM {self.MD5SUM_TABLE_NAME} WHERE Md5Sum = ?", (checksum,))
            result = self.cursor.fetchone()

            if result:
                return {
                    'filename': result[0],
                    'md5sum': result[1],
                    'patch_version': result[2],
                    'patch_name': result[3],
                    'description': result[4],
                    'status': result[5],
                    'date_string': result[6]
                }
            return None
        except Exception as e:
            logging.error(f"Error getting MD5SUM: {e}")
            return None
        finally:
            self.disconnect()

    def save_update_settings(self, settings: Dict[str, Any]) -> bool:
        """Save update settings to the database"""
        self.connect()
        try:
            # Convert settings keys to match database column names if needed
            db_settings = {}
            for key, value in settings.items():
                if key == 'update_method':
                    db_settings['Method'] = value
                elif key == 'update_on_boot':
                    db_settings['UpdateOnBoot'] = value
                elif key == 'auto_update':
                    db_settings['AutoUpdate'] = value
                elif key == 'server_url':
                    db_settings['IP'] = value
                else:
                    # For other keys, use them as is
                    db_settings[key] = value
            
            # Build the SET part of the UPDATE query
            set_clause = ", ".join([f"{key} = ?" for key in db_settings.keys()])
            query = f"UPDATE {self.TABLE_NAME} SET {set_clause} WHERE id = 1"
            
            # Execute the query with the values
            self.cursor.execute(query, list(db_settings.values()))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(f"Error saving update settings: {e}")
            return False
        finally:
            self.disconnect()
    
    def connect(self):
        """Connect to the database"""
        if not self.conn:
            self.conn = sqlite3.connect(self.DB_PATH)
            self.cursor = self.conn.cursor()
    
    def disconnect(self):
        """Disconnect from the database"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    

    