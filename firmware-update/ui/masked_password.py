from PySide6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon

class Leforpassword(QWidget):
    """A custom password input widget with a toggle button to show/hide password."""
    
    # Define signals
    textChanged = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Create line edit
        self.line_edit = QLineEdit(self)
        self.line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Create toggle button
        self.toggle_button = QPushButton(self)
        self.toggle_button.setFixedSize(27, 27)  # More compact size
        self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_button.setIcon(QIcon("./resources/images/eye-closed.png"))
        self.toggle_button.setIconSize(QSize(14, 14))  # Smaller icon
        self.toggle_button.clicked.connect(self.toggle_password_visibility)
        
        # Add widgets to layout
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.toggle_button)
        
        # Connect text changed signal
        self.line_edit.textChanged.connect(self.on_text_changed)
        
        # Set the same style as QLineEdit
        self.setStyleSheet("""
            Leforpassword {
                background-color: transparent;
            }
            Leforpassword QLineEdit {
                border: 1px solid #9c9a9c;
                border-right: none;
                background: white;
                padding-left: 8px;
                padding-right: 0px;
            }
            Leforpassword QPushButton {
                border: 1px solid #9c9a9c;
                border-left: none;
                background: white;
                margin: 0px;
                padding: 0px;
            }
        """)
    
    def setFixedSize(self, width, height):
        """Override setFixedSize to properly size the internal QLineEdit."""
        super().setFixedSize(width, height)
        # Calculate QLineEdit width by subtracting button width and any margins
        line_edit_width = width - self.toggle_button.width()
        self.line_edit.setFixedSize(line_edit_width, height)
    
    def resizeEvent(self, event):
        """Handle resize events to ensure proper internal widget sizing."""
        super().resizeEvent(event)
        # Ensure QLineEdit fills available space minus button width
        available_width = self.width() - self.toggle_button.width()
        self.line_edit.setFixedSize(available_width, self.height())
        
    def on_text_changed(self, text):
        """Handle text changes in the line edit."""
        # Emit text changed signal
        self.textChanged.emit(text)
        
        if text:
            # When text is entered, show eye-open icon
            self.toggle_button.setIcon(QIcon("./resources/images/eye-open.png"))
        else:
            # When field is empty, reset to password mode and show eye-closed icon
            self.line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_button.setIcon(QIcon("./resources/images/eye-closed.png"))
            
    def toggle_password_visibility(self):
        """Toggle between password and plain text mode."""
        if self.line_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_button.setIcon(QIcon("./resources/images/eye-open.png"))
        else:
            self.line_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_button.setIcon(QIcon("./resources/images/eye-closed.png"))
            
    def text(self):
        """Get the current text."""
        return self.line_edit.text()
        
    def setText(self, text):
        """Set the text."""
        self.line_edit.setText(text)
        
    def setPlaceholderText(self, text):
        """Set the placeholder text."""
        self.line_edit.setPlaceholderText(text)
        
    def setMaxLength(self, length):
        """Set the maximum text length."""
        self.line_edit.setMaxLength(length)
        
    def setFocusPolicy(self, policy):
        """Set the focus policy."""
        self.line_edit.setFocusPolicy(policy)
        
    def setEnabled(self, enabled):
        """Enable or disable the widget."""
        super().setEnabled(enabled)
        self.line_edit.setEnabled(enabled)
        self.toggle_button.setEnabled(enabled)
        
    def clear(self):
        """Clear the text."""
        self.line_edit.clear()
    
