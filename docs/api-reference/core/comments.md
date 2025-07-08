# Confluence Comments API Reference

## Overview

The Confluence Comments API provides comprehensive functionality for managing comments on pages, blog posts, and attachments. Comments support threaded discussions, inline comments, and rich text formatting, making them essential for collaboration and feedback.

### Use Cases
- Automated comment moderation and management
- Integration with external communication tools
- Comment migration between spaces or instances
- Notification systems for comment activity
- Sentiment analysis and feedback tracking
- Automated responses to common questions
- Comment archival and compliance

## Authentication Requirements

All Comment API operations require authentication:

### API Token (Recommended for Cloud)
```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
  https://your-domain.atlassian.net/wiki/rest/api/content/{id}/child/comment
```

### Basic Authentication
```bash
curl -u username:api_token \
  https://your-domain.atlassian.net/wiki/rest/api/content/{id}/child/comment
```

## Available Endpoints

### 1. Create Comment
**Method:** POST  
**Path:** `/rest/api/content/{id}/child/comment`

Creates a new comment on a page, blog post, or attachment.

#### Request Example
```json
{
  "type": "comment",
  "container": {
    "id": "123456789",
    "type": "page"
  },
  "body": {
    "storage": {
      "value": "<p>This is a great documentation page! I have a few suggestions...</p>",
      "representation": "storage"
    }
  }
}
```

#### Python Example
```python
import requests
import json

def create_comment(base_url, auth, content_id, comment_text, parent_comment_id=None):
    """Create a comment on a Confluence page or blog post"""
    
    url = f"{base_url}/rest/api/content/{content_id}/child/comment"
    
    payload = {
        "type": "comment",
        "body": {
            "storage": {
                "value": f"<p>{comment_text}</p>",
                "representation": "storage"
            }
        }
    }
    
    # If replying to another comment
    if parent_comment_id:
        payload["ancestors"] = [{"id": parent_comment_id}]
    
    response = requests.post(
        url,
        auth=auth,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    
    return response.json()

# Create a comment
comment = create_comment(
    "https://your-domain.atlassian.net/wiki",
    ("user@example.com", "api_token"),
    "123456789",
    "Great work on this documentation! One suggestion: could we add more examples?"
)
```

### 2. Get Comments
**Method:** GET  
**Path:** `/rest/api/content/{id}/child/comment`

Retrieves all comments for a specific content item.

#### Parameters
- `start`: Pagination start index
- `limit`: Maximum results (default: 25, max: 100)
- `location`: Filter by location (inline comments)
- `status`: Filter by status
- `expand`: Properties to expand
- `depth`: Comment depth for nested replies

#### cURL Example
```bash
curl -u user@example.com:api_token \
  "https://your-domain.atlassian.net/wiki/rest/api/content/123456789/child/comment?expand=body.view,version&depth=all"
```

#### Python Example
```python
def get_comments(base_url, auth, content_id, depth='all', expand='body.storage,version'):
    """Get all comments for a page or blog post"""
    
    url = f"{base_url}/rest/api/content/{content_id}/child/comment"
    
    params = {
        "depth": depth,
        "expand": expand,
        "limit": 100
    }
    
    all_comments = []
    start = 0
    
    while True:
        params["start"] = start
        response = requests.get(url, auth=auth, params=params)
        data = response.json()
        
        all_comments.extend(data['results'])
        
        if 'next' not in data['_links']:
            break
            
        start += data['limit']
    
    return all_comments

# Get all comments with nested replies
comments = get_comments(
    "https://your-domain.atlassian.net/wiki",
    auth,
    "123456789"
)
```

### 3. Get Single Comment
**Method:** GET  
**Path:** `/rest/api/content/{id}`

Retrieves a specific comment by its ID.

#### Response Example
```json
{
  "id": "987654321",
  "type": "comment",
  "status": "current",
  "body": {
    "storage": {
      "value": "<p>This is a comment</p>",
      "representation": "storage"
    },
    "view": {
      "value": "<p>This is a comment</p>",
      "representation": "view"
    }
  },
  "version": {
    "by": {
      "type": "known",
      "username": "john.doe",
      "displayName": "John Doe"
    },
    "when": "2024-01-15T10:30:00.000Z",
    "number": 1
  },
  "ancestors": [
    {
      "id": "123456789",
      "type": "page"
    }
  ]
}
```

