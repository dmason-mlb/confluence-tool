# Testing the Confluence Tool

## Prerequisites

1. **Confluence Cloud Instance**: You need access to a Confluence Cloud instance
2. **API Token**: Create one at https://id.atlassian.com/manage-profile/security/api-tokens
3. **Space ID**: A numeric ID of a space where you have write permissions

## Quick Test

### Option 1: Interactive Setup (Recommended)
```bash
# Run the interactive setup script
./setup_env.sh

# This creates a .env file with your configuration
# The Python scripts will automatically load from this file

# Test your connection
python3 scripts/test_connection.py

# Create a test page
python3 scripts/test_formatting.py
```

### Option 2: Manual .env File
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your values
nano .env  # or use your preferred editor

# Run the test (no need to export variables)
python3 scripts/test_formatting.py
```

### Option 3: Environment Variables
```bash
# You can still use environment variables if preferred
export CONFLUENCE_DOMAIN="your-domain.atlassian.net"
export CONFLUENCE_EMAIL="your-email@example.com"
export CONFLUENCE_API_TOKEN="your-api-token"
export CONFLUENCE_SPACE_ID="123456"

# Run the test
python3 scripts/test_formatting.py
```

**Note**: The scripts check for a .env file first, then fall back to environment variables.

## What the Test Creates

The `test_formatting.py` script creates a comprehensive Confluence page demonstrating:

### Text Formatting
- Bold, italic, underline, strikethrough
- Inline code, superscript, subscript
- Colored and highlighted text

### Structure Elements
- All heading levels (H1-H6)
- Ordered lists with nesting
- Unordered lists with nesting
- Mixed nested lists (ordered inside unordered and vice versa)

### Tables
- Simple tables
- Complex tables with status macros
- Tables with custom column widths

### Links
- External links
- Anchor links within the page
- Email links
- User mentions

### Confluence Macros
- Table of Contents
- Info, Warning, Note, Success panels
- Code blocks with syntax highlighting
- Expand/collapse sections
- Custom panels with colors
- Status badges
- Task lists
- Emoticons
- Recently updated macro

### Layout
- Two-column layouts
- Block quotes
- Horizontal rules

## Finding Your Space ID

1. Navigate to your Confluence space
2. Look at the URL: `https://yoursite.atlassian.net/wiki/spaces/SPACEKEY/overview`
3. Click on "Space settings" (if you have permissions)
4. The Space ID is shown in the space details

Alternatively, use the API:
```bash
curl -u your-email@example.com:your-api-token \
  https://your-domain.atlassian.net/wiki/api/v2/spaces
```

## Verification

After running the test, you should see:
1. Success message with the page ID
2. URL to view the created page
3. Confirmation that labels and comments were added

The created page will demonstrate all formatting capabilities supported by the Confluence API v2.

## Troubleshooting

### Authentication Failed
- Verify your API token is correct
- Ensure your email matches the Atlassian account
- Check that the domain includes `.atlassian.net`

### Space Not Found
- Verify the SPACE_ID is numeric (not the space key)
- Ensure you have write permissions to the space
- Try listing spaces first to verify access

### Rate Limiting
- The client automatically handles rate limits
- If you see 429 errors, the script will retry with backoff

## Next Steps

Once the test page is created, you can:
1. View it in your browser
2. Try other example scripts in `scripts/examples/`
3. Modify the test to experiment with different formatting
4. Use the client library in your own scripts