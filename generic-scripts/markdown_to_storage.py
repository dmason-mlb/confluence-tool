#!/usr/bin/env python3
"""
Convert Markdown content to Confluence storage format.

This script provides a more comprehensive Markdown to Confluence storage format converter
that can be used standalone or imported by other scripts.

Usage:
    # Convert a markdown file
    python markdown_to_storage.py input.md > output.html
    
    # Convert from stdin
    echo "# Hello World" | python markdown_to_storage.py
    
    # Save to file
    python markdown_to_storage.py input.md -o output.html
    
    # Show supported syntax
    python markdown_to_storage.py --show-syntax

Supported Markdown Elements:
    - Headers (h1-h6)
    - Bold, italic, bold+italic
    - Inline code and code blocks with language support
    - Links and images
    - Ordered and unordered lists (including nested)
    - Tables
    - Blockquotes
    - Horizontal rules
    - Task lists
    - Info, warning, and note panels (using special syntax)
"""

import argparse
import re
import sys
from pathlib import Path


class MarkdownToStorageConverter:
    """Convert Markdown to Confluence storage format."""
    
    def __init__(self):
        """Initialize the converter."""
        pass
    
    def convert(self, markdown_content):
        """
        Convert markdown content to Confluence storage format.
        
        Args:
            markdown_content: String containing markdown
            
        Returns:
            str: Confluence storage format HTML
        """
        # Process in order to avoid conflicts
        html = markdown_content
        
        # Preserve code blocks first
        code_blocks = []
        
        def preserve_code_block(match):
            index = len(code_blocks)
            code_blocks.append(match.group(0))
            return f'__CODE_BLOCK_{index}__'
        
        html = re.sub(r'```[\s\S]*?```', preserve_code_block, html)
        
        # Convert special panels (before other conversions)
        html = self._convert_panels(html)
        
        # Convert headers
        html = self._convert_headers(html)
        
        # Convert emphasis (bold, italic)
        html = self._convert_emphasis(html)
        
        # Convert inline code
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
        
        # Convert links and images
        html = self._convert_links_and_images(html)
        
        # Convert lists
        html = self._convert_lists(html)
        
        # Convert tables
        html = self._convert_tables(html)
        
        # Convert blockquotes
        html = self._convert_blockquotes(html)
        
        # Convert horizontal rules
        html = re.sub(r'^---+$', '<hr/>', html, flags=re.MULTILINE)
        html = re.sub(r'^\*\*\*+$', '<hr/>', html, flags=re.MULTILINE)
        
        # Convert task lists
        html = self._convert_task_lists(html)
        
        # Restore and convert code blocks
        for i, code_block in enumerate(code_blocks):
            html = html.replace(f'__CODE_BLOCK_{i}__', self._convert_code_block(code_block))
        
        # Convert paragraphs
        html = self._convert_paragraphs(html)
        
        return html
    
    def _convert_headers(self, text):
        """Convert markdown headers to HTML."""
        text = re.sub(r'^###### (.+)$', r'<h6>\1</h6>', text, flags=re.MULTILINE)
        text = re.sub(r'^##### (.+)$', r'<h5>\1</h5>', text, flags=re.MULTILINE)
        text = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
        text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
        return text
    
    def _convert_emphasis(self, text):
        """Convert bold and italic markdown."""
        # Bold + italic
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
        text = re.sub(r'___(.+?)___', r'<strong><em>\1</em></strong>', text)
        
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)
        
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
        
        return text
    
    def _convert_links_and_images(self, text):
        """Convert markdown links and images."""
        # Images
        text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', 
                     r'<ac:image><ri:url ri:value="\2" /></ac:image>', text)
        
        # Links
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        
        return text
    
    def _convert_code_block(self, code_block):
        """Convert a markdown code block to Confluence format."""
        match = re.match(r'```(\w*)\n(.*?)```', code_block, re.DOTALL)
        if match:
            lang = match.group(1) or 'text'
            code = match.group(2).rstrip()
            
            # Map common language names
            lang_map = {
                'js': 'javascript',
                'ts': 'typescript',
                'py': 'python',
                'rb': 'ruby',
                'yml': 'yaml',
                'sh': 'bash',
                'dockerfile': 'docker',
            }
            lang = lang_map.get(lang.lower(), lang)
            
            return f'''<ac:structured-macro ac:name="code">
    <ac:parameter ac:name="language">{lang}</ac:parameter>
    <ac:plain-text-body><![CDATA[{code}]]></ac:plain-text-body>
</ac:structured-macro>'''
        return code_block
    
    def _convert_lists(self, text):
        """Convert markdown lists to HTML."""
        lines = text.split('\n')
        result = []
        list_stack = []  # Track open lists
        prev_indent = -1
        
        for line in lines:
            # Check for unordered list item
            ul_match = re.match(r'^(\s*)[-*+] (.+)$', line)
            # Check for ordered list item
            ol_match = re.match(r'^(\s*)\d+\. (.+)$', line)
            
            if ul_match or ol_match:
                if ul_match:
                    indent = len(ul_match.group(1))
                    content = ul_match.group(2)
                    list_type = 'ul'
                else:
                    indent = len(ol_match.group(1))
                    content = ol_match.group(2)
                    list_type = 'ol'
                
                # Calculate indent level (assuming 2 or 4 spaces per level)
                level = indent // 2 if indent > 0 else 0
                
                # Close lists if we're dedenting
                while len(list_stack) > level:
                    result.append(f'</{list_stack.pop()}>')
                
                # Open new list if needed
                if len(list_stack) == level:
                    if not list_stack or list_stack[-1] != list_type:
                        if list_stack:
                            result.append(f'</{list_stack.pop()}>')
                        result.append(f'<{list_type}>')
                        list_stack.append(list_type)
                    else:
                        # Check if we need to open a new list at this level
                        if level == 0 or (level > 0 and len(list_stack) == level):
                            if not list_stack or list_stack[-1] != list_type:
                                result.append(f'<{list_type}>')
                                list_stack.append(list_type)
                
                result.append(f'<li>{content}</li>')
                prev_indent = indent
            else:
                # Close all open lists
                while list_stack:
                    result.append(f'</{list_stack.pop()}>')
                result.append(line)
                prev_indent = -1
        
        # Close any remaining open lists
        while list_stack:
            result.append(f'</{list_stack.pop()}>')
        
        return '\n'.join(result)
    
    def _convert_tables(self, text):
        """Convert markdown tables to HTML tables."""
        lines = text.split('\n')
        result = []
        in_table = False
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Check if this looks like a table row
            if '|' in line and not in_table:
                # Check if next line is separator
                if i + 1 < len(lines) and re.match(r'^[\s|:-]+$', lines[i + 1]):
                    # Start table
                    in_table = True
                    result.append('<table>')
                    
                    # Parse header row
                    headers = [cell.strip() for cell in line.split('|')[1:-1]]
                    result.append('<thead>')
                    result.append('<tr>')
                    for header in headers:
                        result.append(f'<th>{header}</th>')
                    result.append('</tr>')
                    result.append('</thead>')
                    result.append('<tbody>')
                    
                    # Skip separator line
                    i += 2
                    continue
            
            elif '|' in line and in_table:
                # Parse body row
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                result.append('<tr>')
                for cell in cells:
                    result.append(f'<td>{cell}</td>')
                result.append('</tr>')
            
            elif in_table and '|' not in line:
                # End of table
                result.append('</tbody>')
                result.append('</table>')
                in_table = False
                result.append(line)
            
            else:
                result.append(line)
            
            i += 1
        
        # Close table if still open
        if in_table:
            result.append('</tbody>')
            result.append('</table>')
        
        return '\n'.join(result)
    
    def _convert_blockquotes(self, text):
        """Convert markdown blockquotes."""
        lines = text.split('\n')
        result = []
        in_blockquote = False
        
        for line in lines:
            if line.startswith('>'):
                if not in_blockquote:
                    result.append('<blockquote>')
                    in_blockquote = True
                result.append(line[1:].strip())
            else:
                if in_blockquote:
                    result.append('</blockquote>')
                    in_blockquote = False
                result.append(line)
        
        if in_blockquote:
            result.append('</blockquote>')
        
        return '\n'.join(result)
    
    def _convert_task_lists(self, text):
        """Convert GitHub-style task lists."""
        # Unchecked tasks
        text = re.sub(r'^- \[ \] (.+)$', 
                     r'<ac:task><ac:task-status>incomplete</ac:task-status><ac:task-body>\1</ac:task-body></ac:task>',
                     text, flags=re.MULTILINE)
        
        # Checked tasks
        text = re.sub(r'^- \[x\] (.+)$', 
                     r'<ac:task><ac:task-status>complete</ac:task-status><ac:task-body>\1</ac:task-body></ac:task>',
                     text, flags=re.MULTILINE)
        
        return text
    
    def _convert_panels(self, text):
        """Convert special panel syntax to Confluence macros."""
        # Info panels: ::: info
        text = re.sub(r'^::: info(?: "([^"]+)")?\n([\s\S]*?)\n:::', 
                     lambda m: self._create_panel('info', m.group(1), m.group(2)),
                     text, flags=re.MULTILINE)
        
        # Warning panels: ::: warning
        text = re.sub(r'^::: warning(?: "([^"]+)")?\n([\s\S]*?)\n:::', 
                     lambda m: self._create_panel('warning', m.group(1), m.group(2)),
                     text, flags=re.MULTILINE)
        
        # Note panels: ::: note
        text = re.sub(r'^::: note(?: "([^"]+)")?\n([\s\S]*?)\n:::', 
                     lambda m: self._create_panel('note', m.group(1), m.group(2)),
                     text, flags=re.MULTILINE)
        
        # Success panels: ::: success
        text = re.sub(r'^::: success(?: "([^"]+)")?\n([\s\S]*?)\n:::', 
                     lambda m: self._create_panel('success', m.group(1), m.group(2)),
                     text, flags=re.MULTILINE)
        
        return text
    
    def _create_panel(self, panel_type, title, content):
        """Create a Confluence panel macro."""
        if title:
            return f'''<ac:structured-macro ac:name="{panel_type}">
    <ac:parameter ac:name="title">{title}</ac:parameter>
    <ac:rich-text-body>
        <p>{content.strip()}</p>
    </ac:rich-text-body>
</ac:structured-macro>'''
        else:
            return f'''<ac:structured-macro ac:name="{panel_type}">
    <ac:rich-text-body>
        <p>{content.strip()}</p>
    </ac:rich-text-body>
</ac:structured-macro>'''
    
    def _convert_paragraphs(self, text):
        """Convert plain text to paragraphs."""
        lines = text.split('\n')
        result = []
        current_para = []
        
        for line in lines:
            if line.strip() == '':
                if current_para:
                    para_content = ' '.join(current_para)
                    # Don't wrap if already contains block elements
                    if not re.match(r'^<(?:h[1-6]|p|ul|ol|li|table|blockquote|ac:|hr)', para_content):
                        para_content = f'<p>{para_content}</p>'
                    result.append(para_content)
                    current_para = []
                result.append('')
            else:
                current_para.append(line)
        
        # Handle last paragraph
        if current_para:
            para_content = ' '.join(current_para)
            if not re.match(r'^<(?:h[1-6]|p|ul|ol|li|table|blockquote|ac:|hr)', para_content):
                para_content = f'<p>{para_content}</p>'
            result.append(para_content)
        
        return '\n'.join(result)


