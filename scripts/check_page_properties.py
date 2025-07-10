#!/usr/bin/env python3
"""
Check content properties of a Confluence page.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from confluence_client import ConfluenceClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_page_properties(page_id):
    """Check properties of a specific page."""
    
    # Load configuration
    from config import get_config
    config = get_config()
    if not config:
        sys.exit(1)
    
    DOMAIN = config['domain']
    EMAIL = config['email'] 
    API_TOKEN = config['api_token']
    
    # Initialize client
    client = ConfluenceClient(DOMAIN, EMAIL, API_TOKEN)
    
    try:
        # Get all properties
        logger.info(f"Getting properties for page {page_id}...")
        properties = client.get_content_properties(page_id)
        
        if not properties:
            logger.info("No properties found on this page")
        else:
            logger.info(f"Found {len(properties)} properties:")
            for prop in properties:
                logger.info(f"  - Key: {prop.get('key')}, ID: {prop.get('id')}")
                
                # Get editor property details if it exists
                if prop.get('key') == 'editor':
                    try:
                        editor_prop = client.get_content_property(page_id, 'editor')
                        logger.info(f"    Editor property value: {editor_prop.get('value')}")
                    except Exception as e:
                        logger.error(f"    Could not get editor property details: {e}")
        
        # Also get the page details
        page = client.get_page(page_id)
        logger.info(f"\nPage title: {page['title']}")
        logger.info(f"Page version: {page['version']['number']}")
        
    except Exception as e:
        logger.error(f"Error checking page properties: {e}")
        raise


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Use the last created page ID as default
        page_id = "4940267532"
        print(f"Usage: python3 {sys.argv[0]} <page_id>")
        print(f"Using default page ID: {page_id}")
    else:
        page_id = sys.argv[1]
    
    check_page_properties(page_id)