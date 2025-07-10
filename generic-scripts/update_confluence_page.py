#!/usr/bin/env python3
"""
Generic script to update an existing Confluence page.

This script can be called from any repository to update a Confluence page.
It supports reading content from files, stdin, or command line arguments.

Usage:
    # Update page with content from file
    python update_confluence_page.py --page-id 123456 --file content.md
    
    # Update page title and content
    python update_confluence_page.py --page-id 123456 --title "New Title" --file content.html
    
    # Update from stdin
    echo "# Updated Content" | python update_confluence_page.py --page-id 123456
    
    # Append content to existing page
    python update_confluence_page.py --page-id 123456 --append --content "Additional section"
    
    # Find page by title and update
    python update_confluence_page.py --space-id 789 --find-title "My Page" --file content.md

Environment Variables:
    CONFLUENCE_DOMAIN: Your Confluence domain (e.g., 'yoursite.atlassian.net')
    CONFLUENCE_EMAIL: Your email address
    CONFLUENCE_API_TOKEN: Your API token
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Add parent directory to path to import confluence_client
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from scripts.confluence_client import ConfluenceClient
except ImportError:
    print("Error: Could not import ConfluenceClient. Make sure this script is in the confluence-tool repository.")
    sys.exit(1)


def get_credentials():
    """
    Get Confluence credentials from environment variables.
    
    Returns:
        tuple: (domain, email, api_token) or None if not found
    """
    domain = os.environ.get('CONFLUENCE_DOMAIN')
    email = os.environ.get('CONFLUENCE_EMAIL')
    api_token = os.environ.get('CONFLUENCE_API_TOKEN')
    
    if not all([domain, email, api_token]):
        missing = []
        if not domain:
            missing.append('CONFLUENCE_DOMAIN')
        if not email:
            missing.append('CONFLUENCE_EMAIL')
        if not api_token:
            missing.append('CONFLUENCE_API_TOKEN')
        
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        print("\nPlease set the following environment variables:")
        print("  export CONFLUENCE_DOMAIN='yoursite.atlassian.net'")
        print("  export CONFLUENCE_EMAIL='your-email@example.com'")
        print("  export CONFLUENCE_API_TOKEN='your-api-token'")
        print("\nGet your API token from: https://id.atlassian.com/manage-profile/security/api-tokens")
        return None
    
    return domain, email, api_token


def read_content(args):
    """
    Read content from file, stdin, or command line argument.
    
    Args:
        args: Parsed command line arguments
        
    Returns:
        str: Content to update page with
    """
    if args.file:
        # Read from file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if it's markdown and needs conversion
        if file_path.suffix.lower() in ['.md', '.markdown']:
            if args.format == 'auto':
                args.format = 'markdown'
                
    elif args.content:
        # Use inline content
        content = args.content
        
    else:
        # Read from stdin
        if sys.stdin.isatty():
            print("Error: No content provided. Use --file, --content, or pipe content via stdin.")
            sys.exit(1)
        content = sys.stdin.read()
    
    return content


def convert_markdown_to_storage(markdown_content):
    """
    Basic conversion from Markdown to Confluence storage format.
    
    This is a simple converter that handles common Markdown elements.
    For more complex conversions, consider using a dedicated library.
    
    Args:
        markdown_content: Markdown formatted text
        
    Returns:
        str: Confluence storage format HTML
    """
    import re
    
    # Start with the markdown content
    html = markdown_content
    
    # Convert headers (must be done before other conversions)
    html = re.sub(r'^###### (.+)$', r'<h6>\1</h6>', html, flags=re.MULTILINE)
    html = re.sub(r'^##### (.+)$', r'<h5>\1</h5>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Convert bold and italic
    html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    html = re.sub(r'__(.+?)__', r'<strong>\1</strong>', html)
    html = re.sub(r'_(.+?)_', r'<em>\1</em>', html)
    
    # Convert inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Convert code blocks
    def replace_code_block(match):
        lang = match.group(1) or 'text'
        code = match.group(2)
        return f'''<ac:structured-macro ac:name="code">
    <ac:parameter ac:name="language">{lang}</ac:parameter>
    <ac:plain-text-body><![CDATA[{code}]]></ac:plain-text-body>
</ac:structured-macro>'''
    
    html = re.sub(r'```(\w*)\n(.*?)```', replace_code_block, html, flags=re.DOTALL)
    
    # Convert links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    
    # Convert unordered lists
    lines = html.split('\n')
    in_list = False
    new_lines = []
    
    for line in lines:
        if re.match(r'^\* ', line):
            if not in_list:
                new_lines.append('<ul>')
                in_list = True
            new_lines.append(f'<li>{line[2:]}</li>')
        elif re.match(r'^\d+\. ', line):
            if in_list and new_lines[-1] == '</ul>':
                new_lines.pop()
            if not in_list or new_lines[-1] == '</ul>':
                new_lines.append('<ol>')
                in_list = True
            content = re.sub(r'^\d+\. ', '', line)
            new_lines.append(f'<li>{content}</li>')
        else:
            if in_list:
                if '<ul>' in new_lines[-2]:
                    new_lines.append('</ul>')
                else:
                    new_lines.append('</ol>')
                in_list = False
            new_lines.append(line)
    
    if in_list:
        if '<ul>' in new_lines[-2]:
            new_lines.append('</ul>')
        else:
            new_lines.append('</ol>')
    
    html = '\n'.join(new_lines)
    
    # Convert line breaks to paragraphs
    paragraphs = []
    current_para = []
    
    for line in html.split('\n'):
        if line.strip() == '':
            if current_para:
                para_content = ' '.join(current_para)
                if not re.match(r'^<[hpulo]', para_content):
                    para_content = f'<p>{para_content}</p>'
                paragraphs.append(para_content)
                current_para = []
        else:
            current_para.append(line)
    
    if current_para:
        para_content = ' '.join(current_para)
        if not re.match(r'^<[hpulo]', para_content):
            para_content = f'<p>{para_content}</p>'
        paragraphs.append(para_content)
    
    return '\n'.join(paragraphs)


def find_page_by_title(client, space_id, title):
    """
    Find a page by title in a specific space.
    
    Args:
        client: ConfluenceClient instance
        space_id: Space ID to search in
        title: Page title to find
        
    Returns:
        dict: Page data or None if not found
    """
    # Use CQL to search for exact title match in space
    cql = f'space={space_id} AND title="{title}"'
    results = client.search_pages(cql, limit=1)
    
    if results:
        return results[0]
    
    return None


def main():
    """Main function to update a Confluence page."""
    parser = argparse.ArgumentParser(
        description='Update an existing Confluence page',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Page identification (one required)
    id_group = parser.add_mutually_exclusive_group(required=True)
    id_group.add_argument('--page-id', type=int, help='Page ID to update')
    id_group.add_argument('--find-title', help='Find page by title (requires --space-id)')
    
    # Space ID for title search
    parser.add_argument('--space-id', type=int, 
                       help='Space ID (required when using --find-title)')
    
    # Content source (one required unless using --append with existing content)
    content_group = parser.add_mutually_exclusive_group()
    content_group.add_argument('--file', help='Read content from file')
    content_group.add_argument('--content', help='Inline content')
    
    # Optional arguments
    parser.add_argument('--title', help='New page title (optional)')
    parser.add_argument('--append', action='store_true',
                       help='Append content to existing page instead of replacing')
    parser.add_argument('--prepend', action='store_true',
                       help='Prepend content to existing page instead of replacing')
    parser.add_argument('--format', choices=['storage', 'markdown', 'auto'], default='auto',
                       help='Content format (auto-detects based on file extension)')
    parser.add_argument('--version-message', help='Version comment for the update')
    parser.add_argument('--json', action='store_true',
                       help='Output result as JSON')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be updated without actually updating')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.find_title and not args.space_id:
        print("Error: --space-id is required when using --find-title")
        sys.exit(1)
    
    if args.append and args.prepend:
        print("Error: Cannot use both --append and --prepend")
        sys.exit(1)
    
    # Get credentials
    creds = get_credentials()
    if not creds:
        sys.exit(1)
    
    domain, email, api_token = creds
    
    # Create client
    try:
        client = ConfluenceClient(domain, email, api_token)
    except Exception as e:
        print(f"Error initializing Confluence client: {e}")
        sys.exit(1)
    
    # Find page if searching by title
    if args.find_title:
        page = find_page_by_title(client, args.space_id, args.find_title)
        if not page:
            print(f"Error: No page found with title '{args.find_title}' in space {args.space_id}")
            sys.exit(1)
        page_id = page['id']
    else:
        page_id = args.page_id
    
    # Get current page data
    try:
        current_page = client.get_page(page_id, expand=['body.storage'])
    except Exception as e:
        print(f"Error getting page {page_id}: {e}")
        sys.exit(1)
    
    # Determine new content
    if args.append or args.prepend:
        # Read new content to append/prepend
        new_content = read_content(args)
        
        # Convert markdown if needed
        if args.format == 'markdown' or (args.format == 'auto' and args.file and 
                                         Path(args.file).suffix.lower() in ['.md', '.markdown']):
            new_content = convert_markdown_to_storage(new_content)
        
        # Get current content
        current_content = current_page.get('body', {}).get('storage', {}).get('value', '')
        
        # Combine content
        if args.append:
            content = current_content + '\n' + new_content
        else:  # prepend
            content = new_content + '\n' + current_content
    else:
        # Replace content entirely
        content = read_content(args)
        
        # Convert markdown if needed
        if args.format == 'markdown' or (args.format == 'auto' and args.file and 
                                         Path(args.file).suffix.lower() in ['.md', '.markdown']):
            content = convert_markdown_to_storage(content)
    
    # Determine title
    title = args.title or current_page['title']
    
    # Get current version
    current_version = current_page['version']['number']
    
    # Show dry run info
    if args.dry_run:
        print("DRY RUN - Would update page with:")
        print(f"  Page ID: {page_id}")
        print(f"  Current title: {current_page['title']}")
        if args.title:
            print(f"  New title: {title}")
        print(f"  Current version: {current_version}")
        print(f"  Content length: {len(content)} characters")
        if args.append:
            print("  Mode: Append")
        elif args.prepend:
            print("  Mode: Prepend")
        else:
            print("  Mode: Replace")
        if args.version_message:
            print(f"  Version message: {args.version_message}")
        return
    
    # Update the page
    try:
        updated_page = client.update_page(
            page_id=page_id,
            title=title,
            content=content,
            version=current_version,
            version_message=args.version_message or 'Updated via API'
        )
        
        # Output result
        if args.json:
            print(json.dumps({
                'success': True,
                'page_id': updated_page['id'],
                'title': updated_page['title'],
                'url': f"https://{domain}/wiki/spaces/{current_page.get('spaceId')}/pages/{updated_page['id']}",
                'version': updated_page.get('version', {}).get('number'),
                'previous_version': current_version
            }, indent=2))
        else:
            print(f"Successfully updated page: {updated_page['title']}")
            print(f"Page ID: {updated_page['id']}")
            print(f"Version: {current_version} -> {updated_page.get('version', {}).get('number')}")
            print(f"URL: https://{domain}/wiki/spaces/{current_page.get('spaceId')}/pages/{updated_page['id']}")
            
    except Exception as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': str(e)
            }, indent=2))
        else:
            print(f"Error updating page: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()