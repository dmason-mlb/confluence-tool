# Confluence Attachments API Reference

## Overview

The Confluence Attachments API provides functionality for uploading, downloading, updating, and managing file attachments on Confluence pages and blog posts. Attachments can include documents, images, spreadsheets, PDFs, and any other file types.

### Use Cases
- Automated documentation asset management
- Bulk file uploads for migration projects
- Image gallery creation
- Version control for attached documents
- Backup and archival of attachments
- Integration with external file storage systems
- Automated report attachment

## Authentication Requirements

All Attachment API operations require authentication:

### API Token (Recommended for Cloud)
```bash
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
  -X POST https://your-domain.atlassian.net/wiki/rest/api/content/{id}/child/attachment
```

### Basic Authentication
```bash
curl -u username:api_token \
  -X POST https://your-domain.atlassian.net/wiki/rest/api/content/{id}/child/attachment
```

## Available Endpoints

### 1. Upload Attachment
**Method:** POST  
**Path:** `/rest/api/content/{id}/child/attachment`

Uploads a new attachment to a page or blog post.

#### Headers Required
- `X-Atlassian-Token: no-check` (CSRF protection)
- `Content-Type: multipart/form-data`

#### cURL Example
```bash
curl -u user@example.com:api_token \
  -X POST \
  -H "X-Atlassian-Token: no-check" \
  -F "file=@/path/to/document.pdf" \
  -F "comment=Initial version" \
  "https://your-domain.atlassian.net/wiki/rest/api/content/123456789/child/attachment"
```

#### Python Example
```python
import requests
import os

def upload_attachment(base_url, auth, content_id, file_path, comment=None):
    """Upload a file attachment to a Confluence page or blog post"""
    
    url = f"{base_url}/rest/api/content/{content_id}/child/attachment"
    
    headers = {
        "X-Atlassian-Token": "no-check"
    }
    
    with open(file_path, 'rb') as file:
        files = {
            'file': (os.path.basename(file_path), file)
        }
        
        data = {}
        if comment:
            data['comment'] = comment
        
        response = requests.post(
            url,
            auth=auth,
            headers=headers,
            files=files,
            data=data
        )
    
    return response.json()

# Usage
attachment = upload_attachment(
    "https://your-domain.atlassian.net/wiki",
    ("user@example.com", "api_token"),
    "123456789",
    "/path/to/report.pdf",
    "Q4 2024 Financial Report"
)
```

#### Response Example
```json
{
  "results": [
    {
      "id": "att987654321",
      "type": "attachment",
      "status": "current",
      "title": "report.pdf",
      "metadata": {
        "mediaType": "application/pdf",
        "size": 1048576
      },
      "extensions": {
        "mediaType": "application/pdf",
        "fileSize": 1048576,
        "comment": "Q4 2024 Financial Report"
      },
      "version": {
        "by": {
          "type": "known",
          "username": "john.doe",
          "displayName": "John Doe"
        },
        "when": "2024-01-15T10:30:00.000Z",
        "number": 1
      }
    }
  ]
}
```

### 2. Get Attachments
**Method:** GET  
**Path:** `/rest/api/content/{id}/child/attachment`

Lists all attachments for a specific page or blog post.

#### Parameters
- `start`: Pagination start index
- `limit`: Maximum results (default: 25, max: 100)
- `expand`: Properties to expand
- `filename`: Filter by filename
- `mediaType`: Filter by media type

#### Python Example
```python
def get_attachments(base_url, auth, content_id, filename=None, media_type=None):
    """Get all attachments for a page or blog post"""
    
    url = f"{base_url}/rest/api/content/{content_id}/child/attachment"
    
    params = {
        "expand": "version,metadata",
        "limit": 100
    }
    
    if filename:
        params["filename"] = filename
    if media_type:
        params["mediaType"] = media_type
    
    response = requests.get(url, auth=auth, params=params)
    return response.json()

# Get all PDF attachments
pdf_attachments = get_attachments(
    "https://your-domain.atlassian.net/wiki",
    auth,
    "123456789",
    media_type="application/pdf"
)
```

