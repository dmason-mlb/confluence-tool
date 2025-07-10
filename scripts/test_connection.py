#!/usr/bin/env python3
"""
Test connection to Confluence and list available spaces.
This helps verify your credentials are working.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from confluence_client import ConfluenceClient
from config import get_config
import json


def test_connection():
    """Test connection and list available spaces."""
    
    # Load configuration
    config = get_config()
    if not config:
        sys.exit(1)
    
    DOMAIN = config['domain']
    EMAIL = config['email']
    API_TOKEN = config['api_token']
    
    print(f"Testing connection to {DOMAIN}...")
    print(f"Using email: {EMAIL}")
    print("")
    
    try:
        # Initialize client
        client = ConfluenceClient(DOMAIN, EMAIL, API_TOKEN)
        
        # Note: v2 API doesn't have a current user endpoint
        print("1. Authentication configured with:")
        print(f"   Email: {EMAIL}")
        print("")
        
        # Test: List spaces (this will verify authentication is working)
        print("2. Testing connection by fetching available spaces...")
        spaces = client.get_spaces(limit=10)
        
        if spaces:
            print(f"✓ Found {len(spaces)} spaces:")
            print("")
            print(f"{'Space Name':<30} {'Key':<10} {'ID':<10} {'Type':<10}")
            print("-" * 70)
            
            for space in spaces:
                name = space.get('name', 'Unknown')[:29]
                key = space.get('key', 'Unknown')
                space_id = space.get('id', 'Unknown')
                space_type = space.get('type', 'Unknown')
                print(f"{name:<30} {key:<10} {space_id:<10} {space_type:<10}")
            
            print("")
            print("You can use any of these Space IDs for testing:")
            print(f"export CONFLUENCE_SPACE_ID={spaces[0].get('id', 'Unknown')}")
            
        else:
            print("✗ No spaces found. You may need to create a space first.")
        
        print("")
        print("Connection test successful! ✓")
        return True
        
    except Exception as e:
        print(f"✗ Connection test failed: {e}")
        print("")
        print("Troubleshooting:")
        print("1. Verify your API token at: https://id.atlassian.com/manage-profile/security/api-tokens")
        print("2. Check your domain includes .atlassian.net")
        print("3. Ensure your email matches your Atlassian account")
        return False


if __name__ == "__main__":
    test_connection()