def show_syntax_guide():
    """Display supported Markdown syntax."""
    guide = """
Supported Markdown Syntax for Confluence Conversion
==================================================

Headers
-------
# H1 Header
## H2 Header
### H3 Header
#### H4 Header
##### H5 Header
###### H6 Header

Emphasis
--------
*italic* or _italic_
**bold** or __bold__
***bold italic*** or ___bold italic___

Links and Images
----------------
[Link text](https://example.com)
![Alt text](image-url.jpg)

Code
----
`inline code`

```python
# Code block with syntax highlighting
def hello():
    print("Hello, World!")
```

Lists
-----
Unordered:
- Item 1
- Item 2
  - Nested item
  - Another nested item
- Item 3

Ordered:
1. First item
2. Second item
   1. Nested item
   2. Another nested item
3. Third item

Tables
------
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |

Blockquotes
-----------
> This is a blockquote
> It can span multiple lines

Task Lists
----------
- [ ] Uncompleted task
- [x] Completed task

Horizontal Rule
---------------
---
or
***

Special Panels (Confluence-specific)
------------------------------------
::: info "Optional Title"
This is an info panel
:::

::: warning "Warning!"
This is a warning panel
:::

::: note
This is a note panel (no title)
:::

::: success "Success"
This is a success panel
:::
"""
    print(guide)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Convert Markdown to Confluence storage format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('input', nargs='?', help='Input markdown file (or stdin)')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('--show-syntax', action='store_true',
                       help='Show supported Markdown syntax and exit')
    
    args = parser.parse_args()
    
    if args.show_syntax:
        show_syntax_guide()
        return
    
    # Read input
    if args.input:
        if not Path(args.input).exists():
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        # Read from stdin
        if sys.stdin.isatty():
            print("Error: No input provided. Use a file argument or pipe content via stdin.",
                  file=sys.stderr)
            print("Use --show-syntax to see supported Markdown syntax.", file=sys.stderr)
            sys.exit(1)
        content = sys.stdin.read()
    
    # Convert
    converter = MarkdownToStorageConverter()
    html = converter.convert(content)
    
    # Write output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Converted content written to: {args.output}")
    else:
        print(html)


if __name__ == '__main__':
    main()