### 4. Update Comment
**Method:** PUT  
**Path:** `/rest/api/content/{id}`

Updates an existing comment.

#### Request Example
```json
{
  "id": "987654321",
  "type": "comment",
  "body": {
    "storage": {
      "value": "<p>Updated comment text with additional information</p>",
      "representation": "storage"
    }
  },
  "version": {
    "number": 2
  }
}
```

#### Python Example
```python
def update_comment(base_url, auth, comment_id, new_text):
    """Update an existing comment"""
    
    # Get current comment to retrieve version
    current_url = f"{base_url}/rest/api/content/{comment_id}?expand=version"
    current = requests.get(current_url, auth=auth).json()
    
    # Update comment
    url = f"{base_url}/rest/api/content/{comment_id}"
    
    payload = {
        "id": comment_id,
        "type": "comment",
        "body": {
            "storage": {
                "value": f"<p>{new_text}</p>",
                "representation": "storage"
            }
        },
        "version": {
            "number": current['version']['number'] + 1
        }
    }
    
    response = requests.put(
        url,
        auth=auth,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    
    return response.json()
```

### 5. Delete Comment
**Method:** DELETE  
**Path:** `/rest/api/content/{id}`

Deletes a comment.

#### cURL Example
```bash
# Delete comment
curl -X DELETE -u user@example.com:api_token \
  "https://your-domain.atlassian.net/wiki/rest/api/content/987654321"
```

### 6. Create Inline Comment
**Method:** POST  
**Path:** `/rest/api/content/{id}/child/comment`

Creates an inline comment at a specific location in the content.

#### Request Example
```json
{
  "type": "comment",
  "container": {
    "id": "123456789",
    "type": "page"
  },
  "body": {
    "storage": {
      "value": "<p>This section needs clarification</p>",
      "representation": "storage"
    }
  },
  "location": {
    "type": "inline",
    "selection": {
      "start": 100,
      "end": 150
    }
  }
}
```

### 7. Get Comment Children (Replies)
**Method:** GET  
**Path:** `/rest/api/content/{id}/child/comment`

Gets all replies to a specific comment.

#### Python Example
```python
def get_comment_replies(base_url, auth, comment_id):
    """Get all replies to a comment"""
    
    url = f"{base_url}/rest/api/content/{comment_id}/child/comment"
    
    params = {
        "expand": "body.storage,version",
        "limit": 100
    }
    
    response = requests.get(url, auth=auth, params=params)
    return response.json()
```

## Common Parameters

### Expansion Parameters
- `body.storage`: Raw storage format
- `body.view`: Rendered HTML
- `version`: Version information
- `ancestors`: Parent content/comments
- `children`: Child comments (replies)
- `container`: Parent page/blog post
- `location`: Inline comment location
- `extensions`: Additional metadata
- `restrictions`: Access restrictions

### Filter Parameters
- `location`: Filter by comment location
- `status`: Filter by status (current, deleted)
- `depth`: Depth of nested comments ('all' or number)

## Error Handling

### Common Error Scenarios

#### 1. Parent Content Not Found
```json
{
  "statusCode": 404,
  "message": "Content with ID 123456789 not found"
}
```

#### 2. No Permission to Comment
```json
{
  "statusCode": 403,
  "message": "User does not have permission to comment on this content"
}
```

#### 3. Invalid Comment Format
```json
{
  "statusCode": 400,
  "message": "Invalid comment body format"
}
```

### Python Error Handling
```python
def safe_create_comment(base_url, auth, content_id, comment_text, max_retries=3):
    """Create comment with comprehensive error handling"""
    
    for attempt in range(max_retries):
        try:
            result = create_comment(base_url, auth, content_id, comment_text)
            return result
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print("No permission to comment on this content")
                raise
            elif e.response.status_code == 404:
                print("Content not found")
                raise
            elif e.response.status_code == 429:
                # Rate limited
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
            raise
```

## Best Practices

