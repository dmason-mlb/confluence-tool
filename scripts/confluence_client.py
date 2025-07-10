#!/usr/bin/env python3
"""
Confluence Cloud API v2 Client

A comprehensive Python client for interacting with Confluence Cloud REST API v2.
Supports all major operations including pages, blog posts, attachments, and more.
"""

import json
import base64
import requests
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import time
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfluenceClient:
    """Main client for Confluence Cloud API v2 operations."""
    
    def __init__(self, domain: str, email: str, api_token: str):
        """
        Initialize Confluence client.
        
        Args:
            domain: Your Confluence domain (e.g., 'yoursite.atlassian.net')
            email: Your email address
            api_token: Your API token
        """
        self.domain = domain.rstrip('/')
        self.email = email
        self.base_url = f"https://{domain}/wiki/api/v2"
        self.auth = self._create_auth(email, api_token)
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': self.auth,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _create_auth(self, email: str, api_token: str) -> str:
        """Create Basic auth header."""
        credentials = f"{email}:{api_token}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"
    
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Make HTTP request with error handling and rate limiting.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request parameters
            
        Returns:
            Response object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Rate limiting retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.session.request(method, url, **kwargs)
                
                if response.status_code == 429:  # Rate limited
                    retry_after = int(response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                
                response.raise_for_status()
                return response
                
            except requests.exceptions.HTTPError as e:
                if attempt == max_retries - 1:
                    logger.error(f"Request failed: {e}")
                    logger.error(f"Response: {response.text}")
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return response
    
    def _paginate(self, endpoint: str, params: Dict = None, limit: int = None) -> List[Dict]:
        """
        Handle pagination for list endpoints.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            limit: Maximum items to return (None for all)
            
        Returns:
            List of all items
        """
        if params is None:
            params = {}
        
        items = []
        params['limit'] = 25  # API max per page
        start = 0
        
        while True:
            params['start'] = start
            response = self._request('GET', endpoint, params=params)
            data = response.json()
            
            items.extend(data.get('results', []))
            
            if limit and len(items) >= limit:
                return items[:limit]
            
            # Check if more pages exist
            if not data.get('_links', {}).get('next'):
                break
                
            start += params['limit']
        
        return items
    
    # Page Operations
    
    def create_page(self, space_id: int, title: str, content: str, 
                   parent_id: Optional[int] = None, **kwargs) -> Dict:
        """
        Create a new page.
        
        Args:
            space_id: Space ID
            title: Page title
            content: Page content (HTML or storage format)
            parent_id: Optional parent page ID
            **kwargs: Additional page properties
            
        Returns:
            Created page data
        """
        data = {
            'spaceId': str(space_id),
            'status': kwargs.get('status', 'current'),
            'title': title,
            'body': {
                'value': content,
                'representation': kwargs.get('representation', 'storage')
            }
        }
        
        if parent_id:
            data['parentId'] = parent_id
        
        data.update(kwargs)
        logger.info(f"Creating page with data: {json.dumps(data, indent=2)[:500]}...")
        response = self._request('POST', 'pages', json=data)
        return response.json()
    
    def get_page(self, page_id: Union[int, str], expand: List[str] = None) -> Dict:
        """
        Get page by ID.
        
        Args:
            page_id: Page ID
            expand: Fields to expand (e.g., ['body.storage', 'version'])
            
        Returns:
            Page data
        """
        params = {}
        if expand:
            params['body-format'] = 'storage'
            params.update({f'include-{e}': 'true' for e in expand})
        
        response = self._request('GET', f'pages/{page_id}', params=params)
        return response.json()
    
    def update_page(self, page_id: Union[int, str], title: str, content: str, 
                   version: int, **kwargs) -> Dict:
        """
        Update an existing page.
        
        Args:
            page_id: Page ID
            title: New title
            content: New content
            version: Current version number
            **kwargs: Additional update parameters
            
        Returns:
            Updated page data
        """
        data = {
            'id': str(page_id),
            'status': 'current',
            'title': title,
            'body': {
                'value': content,
                'representation': kwargs.get('representation', 'storage')
            },
            'version': {
                'number': version + 1,
                'message': kwargs.get('version_message', 'Updated via API')
            }
        }
        
        data.update(kwargs)
        response = self._request('PUT', f'pages/{page_id}', json=data)
        return response.json()
    
    def delete_page(self, page_id: Union[int, str]) -> None:
        """Delete a page."""
        self._request('DELETE', f'pages/{page_id}')
    
    def search_pages(self, cql: str, limit: int = None) -> List[Dict]:
        """
        Search pages using CQL.
        
        Args:
            cql: Confluence Query Language query
            limit: Maximum results
            
        Returns:
            List of matching pages
        """
        endpoint = 'pages'
        params = {'cql': cql}
        return self._paginate(endpoint, params, limit)
    
    # Blog Post Operations
    
    def create_blog_post(self, space_id: int, title: str, content: str, **kwargs) -> Dict:
        """
        Create a new blog post.
        
        Args:
            space_id: Space ID
            title: Blog post title
            content: Blog post content
            **kwargs: Additional properties
            
        Returns:
            Created blog post data
        """
        data = {
            'spaceId': str(space_id),
            'status': kwargs.get('status', 'current'),
            'title': title,
            'body': {
                'value': content,
                'representation': kwargs.get('representation', 'storage')
            }
        }
        
        data.update(kwargs)
        response = self._request('POST', 'blogposts', json=data)
        return response.json()
    
    def get_blog_post(self, post_id: Union[int, str]) -> Dict:
        """Get blog post by ID."""
        response = self._request('GET', f'blogposts/{post_id}')
        return response.json()
    
    # Attachment Operations
    
    def upload_attachment(self, page_id: Union[int, str], file_path: str, 
                         comment: str = None) -> Dict:
        """
        Upload attachment to a page.
        
        Args:
            page_id: Page ID
            file_path: Path to file
            comment: Optional comment
            
        Returns:
            Attachment data
        """
        path = Path(file_path)
        
        # Prepare multipart form data
        files = {'file': (path.name, open(path, 'rb'), 'application/octet-stream')}
        data = {}
        if comment:
            data['comment'] = comment
        
        # Temporarily remove Content-Type for multipart
        headers = self.session.headers.copy()
        del headers['Content-Type']
        
        response = self._request(
            'POST', 
            f'pages/{page_id}/attachments',
            files=files,
            data=data,
            headers=headers
        )
        
        return response.json()
    
    def get_attachments(self, page_id: Union[int, str]) -> List[Dict]:
        """Get all attachments for a page."""
        return self._paginate(f'pages/{page_id}/attachments')
    
    def download_attachment(self, attachment_id: str, save_path: str) -> str:
        """
        Download attachment to file.
        
        Args:
            attachment_id: Attachment ID
            save_path: Where to save file
            
        Returns:
            Path to saved file
        """
        response = self._request('GET', f'attachments/{attachment_id}/download', stream=True)
        
        path = Path(save_path)
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return str(path)
    
    # Space Operations
    
    def get_spaces(self, limit: int = None, **params) -> List[Dict]:
        """
        Get all spaces.
        
        Args:
            limit: Maximum spaces to return
            **params: Additional query parameters
            
        Returns:
            List of spaces
        """
        return self._paginate('spaces', params, limit)
    
    def get_space(self, space_id: Union[int, str]) -> Dict:
        """Get space by ID."""
        response = self._request('GET', f'spaces/{space_id}')
        return response.json()
    
    def create_space(self, key: str, name: str, description: str = None) -> Dict:
        """
        Create a new space.
        
        Args:
            key: Space key (uppercase, no spaces)
            name: Space name
            description: Optional description
            
        Returns:
            Created space data
        """
        data = {
            'key': key.upper(),
            'name': name
        }
        
        if description:
            data['description'] = {
                'plain': {
                    'value': description,
                    'representation': 'plain'
                }
            }
        
        response = self._request('POST', 'spaces', json=data)
        return response.json()
    
    # Comment Operations
    
    def add_comment(self, page_id: Union[int, str], content: str, 
                   parent_id: Optional[str] = None) -> Dict:
        """
        Add comment to page.
        
        Args:
            page_id: Page ID
            content: Comment content
            parent_id: Optional parent comment ID for replies
            
        Returns:
            Comment data
        """
        data = {
            'body': {
                'value': content,
                'representation': 'storage'
            }
        }
        
        if parent_id:
            data['parentCommentId'] = parent_id
        
        response = self._request('POST', f'pages/{page_id}/footer-comments', json=data)
        return response.json()
    
    def get_comments(self, page_id: Union[int, str]) -> List[Dict]:
        """Get all comments for a page."""
        return self._paginate(f'pages/{page_id}/footer-comments')
    
    # User Operations
    
    def get_current_user(self) -> Dict:
        """
        Get current authenticated user.
        Note: v2 API doesn't have a dedicated current user endpoint.
        This method returns basic auth info for compatibility.
        """
        # V2 API doesn't have users/current endpoint
        # Return basic info from auth credentials
        return {
            'email': self.email,
            'displayName': self.email.split('@')[0],
            'accountId': 'authenticated-user'
        }
    
    def get_users_bulk(self, account_ids: List[str]) -> Dict:
        """
        Get user details for multiple account IDs.
        
        Args:
            account_ids: List of account IDs
            
        Returns:
            User details
        """
        data = {'accountIds': account_ids}
        response = self._request('POST', 'users-bulk', json=data)
        return response.json()
    
    # Label Operations
    
    def add_labels(self, page_id: Union[int, str], labels: List[str]) -> Dict:
        """
        Add labels to a page.
        
        Args:
            page_id: Page ID
            labels: List of label names
            
        Returns:
            Label data
        """
        data = [{'name': label} for label in labels]
        response = self._request('POST', f'pages/{page_id}/labels', json=data)
        return response.json()
    
    def get_labels(self, page_id: Union[int, str]) -> List[Dict]:
        """Get labels for a page."""
        response = self._request('GET', f'pages/{page_id}/labels')
        return response.json().get('results', [])
    
    # Content Property Operations
    
    def get_content_properties(self, page_id: Union[int, str]) -> List[Dict]:
        """
        Get all content properties for a page.
        
        Args:
            page_id: Page ID
            
        Returns:
            List of properties
        """
        response = self._request('GET', f'pages/{page_id}/properties')
        return response.json().get('results', [])
    
    def get_content_property(self, page_id: Union[int, str], key: str) -> Dict:
        """
        Get a specific content property by key.
        
        Args:
            page_id: Page ID
            key: Property key
            
        Returns:
            Property data
        """
        # First get all properties to find the one with matching key
        properties = self.get_content_properties(page_id)
        for prop in properties:
            if prop.get('key') == key:
                # Get the full property details
                response = self._request('GET', f'pages/{page_id}/properties/{prop["id"]}')
                return response.json()
        raise ValueError(f"Property with key '{key}' not found")
    
    def set_content_property(self, page_id: Union[int, str], key: str, value: Any) -> Dict:
        """
        Set or update a content property on a page.
        
        Args:
            page_id: Page ID
            key: Property key
            value: Property value
            
        Returns:
            Property data
        """
        data = {
            'key': key,
            'value': value
        }
        
        # First try to create the property
        try:
            response = self._request('POST', f'pages/{page_id}/properties', json=data)
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 409:  # Property already exists
                # Try to update instead
                logger.info(f"Property {key} already exists, attempting to update...")
                response = self._request('PUT', f'pages/{page_id}/properties/{key}', json={'value': value})
                return response.json()
            else:
                raise
    
    def create_page_modern_editor(self, space_id: int, title: str, content: str, 
                                parent_id: Optional[int] = None, **kwargs) -> Dict:
        """
        Create a page using the modern editor by setting the editor property.
        
        This is a 3-step process:
        1. Create a blank page with title only
        2. Set the editor property to 'v2' 
        3. Update the page with content
        
        Args:
            space_id: Space ID
            title: Page title
            content: Page content (HTML or storage format)
            parent_id: Optional parent page ID
            **kwargs: Additional page properties
            
        Returns:
            Created page data
        """
        # Step 1: Create blank page with title only
        logger.info("Step 1: Creating blank page...")
        blank_page = self.create_page(
            space_id=space_id,
            title=title,
            content="<p> </p>",  # Minimal content
            parent_id=parent_id,
            **kwargs
        )
        page_id = blank_page['id']
        
        # Step 2: Check and set editor property to v2
        logger.info(f"Step 2: Checking editor property for page {page_id}...")
        try:
            # First check if the property already exists and has the correct value
            try:
                editor_prop = self.get_content_property(page_id, 'editor')
                if editor_prop.get('value') == 'v2':
                    logger.info("Editor property is already set to v2 - skipping update")
                else:
                    logger.info(f"Editor property exists but has value '{editor_prop.get('value')}' - attempting to update")
                    self.set_content_property(page_id, 'editor', 'v2')
            except ValueError:
                # Property doesn't exist, create it
                logger.info("Editor property doesn't exist - creating it")
                self.set_content_property(page_id, 'editor', 'v2')
                logger.info("Successfully set editor property to v2")
        except Exception as e:
            logger.warning(f"Could not set editor property: {e}")
            # Continue anyway as it might already be configured correctly
        
        # Step 3: Update page with actual content
        logger.info("Step 3: Updating page with content...")
        # Get current version
        page_data = self.get_page(page_id)
        current_version = page_data['version']['number']
        
        # Update with content
        updated_page = self.update_page(
            page_id=page_id,
            title=title,
            content=content,
            version=current_version
        )
        
        return updated_page
    
    # Bulk Operations
    
    def bulk_create_pages(self, pages: List[Dict]) -> List[Dict]:
        """
        Create multiple pages efficiently.
        
        Args:
            pages: List of page data dictionaries
            
        Returns:
            List of created pages
        """
        created = []
        for page in pages:
            try:
                result = self.create_page(**page)
                created.append(result)
                logger.info(f"Created page: {result['title']}")
            except Exception as e:
                logger.error(f"Failed to create page: {page.get('title')} - {e}")
        
        return created
    
    # Utility Methods
    
    def export_space_to_pdf(self, space_id: Union[int, str]) -> bytes:
        """
        Export entire space to PDF.
        
        Args:
            space_id: Space ID
            
        Returns:
            PDF content as bytes
        """
        # This would require additional implementation using export API
        raise NotImplementedError("PDF export requires additional API setup")
    
    def copy_page(self, source_id: Union[int, str], target_space_id: int, 
                  new_title: str = None) -> Dict:
        """
        Copy a page to another space.
        
        Args:
            source_id: Source page ID
            target_space_id: Target space ID
            new_title: Optional new title
            
        Returns:
            Copied page data
        """
        # Get source page
        source = self.get_page(source_id, expand=['body.storage'])
        
        # Create copy
        return self.create_page(
            space_id=target_space_id,
            title=new_title or f"Copy of {source['title']}",
            content=source['body']['storage']['value']
        )