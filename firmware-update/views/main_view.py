# views/main_view.py

from PySide6.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Slot, Qt, QSize
from PySide6.QtGui import QMovie
from ui.updatedialog import Ui_UpdateDialog

import os

class MainView(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_UpdateDialog()
        self.ui.setupUi(self)
        
        # Initialize loading animation
        self.loading_movie = QMovie("resources/images/loading.gif")
        self.loading_movie.setScaledSize(QSize(32, 32))
        self.ui.LB_ShowText.setMovie(self.loading_movie)
        
        # Hide LB_ShowText initially
        self.ui.LB_ShowText.setVisible(False)

        # Disable the Maximize Button from window
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        # Load the stylesheet
        self._load_stylesheet()
        
        # Initialize UI state
        self._hide_radio_buttons()
        
        # Load initial items
        self.load_combo_box_items()  # Load Upgrade Type items
        self.load_methods_combo_box_items()  # Load Methods items
        
        # Connect signals
        self.ui.CHK_UpdateOnBoot.stateChanged.connect(self._on_update_on_boot_changed)
        self.ui.CB_UpgradeType.currentIndexChanged.connect(self.handle_upgrade_type_change)
        self.ui.CB_Method.currentIndexChanged.connect(self.change_stack_widget)
        
        # Set up radio button group to ensure only one can be selected
        self._setup_radio_button_group()
        
        # Set initial visibility based on current selection
        self.handle_upgrade_type_change()
        
        # Set initial stack widget based on current method
        self.change_stack_widget(self.ui.CB_Method.currentIndex())
    
    def _setup_radio_button_group(self):
        """Set up the radio button group to ensure only one can be selected"""
        # Connect the radio buttons to each other
        self.ui.RB_UpdateOnBoot.toggled.connect(self._on_radio_button_toggled)
        self.ui.RB_PromptUser.toggled.connect(self._on_radio_button_toggled)
    
    def _on_radio_button_toggled(self, checked):
        """Handle radio button toggled event"""
        # If one radio button is checked, ensure the other is unchecked
        if checked:
            sender = self.sender()
            if sender == self.ui.RB_UpdateOnBoot:
                self.ui.RB_PromptUser.setChecked(False)
            elif sender == self.ui.RB_PromptUser:
                self.ui.RB_UpdateOnBoot.setChecked(False)
    
    @Slot(int)
    def change_stack_widget(self, index):
        """Change the stack widget based on the index"""
        method = self.ui.CB_Method.currentText()
        
        if method == "DHCP":
            self.ui.stackedWidget.setCurrentWidget(self.ui.pageDHCP)
        elif method == "HTTP" or method == "HTTPS":
            self.ui.stackedWidget.setCurrentWidget(self.ui.pageHTTPFTP)
        elif method == "FTP" or method == "FTPS ":
            self.ui.stackedWidget.setCurrentWidget(self.ui.pageHTTPFTP)
        elif method == "Local Storage":
            self.ui.stackedWidget.setCurrentWidget(self.ui.USB)
        elif method == "Peer-to-Peer":
            self.ui.stackedWidget.setCurrentWidget(self.ui.pageBuddy)
    
    # Load QSS Stylesheet
    def _load_stylesheet(self):
        """Load and apply the QSS styleshet"""
        # Get the absolute path to the stylesheet file
        stylesheet_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                          "resources", "qss", "stylesheet.qss")
        
        # Get the absolute path to the images directory
        images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                     "resources", "qss", "images")
        # Read the stylesheet file
        with open(stylesheet_path, 'r') as file:
            stylesheet = file.read()
            
        # Replace relative image paths with absolute paths
        stylesheet = stylesheet.replace('url(images/', f'url({images_dir}/')
            
        # Apply stylesheet
        QApplication.instance().setStyleSheet(stylesheet)

    def _hide_radio_buttons(self):
        """Hide the radio buttons initially"""
        self.ui.RB_UpdateOnBoot.setVisible(False)
        self.ui.RB_PromptUser.setVisible(False)
    
    def _show_radio_buttons(self):
        """Show the radio buttons"""
        self.ui.RB_UpdateOnBoot.setVisible(True)
        self.ui.RB_PromptUser.setVisible(True)

    def set_update_on_boot(self, enabled):
        """Set the update on boot checkbox state"""
        self.ui.CHK_UpdateOnBoot.setChecked(enabled)
        if enabled:
            self._show_radio_buttons()
        else:
            self._hide_radio_buttons()

    def set_auto_update(self, enabled):
        """Set the auto update radio button state"""
        if enabled:
            self.ui.RB_UpdateOnBoot.setChecked(True)
            self.ui.RB_PromptUser.setChecked(False)
        else:
            self.ui.RB_UpdateOnBoot.setChecked(False)
            self.ui.RB_PromptUser.setChecked(True)

    # Get the Ui settings
    def get_settings(self):
        """Get the current settings from the UI"""
        settings = {
            "UpdateOnBoot": self.ui.CHK_UpdateOnBoot.isChecked(),
            "AutoUpdate": self.ui.RB_UpdateOnBoot.isChecked()
        }
        
        # Get the current update method
        method = self.ui.CB_Method.currentText()
        
        # Add server URL, username, password, and upgrade file path if available
        if method in ["HTTP", "HTTPS", "FTP", "FTPS"]:
            settings["server_url"] = self.ui.LE_IP.text()
            settings["username"] = self.ui.LE_Username.text()
            settings["password"] = self.ui.LE_Password.text()
            
            # Get the upgrade file path based on the upgrade type
            if self.ui.CB_UpgradeType.currentText() == "Firmware Upgrade":
                settings["upgrade_filepath"] = self.ui.LE_UpgFilename.text()
            
        return settings
            
    # Setup connection
    def setup_connections(self, callbacks):
        """Set up signal connections"""
        # Connect checkbox and button signals
        self.ui.CHK_UpdateOnBoot.stateChanged.connect(callbacks["update_on_boot_changed"])
        self.ui.PB_Close.clicked.connect(callbacks["close_clicked"])
        self.ui.PB_Save.clicked.connect(callbacks["save_clicked"])
        self.ui.PB_SaveUpdate.clicked.connect(callbacks["save_update_clicked"])
        
        # Connect ComboBox signals
        self.ui.CB_Method.currentIndexChanged.connect(self.change_stack_widget)
        self.ui.CB_UpgradeType.currentIndexChanged.connect(self.handle_upgrade_type_change)
        
        # Connect radio button signals
        self.ui.RB_UpdateOnBoot.toggled.connect(lambda checked: callbacks["auto_update_changed"](checked))
        self.ui.RB_PromptUser.toggled.connect(lambda checked: callbacks["auto_update_changed"](not checked))
        
        
    
    # Load ComboBox items: Upgrade Type
    def load_combo_box_items(self):
        """Load items into the upgrade type ComboBox"""
        self.ui.CB_UpgradeType.addItem("Firmware Upgrade")
        self.ui.CB_UpgradeType.addItem("Configuration Upgrade")

    # Load ComboBox items: Methods
    def load_methods_combo_box_items(self):
        """Load items into the update methods ComboBox"""
        self.ui.CB_Method.clear()
        self.ui.CB_Method.addItem("DHCP")
        self.ui.CB_Method.addItem("HTTP")
        self.ui.CB_Method.addItem("HTTPS")
        self.ui.CB_Method.addItem("FTP")
        self.ui.CB_Method.addItem("FTPS")
        self.ui.CB_Method.addItem("Local Storage")
        self.ui.CB_Method.addItem("Peer-to-Peer")

    def get_update_method(self):
        """Get the selected update method from the ComboBox"""
        return self.ui.CB_Method.currentText()

    def set_update_method(self, method):
        """Set the selected update method in the ComboBox"""
        # If method is an integer, convert it to the corresponding text
        if isinstance(method, int):
            method_map = {
                0: "DHCP",
                1: "HTTP",
                2: "HTTPS",
                3: "FTP",
                4: "FTPS",
                5: "Local Storage",
                6: "Peer-to-Peer"
            }
            method = method_map.get(method, "DHCP")  # Default to DHCP if method not found
        
        # Find and set the index
        index = self.ui.CB_Method.findText(method)
        if index >= 0:
            self.ui.CB_Method.setCurrentIndex(index)

    def set_server_url(self, server_url):
        """Set the server URL in the UI"""
        self.ui.LE_IP.setText(server_url)
    
    def set_username(self, username):
        """Set the username in the UI"""
        self.ui.LE_Username.setText(username)
    
    def set_password(self, password):
        """Set the password in the UI"""
        self.ui.LE_Password.setText(password)
    
    def set_upgrade_filepath(self, filepath):
        """Set the upgrade file path in the UI based on the current upgrade type"""
        upgrade_type = self.ui.CB_UpgradeType.currentText()
        if upgrade_type == "Firmware Upgrade":
            self.ui.LE_UpgFilename.setText(filepath)
        
    def handle_upgrade_type_change(self):
        """Handle the Upgrade Type ComboBox selection change"""
        upgrade_type = self.ui.CB_UpgradeType.currentText()
        
        # Hide the PB_LVFS_Device button if the upgrade type is "Firmware Upgrade"
        if upgrade_type == "Firmware Upgrade":
            self.ui.PB_LVFS_Device.setVisible(False)
            self.ui.LB_BiosPassword.setVisible(False)
            self.ui.LE_BiosPassword.setVisible(False)
            self.ui.PB_LVFS_Refresh.setVisible(False)
        else:
            self.ui.PB_LVFS_Device.setVisible(True)
            self.ui.LB_BiosPassword.setVisible(True)
            self.ui.LE_BiosPassword.setVisible(True)
            self.ui.PB_LVFS_Refresh.setVisible(True)

    def show_error(self, message: str) -> None:
        """
        Show an error message to the user.
        
        Args:
            message: The error message to display
        """
        QMessageBox.critical(self, "Error", message)
    
    def show_success(self, message: str) -> None:
        """
        Show a success message to the user.
        
        Args:
            message: The success message to display
        """
        QMessageBox.information(self, "Success", message)

    def _on_update_on_boot_changed(self, state):
        """Handle CHK_UpdateOnBoot state change."""
        if state == Qt.Checked:
            self._show_radio_buttons()
        else:
            self._hide_radio_buttons()

    def show_loading(self, show: bool = True):
        """Show or hide the loading animation"""
        if show:
            self.ui.LB_ShowText.setVisible(True)
            if not self.loading_movie.isValid():
                self.loading_movie.setFileName("resources/images/loading.gif")
            self.loading_movie.jumpToFrame(0)  # Reset to first frame
            self.loading_movie.start()
        else:
            self.loading_movie.stop()
            self.ui.LB_ShowText.setVisible(False)