### 1. Comment Threading Management
```python
class CommentThread:
    """Manage comment threads and discussions"""
    
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth
    
    def create_thread(self, content_id, initial_comment):
        """Start a new comment thread"""
        
        # Create initial comment
        parent = create_comment(
            self.base_url,
            self.auth,
            content_id,
            initial_comment
        )
        
        return {
            'thread_id': parent['id'],
            'content_id': content_id,
            'created': parent['version']['when']
        }
    
    def add_reply(self, thread_id, reply_text, mention_users=None):
        """Add a reply to a thread with optional mentions"""
        
        # Format mentions
        if mention_users:
            for user in mention_users:
                reply_text = f"@{user} {reply_text}"
        
        return create_comment(
            self.base_url,
            self.auth,
            thread_id,  # Parent comment ID
            reply_text
        )
    
    def get_thread_summary(self, thread_id):
        """Get a summary of a comment thread"""
        
        # Get parent comment
        parent = requests.get(
            f"{self.base_url}/rest/api/content/{thread_id}?expand=body.storage,version",
            auth=self.auth
        ).json()
        
        # Get all replies
        replies = get_comment_replies(self.base_url, self.auth, thread_id)
        
        return {
            'parent': parent,
            'reply_count': replies['size'],
            'participants': self._get_unique_participants(parent, replies),
            'last_activity': self._get_last_activity(parent, replies)
        }
    
    def _get_unique_participants(self, parent, replies):
        """Get unique participants in a thread"""
        participants = {parent['version']['by']['username']}
        
        for reply in replies.get('results', []):
            participants.add(reply['version']['by']['username'])
        
        return list(participants)
    
    def _get_last_activity(self, parent, replies):
        """Get timestamp of last activity"""
        timestamps = [parent['version']['when']]
        
        for reply in replies.get('results', []):
            timestamps.append(reply['version']['when'])
        
        return max(timestamps)
```

### 2. Comment Moderation
```python
class CommentModerator:
    """Automated comment moderation"""
    
    def __init__(self, base_url, auth, forbidden_words=None):
        self.base_url = base_url
        self.auth = auth
        self.forbidden_words = forbidden_words or []
    
    def moderate_comments(self, content_id):
        """Moderate comments on a page"""
        
        comments = get_comments(self.base_url, self.auth, content_id)
        moderated = []
        
        for comment in comments:
            # Extract text content
            content = comment['body']['storage']['value']
            text = self._strip_html(content).lower()
            
            # Check for forbidden words
            if any(word in text for word in self.forbidden_words):
                # Delete or flag comment
                self._flag_comment(comment['id'])
                moderated.append(comment)
            
            # Check for spam patterns
            if self._is_spam(text):
                self._flag_comment(comment['id'])
                moderated.append(comment)
        
        return moderated
    
    def _strip_html(self, html):
        """Remove HTML tags from content"""
        import re
        return re.sub('<[^<]+?>', '', html)
    
    def _is_spam(self, text):
        """Check for spam patterns"""
        spam_patterns = [
            r'buy.*now',
            r'click.*here',
            r'limited.*offer',
            r'act.*now'
        ]
        
        import re
        return any(re.search(pattern, text) for pattern in spam_patterns)
    
    def _flag_comment(self, comment_id):
        """Flag a comment for review"""
        # Add property to mark as flagged
        set_attachment_property(
            self.base_url,
            self.auth,
            comment_id,
            "moderation-status",
            {"flagged": True, "reason": "automated-moderation"}
        )
```

### 3. Comment Analytics
```python
def analyze_comment_activity(base_url, auth, space_key, days=30):
    """Analyze comment activity in a space"""
    
    from datetime import datetime, timedelta
    
    # Search for content with recent comments
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    cql = f'space={space_key} and lastmodified>"{cutoff_date}"'
    search_url = f"{base_url}/rest/api/content/search"
    
    params = {
        "cql": cql,
        "limit": 100
    }
    
    content_items = requests.get(search_url, auth=auth, params=params).json()
    
    analytics = {
        'total_comments': 0,
        'comments_by_user': {},
        'comments_by_page': {},
        'average_response_time': [],
        'most_discussed': []
    }
    
    for item in content_items['results']:
        comments = get_comments(base_url, auth, item['id'])
        
        if comments:
            page_comments = len(comments)
            analytics['total_comments'] += page_comments
            
            # Track by page
            analytics['comments_by_page'][item['title']] = page_comments
            
            # Track by user
            for comment in comments:
                user = comment['version']['by']['displayName']
                analytics['comments_by_user'][user] = \
                    analytics['comments_by_user'].get(user, 0) + 1
            
            # Calculate response times
            if len(comments) > 1:
                for i in range(1, len(comments)):
                    prev_time = datetime.fromisoformat(
                        comments[i-1]['version']['when'].replace('Z', '+00:00')
                    )
                    curr_time = datetime.fromisoformat(
                        comments[i]['version']['when'].replace('Z', '+00:00')
                    )
                    
                    response_time = (curr_time - prev_time).total_seconds() / 3600
                    analytics['average_response_time'].append(response_time)
    
    # Calculate averages
    if analytics['average_response_time']:
        avg_response = sum(analytics['average_response_time']) / len(analytics['average_response_time'])
        analytics['average_response_hours'] = round(avg_response, 2)
    
    # Find most discussed pages
    analytics['most_discussed'] = sorted(
        analytics['comments_by_page'].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    return analytics
```