### 3. Download Attachment
**Method:** GET  
**Path:** `/rest/api/content/{id}/download`

Downloads an attachment file.

#### Python Download Example
```python
def download_attachment(base_url, auth, attachment_id, save_path):
    """Download an attachment to local file system"""
    
    # Get attachment metadata first
    metadata_url = f"{base_url}/rest/api/content/{attachment_id}"
    metadata = requests.get(metadata_url, auth=auth).json()
    
    # Download the file
    download_url = f"{base_url}/rest/api/content/{attachment_id}/download"
    
    response = requests.get(download_url, auth=auth, stream=True)
    response.raise_for_status()
    
    # Save to file
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    
    return {
        'filename': metadata['title'],
        'size': metadata['extensions']['fileSize'],
        'saved_to': save_path
    }

# Download attachment
result = download_attachment(
    "https://your-domain.atlassian.net/wiki",
    auth,
    "att987654321",
    "/local/path/downloaded_report.pdf"
)
```

### 4. Update Attachment
**Method:** POST  
**Path:** `/rest/api/content/{content_id}/child/attachment/{attachment_id}/data`

Updates an existing attachment with a new version.

#### cURL Example
```bash
curl -u user@example.com:api_token \
  -X POST \
  -H "X-Atlassian-Token: no-check" \
  -F "file=@/path/to/updated_document.pdf" \
  -F "comment=Updated with Q4 results" \
  "https://your-domain.atlassian.net/wiki/rest/api/content/123456789/child/attachment/att987654321/data"
```

#### Python Update Example
```python
def update_attachment(base_url, auth, content_id, attachment_id, new_file_path, comment=None):
    """Update an existing attachment with a new version"""
    
    url = f"{base_url}/rest/api/content/{content_id}/child/attachment/{attachment_id}/data"
    
    headers = {
        "X-Atlassian-Token": "no-check"
    }
    
    with open(new_file_path, 'rb') as file:
        files = {
            'file': (os.path.basename(new_file_path), file)
        }
        
        data = {}
        if comment:
            data['comment'] = comment
        
        response = requests.post(
            url,
            auth=auth,
            headers=headers,
            files=files,
            data=data
        )
    
    return response.json()
```

### 5. Delete Attachment
**Method:** DELETE  
**Path:** `/rest/api/content/{id}`

Deletes an attachment (moves to trash or permanently deletes).

#### cURL Example
```bash
# Move to trash
curl -X DELETE -u user@example.com:api_token \
  "https://your-domain.atlassian.net/wiki/rest/api/content/att987654321?status=trashed"

# Permanent delete (requires admin)
curl -X DELETE -u admin@example.com:api_token \
  "https://your-domain.atlassian.net/wiki/rest/api/content/att987654321"
```

### 6. Get Attachment Properties
**Method:** GET  
**Path:** `/rest/api/content/{id}/property`

Retrieves custom properties of an attachment.

#### Python Example
```python
def get_attachment_properties(base_url, auth, attachment_id):
    """Get all custom properties of an attachment"""
    
    url = f"{base_url}/rest/api/content/{attachment_id}/property"
    
    response = requests.get(url, auth=auth)
    return response.json()

# Get properties
properties = get_attachment_properties(
    "https://your-domain.atlassian.net/wiki",
    auth,
    "att987654321"
)
```

### 7. Set Attachment Property
**Method:** POST  
**Path:** `/rest/api/content/{id}/property`

Sets a custom property on an attachment.

#### Python Example
```python
def set_attachment_property(base_url, auth, attachment_id, key, value):
    """Set a custom property on an attachment"""
    
    url = f"{base_url}/rest/api/content/{attachment_id}/property"
    
    payload = {
        "key": key,
        "value": value
    }
    
    response = requests.post(
        url,
        auth=auth,
        headers={"Content-Type": "application/json"},
        json=payload
    )
    
    return response.json()

# Tag attachment with metadata
set_attachment_property(
    "https://your-domain.atlassian.net/wiki",
    auth,
    "att987654321",
    "document-status",
    {"status": "approved", "approver": "jane.doe", "date": "2024-01-15"}
)
```

