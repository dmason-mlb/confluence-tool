#!/usr/bin/env python3
"""
Bulk Operations Utilities

Perform bulk operations on Confluence content efficiently.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from confluence_client import ConfluenceClient
import csv
from pathlib import Path
import concurrent.futures
import logging
from typing import List, Dict, Callable
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BulkOperations:
    """Handle bulk operations on Confluence content."""
    
    def __init__(self, client: ConfluenceClient, max_workers: int = 5):
        """
        Initialize bulk operations handler.
        
        Args:
            client: Confluence client instance
            max_workers: Maximum concurrent workers
        """
        self.client = client
        self.max_workers = max_workers
    
    def create_pages_from_csv(self, csv_file: str, space_id: int) -> List[Dict]:
        """
        Create multiple pages from CSV file.
        
        CSV format: title,parent_title,content,labels
        
        Args:
            csv_file: Path to CSV file
            space_id: Target space ID
            
        Returns:
            List of created pages
        """
        logger.info(f"Creating pages from {csv_file}")
        
        created_pages = []
        page_lookup = {}  # Map titles to IDs for parent relationships
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    # Look up parent ID if specified
                    parent_id = None
                    if row.get('parent_title'):
                        parent_id = page_lookup.get(row['parent_title'])
                    
                    # Create page
                    page = self.client.create_page(
                        space_id=space_id,
                        title=row['title'],
                        content=row.get('content', f"<p>Content for {row['title']}</p>"),
                        parent_id=parent_id
                    )
                    
                    # Store mapping
                    page_lookup[row['title']] = page['id']
                    created_pages.append(page)
                    
                    # Add labels if specified
                    if row.get('labels'):
                        labels = [l.strip() for l in row['labels'].split(',')]
                        self.client.add_labels(page['id'], labels)
                    
                    logger.info(f"Created: {page['title']} (ID: {page['id']})")
                    
                except Exception as e:
                    logger.error(f"Failed to create page '{row.get('title')}': {e}")
        
        logger.info(f"Created {len(created_pages)} pages")
        return created_pages
    
    def update_pages_bulk(self, updates: List[Dict]) -> List[Dict]:
        """
        Update multiple pages concurrently.
        
        Args:
            updates: List of dicts with page_id, title, content, version
            
        Returns:
            List of updated pages
        """
        logger.info(f"Updating {len(updates)} pages")
        
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_update = {
                executor.submit(self._update_single_page, update): update
                for update in updates
            }
            
            for future in concurrent.futures.as_completed(future_to_update):
                update = future_to_update[future]
                try:
                    result = future.result()
                    results.append(result)
                    logger.info(f"Updated: {result['title']}")
                except Exception as e:
                    logger.error(f"Failed to update page {update['page_id']}: {e}")
        
        return results
    
    def _update_single_page(self, update: Dict) -> Dict:
        """Update a single page."""
        return self.client.update_page(**update)
    
    def delete_pages_by_criteria(self, space_key: str, criteria: str, 
                                dry_run: bool = True) -> List[str]:
        """
        Delete pages matching CQL criteria.
        
        Args:
            space_key: Space key
            criteria: Additional CQL criteria
            dry_run: If True, only list pages that would be deleted
            
        Returns:
            List of deleted page IDs
        """
        cql = f"space = {space_key} AND type = page AND {criteria}"
        pages = self.client.search_pages(cql)
        
        logger.info(f"Found {len(pages)} pages matching criteria")
        
        if dry_run:
            logger.info("DRY RUN - Pages that would be deleted:")
            for page in pages:
                logger.info(f"  - {page['title']} (ID: {page['id']})")
            return []
        
        deleted = []
        for page in pages:
            try:
                self.client.delete_page(page['id'])
                deleted.append(page['id'])
                logger.info(f"Deleted: {page['title']} (ID: {page['id']})")
            except Exception as e:
                logger.error(f"Failed to delete {page['title']}: {e}")
        
        return deleted
    
    def apply_labels_bulk(self, page_ids: List[str], labels: List[str]) -> Dict[str, bool]:
        """
        Apply labels to multiple pages.
        
        Args:
            page_ids: List of page IDs
            labels: Labels to apply
            
        Returns:
            Dict mapping page ID to success status
        """
        logger.info(f"Applying {len(labels)} labels to {len(page_ids)} pages")
        
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_page = {
                executor.submit(self.client.add_labels, page_id, labels): page_id
                for page_id in page_ids
            }
            
            for future in concurrent.futures.as_completed(future_to_page):
                page_id = future_to_page[future]
                try:
                    future.result()
                    results[page_id] = True
                    logger.info(f"Labeled: {page_id}")
                except Exception as e:
                    results[page_id] = False
                    logger.error(f"Failed to label {page_id}: {e}")
        
        return results
    
    def find_and_replace_content(self, space_key: str, find_text: str, 
                                replace_text: str, dry_run: bool = True) -> List[Dict]:
        """
        Find and replace text across all pages in a space.
        
        Args:
            space_key: Space key
            find_text: Text to find
            replace_text: Replacement text
            dry_run: If True, only show what would be changed
            
        Returns:
            List of modified pages
        """
        logger.info(f"Finding '{find_text}' in space {space_key}")
        
        # Search for pages containing the text
        cql = f"space = {space_key} AND type = page AND text ~ '{find_text}'"
        pages = self.client.search_pages(cql)
        
        logger.info(f"Found {len(pages)} pages containing '{find_text}'")
        
        modified = []
        for page in pages:
            try:
                # Get full page content
                full_page = self.client.get_page(page['id'], expand=['body.storage'])
                content = full_page['body']['storage']['value']
                
                # Check if text exists
                if find_text in content:
                    new_content = content.replace(find_text, replace_text)
                    
                    if dry_run:
                        logger.info(f"Would update: {page['title']} (ID: {page['id']})")
                        modified.append({
                            'page_id': page['id'],
                            'title': page['title'],
                            'occurrences': content.count(find_text)
                        })
                    else:
                        # Update page
                        updated = self.client.update_page(
                            page_id=page['id'],
                            title=full_page['title'],
                            content=new_content,
                            version=full_page['version']['number'],
                            version_message=f"Replaced '{find_text}' with '{replace_text}'"
                        )
                        modified.append(updated)
                        logger.info(f"Updated: {page['title']}")
                        
            except Exception as e:
                logger.error(f"Failed to process {page['title']}: {e}")
        
        return modified
    
    def archive_old_pages(self, space_key: str, days_old: int, 
                         archive_label: str = "archived") -> List[str]:
        """
        Add archive label to pages older than specified days.
        
        Args:
            space_key: Space key
            days_old: Age threshold in days
            archive_label: Label to apply
            
        Returns:
            List of archived page IDs
        """
        # CQL to find old pages
        cql = f"space = {space_key} AND type = page AND lastModified < now('-{days_old}d')"
        pages = self.client.search_pages(cql)
        
        logger.info(f"Found {len(pages)} pages older than {days_old} days")
        
        archived = []
        for page in pages:
            try:
                self.client.add_labels(page['id'], [archive_label])
                archived.append(page['id'])
                logger.info(f"Archived: {page['title']} (ID: {page['id']})")
            except Exception as e:
                logger.error(f"Failed to archive {page['title']}: {e}")
        
        return archived
    
    def generate_index_page(self, space_id: int, parent_id: str = None) -> Dict:
        """
        Generate an index page with links to all child pages.
        
        Args:
            space_id: Space ID
            parent_id: Parent page ID (optional)
            
        Returns:
            Created index page
        """
        # Get pages
        if parent_id:
            # Get children of specific page
            response = self.client._request('GET', f'pages/{parent_id}/children')
            pages = response.json().get('results', [])
            title = "Page Index"
        else:
            # Get all pages in space
            cql = f"space = {space_id} AND type = page"
            pages = self.client.search_pages(cql, limit=100)
            title = "Space Index"
        
        # Sort pages by title
        pages.sort(key=lambda p: p['title'])
        
        # Generate index content
        content = f"<h1>{title}</h1>\n"
        content += f"<p>Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}</p>\n"
        content += "<ul>\n"
        
        for page in pages:
            content += f'  <li><a href="/wiki/spaces/{space_id}/pages/{page["id"]}">{page["title"]}</a></li>\n'
        
        content += "</ul>\n"
        content += f"<p>Total pages: {len(pages)}</p>"
        
        # Create index page
        index_page = self.client.create_page(
            space_id=space_id,
            title=title,
            content=content,
            parent_id=parent_id
        )
        
        logger.info(f"Created index page: {index_page['title']} (ID: {index_page['id']})")
        return index_page
    
    def export_pages_to_markdown(self, space_key: str, output_dir: str):
        """
        Export all pages in a space to Markdown files.
        
        Args:
            space_key: Space key
            output_dir: Output directory
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Get all pages
        cql = f"space = {space_key} AND type = page"
        pages = self.client.search_pages(cql)
        
        logger.info(f"Exporting {len(pages)} pages to {output_dir}")
        
        for page in pages:
            try:
                # Get full page content
                full_page = self.client.get_page(page['id'], expand=['body.storage'])
                
                # Convert to markdown (simplified - real conversion would be more complex)
                content = full_page['body']['storage']['value']
                content = content.replace('<p>', '').replace('</p>', '\n\n')
                content = content.replace('<h1>', '# ').replace('</h1>', '\n')
                content = content.replace('<h2>', '## ').replace('</h2>', '\n')
                content = content.replace('<h3>', '### ').replace('</h3>', '\n')
                
                # Save to file
                filename = f"{page['title'].replace('/', '-')}.md"
                filepath = output_path / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# {page['title']}\n\n")
                    f.write(f"Page ID: {page['id']}\n\n")
                    f.write(content)
                
                logger.info(f"Exported: {filename}")
                
            except Exception as e:
                logger.error(f"Failed to export {page['title']}: {e}")


def main():
    """Example usage of bulk operations."""
    # Configuration
    DOMAIN = os.getenv('CONFLUENCE_DOMAIN')
    EMAIL = os.getenv('CONFLUENCE_EMAIL')
    API_TOKEN = os.getenv('CONFLUENCE_API_TOKEN')
    
    if not all([DOMAIN, EMAIL, API_TOKEN]):
        print("Please set CONFLUENCE_DOMAIN, CONFLUENCE_EMAIL, and CONFLUENCE_API_TOKEN")
        sys.exit(1)
    
    # Initialize
    client = ConfluenceClient(DOMAIN, EMAIL, API_TOKEN)
    bulk = BulkOperations(client)
    
    # Example: Create pages from CSV
    # bulk.create_pages_from_csv('pages.csv', space_id=123456)
    
    # Example: Archive old pages
    # bulk.archive_old_pages('DEMO', days_old=365)
    
    # Example: Find and replace
    # bulk.find_and_replace_content('DEMO', 'old text', 'new text', dry_run=True)
    
    # Example: Generate index
    # bulk.generate_index_page(space_id=123456)
    
    logger.info("Bulk operations example completed")


if __name__ == "__main__":
    main()