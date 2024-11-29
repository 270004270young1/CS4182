import os
import sys

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, whether running as a script or as an executable.
    """
    if getattr(sys, 'frozen', False):
        # Running in a bundle (PyInstaller)
        base_path = sys._MEIPASS  # Temporary directory created by PyInstaller
    else:
        # Running in a normal Python environment
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.path.pardir)
        # base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)