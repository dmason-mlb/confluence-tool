# Confluence Blog Posts API Reference

## Overview

The Confluence Blog Posts API enables programmatic creation, retrieval, updating, and deletion of blog posts within Confluence spaces. Blog posts are time-based content entries that are ideal for announcements, updates, and periodic communications.

### Use Cases
- Automated release notes publication
- Team status update automation
- News feed integration
- Event announcements
- Knowledge base article scheduling
- Cross-platform content syndication
- Periodic report generation

## Authentication Requirements

Blog Post API endpoints require the same authentication methods as other Confluence APIs:

### API Token Authentication (Recommended)
```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
  https://your-domain.atlassian.net/wiki/rest/api/content
```

### Basic Authentication
```bash
curl -u username:api_token \
  https://your-domain.atlassian.net/wiki/rest/api/content
```

### OAuth 2.0
For applications requiring delegated access with user consent.

## Available Endpoints

### 1. Create Blog Post
**Method:** POST  
**Path:** `/rest/api/content`

Creates a new blog post in a specified space.

#### Request Example
```json
{
  "type": "blogpost",
  "title": "Q4 2024 Release Notes",
  "space": {
    "key": "BLOG"
  },
  "body": {
    "storage": {
      "value": "<h2>New Features</h2><p>Feature descriptions here</p>",
      "representation": "storage"
    }
  },
  "metadata": {
    "properties": {
      "publish-date": "2024-01-15"
    }
  }
}
```

#### Python Example
```python
import requests
import json
from datetime import datetime

def create_blog_post(base_url, auth, space_key, title, content, publish_date=None):
    url = f"{base_url}/rest/api/content"
    
    payload = {
        "type": "blogpost",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        }
    }
    
    # Add publish date if specified
    if publish_date:
        payload["metadata"] = {
            "properties": {
                "publish-date": publish_date
            }
        }
    
    response = requests.post(
        url,
        auth=auth,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    
    return response.json()

# Usage example
auth = ("user@example.com", "api_token")
blog_post = create_blog_post(
    "https://your-domain.atlassian.net/wiki",
    auth,
    "BLOG",
    "Weekly Team Update - Week 3",
    """<h2>Achievements</h2>
    <ul>
        <li>Completed API integration</li>
        <li>Fixed critical bugs</li>
    </ul>
    <h2>Next Week</h2>
    <p>Focus on performance optimization</p>""",
    datetime.now().strftime("%Y-%m-%d")
)
```

### 2. Get Blog Post
**Method:** GET  
**Path:** `/rest/api/content/{id}`

Retrieves a blog post by its ID.

#### Common Parameters
- `expand`: Properties to expand
  - `body.storage`: Raw content
  - `body.view`: Rendered HTML
  - `version`: Version info
  - `space`: Space details
  - `history`: Change history
  - `metadata`: Custom metadata

#### cURL Example
```bash
curl -u user@example.com:api_token \
  "https://your-domain.atlassian.net/wiki/rest/api/content/987654321?expand=body.storage,version,metadata"
```

#### Response Example
```json
{
  "id": "987654321",
  "type": "blogpost",
  "status": "current",
  "title": "Q4 2024 Release Notes",
  "space": {
    "id": 12345,
    "key": "BLOG",
    "name": "Company Blog"
  },
  "body": {
    "storage": {
      "value": "<h2>New Features</h2><p>Content here</p>",
      "representation": "storage"
    }
  },
  "version": {
    "by": {
      "type": "known",
      "username": "jane.smith",
      "displayName": "Jane Smith"
    },
    "when": "2024-01-15T14:30:00.000Z",
    "number": 1
  },
  "metadata": {
    "properties": {
      "publish-date": "2024-01-15"
    }
  }
}
```

### 3. List Blog Posts in Space
**Method:** GET  
**Path:** `/rest/api/content`

Lists all blog posts in a specific space.

#### Parameters
- `spaceKey`: Space key
- `type`: Set to "blogpost"
- `start`: Starting index
- `limit`: Maximum results
- `orderby`: Sort order (e.g., "created", "modified")

#### Python Example
```python
def list_blog_posts(base_url, auth, space_key, limit=25):
    url = f"{base_url}/rest/api/content"
    
    params = {
        "spaceKey": space_key,
        "type": "blogpost",
        "limit": limit,
        "expand": "body.storage,version",
        "orderby": "-created"  # Most recent first
    }
    
    response = requests.get(url, auth=auth, params=params)
    return response.json()

# Get recent blog posts
recent_posts = list_blog_posts(
    "https://your-domain.atlassian.net/wiki",
    auth,
    "BLOG",
    limit=10
)
```

