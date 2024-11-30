import os
import sys
import flask

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.main import create_dash_app

# Run the application
if __name__ == "__main__":
    app = create_dash_app()

    # Override Dash's default server run method to customize the startup message
    original_run = app.server.run


    def custom_run(*args, **kwargs):
        # Clear the terminal (optional)
        print('\033c', end='')
        print("Dash is running on http://127.0.0.1:8050/")
        return original_run(*args, **kwargs)


    app.server.run = custom_run

    app.run_server(host='0.0.0.0', port=8050, debug=True)