### 4. Comment Templates
```python
class CommentTemplates:
    """Manage comment templates for common responses"""
    
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth
        self.templates = {
            'review_requested': """
                <p>Hi team,</p>
                <p>This document is ready for review. Please provide your feedback by {deadline}.</p>
                <p>Key areas to review:</p>
                <ul>
                    <li>Technical accuracy</li>
                    <li>Completeness</li>
                    <li>Clarity</li>
                </ul>
            """,
            'approved': """
                <p>✅ This document has been reviewed and approved.</p>
                <p>Approved by: {approver}</p>
                <p>Date: {date}</p>
            """,
            'needs_update': """
                <p>⚠️ This document needs to be updated.</p>
                <p>Reason: {reason}</p>
                <p>Please update by: {deadline}</p>
            """
        }
    
    def post_template_comment(self, content_id, template_name, variables=None):
        """Post a comment using a template"""
        
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        # Get template
        template = self.templates[template_name]
        
        # Replace variables
        if variables:
            for key, value in variables.items():
                template = template.replace(f'{{{key}}}', str(value))
        
        # Create comment
        return create_comment(
            self.base_url,
            self.auth,
            content_id,
            template
        )
```

### 5. Comment Migration
```python
def migrate_comments(source_url, source_auth, target_url, target_auth,
                    source_content_id, target_content_id):
    """Migrate comments between content items or instances"""
    
    # Get all comments from source
    source_comments = get_comments(
        source_url,
        source_auth,
        source_content_id,
        depth='all'
    )
    
    # Build comment hierarchy
    comment_map = {}
    root_comments = []
    
    for comment in source_comments:
        comment_map[comment['id']] = comment
        
        # Check if it's a root comment or reply
        ancestors = comment.get('ancestors', [])
        is_reply = any(a['type'] == 'comment' for a in ancestors)
        
        if not is_reply:
            root_comments.append(comment)
    
    # Migrate comments maintaining hierarchy
    migrated_map = {}
    
    def migrate_comment_tree(comment, parent_id=None):
        """Recursively migrate comment and its replies"""
        
        # Create comment in target
        body = comment['body']['storage']['value']
        
        # Add migration note
        migration_note = f"\n<p><em>[Migrated from {source_url} on {datetime.now().strftime('%Y-%m-%d')}]</em></p>"
        body += migration_note
        
        if parent_id:
            # It's a reply
            new_comment = create_comment(
                target_url,
                target_auth,
                parent_id,
                body
            )
        else:
            # It's a root comment
            new_comment = create_comment(
                target_url,
                target_auth,
                target_content_id,
                body
            )
        
        migrated_map[comment['id']] = new_comment['id']
        
        # Migrate replies
        replies = get_comment_replies(source_url, source_auth, comment['id'])
        
        for reply in replies.get('results', []):
            migrate_comment_tree(reply, new_comment['id'])
    
    # Migrate all root comments and their trees
    for root_comment in root_comments:
        migrate_comment_tree(root_comment)
    
    return {
        'total_migrated': len(migrated_map),
        'mapping': migrated_map
    }
```