## Common Parameters

### File Upload Parameters
- `file`: The file to upload (multipart/form-data)
- `comment`: Version comment for the upload
- `minorEdit`: Whether this is a minor edit (boolean)

### Query Parameters
- `filename`: Filter by filename (exact or partial match)
- `mediaType`: Filter by MIME type
- `expand`: Expand additional properties
  - `version`: Version information
  - `metadata`: File metadata
  - `container`: Parent page/blog post
  - `operations`: Available operations
  - `restrictions`: Access restrictions

### Expansion Options
- `metadata`: File metadata including size and type
- `version`: Version history information
- `ancestors`: Parent content hierarchy
- `container`: Parent page or blog post
- `operations`: Available operations on the attachment
- `restrictions`: View/edit restrictions

## Error Handling

### Common Error Scenarios

#### 1. File Size Limit Exceeded
```json
{
  "statusCode": 413,
  "message": "File size exceeds maximum allowed size of 100MB"
}
```

#### 2. Unsupported File Type
```json
{
  "statusCode": 415,
  "message": "File type not supported"
}
```

#### 3. No Permission
```json
{
  "statusCode": 403,
  "message": "User does not have permission to add attachments"
}
```

### Python Error Handling
```python
def safe_upload_attachment(base_url, auth, content_id, file_path, max_retries=3):
    """Upload attachment with comprehensive error handling"""
    
    # Check file size before upload
    file_size = os.path.getsize(file_path)
    if file_size > 100 * 1024 * 1024:  # 100MB limit
        raise ValueError(f"File size {file_size} exceeds 100MB limit")
    
    for attempt in range(max_retries):
        try:
            result = upload_attachment(base_url, auth, content_id, file_path)
            return result
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 413:
                print("File too large")
                raise
            elif e.response.status_code == 415:
                print("Unsupported file type")
                raise
            elif e.response.status_code == 401:
                print("Authentication failed")
                raise
            elif e.response.status_code == 403:
                print("No permission to upload attachments")
                raise
            elif e.response.status_code == 429:
                # Rate limited - retry with backoff
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
            raise
```

## Best Practices

### 1. File Size Management
```python
def upload_large_file_chunked(base_url, auth, content_id, file_path, chunk_size=50*1024*1024):
    """Upload large files in chunks if needed"""
    
    file_size = os.path.getsize(file_path)
    
    if file_size <= chunk_size:
        # Small file - direct upload
        return upload_attachment(base_url, auth, content_id, file_path)
    else:
        # For very large files, consider:
        # 1. Compress the file first
        # 2. Split into multiple attachments
        # 3. Use external storage with link
        print(f"File size {file_size} may require special handling")
        
        # Example: Compress before upload
        import zipfile
        zip_path = file_path + ".zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, os.path.basename(file_path))
        
        return upload_attachment(base_url, auth, content_id, zip_path)
```

### 2. Bulk Upload Management
```python
def bulk_upload_attachments(base_url, auth, content_id, file_paths, batch_size=5):
    """Upload multiple files with rate limiting"""
    
    uploaded = []
    failed = []
    
    for i in range(0, len(file_paths), batch_size):
        batch = file_paths[i:i + batch_size]
        
        for file_path in batch:
            try:
                result = upload_attachment(base_url, auth, content_id, file_path)
                uploaded.append({
                    'file': file_path,
                    'attachment_id': result['results'][0]['id'],
                    'title': result['results'][0]['title']
                })
                print(f"Uploaded: {os.path.basename(file_path)}")
                
            except Exception as e:
                failed.append({
                    'file': file_path,
                    'error': str(e)
                })
                print(f"Failed: {os.path.basename(file_path)} - {e}")
        
        # Rate limiting between batches
        if i + batch_size < len(file_paths):
            time.sleep(2)
    
    return {
        'uploaded': uploaded,
        'failed': failed,
        'total': len(file_paths)
    }
```

