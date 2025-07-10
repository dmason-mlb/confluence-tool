#!/usr/bin/env python3
"""
Test script to create a Confluence page with comprehensive formatting examples.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from confluence_client import ConfluenceClient
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_test_page():
    """Create a test page with various formatting elements."""
    
    # Load configuration
    from config import get_config
    config = get_config()
    if not config:
        sys.exit(1)
    
    DOMAIN = config['domain']
    EMAIL = config['email'] 
    API_TOKEN = config['api_token']
    SPACE_ID = config['space_id']
    
    if not SPACE_ID:
        print("Error: CONFLUENCE_SPACE_ID is required for this test.")
        print("Run 'python3 scripts/test_connection.py' to find available space IDs.")
        sys.exit(1)
    
    # Initialize client
    client = ConfluenceClient(DOMAIN, EMAIL, API_TOKEN)
    logger.info(f"Initialized client for {DOMAIN}")
    
    # Create comprehensive content with various formatting
    current_date = datetime.now().isoformat()
    content = """
    <h1>Confluence API Test Page - Comprehensive Formatting</h1>
    <p>Created on: {current_date}</p>
    
    <ac:structured-macro ac:name="toc">
        <ac:parameter ac:name="maxLevel">3</ac:parameter>
    </ac:structured-macro>
    
    <h2>1. Text Formatting</h2>
    <p>This section demonstrates various text formatting options:</p>
    <ul>
        <li><strong>Bold text</strong> using strong tags</li>
        <li><em>Italic text</em> using em tags</li>
        <li><u>Underlined text</u> using u tags</li>
        <li><del>Strikethrough text</del> using del tags</li>
        <li><code>Inline code</code> using code tags</li>
        <li>Text with <sup>superscript</sup> and <sub>subscript</sub></li>
        <li><span style="color: rgb(255, 0, 0);">Colored text</span> using span with style</li>
        <li><span style="background-color: rgb(255, 255, 0);">Highlighted text</span></li>
    </ul>
    
    <h2>2. Headings Hierarchy</h2>
    <h3>2.1 Subheading Level 3</h3>
    <p>Content under level 3 heading.</p>
    <h4>2.1.1 Subheading Level 4</h4>
    <p>Content under level 4 heading.</p>
    <h5>2.1.1.1 Subheading Level 5</h5>
    <p>Content under level 5 heading.</p>
    <h6>2.1.1.1.1 Subheading Level 6</h6>
    <p>This is the deepest heading level.</p>
    
    <h2>3. Lists</h2>
    
    <h3>3.1 Ordered List</h3>
    <ol>
        <li>First item</li>
        <li>Second item
            <ol>
                <li>Nested item 2.1</li>
                <li>Nested item 2.2</li>
            </ol>
        </li>
        <li>Third item</li>
    </ol>
    
    <h3>3.2 Unordered List</h3>
    <ul>
        <li>Bullet point one</li>
        <li>Bullet point two
            <ul>
                <li>Sub-bullet 2.1</li>
                <li>Sub-bullet 2.2</li>
            </ul>
        </li>
        <li>Bullet point three</li>
    </ul>
    
    <h3>3.3 Mixed Nested Lists</h3>
    <ol>
        <li>Ordered item 1</li>
        <li>Ordered item 2
            <ul>
                <li>Unordered sub-item A</li>
                <li>Unordered sub-item B
                    <ol>
                        <li>Ordered sub-sub-item i</li>
                        <li>Ordered sub-sub-item ii</li>
                    </ol>
                </li>
                <li>Unordered sub-item C</li>
            </ul>
        </li>
        <li>Ordered item 3</li>
    </ol>
    
    <h2>4. Tables</h2>
    
    <h3>4.1 Simple Table</h3>
    <table>
        <thead>
            <tr>
                <th>Header 1</th>
                <th>Header 2</th>
                <th>Header 3</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Row 1, Cell 1</td>
                <td>Row 1, Cell 2</td>
                <td>Row 1, Cell 3</td>
            </tr>
            <tr>
                <td>Row 2, Cell 1</td>
                <td>Row 2, Cell 2</td>
                <td>Row 2, Cell 3</td>
            </tr>
        </tbody>
    </table>
    
    <h3>4.2 Complex Table with Formatting</h3>
    <table>
        <colgroup>
            <col style="width: 20%;" />
            <col style="width: 40%;" />
            <col style="width: 40%;" />
        </colgroup>
        <thead>
            <tr>
                <th>Status</th>
                <th>Description</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>
                    <ac:structured-macro ac:name="status">
                        <ac:parameter ac:name="colour">Green</ac:parameter>
                        <ac:parameter ac:name="title">Complete</ac:parameter>
                    </ac:structured-macro>
                </td>
                <td><strong>Task 1:</strong> Implementation finished</td>
                <td><code>git commit -m "Done"</code></td>
            </tr>
            <tr>
                <td>
                    <ac:structured-macro ac:name="status">
                        <ac:parameter ac:name="colour">Yellow</ac:parameter>
                        <ac:parameter ac:name="title">In Progress</ac:parameter>
                    </ac:structured-macro>
                </td>
                <td><em>Task 2:</em> Currently working on this</td>
                <td>Review PR <a href="#anchor1">#1234</a></td>
            </tr>
            <tr>
                <td>
                    <ac:structured-macro ac:name="status">
                        <ac:parameter ac:name="colour">Red</ac:parameter>
                        <ac:parameter ac:name="title">Blocked</ac:parameter>
                    </ac:structured-macro>
                </td>
                <td><del>Task 3:</del> Waiting for dependencies</td>
                <td>Contact <ac:link><ri:user ri:account-id="current-user"/></ac:link></td>
            </tr>
        </tbody>
    </table>
    
    <h2>5. Links and Anchors</h2>
    
    <h3 id="anchor1">5.1 Link Types</h3>
    <ul>
        <li><a href="https://www.atlassian.com">External link to Atlassian</a></li>
        <li><a href="#anchor2">Anchor link to section 5.2</a></li>
        <li><a href="mailto:example@email.com">Email link</a></li>
        <li>Link to top: <a href="#top">Back to top</a></li>
    </ul>
    
    <h3 id="anchor2">5.2 Anchor Target</h3>
    <p>This is the target of the anchor link from above.</p>
    
    <h2>6. Macros</h2>
    
    <h3>6.1 Info Panel</h3>
    <ac:structured-macro ac:name="info">
        <ac:parameter ac:name="title">Information</ac:parameter>
        <ac:rich-text-body>
            <p>This is an info panel with a custom title. It's useful for highlighting important information.</p>
        </ac:rich-text-body>
    </ac:structured-macro>
    
    <h3>6.2 Warning Panel</h3>
    <ac:structured-macro ac:name="warning">
        <ac:parameter ac:name="title">Warning!</ac:parameter>
        <ac:rich-text-body>
            <p>This is a warning panel. Use it for important warnings or cautions.</p>
        </ac:rich-text-body>
    </ac:structured-macro>
    
    <h3>6.3 Note Panel</h3>
    <ac:structured-macro ac:name="note">
        <ac:rich-text-body>
            <p>This is a note panel without a custom title.</p>
        </ac:rich-text-body>
    </ac:structured-macro>
    
    <h3>6.4 Success Panel</h3>
    <ac:structured-macro ac:name="success">
        <ac:parameter ac:name="title">Success!</ac:parameter>
        <ac:rich-text-body>
            <p>Operation completed successfully!</p>
        </ac:rich-text-body>
    </ac:structured-macro>
    
    <h3>6.5 Code Block</h3>
    <ac:structured-macro ac:name="code">
        <ac:parameter ac:name="language">python</ac:parameter>
        <ac:parameter ac:name="theme">RDark</ac:parameter>
        <ac:parameter ac:name="linenumbers">true</ac:parameter>
        <ac:parameter ac:name="title">example.py</ac:parameter>
        <ac:plain-text-body><![CDATA[
def create_confluence_page(client, space_id, title, content):
    '''Create a new Confluence page.'''
    page = client.create_page(
        space_id=space_id,
        title=title,
        content=content
    )
    print("Created page: " + page['title'] + " (ID: " + page['id'] + ")")
    return page

# Example usage
if __name__ == "__main__":
    page = create_confluence_page(
        client, 
        123456, 
        "My Page",
        "<p>Hello, World!</p>"
    )
        ]]></ac:plain-text-body>
    </ac:structured-macro>
    
    <h3>6.6 Expand Macro</h3>
    <ac:structured-macro ac:name="expand">
        <ac:parameter ac:name="title">Click to reveal hidden content</ac:parameter>
        <ac:rich-text-body>
            <p>This content is hidden by default and revealed when the user clicks the expand button.</p>
            <p>It's useful for:</p>
            <ul>
                <li>Additional details</li>
                <li>Optional information</li>
                <li>Troubleshooting steps</li>
            </ul>
        </ac:rich-text-body>
    </ac:structured-macro>
    
    <h3>6.7 Panel Macro</h3>
    <ac:structured-macro ac:name="panel">
        <ac:parameter ac:name="title">Custom Panel</ac:parameter>
        <ac:parameter ac:name="borderStyle">solid</ac:parameter>
        <ac:parameter ac:name="borderColor">#0052cc</ac:parameter>
        <ac:parameter ac:name="bgColor">#deebff</ac:parameter>
        <ac:rich-text-body>
            <p>This is a custom panel with specific colors and border style.</p>
        </ac:rich-text-body>
    </ac:structured-macro>
    
    <h2>7. Advanced Content</h2>
    
    <h3>7.1 Horizontal Rule</h3>
    <p>Content before the rule.</p>
    <hr/>
    <p>Content after the rule.</p>
    
    <h3>7.2 Block Quote</h3>
    <blockquote>
        <p>This is a block quote. It's useful for highlighting quotes or important passages from other sources.</p>
        <p>- Anonymous</p>
    </blockquote>
    
    <h3>7.3 Task List</h3>
    <ac:task-list>
        <ac:task>
            <ac:task-id>1</ac:task-id>
            <ac:task-status>complete</ac:task-status>
            <ac:task-body>Completed task</ac:task-body>
        </ac:task>
        <ac:task>
            <ac:task-id>2</ac:task-id>
            <ac:task-status>incomplete</ac:task-status>
            <ac:task-body>Pending task</ac:task-body>
        </ac:task>
    </ac:task-list>
    
    <h3>7.4 Emoticons</h3>
    <p>Confluence supports emoticons: 
        <ac:emoticon ac:name="smile" /> 
        <ac:emoticon ac:name="sad" /> 
        <ac:emoticon ac:name="cheeky" /> 
        <ac:emoticon ac:name="laugh" /> 
        <ac:emoticon ac:name="wink" /> 
        <ac:emoticon ac:name="thumbs-up" /> 
        <ac:emoticon ac:name="thumbs-down" /> 
        <ac:emoticon ac:name="information" /> 
        <ac:emoticon ac:name="tick" /> 
        <ac:emoticon ac:name="cross" /> 
        <ac:emoticon ac:name="warning" /> 
        <ac:emoticon ac:name="plus" /> 
        <ac:emoticon ac:name="minus" /> 
        <ac:emoticon ac:name="question" /> 
        <ac:emoticon ac:name="light-on" /> 
        <ac:emoticon ac:name="yellow-star" />
    </p>
    
    <h2>8. Layout and Columns</h2>
    
    <ac:layout>
        <ac:layout-section ac:type="two_equal">
            <ac:layout-cell>
                <h4>Left Column</h4>
                <p>This is content in the left column of a two-column layout.</p>
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                    <li>Item 3</li>
                </ul>
            </ac:layout-cell>
            <ac:layout-cell>
                <h4>Right Column</h4>
                <p>This is content in the right column of a two-column layout.</p>
                <ol>
                    <li>Step 1</li>
                    <li>Step 2</li>
                    <li>Step 3</li>
                </ol>
            </ac:layout-cell>
        </ac:layout-section>
    </ac:layout>
    
    <h2>9. Mentions and Smart Links</h2>
    
    <p>Mention a user: <ac:link><ri:user ri:account-id="current-user"/></ac:link></p>
    <p>Link to another page: <ac:link><ri:page ri:content-title="Home" /></ac:link></p>
    
    <h2>10. Conclusion</h2>
    <p>This page demonstrates a wide variety of Confluence formatting options and macros available through the REST API v2.</p>
    
    <ac:structured-macro ac:name="recently-updated">
        <ac:parameter ac:name="max">5</ac:parameter>
    </ac:structured-macro>
    """
    
    # Format the content with the current date
    content = content.format(current_date=current_date)
    
    try:
        # Create the page using modern editor method
        logger.info("Creating test page with modern editor...")
        page = client.create_page_modern_editor(
            space_id=SPACE_ID,
            title=f"API Test - Comprehensive Formatting {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            content=content
        )
        
        logger.info(f"Successfully created page: {page['title']}")
        logger.info(f"Page ID: {page['id']}")
        logger.info(f"Page URL: https://{DOMAIN}/wiki/spaces/{SPACE_ID}/pages/{page['id']}")
        
        # Note: v2 API doesn't support adding labels via POST
        logger.info("Note: Label addition is not supported in v2 API")
        
        # Try to add a comment (footer comments should work)
        try:
            logger.info("Adding a comment...")
            comment = client.add_comment(
                page['id'],
                "<p>This page was created using the Python client for Confluence API v2!</p>"
            )
            logger.info("Added comment successfully")
        except Exception as e:
            logger.warning(f"Could not add comment: {e}")
        
        return page
        
    except Exception as e:
        logger.error(f"Error creating page: {e}")
        raise


if __name__ == "__main__":
    page = create_test_page()
    print("\nTest page created successfully!")
    
    # Get config again for the URL
    from config import get_config
    config = get_config()
    print(f"View it at: https://{config['domain']}/wiki/spaces/{config['space_id']}/pages/{page['id']}")