### 4. Update Blog Post
**Method:** PUT  
**Path:** `/rest/api/content/{id}`

Updates an existing blog post.

#### Request Example
```json
{
  "id": "987654321",
  "type": "blogpost",
  "title": "Q4 2024 Release Notes - Updated",
  "space": {
    "key": "BLOG"
  },
  "body": {
    "storage": {
      "value": "<h2>New Features</h2><p>Updated content</p>",
      "representation": "storage"
    }
  },
  "version": {
    "number": 2,
    "minorEdit": false
  }
}
```

#### Python Example
```python
def update_blog_post(base_url, auth, post_id, title, content, version_number):
    # First, get current version
    current = requests.get(
        f"{base_url}/rest/api/content/{post_id}?expand=version",
        auth=auth
    ).json()
    
    url = f"{base_url}/rest/api/content/{post_id}"
    
    payload = {
        "id": post_id,
        "type": "blogpost",
        "title": title,
        "space": {"key": current['space']['key']},
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        },
        "version": {
            "number": current['version']['number'] + 1,
            "minorEdit": False
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

### 5. Delete Blog Post
**Method:** DELETE  
**Path:** `/rest/api/content/{id}`

Deletes a blog post or moves it to trash.

#### cURL Example
```bash
# Move to trash
curl -X DELETE -u user@example.com:api_token \
  "https://your-domain.atlassian.net/wiki/rest/api/content/987654321?status=trashed"
```

### 6. Search Blog Posts
**Method:** GET  
**Path:** `/rest/api/content/search`

Search blog posts using CQL.

#### CQL Examples for Blog Posts
```bash
# Find blog posts by space
cql=type=blogpost and space=BLOG

# Find blog posts by title
cql=type=blogpost and title~"Release Notes"

# Find recent blog posts
cql=type=blogpost and created>now("-30d")

# Find blog posts by author
cql=type=blogpost and creator="john.doe"

# Find blog posts with specific labels
cql=type=blogpost and label="announcement"
```

#### Python Search Example
```python
def search_blog_posts(base_url, auth, search_term, space_key=None):
    url = f"{base_url}/rest/api/content/search"
    
    cql = f'type=blogpost and title~"{search_term}"'
    if space_key:
        cql += f' and space={space_key}'
    
    params = {
        "cql": cql,
        "limit": 50,
        "expand": "body.storage,metadata"
    }
    
    response = requests.get(url, auth=auth, params=params)
    return response.json()
```

### 7. Get Blog Post Comments
**Method:** GET  
**Path:** `/rest/api/content/{id}/child/comment`

Retrieves comments on a blog post.

#### cURL Example
```bash
curl -u user@example.com:api_token \
  "https://your-domain.atlassian.net/wiki/rest/api/content/987654321/child/comment?expand=body.storage"
```

## Common Parameters

### Content Representation
- `storage`: Confluence storage format (XML/HTML)
- `view`: Rendered HTML for display
- `export_view`: HTML suitable for export
- `styled_view`: HTML with Confluence styling
- `editor`: Format for Confluence editor

### Expansion Options
- `body.storage`: Raw content
- `body.view`: Rendered content
- `version`: Version information
- `ancestors`: Parent content
- `children`: Child content
- `descendants`: All descendants
- `space`: Space information
- `history`: Change history
- `metadata`: Custom properties
- `restrictions`: Access restrictions

## Error Handling

### Common Error Scenarios

#### 1. Duplicate Title
```json
{
  "statusCode": 400,
  "message": "A blog post with this title already exists in this space"
}
```

#### 2. Space Not Found
```json
{
  "statusCode": 404,
  "message": "No space with key 'INVALID' exists"
}
```

#### 3. Version Conflict
```json
{
  "statusCode": 409,
  "message": "Version conflict - page has been modified"
}
```

### Python Error Handling Pattern
```python
def robust_create_blog_post(base_url, auth, space_key, title, content, max_retries=3):
    """Create blog post with retry logic and error handling"""
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{base_url}/rest/api/content",
                auth=auth,
                headers={"Content-Type": "application/json"},
                json={
                    "type": "blogpost",
                    "title": title,
                    "space": {"key": space_key},
                    "body": {"storage": {"value": content, "representation": "storage"}}
                }
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                # Check if title exists
                if "already exists" in response.text:
                    title = f"{title} - {datetime.now().strftime('%Y%m%d%H%M%S')}"
                    continue
            else:
                response.raise_for_status()
                
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

