#!/usr/bin/env python3
"""
Configuration loader for Confluence scripts.
Loads from .env file first, then falls back to environment variables.
"""

import os
from pathlib import Path


def load_dotenv(env_file='.env'):
    """
    Simple .env file loader.
    Loads KEY=VALUE pairs from a .env file into environment variables.
    """
    # Try to find .env file
    env_path = Path(env_file)
    
    # If not found in current dir, try parent directory (for scripts in subdirs)
    if not env_path.exists():
        parent_env = Path(__file__).parent.parent / '.env'
        if parent_env.exists():
            env_path = parent_env
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    # Handle KEY=VALUE format
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Remove quotes if present
                        if value and value[0] in '"\'':
                            value = value.strip('"\'')
                        # Only set if not already in environment
                        if key and not os.getenv(key):
                            os.environ[key] = value
        return True
    return False


def get_config():
    """
    Get Confluence configuration from .env or environment variables.
    Returns a dictionary with the configuration values.
    """
    # Try to load from .env file first
    load_dotenv()
    
    config = {
        'domain': os.getenv('CONFLUENCE_DOMAIN'),
        'email': os.getenv('CONFLUENCE_EMAIL'),
        'api_token': os.getenv('CONFLUENCE_API_TOKEN'),
        'space_id': os.getenv('CONFLUENCE_SPACE_ID'),
        'space_key': os.getenv('CONFLUENCE_SPACE_KEY')
    }
    
    # Check required fields
    required = ['domain', 'email', 'api_token']
    missing = [k for k in required if not config[k]]
    
    if missing:
        print("Missing required configuration:")
        for field in missing:
            env_var = f"CONFLUENCE_{field.upper()}"
            print(f"  - {env_var}")
        print("\nPlease run: ./setup_env.sh")
        print("Or set the environment variables manually.")
        return None
    
    # Convert space_id to int if present
    if config['space_id']:
        try:
            config['space_id'] = int(config['space_id'])
        except ValueError:
            print(f"Warning: CONFLUENCE_SPACE_ID should be numeric, got: {config['space_id']}")
            config['space_id'] = None
    
    return config


def print_config(config, hide_token=True):
    """Print configuration summary."""
    print("Configuration:")
    print(f"  Domain: {config['domain']}")
    print(f"  Email: {config['email']}")
    if hide_token:
        print(f"  API Token: {'*' * 10}")
    else:
        print(f"  API Token: {config['api_token']}")
    if config['space_id']:
        print(f"  Space ID: {config['space_id']}")
    if config['space_key']:
        print(f"  Space Key: {config['space_key']}")


if __name__ == "__main__":
    # Test configuration loading
    config = get_config()
    if config:
        print("✅ Configuration loaded successfully!")
        print_config(config)
    else:
        print("❌ Configuration loading failed!")