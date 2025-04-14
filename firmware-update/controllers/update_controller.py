# controllers/update_controller.py

from PySide6.QtCore import Qt
from models.update_model import UpdateModel
from utils.logger import Logger
from processes.protocols import ProtocolFactory, NetworkSettings


class UpdateController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.logger = Logger()
        
        # Set up signal connections
        callbacks = {
            "update_on_boot_changed": self._on_update_on_boot_changed,
            "auto_update_changed": self._on_auto_update_changed,
            "close_clicked": self._on_close_clicked,
            "save_clicked": self._on_save_clicked,
            "save_update_clicked": self._on_save_update_clicked
        }
        self.view.setup_connections(callbacks)
        
        # Load initial settings
        self._load_initial_settings()
        
        # Show the view
        self.view.show()
    
    def _setup_connections(self):
        """Connect view signals to controller methods"""
        callbacks = {
            "update_on_boot_changed": self.on_update_on_boot_changed,
            "close_clicked": self.on_close_clicked,
            "save_clicked": self.on_save_clicked,
            "save_update_clicked": self._on_save_update_clicked
        }
        self.view.setup_connections(callbacks)
    
    def _load_initial_settings(self):
        """Load initial settings from the database"""
        # Load update on boot setting
        update_on_boot = self.model.get_update_on_boot()
        self.view.set_update_on_boot(update_on_boot)
        
        # Load auto update setting
        auto_update = self.model.get_auto_update()
        self.view.set_auto_update(auto_update)
        
        # Load update method
        update_method = self.model.get_update_method()
        self.view.set_update_method(update_method)
        
        # Load server URL
        server_url = self.model.get_server_url()
        if server_url:
            self.view.set_server_url(server_url)
        
        # Load username
        username = self.model.get_username()
        if username:
            self.view.set_username(username)
        
        # Load password
        password = self.model.get_password()
        if password:
            self.view.set_password(password)
        
        # Load upgrade file path
        upgrade_filepath = self.model.get_upgrade_filepath()
        if upgrade_filepath:
            self.view.set_upgrade_filepath(upgrade_filepath)
    
    def _set_update_method(self, method):
        """Set the update method in the UI"""
        # Convert method index to string representation
        method_map = {
            0: "DHCP",
            1: "HTTP",
            2: "HTTPS",
            3: "FTP",
            4: "FTPS",
            5: "Local Storage",
            6: "Peer-to-Peer"
        }
        method_text = method_map.get(method, "DHCP")  # Default to DHCP if method not found
        
        # Find the index of the method text in the ComboBox
        index = self.view.ui.CB_Method.findText(method_text)
        if index >= 0:
            self.view.ui.CB_Method.setCurrentIndex(index)
    
    def on_update_on_boot_changed(self, state):
        """Handle CHK_UpdateOnBoot state change."""
        is_checked = state == 2  # 2 is the value for Checked state
        
        # Show/hide radio buttons based on checkbox state
        if is_checked:
            self.view._show_radio_buttons()
        else:
            self.view._hide_radio_buttons()
    
    def on_save_clicked(self):
        """Handle Save button click"""
        self._save_settings()
    
    def _on_save_update_clicked(self):
        """Handle Save & Update button click"""
        # Show loading animation immediately
        self.view.show_loading(True)

        
        self.logger.info("Save & Update clicked")
        # Get the current text of the ComboBox
        method_text = self.view.ui.CB_Method.currentText()
        self.logger.info(f"Selected method: {method_text}")

        # Handle HTTP/HTTPS update
        if method_text.upper() in ["HTTP", "HTTPS"]:
            try:
                # Get HTTP handler from factory
                handler = ProtocolFactory.get_handler(method_text)
                if not handler:
                    self.logger.error(f"Unsupported update method: {method_text}")
                    self.view.show_error(f"Unsupported update method: {method_text}")
                    return
                
                # Create settings object with values from UI
                settings = NetworkSettings(
                    server_url=self.view.ui.LE_IP.text().strip(),
                    username=self.view.ui.LE_Username.text().strip(),
                    password=self.view.ui.LE_Password.text().strip(),
                    firmware_path=self.view.ui.LE_UpgFilename.text().strip(),
                    is_secure=False  # HTTP is not secure
                )
                
                # Execute update process - this will handle all validations
                is_success, message = handler.execute_update(settings)
                if not is_success:
                    raise ValueError(message)
                else:
                    # Save the settings in the database
                    self._save_settings()
                    self.logger.info(f"Update process completed successfully: {message}")
                    self.view.show_success(message)
            except ValueError as e:
                # Show validation errors
                self.logger.error(str(e))
                self.view.show_error(str(e))
            except Exception as e:
                # Show other errors
                self.logger.error(f"Update process failed: {str(e)}")
                self.view.show_error(f"Update process failed: {str(e)}")
            finally:
                # Hide loading animation
                self.view.show_loading(False)
        elif method_text.upper() in ["FTP", "FTPS"]:
            try:
                # Get FTP handler from factory
                handler = ProtocolFactory.get_handler(method_text)
                if not handler:
                    self.logger.error(f"Unsupported update method: {method_text}")
                    self.view.show_error(f"Unsupported update method: {method_text}")
                    return
                # Create settings object with values from UI
                settings = NetworkSettings(
                    server_url=self.view.ui.LE_IP.text().strip(),
                    username=self.view.ui.LE_Username.text().strip(),
                    password=self.view.ui.LE_Password.text().strip(),
                    firmware_path=self.view.ui.LE_UpgFilename.text().strip(),
                    is_secure=False  # FTP is not secure
                )
                # Execute update process - this will handle all validations
                is_success, message = handler.execute_update(settings)
                if not is_success:
                    raise ValueError(message)
                else:
                    # Save the settings in the database
                    self._save_settings()
                    self.logger.info(f"Update process completed successfully: {message}")
                    self.view.show_success(message)
            except ValueError as e:
                # Show validation errors
                self.logger.error(str(e))
                self.view.show_error(str(e))
            except Exception as e:
                # Show other errors
                self.logger.error(f"Update process failed: {str(e)}")
                self.view.show_error(f"Update process failed: {str(e)}")
            finally:
                # Hide loading animation
                self.view.show_loading(False)
        else:
            self.logger.error(f"Method {method_text} not implemented yet")
            self.view.show_error(f"Method {method_text} not implemented yet")
            # Hide loading animation
            self.view.show_loading(False)
    
    def _save_settings(self):
        print("Saving settings...")
        """Save current settings to the database"""
        settings = self.view.get_settings()
        
        # Save UpdateOnBoot setting
        update_on_boot = settings.get('UpdateOnBoot', False)
        self.model.save_update_on_boot(update_on_boot)
        
        # Save AutoUpdate setting
        auto_update = settings.get('AutoUpdate', True)
        self.model.save_auto_update(auto_update)
        
        # Save UpdateMethod setting
        # Get the current index of the ComboBox
        method_index = self.view.ui.CB_Method.currentIndex()
        self.model.save_update_method(method_index)
        
        # Save server URL if available
        if 'server_url' in settings:
            server_url = settings.get('server_url', '')
            self.model.save_server_url(server_url)
        
        # Save username if available
        if 'username' in settings:
            username = settings.get('username', '')
            self.model.save_username(username)
        
        # Save password if available
        if 'password' in settings:
            password = settings.get('password', '')
            self.model.save_password(password)
        
        # Save upgrade file path if available
        if 'upgrade_filepath' in settings:
            upgrade_filepath = settings.get('upgrade_filepath', '')
            self.model.save_upgrade_filepath(upgrade_filepath)
    
    def on_close_clicked(self):
        """Handle close button click."""
        self.view.close()

    def get_update_method(self):
        """Get the UpdateMethod setting from the model"""
        return self.model.get_update_method()

    def save_update_method(self, method):
        """Save the UpdateMethod setting to the model"""
        return self.model.save_update_method(method)

    def _on_update_on_boot_changed(self, state):
        """Handle CHK_UpdateOnBoot state change."""
        is_checked = state == 2  # 2 is the value for Checked state
        
        # Show/hide radio buttons based on checkbox state
        if is_checked:
            self.view._show_radio_buttons()
        else:
            self.view._hide_radio_buttons()

    def _on_auto_update_changed(self, state):
        """Handle CHK_AutoUpdate state change."""
        is_checked = state == 2  # 2 is the value for Checked state
        self.model.save_auto_update(is_checked)

    def _on_close_clicked(self):
        """Handle close button click."""
        self.view.close()

    def _on_save_clicked(self):
        """Handle Save button click"""
        self._save_settings()

    def _on_server_url_changed(self, text):
        """Handle server URL text change."""
        self.model.save_server_url(text)

    def _on_username_changed(self, text):
        """Handle username text change."""
        self.model.save_username(text)

    def _on_password_changed(self, text):
        """Handle password text change."""
        self.model.save_password(text)

    def _on_upgrade_filepath_changed(self, text):
        """Handle upgrade file path text change."""
        self.model.save_upgrade_filepath(text)