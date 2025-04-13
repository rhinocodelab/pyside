# main.py

import sys
from PySide6.QtWidgets import QApplication
from views.main_view import MainView
from controllers.update_controller import UpdateController
from models.update_model import UpdateModel

def main():
    app = QApplication(sys.argv)
    
    # Create model and view instances
    model = UpdateModel()
    view = MainView()
    
    # Create controller with both view and model
    controller = UpdateController(view, model)
    
    # Show the view
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()