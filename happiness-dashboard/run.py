import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.main import create_dash_app

# Run the application
if __name__ == "__main__":
    app = create_dash_app()
    app.run_server(host='0.0.0.0', port=8050, debug=True)