### 6. Comment Notifications
```python
class CommentNotifier:
    """Handle comment notifications"""
    
    def __init__(self, base_url, auth, notification_handler):
        self.base_url = base_url
        self.auth = auth
        self.notification_handler = notification_handler
    
    def monitor_comments(self, content_ids, check_interval=300):
        """Monitor content for new comments"""
        
        import time
        
        last_check = {}
        
        # Initialize last check times
        for content_id in content_ids:
            last_check[content_id] = datetime.now()
        
        while True:
            for content_id in content_ids:
                # Get recent comments
                comments = get_comments(self.base_url, self.auth, content_id)
                
                # Check for new comments since last check
                new_comments = []
                
                for comment in comments:
                    comment_time = datetime.fromisoformat(
                        comment['version']['when'].replace('Z', '+00:00')
                    )
                    
                    if comment_time > last_check[content_id]:
                        new_comments.append(comment)
                
                # Send notifications for new comments
                if new_comments:
                    self._notify_new_comments(content_id, new_comments)
                
                # Update last check time
                last_check[content_id] = datetime.now()
            
            # Wait before next check
            time.sleep(check_interval)
    
    def _notify_new_comments(self, content_id, comments):
        """Send notifications for new comments"""
        
        for comment in comments:
            # Extract comment details
            author = comment['version']['by']['displayName']
            content = self._extract_text(comment['body']['storage']['value'])
            
            # Get page details
            page_url = f"{self.base_url}/rest/api/content/{content_id}"
            page = requests.get(page_url, auth=self.auth).json()
            
            # Send notification
            self.notification_handler({
                'type': 'new_comment',
                'page_title': page['title'],
                'page_id': content_id,
                'comment_author': author,
                'comment_preview': content[:100] + '...' if len(content) > 100 else content,
                'comment_id': comment['id']
            })
```

### 7. Bulk Comment Operations
```python
def bulk_comment_operations(base_url, auth, operations):
    """Perform bulk comment operations efficiently"""
    
    results = {
        'created': [],
        'updated': [],
        'deleted': [],
        'failed': []
    }
    
    for operation in operations:
        try:
            if operation['action'] == 'create':
                result = create_comment(
                    base_url,
                    auth,
                    operation['content_id'],
                    operation['text']
                )
                results['created'].append(result)
                
            elif operation['action'] == 'update':
                result = update_comment(
                    base_url,
                    auth,
                    operation['comment_id'],
                    operation['new_text']
                )
                results['updated'].append(result)
                
            elif operation['action'] == 'delete':
                requests.delete(
                    f"{base_url}/rest/api/content/{operation['comment_id']}",
                    auth=auth
                )
                results['deleted'].append(operation['comment_id'])
                
        except Exception as e:
            results['failed'].append({
                'operation': operation,
                'error': str(e)
            })
    
    return results
```

## Advanced Features

### Working with Comment Properties
```python
def add_comment_metadata(base_url, auth, comment_id, metadata):
    """Add custom metadata to a comment"""
    
    url = f"{base_url}/rest/api/content/{comment_id}/property"
    
    # Add multiple properties
    for key, value in metadata.items():
        payload = {
            "key": key,
            "value": value
        }
        
        requests.post(
            url,
            auth=auth,
            headers={"Content-Type": "application/json"},
            json=payload
        )
```

### Comment Search
```python
def search_comments(base_url, auth, search_term, space_key=None):
    """Search for comments containing specific text"""
    
    # Build CQL query
    cql = f'type=comment and text~"{search_term}"'
    
    if space_key:
        cql += f' and space={space_key}'
    
    search_url = f"{base_url}/rest/api/content/search"
    
    params = {
        "cql": cql,
        "limit": 100,
        "expand": "body.storage,container"
    }
    
    response = requests.get(search_url, auth=auth, params=params)
    return response.json()
```

### Comment Export
```python
def export_comments_to_csv(base_url, auth, content_id, output_file):
    """Export comments to CSV format"""
    
    import csv
    
    comments = get_comments(base_url, auth, content_id)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'author', 'date', 'content', 'parent_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for comment in comments:
            # Extract text content
            content = comment['body']['storage']['value']
            text = re.sub('<[^<]+?>', '', content)  # Strip HTML
            
            # Find parent comment if any
            parent_id = None
            for ancestor in comment.get('ancestors', []):
                if ancestor['type'] == 'comment':
                    parent_id = ancestor['id']
                    break
            
            writer.writerow({
                'id': comment['id'],
                'author': comment['version']['by']['displayName'],
                'date': comment['version']['when'],
                'content': text,
                'parent_id': parent_id or ''
            })
    
    return len(comments)
```