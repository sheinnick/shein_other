#!/usr/bin/env python3
"""
Module for collecting and processing text files from a directory.
Creates a single markdown file with sorted content.
python text_collector_from_tg_transcribed_voices.py /path/to/source/directory /path/to/output/file.md
"""

import os
import argparse
from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TextFile:
    """Class for storing text file information."""
    filename: str
    content: str
    order: int

    @classmethod
    def from_filename(cls, filename: str, content: str) -> 'TextFile':
        """Creates a TextFile instance from filename and content."""
        try:
            order = int(filename.split('@')[0].split('_')[1])
            return cls(filename=filename, content=content, order=order)
        except (IndexError, ValueError) as e:
            logger.error(f"Error processing filename {filename}: {e}")
            raise

class TextCollector:
    """Class for collecting and processing text files."""
    
    def __init__(self, directory_path: str):
        self.directory_path = Path(directory_path)
        if not self.directory_path.exists():
            raise FileNotFoundError(f"Directory {directory_path} does not exist")
        
    def collect_files(self) -> List[TextFile]:
        """Collects and sorts text files from directory."""
        text_files: List[TextFile] = []
        
        try:
            # Get list of .txt files and sort them
            txt_files = sorted(
                f for f in self.directory_path.glob('*.txt')
                if f.is_file()
            )
            
            # Read file contents
            for file_path in txt_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        text_file = TextFile.from_filename(
                            filename=file_path.name,
                            content=content
                        )
                        text_files.append(text_file)
                except Exception as e:
                    logger.error(f"Error reading file {file_path}: {e}")
            
            # Sort files by order
            text_files.sort(key=lambda x: x.order)
            return text_files
            
        except Exception as e:
            logger.error(f"Error collecting files: {e}")
            raise
    
    def create_markdown(self, output_path: str, text_files: List[TextFile]) -> None:
        """Creates a markdown file with contents of all text files."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as md_file:
                for text_file in text_files:
                    md_file.write(f'# {text_file.filename}\n\n')
                    md_file.write(f'{text_file.content}\n\n')
            
            logger.info(f"Created file {output_path} with {len(text_files)} files")
            
        except Exception as e:
            logger.error(f"Error creating markdown file: {e}")
            raise

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Collect text files and create a markdown file.'
    )
    parser.add_argument(
        'source_dir',
        type=str,
        help='Path to directory containing text files'
    )
    parser.add_argument(
        'output_file',
        type=str,
        help='Path where to save the resulting markdown file'
    )
    return parser.parse_args()

def main():
    """Main function to run the script."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Create collector instance
        collector = TextCollector(args.source_dir)
        
        # Collect files
        text_files = collector.collect_files()
        
        # Create markdown file
        collector.create_markdown(args.output_file, text_files)
        
    except Exception as e:
        logger.error(f"Critical error: {e}")
        raise

if __name__ == '__main__':
    main() 