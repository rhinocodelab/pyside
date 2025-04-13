import sqlite3
from typing import Optional, Dict, Any
import os
import logging

class DatabaseManager:
    """Database manager for handling UpdateSettings table operations"""
    DB_PATH = "/data/sysconf.db"
    TABLE_NAME = "UpdateSettings"

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
                    ConfScopeID INTEGER DEFAULT 130,
                    UpgScopeID INTEGER DEFAULT 131,
                    IP TEXT DEFAULT '',
                    ConfFilepath TEXT DEFAULT '',
                    UpgFilepath TEXT DEFAULT '',
                    Username TEXT DEFAULT '',
                    Password TEXT DEFAULT '',
                    PromptUser INTEGER DEFAULT 0,
                    AutoUpdate INTEGER DEFAULT 1,
                    Extra3 INTEGER,
                    Extra4 TEXT,
                    Extra5 TEXT
                )
            ''')
            
            # Check if there are any records in the table
            self.cursor.execute(f"SELECT COUNT(*) FROM {self.TABLE_NAME}")
            count = self.cursor.fetchone()[0]
            
            # If no records exist, insert default settings
            if count == 0:
                self.cursor.execute(f'''
                    INSERT INTO {self.TABLE_NAME} (
                        UpdateOnBoot, Method, ConfScopeID, UpgScopeID, IP, 
                        ConfFilepath, UpgFilepath, Username, Password, 
                        PromptUser, AutoUpdate
                    ) VALUES (
                        0, 0, 130, 131, '', 
                        '', '', '', '', 
                        0, 1
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
            
            self.cursor.execute(f"SELECT UpdateOnBoot, AutoUpdate, Method, IP, Username, Password, UpgFilepath FROM {self.TABLE_NAME} WHERE id = 1")
            result = self.cursor.fetchone()
            
            if result:
                settings = {
                    'UpdateOnBoot': bool(result[0]),
                    'AutoUpdate': bool(result[1]),
                    'Method': result[2],
                    'IP': result[3],
                    'Username': result[4],
                    'Password': result[5],
                    'UpgFilepath': result[6]
                }
                return settings
            
            return None
        except Exception as e:
            logging.error(f"Error getting settings: {e}")
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
    
    def _ensure_table_exists(self):
        """Ensure the UpdateSettings table exists"""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS UpdateSettings (
                    UpdateOnBoot INTEGER,
                    Method INTEGER,
                    ConfScopeID INTEGER,
                    UpgScopeID INTEGER,
                    IP TEXT,
                    ConfFilepath TEXT,
                    UpgFilepath TEXT,
                    Username TEXT,
                    Password TEXT,
                    PromptUser BOOLEAN,
                    AutoUpdate BOOLEAN DEFAULT 1,
                    Extra3 INTEGER,
                    Extra4 TEXT,
                    Extra5 TEXT
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error creating table: {e}")
        finally:
            conn.close()
        
    def _ensure_default_settings(self):
        """Insert default settings if the table is empty"""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()
        
        try:
            # Check if the table is empty
            cursor.execute(f"SELECT COUNT(*) FROM {self.TABLE_NAME}")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insert default settings
                cursor.execute(f'''
                    INSERT INTO {self.TABLE_NAME} (
                        UpdateOnBoot, Method, ConfScopeID, UpgScopeID, IP, 
                        ConfFilepath, UpgFilepath, Username, Password, 
                        PromptUser, AutoUpdate
                    ) VALUES (
                        0, 0, 130, 131, '', 
                        '', '', '', '', 
                        0, 1
                    )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error checking/inserting default settings: {e}")
        finally:
            conn.close()
    
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
    
    def get_update_settings(self) -> Optional[Dict[str, Any]]:
        """Retrieve update settings from the database"""
        self.connect()
        try:
            self.cursor.execute(f"SELECT * FROM {self.TABLE_NAME}")
            settings = self.cursor.fetchone()
            
            if settings:
                keys = ["id", "UpdateOnBoot", "Method", "ConfScopeID", "UpgScopeID", "IP", "ConfFilepath", "UpgFilepath", "Username", "Password", "PromptUser", "AutoUpdate", "Extra3", "Extra4", "Extra5"]
                return dict(zip(keys, settings))
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error retrieving update settings: {e}")
            return None
        finally:
            self.disconnect()
    
    
    