## Best Practices

### 1. Content Management
- Use meaningful titles with dates for time-sensitive content
- Include metadata for better organization
- Tag blog posts with appropriate labels
- Use consistent formatting templates

### 2. Publishing Strategy
```python
def schedule_blog_post(base_url, auth, space_key, title, content, publish_date):
    """Create a blog post with scheduled publishing"""
    
    # Create as draft first
    draft = create_blog_post(base_url, auth, space_key, f"DRAFT: {title}", content)
    
    # Add scheduling metadata
    metadata_url = f"{base_url}/rest/api/content/{draft['id']}/property"
    
    requests.post(
        metadata_url,
        auth=auth,
        json={
            "key": "scheduled-publish",
            "value": {
                "publishDate": publish_date,
                "originalTitle": title
            }
        }
    )
    
    return draft
```

### 3. Template-Based Creation
```python
def create_weekly_update(base_url, auth, space_key, week_number, updates):
    """Create standardized weekly update blog post"""
    
    template = """
    <h2>Week {week} Summary</h2>
    
    <h3>Completed Items</h3>
    <ul>
    {completed_items}
    </ul>
    
    <h3>In Progress</h3>
    <ul>
    {in_progress_items}
    </ul>
    
    <h3>Upcoming</h3>
    <ul>
    {upcoming_items}
    </ul>
    
    <h3>Team Notes</h3>
    <p>{notes}</p>
    """
    
    content = template.format(
        week=week_number,
        completed_items="".join(f"<li>{item}</li>" for item in updates['completed']),
        in_progress_items="".join(f"<li>{item}</li>" for item in updates['in_progress']),
        upcoming_items="".join(f"<li>{item}</li>" for item in updates['upcoming']),
        notes=updates.get('notes', 'No additional notes')
    )
    
    return create_blog_post(
        base_url,
        auth,
        space_key,
        f"Week {week_number} Team Update - {datetime.now().strftime('%B %d, %Y')}",
        content
    )
```

### 4. Blog Post Series Management
```python
class BlogPostSeries:
    """Manage a series of related blog posts"""
    
    def __init__(self, base_url, auth, space_key, series_name):
        self.base_url = base_url
        self.auth = auth
        self.space_key = space_key
        self.series_name = series_name
        
    def create_episode(self, episode_number, title, content):
        """Create a new episode in the series"""
        
        full_title = f"{self.series_name} - Part {episode_number}: {title}"
        
        # Add series navigation
        nav_content = self._generate_navigation(episode_number)
        full_content = nav_content + content
        
        post = create_blog_post(
            self.base_url,
            self.auth,
            self.space_key,
            full_title,
            full_content
        )
        
        # Add series label
        self._add_label(post['id'], f"series-{self.series_name.lower().replace(' ', '-')}")
        
        return post
    
    def _generate_navigation(self, current_episode):
        """Generate navigation links for the series"""
        
        # Search for other episodes
        cql = f'type=blogpost and title~"{self.series_name}" and space={self.space_key}'
        results = search_blog_posts(self.base_url, self.auth, self.series_name, self.space_key)
        
        nav = '<div class="series-navigation"><h4>Series Navigation</h4><ul>'
        
        for post in sorted(results['results'], key=lambda x: x['title']):
            if f"Part {current_episode}:" in post['title']:
                nav += f'<li><strong>{post["title"]}</strong> (Current)</li>'
            else:
                nav += f'<li><a href="/wiki/spaces/{self.space_key}/blog/{post["id"]}">{post["title"]}</a></li>'
        
        nav += '</ul></div><hr/>'
        
        return nav
```

### 5. Analytics and Metrics
```python
def get_blog_post_metrics(base_url, auth, space_key, days=30):
    """Get blog post metrics for the last N days"""
    
    # Search for recent blog posts
    cql = f'type=blogpost and space={space_key} and created>now("-{days}d")'
    
    results = search_blog_posts(base_url, auth, "", space_key)
    
    metrics = {
        'total_posts': len(results['results']),
        'authors': {},
        'posts_by_day': {},
        'most_viewed': [],
        'most_commented': []
    }
    
    for post in results['results']:
        # Count by author
        author = post['version']['by']['displayName']
        metrics['authors'][author] = metrics['authors'].get(author, 0) + 1
        
        # Count by day
        created_date = post['version']['when'][:10]
        metrics['posts_by_day'][created_date] = metrics['posts_by_day'].get(created_date, 0) + 1
    
    return metrics
```

