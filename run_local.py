#!/usr/bin/env python3
"""
TALYOUTH SDG Leadership Program - Local Development Server
Run this file to start the application locally
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables if .env exists
if os.path.exists('.env'):
    load_dotenv()

# Set default environment variables for local development
os.environ.setdefault('FLASK_ENV', 'development')
os.environ.setdefault('FLASK_DEBUG', 'True')
os.environ.setdefault('SESSION_SECRET', 'talyouth-local-dev-secret-2024')
os.environ.setdefault('DATABASE_URL', 'sqlite:///talyouth.db')

from app_local import create_app

def main():
    """Main function to run the local development server"""
    app = create_app()
    
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    
    print("=" * 60)
    print("TALYOUTH SDG Leadership Program - Local Development Server")
    print("=" * 60)
    print(f"Server starting on: http://localhost:{port}")
    print(f"Debug mode: {debug}")
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        app.run(host='127.0.0.1', port=port, debug=debug)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()