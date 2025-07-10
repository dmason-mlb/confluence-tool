#!/usr/bin/env python3
"""
Generic script to create a Confluence page.

This script can be called from any repository to create a new Confluence page.
It supports reading content from files, stdin, or command line arguments.

Usage:
    # Create page with content from file
    python create_confluence_page.py --space-id 123456 --title "My Page" --file content.md
    
    # Create page with content from stdin
    echo "# Hello World" | python create_confluence_page.py --space-id 123456 --title "My Page"
    
    # Create page with inline content
    python create_confluence_page.py --space-id 123456 --title "My Page" --content "Hello World"
    
    # Create child page
    python create_confluence_page.py --space-id 123456 --title "Child Page" --parent-id 789012 --file content.html

Environment Variables:
    CONFLUENCE_DOMAIN: Your Confluence domain (e.g., 'yoursite.atlassian.net')
    CONFLUENCE_EMAIL: Your email address
    CONFLUENCE_API_TOKEN: Your API token
    CONFLUENCE_SPACE_ID: Default space ID (can be overridden with --space-id)
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
        str: Content to create page with
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


def main():
    """Main function to create a Confluence page."""
    parser = argparse.ArgumentParser(
        description='Create a new Confluence page',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Required arguments
    parser.add_argument('--title', required=True, help='Page title')
    
    # Space identification (one required)
    parser.add_argument('--space-id', type=int, 
                       help='Space ID (overrides CONFLUENCE_SPACE_ID env var)')
    
    # Content source (one required)
    content_group = parser.add_mutually_exclusive_group()
    content_group.add_argument('--file', help='Read content from file')
    content_group.add_argument('--content', help='Inline content')
    
    # Optional arguments
    parser.add_argument('--parent-id', type=int, help='Parent page ID for creating child pages')
    parser.add_argument('--format', choices=['storage', 'markdown', 'auto'], default='auto',
                       help='Content format (auto-detects based on file extension)')
    parser.add_argument('--modern-editor', action='store_true', default=True,
                       help='Use modern editor (default: True)')
    parser.add_argument('--json', action='store_true',
                       help='Output result as JSON')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be created without actually creating')
    
    args = parser.parse_args()
    
    # Get credentials
    creds = get_credentials()
    if not creds:
        sys.exit(1)
    
    domain, email, api_token = creds
    
    # Get space ID
    space_id = args.space_id or os.environ.get('CONFLUENCE_SPACE_ID')
    if not space_id:
        print("Error: No space ID provided. Use --space-id or set CONFLUENCE_SPACE_ID environment variable.")
        sys.exit(1)
    
    try:
        space_id = int(space_id)
    except ValueError:
        print(f"Error: Invalid space ID: {space_id}")
        sys.exit(1)
    
    # Read content
    content = read_content(args)
    
    # Convert markdown if needed
    if args.format == 'markdown' or (args.format == 'auto' and args.file and 
                                     Path(args.file).suffix.lower() in ['.md', '.markdown']):
        content = convert_markdown_to_storage(content)
    
    # Show dry run info
    if args.dry_run:
        print("DRY RUN - Would create page with:")
        print(f"  Title: {args.title}")
        print(f"  Space ID: {space_id}")
        if args.parent_id:
            print(f"  Parent ID: {args.parent_id}")
        print(f"  Content length: {len(content)} characters")
        print(f"  Modern editor: {args.modern_editor}")
        return
    
    # Create client
    try:
        client = ConfluenceClient(domain, email, api_token)
    except Exception as e:
        print(f"Error initializing Confluence client: {e}")
        sys.exit(1)
    
    # Create the page
    try:
        if args.modern_editor:
            page = client.create_page_modern_editor(
                space_id=space_id,
                title=args.title,
                content=content,
                parent_id=args.parent_id
            )
        else:
            page = client.create_page(
                space_id=space_id,
                title=args.title,
                content=content,
                parent_id=args.parent_id
            )
        
        # Output result
        if args.json:
            print(json.dumps({
                'success': True,
                'page_id': page['id'],
                'title': page['title'],
                'url': f"https://{domain}/wiki/spaces/{space_id}/pages/{page['id']}",
                'version': page.get('version', {}).get('number', 1)
            }, indent=2))
        else:
            print(f"Successfully created page: {page['title']}")
            print(f"Page ID: {page['id']}")
            print(f"URL: https://{domain}/wiki/spaces/{space_id}/pages/{page['id']}")
            
    except Exception as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': str(e)
            }, indent=2))
        else:
            print(f"Error creating page: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()