### 6. Content Migration
```python
def migrate_blog_posts(source_url, source_auth, target_url, target_auth, 
                      source_space, target_space, label_filter=None):
    """Migrate blog posts between spaces or instances"""
    
    # Build search query
    cql = f'type=blogpost and space={source_space}'
    if label_filter:
        cql += f' and label="{label_filter}"'
    
    # Get source blog posts
    posts = search_blog_posts(source_url, source_auth, "", source_space)
    
    migrated = []
    
    for post in posts['results']:
        # Get full content
        full_post = requests.get(
            f"{source_url}/rest/api/content/{post['id']}?expand=body.storage,metadata,attachments",
            auth=source_auth
        ).json()
        
        try:
            # Create in target
            new_post = create_blog_post(
                target_url,
                target_auth,
                target_space,
                full_post['title'],
                full_post['body']['storage']['value']
            )
            
            migrated.append({
                'source_id': post['id'],
                'target_id': new_post['id'],
                'title': post['title']
            })
            
            print(f"Migrated: {post['title']}")
            
        except Exception as e:
            print(f"Failed to migrate {post['title']}: {e}")
    
    return migrated
```

### 7. Automated Reporting
```python
def create_monthly_report(base_url, auth, space_key, report_data):
    """Create automated monthly report blog post"""
    
    month = datetime.now().strftime("%B %Y")
    
    content = f"""
    <h2>Monthly Report - {month}</h2>
    
    <ac:structured-macro ac:name="panel">
        <ac:parameter ac:name="title">Key Metrics</ac:parameter>
        <ac:rich-text-body>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                    <th>Change</th>
                </tr>
                <tr>
                    <td>Total Users</td>
                    <td>{report_data['users']}</td>
                    <td>{report_data['user_change']}%</td>
                </tr>
                <tr>
                    <td>Active Projects</td>
                    <td>{report_data['projects']}</td>
                    <td>{report_data['project_change']}%</td>
                </tr>
            </table>
        </ac:rich-text-body>
    </ac:structured-macro>
    
    <h3>Highlights</h3>
    <ul>
        {"".join(f"<li>{highlight}</li>" for highlight in report_data['highlights'])}
    </ul>
    
    <h3>Upcoming</h3>
    <ul>
        {"".join(f"<li>{item}</li>" for item in report_data['upcoming'])}
    </ul>
    """
    
    return create_blog_post(
        base_url,
        auth,
        space_key,
        f"Monthly Report - {month}",
        content
    )
```

## Advanced Features

### Working with Macros
```python
def create_blog_with_macros(base_url, auth, space_key, title):
    """Create blog post with Confluence macros"""
    
    content = """
    <h2>Status Update</h2>
    
    <ac:structured-macro ac:name="status">
        <ac:parameter ac:name="colour">Green</ac:parameter>
        <ac:parameter ac:name="title">On Track</ac:parameter>
    </ac:structured-macro>
    
    <h2>Recent Changes</h2>
    
    <ac:structured-macro ac:name="recently-updated">
        <ac:parameter ac:name="spaces">DEV</ac:parameter>
        <ac:parameter ac:name="max">10</ac:parameter>
    </ac:structured-macro>
    
    <h2>Team Calendar</h2>
    
    <ac:structured-macro ac:name="calendar">
        <ac:parameter ac:name="spaceKey">TEAM</ac:parameter>
    </ac:structured-macro>
    """
    
    return create_blog_post(base_url, auth, space_key, title, content)
```

### Label Management
```python
def manage_blog_labels(base_url, auth, post_id, labels_to_add, labels_to_remove=None):
    """Add or remove labels from a blog post"""
    
    # Add labels
    for label in labels_to_add:
        requests.post(
            f"{base_url}/rest/api/content/{post_id}/label",
            auth=auth,
            json=[{"name": label}]
        )
    
    # Remove labels if specified
    if labels_to_remove:
        for label in labels_to_remove:
            requests.delete(
                f"{base_url}/rest/api/content/{post_id}/label/{label}",
                auth=auth
            )
```