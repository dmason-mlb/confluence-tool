#!/usr/bin/env python3
"""
Page Operations Examples

Demonstrates common page operations using the Confluence API v2.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from confluence_client import ConfluenceClient
from datetime import datetime
import json


def create_simple_page(client: ConfluenceClient, space_id: int):
    """Create a simple page."""
    print("\n=== Creating Simple Page ===")
    
    page = client.create_page(
        space_id=space_id,
        title=f"API Test Page - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        content="""
        <h1>Welcome to Confluence API</h1>
        <p>This page was created using the Confluence REST API v2.</p>
        <ul>
            <li>Feature 1</li>
            <li>Feature 2</li>
            <li>Feature 3</li>
        </ul>
        """
    )
    
    print(f"Created page: {page['title']} (ID: {page['id']})")
    return page


def create_page_with_table(client: ConfluenceClient, space_id: int):
    """Create a page with a table."""
    print("\n=== Creating Page with Table ===")
    
    content = """
    <h1>Project Status Report</h1>
    <table>
        <thead>
            <tr>
                <th>Project</th>
                <th>Status</th>
                <th>Owner</th>
                <th>Due Date</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Website Redesign</td>
                <td><ac:structured-macro ac:name="status">
                    <ac:parameter ac:name="colour">Green</ac:parameter>
                    <ac:parameter ac:name="title">On Track</ac:parameter>
                </ac:structured-macro></td>
                <td>John Doe</td>
                <td>2025-03-15</td>
            </tr>
            <tr>
                <td>Mobile App</td>
                <td><ac:structured-macro ac:name="status">
                    <ac:parameter ac:name="colour">Yellow</ac:parameter>
                    <ac:parameter ac:name="title">At Risk</ac:parameter>
                </ac:structured-macro></td>
                <td>Jane Smith</td>
                <td>2025-04-01</td>
            </tr>
        </tbody>
    </table>
    """
    
    page = client.create_page(
        space_id=space_id,
        title=f"Status Report - {datetime.now().strftime('%Y-%m-%d')}",
        content=content
    )
    
    print(f"Created page: {page['title']} (ID: {page['id']})")
    return page


def create_page_hierarchy(client: ConfluenceClient, space_id: int):
    """Create a hierarchy of pages."""
    print("\n=== Creating Page Hierarchy ===")
    
    # Create parent page
    parent = client.create_page(
        space_id=space_id,
        title="Documentation Hub",
        content="<h1>Documentation Hub</h1><p>Central location for all documentation.</p>"
    )
    print(f"Created parent: {parent['title']} (ID: {parent['id']})")
    
    # Create child pages
    sections = ["Getting Started", "API Reference", "Best Practices", "FAQ"]
    
    for section in sections:
        child = client.create_page(
            space_id=space_id,
            title=section,
            content=f"<h1>{section}</h1><p>Content for {section} section.</p>",
            parent_id=parent['id']
        )
        print(f"  Created child: {child['title']} (ID: {child['id']})")
    
    return parent


def update_page_content(client: ConfluenceClient, page_id: str):
    """Update an existing page."""
    print("\n=== Updating Page ===")
    
    # Get current page version
    page = client.get_page(page_id)
    current_version = page['version']['number']
    
    # Update content
    updated = client.update_page(
        page_id=page_id,
        title=page['title'] + " (Updated)",
        content="""
        <h1>Updated Content</h1>
        <p>This page was updated via the API at {}</p>
        <p>Previous version: {}</p>
        """.format(datetime.now().isoformat(), current_version),
        version=current_version,
        version_message="Updated via API script"
    )
    
    print(f"Updated page: {updated['title']} (Version: {updated['version']['number']})")
    return updated


def add_page_labels(client: ConfluenceClient, page_id: str):
    """Add labels to a page."""
    print("\n=== Adding Labels ===")
    
    labels = ["api-created", "automated", "python", "v2-api"]
    result = client.add_labels(page_id, labels)
    
    print(f"Added {len(labels)} labels to page {page_id}")
    
    # Get and display labels
    page_labels = client.get_labels(page_id)
    print(f"Current labels: {[label['name'] for label in page_labels]}")


def search_pages(client: ConfluenceClient, space_key: str):
    """Search for pages using CQL."""
    print("\n=== Searching Pages ===")
    
    # Search queries
    queries = [
        f"space = {space_key} AND type = page",
        f"space = {space_key} AND title ~ 'API'",
        f"space = {space_key} AND created >= now('-7d')",
        f"space = {space_key} AND label = 'api-created'"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        results = client.search_pages(query, limit=5)
        
        for page in results:
            print(f"  - {page['title']} (ID: {page['id']})")


def create_page_with_macros(client: ConfluenceClient, space_id: int):
    """Create a page with Confluence macros."""
    print("\n=== Creating Page with Macros ===")
    
    content = """
    <h1>Page with Macros</h1>
    
    <ac:structured-macro ac:name="info">
        <ac:rich-text-body>
            <p>This is an info panel created via API.</p>
        </ac:rich-text-body>
    </ac:structured-macro>
    
    <ac:structured-macro ac:name="code">
        <ac:parameter ac:name="language">python</ac:parameter>
        <ac:plain-text-body><![CDATA[
def hello_world():
    print("Hello from Confluence!")
    return True
        ]]></ac:plain-text-body>
    </ac:structured-macro>
    
    <ac:structured-macro ac:name="expand">
        <ac:parameter ac:name="title">Click to expand</ac:parameter>
        <ac:rich-text-body>
            <p>Hidden content that expands when clicked.</p>
        </ac:rich-text-body>
    </ac:structured-macro>
    """
    
    page = client.create_page(
        space_id=space_id,
        title="Macro Examples",
        content=content
    )
    
    print(f"Created page: {page['title']} (ID: {page['id']})")
    return page


def copy_page_to_space(client: ConfluenceClient, source_page_id: str, target_space_id: int):
    """Copy a page to another space."""
    print("\n=== Copying Page ===")
    
    copied = client.copy_page(
        source_id=source_page_id,
        target_space_id=target_space_id,
        new_title="Copied Page - " + datetime.now().strftime('%Y-%m-%d')
    )
    
    print(f"Copied page: {copied['title']} (ID: {copied['id']})")
    return copied


def main():
    """Run page operation examples."""
    # Configuration
    DOMAIN = os.getenv('CONFLUENCE_DOMAIN', 'your-domain.atlassian.net')
    EMAIL = os.getenv('CONFLUENCE_EMAIL', 'your-email@example.com')
    API_TOKEN = os.getenv('CONFLUENCE_API_TOKEN', 'your-api-token')
    SPACE_ID = int(os.getenv('CONFLUENCE_SPACE_ID', '123456'))
    SPACE_KEY = os.getenv('CONFLUENCE_SPACE_KEY', 'TEST')
    
    # Initialize client
    client = ConfluenceClient(DOMAIN, EMAIL, API_TOKEN)
    
    try:
        # Run examples
        page1 = create_simple_page(client, SPACE_ID)
        page2 = create_page_with_table(client, SPACE_ID)
        parent = create_page_hierarchy(client, SPACE_ID)
        
        # Update and label the first page
        update_page_content(client, page1['id'])
        add_page_labels(client, page1['id'])
        
        # Create page with macros
        macro_page = create_page_with_macros(client, SPACE_ID)
        
        # Search for pages
        search_pages(client, SPACE_KEY)
        
        print("\n=== All operations completed successfully! ===")
        
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()