### 3. Attachment Organization
```python
class AttachmentManager:
    """Manage attachments with organization and metadata"""
    
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth
    
    def upload_with_metadata(self, content_id, file_path, category, tags):
        """Upload attachment with organizational metadata"""
        
        # Upload file
        result = upload_attachment(self.base_url, self.auth, content_id, file_path)
        attachment_id = result['results'][0]['id']
        
        # Add metadata
        metadata = {
            "category": category,
            "tags": tags,
            "upload_date": datetime.now().isoformat(),
            "original_filename": os.path.basename(file_path)
        }
        
        set_attachment_property(
            self.base_url,
            self.auth,
            attachment_id,
            "attachment-metadata",
            metadata
        )
        
        return attachment_id
    
    def find_attachments_by_category(self, content_id, category):
        """Find all attachments with a specific category"""
        
        # Get all attachments
        attachments = get_attachments(self.base_url, self.auth, content_id)
        
        categorized = []
        
        for attachment in attachments['results']:
            # Get properties
            props = get_attachment_properties(
                self.base_url,
                self.auth,
                attachment['id']
            )
            
            # Check category
            for prop in props['results']:
                if prop['key'] == 'attachment-metadata':
                    if prop['value'].get('category') == category:
                        categorized.append(attachment)
        
        return categorized
```

### 4. Version Control
```python
def manage_attachment_versions(base_url, auth, content_id, attachment_id, keep_versions=5):
    """Manage attachment versions, keeping only recent ones"""
    
    # Get attachment history
    url = f"{base_url}/rest/api/content/{attachment_id}?expand=version,history"
    response = requests.get(url, auth=auth)
    attachment = response.json()
    
    # Get all versions
    history_url = f"{base_url}/rest/api/content/{attachment_id}/history"
    history = requests.get(history_url, auth=auth).json()
    
    if history['size'] > keep_versions:
        # Delete old versions (keeping most recent)
        versions_to_delete = history['results'][keep_versions:]
        
        for version in versions_to_delete:
            # Note: Confluence may not allow deletion of individual versions
            # This is a conceptual example
            print(f"Would delete version {version['number']} from {version['when']}")
    
    return history['size']
```

### 5. Image Gallery Creation
```python
def create_image_gallery(base_url, auth, page_id, image_folder):
    """Create an image gallery on a page"""
    
    # Upload all images
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    images = []
    
    for filename in os.listdir(image_folder):
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            file_path = os.path.join(image_folder, filename)
            
            result = upload_attachment(base_url, auth, page_id, file_path)
            images.append({
                'id': result['results'][0]['id'],
                'title': result['results'][0]['title']
            })
    
    # Update page with gallery
    if images:
        gallery_html = '<h2>Image Gallery</h2><p>'
        
        for image in images:
            gallery_html += f'''
            <ac:image>
                <ri:attachment ri:filename="{image['title']}" />
            </ac:image>
            '''
        
        gallery_html += '</p>'
        
        # Update page content (simplified - would need current content)
        print(f"Gallery created with {len(images)} images")
    
    return images
```

### 6. Attachment Backup
```python
def backup_all_attachments(base_url, auth, space_key, backup_dir):
    """Backup all attachments from a space"""
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Search for all content in space
    cql = f"space={space_key} and type in (page, blogpost)"
    search_url = f"{base_url}/rest/api/content/search"
    
    params = {
        "cql": cql,
        "limit": 100,
        "expand": "metadata"
    }
    
    response = requests.get(search_url, auth=auth, params=params)
    content_items = response.json()
    
    total_attachments = 0
    
    for item in content_items['results']:
        # Get attachments for each content item
        attachments = get_attachments(base_url, auth, item['id'])
        
        if attachments['results']:
            # Create directory for this content
            content_dir = os.path.join(
                backup_dir,
                f"{item['id']}_{item['title'].replace('/', '_')}"
            )
            os.makedirs(content_dir, exist_ok=True)
            
            for attachment in attachments['results']:
                # Download each attachment
                save_path = os.path.join(content_dir, attachment['title'])
                
                try:
                    download_attachment(
                        base_url,
                        auth,
                        attachment['id'],
                        save_path
                    )
                    total_attachments += 1
                    print(f"Backed up: {attachment['title']}")
                    
                except Exception as e:
                    print(f"Failed to backup {attachment['title']}: {e}")
    
    return total_attachments
```

