#!/usr/bin/env python3
"""
Content Migration Script

Migrate content between Confluence spaces or instances.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from confluence_client import ConfluenceClient
import json
from pathlib import Path
import logging
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentMigrator:
    """Handle content migration between Confluence spaces."""
    
    def __init__(self, source_client: ConfluenceClient, target_client: ConfluenceClient = None):
        """
        Initialize migrator.
        
        Args:
            source_client: Client for source Confluence
            target_client: Client for target Confluence (can be same as source)
        """
        self.source = source_client
        self.target = target_client or source_client
        self.page_mapping = {}  # Map old IDs to new IDs
        
    def migrate_space(self, source_space_id: int, target_space_id: int, 
                     include_attachments: bool = True):
        """
        Migrate entire space content.
        
        Args:
            source_space_id: Source space ID
            target_space_id: Target space ID  
            include_attachments: Whether to migrate attachments
        """
        logger.info(f"Starting space migration: {source_space_id} -> {target_space_id}")
        
        # Get all pages in source space
        pages = self._get_all_pages(source_space_id)
        logger.info(f"Found {len(pages)} pages to migrate")
        
        # Build parent-child relationships
        page_tree = self._build_page_tree(pages)
        
        # Migrate pages in order (parents first)
        self._migrate_page_tree(page_tree, None, target_space_id, include_attachments)
        
        logger.info("Migration completed!")
        return self.page_mapping
    
    def _get_all_pages(self, space_id: int) -> List[Dict]:
        """Get all pages in a space."""
        cql = f"space = {space_id} AND type = page"
        return self.source.search_pages(cql)
    
    def _build_page_tree(self, pages: List[Dict]) -> Dict:
        """Build parent-child relationship tree."""
        tree = {'root': []}
        page_dict = {p['id']: p for p in pages}
        
        for page in pages:
            parent_id = page.get('parentId')
            if parent_id and parent_id in page_dict:
                if parent_id not in tree:
                    tree[parent_id] = []
                tree[parent_id].append(page)
            else:
                tree['root'].append(page)
        
        return tree
    
    def _migrate_page_tree(self, tree: Dict, parent_id: Optional[str], 
                          target_space_id: int, include_attachments: bool):
        """Recursively migrate pages maintaining hierarchy."""
        pages = tree.get(parent_id or 'root', [])
        
        for page in pages:
            # Get full page content
            full_page = self.source.get_page(page['id'], expand=['body.storage'])
            
            # Create page in target
            new_parent_id = self.page_mapping.get(parent_id) if parent_id else None
            
            try:
                new_page = self.target.create_page(
                    space_id=target_space_id,
                    title=full_page['title'],
                    content=full_page['body']['storage']['value'],
                    parent_id=new_parent_id
                )
                
                self.page_mapping[page['id']] = new_page['id']
                logger.info(f"Migrated: {page['title']} ({page['id']} -> {new_page['id']})")
                
                # Migrate attachments
                if include_attachments:
                    self._migrate_attachments(page['id'], new_page['id'])
                
                # Migrate labels
                self._migrate_labels(page['id'], new_page['id'])
                
                # Migrate children
                if page['id'] in tree:
                    self._migrate_page_tree(tree, page['id'], target_space_id, include_attachments)
                    
            except Exception as e:
                logger.error(f"Failed to migrate {page['title']}: {e}")
    
    def _migrate_attachments(self, source_page_id: str, target_page_id: str):
        """Migrate attachments from source to target page."""
        try:
            attachments = self.source.get_attachments(source_page_id)
            
            for attachment in attachments:
                # Download attachment
                temp_file = f"/tmp/{attachment['title']}"
                self.source.download_attachment(attachment['id'], temp_file)
                
                # Upload to target
                self.target.upload_attachment(target_page_id, temp_file)
                
                # Clean up
                Path(temp_file).unlink()
                
                logger.info(f"  Migrated attachment: {attachment['title']}")
                
        except Exception as e:
            logger.warning(f"  Failed to migrate attachments: {e}")
    
    def _migrate_labels(self, source_page_id: str, target_page_id: str):
        """Migrate labels from source to target page."""
        try:
            labels = self.source.get_labels(source_page_id)
            if labels:
                label_names = [label['name'] for label in labels]
                self.target.add_labels(target_page_id, label_names)
                logger.info(f"  Migrated {len(labels)} labels")
        except Exception as e:
            logger.warning(f"  Failed to migrate labels: {e}")
    
    def export_space_to_json(self, space_id: int, output_file: str):
        """
        Export space content to JSON for backup.
        
        Args:
            space_id: Space to export
            output_file: Output JSON file path
        """
        logger.info(f"Exporting space {space_id} to {output_file}")
        
        export_data = {
            'space_id': space_id,
            'pages': [],
            'metadata': {
                'export_date': str(datetime.now()),
                'page_count': 0
            }
        }
        
        pages = self._get_all_pages(space_id)
        
        for page in pages:
            # Get full page data
            full_page = self.source.get_page(page['id'], expand=['body.storage'])
            
            # Get labels
            labels = self.source.get_labels(page['id'])
            
            # Get attachments metadata
            attachments = self.source.get_attachments(page['id'])
            
            page_data = {
                'id': page['id'],
                'title': full_page['title'],
                'content': full_page['body']['storage']['value'],
                'parent_id': page.get('parentId'),
                'labels': [label['name'] for label in labels],
                'attachments': [{'id': a['id'], 'title': a['title']} for a in attachments]
            }
            
            export_data['pages'].append(page_data)
        
        export_data['metadata']['page_count'] = len(export_data['pages'])
        
        # Save to file
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Exported {len(pages)} pages to {output_file}")
        return export_data
    
    def import_from_json(self, json_file: str, target_space_id: int):
        """
        Import content from JSON backup.
        
        Args:
            json_file: JSON file to import
            target_space_id: Target space ID
        """
        logger.info(f"Importing from {json_file} to space {target_space_id}")
        
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Build page tree for proper parent-child import
        pages_by_id = {p['id']: p for p in data['pages']}
        imported = {}
        
        # Import pages without parents first
        for page in data['pages']:
            if not page.get('parent_id') or page['parent_id'] not in pages_by_id:
                new_id = self._import_page(page, target_space_id, None, imported)
                imported[page['id']] = new_id
        
        # Import remaining pages
        while len(imported) < len(data['pages']):
            for page in data['pages']:
                if page['id'] in imported:
                    continue
                    
                parent_id = page.get('parent_id')
                if parent_id and parent_id in imported:
                    new_id = self._import_page(page, target_space_id, 
                                             imported[parent_id], imported)
                    imported[page['id']] = new_id
        
        logger.info(f"Imported {len(imported)} pages")
        return imported
    
    def _import_page(self, page_data: Dict, space_id: int, 
                    parent_id: Optional[str], imported: Dict) -> str:
        """Import a single page."""
        try:
            # Create page
            new_page = self.target.create_page(
                space_id=space_id,
                title=page_data['title'],
                content=page_data['content'],
                parent_id=parent_id
            )
            
            # Add labels
            if page_data.get('labels'):
                self.target.add_labels(new_page['id'], page_data['labels'])
            
            logger.info(f"Imported: {page_data['title']}")
            return new_page['id']
            
        except Exception as e:
            logger.error(f"Failed to import {page_data['title']}: {e}")
            return None


def main():
    """Run migration examples."""
    # Configuration
    DOMAIN = os.getenv('CONFLUENCE_DOMAIN')
    EMAIL = os.getenv('CONFLUENCE_EMAIL')
    API_TOKEN = os.getenv('CONFLUENCE_API_TOKEN')
    
    if not all([DOMAIN, EMAIL, API_TOKEN]):
        print("Please set CONFLUENCE_DOMAIN, CONFLUENCE_EMAIL, and CONFLUENCE_API_TOKEN")
        sys.exit(1)
    
    # Initialize client
    client = ConfluenceClient(DOMAIN, EMAIL, API_TOKEN)
    migrator = ContentMigrator(client)
    
    # Example: Export space to JSON
    source_space_id = 123456  # Replace with your space ID
    migrator.export_space_to_json(source_space_id, "space_backup.json")
    
    # Example: Migrate space
    # target_space_id = 789012  # Replace with target space ID
    # migrator.migrate_space(source_space_id, target_space_id, include_attachments=True)
    
    # Example: Import from JSON
    # target_space_id = 789012
    # migrator.import_from_json("space_backup.json", target_space_id)


if __name__ == "__main__":
    from datetime import datetime
    main()