### 7. Attachment Migration
```python
def migrate_attachments(source_url, source_auth, target_url, target_auth, 
                       source_content_id, target_content_id):
    """Migrate attachments between Confluence instances"""
    
    # Get source attachments
    attachments = get_attachments(source_url, source_auth, source_content_id)
    
    migrated = []
    
    for attachment in attachments['results']:
        try:
            # Download from source
            temp_file = f"/tmp/{attachment['id']}_{attachment['title']}"
            download_attachment(
                source_url,
                source_auth,
                attachment['id'],
                temp_file
            )
            
            # Upload to target
            result = upload_attachment(
                target_url,
                target_auth,
                target_content_id,
                temp_file,
                f"Migrated from {source_url}"
            )
            
            migrated.append({
                'source_id': attachment['id'],
                'target_id': result['results'][0]['id'],
                'title': attachment['title']
            })
            
            # Cleanup temp file
            os.remove(temp_file)
            
        except Exception as e:
            print(f"Failed to migrate {attachment['title']}: {e}")
    
    return migrated
```

## Advanced Features

### Working with Inline Images
```python
def process_inline_images(base_url, auth, page_id, content_with_images):
    """Process content with inline images"""
    
    import re
    
    # Find image references in content
    image_pattern = r'<ri:attachment ri:filename="([^"]+)"'
    images = re.findall(image_pattern, content_with_images)
    
    # Verify all images exist
    existing_attachments = get_attachments(base_url, auth, page_id)
    attached_files = [att['title'] for att in existing_attachments['results']]
    
    missing_images = [img for img in images if img not in attached_files]
    
    if missing_images:
        print(f"Missing images: {missing_images}")
        # Handle missing images...
    
    return {
        'referenced': images,
        'existing': attached_files,
        'missing': missing_images
    }
```

### Attachment Search
```python
def search_attachments_by_content(base_url, auth, space_key, search_term):
    """Search for attachments containing specific content"""
    
    # Note: Direct content search in attachments may be limited
    # This searches by filename and metadata
    
    cql = f'type=attachment and space={space_key} and title~"{search_term}"'
    
    search_url = f"{base_url}/rest/api/content/search"
    params = {
        "cql": cql,
        "limit": 100
    }
    
    response = requests.get(search_url, auth=auth, params=params)
    return response.json()
```

### Attachment Analytics
```python
def get_attachment_statistics(base_url, auth, space_key):
    """Get statistics about attachments in a space"""
    
    stats = {
        'total_attachments': 0,
        'total_size': 0,
        'by_type': {},
        'by_page': {},
        'largest_files': []
    }
    
    # Search for all content
    cql = f"space={space_key} and type in (page, blogpost)"
    content_items = search_pages(base_url, auth, cql)
    
    all_attachments = []
    
    for item in content_items['results']:
        attachments = get_attachments(base_url, auth, item['id'])
        
        for att in attachments['results']:
            size = att['extensions']['fileSize']
            media_type = att['extensions']['mediaType']
            
            stats['total_attachments'] += 1
            stats['total_size'] += size
            
            # By type
            stats['by_type'][media_type] = stats['by_type'].get(media_type, 0) + 1
            
            # By page
            page_title = item['title']
            if page_title not in stats['by_page']:
                stats['by_page'][page_title] = {'count': 0, 'size': 0}
            
            stats['by_page'][page_title]['count'] += 1
            stats['by_page'][page_title]['size'] += size
            
            # Track for largest files
            all_attachments.append({
                'title': att['title'],
                'size': size,
                'page': page_title
            })
    
    # Get largest files
    stats['largest_files'] = sorted(
        all_attachments,
        key=lambda x: x['size'],
        reverse=True
    )[:10]
    
    # Convert size to human readable
    stats['total_size_mb'] = round(stats['total_size'] / (1024 * 1024), 2)
    
    return stats
```