#!/usr/bin/env python3
"""
YAML Validation Script with Multiple Document Support

This script validates YAML files, including those containing multiple documents
separated by '---'. Each document is validated independently.

Usage:
    python validate_yaml.py <file_or_directory>...

Examples:
    python validate_yaml.py file.yaml
    python validate_yaml.py src/assets/
    python validate_yaml.py file1.yaml file2.yaml dir/
"""

import sys
import os
import yaml
import argparse
from pathlib import Path
from typing import List, Tuple


class YAMLValidationError(Exception):
    """Custom exception for YAML validation errors."""
    pass


def validate_yaml_file(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate a YAML file that may contain multiple documents.
    
    Args:
        file_path: Path to the YAML file to validate
        
    Returns:
        Tuple of (success: bool, errors: List[str])
        - success: True if all documents are valid, False otherwise
        - errors: List of error messages (empty if success)
    """
    errors = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Handle empty files
        if not content.strip():
            return True, []  # Empty files are considered valid
            
        # Parse all documents in the file
        documents = list(yaml.safe_load_all(content))
        
        # Check if we got any documents
        if not documents:
            return True, []  # No documents is valid (empty file)
            
        # Validate each document
        for idx, doc in enumerate(documents, start=1):
            if doc is None:
                # Empty document (e.g., just '---' with no content) is valid
                continue
                
            if not isinstance(doc, (dict, list)):
                errors.append(
                    f"Document {idx}: Invalid YAML structure. "
                    f"Expected dict or list, got {type(doc).__name__}"
                )
        
        return len(errors) == 0, errors
        
    except yaml.YAMLError as e:
        error_msg = str(e)
        if hasattr(e, 'problem_mark'):
            mark = e.problem_mark
            error_msg = (
                f"YAML parsing error at line {mark.line + 1}, "
                f"column {mark.column + 1}: {e.problem}"
            )
        errors.append(error_msg)
        return False, errors
        
    except Exception as e:
        errors.append(f"Unexpected error: {str(e)}")
        return False, errors


def find_yaml_files(paths: List[Path]) -> List[Path]:
    """
    Find all YAML files in the given paths.
    
    Args:
        paths: List of file or directory paths
        
    Returns:
        List of YAML file paths
    """
    yaml_files = []
    yaml_extensions = {'.yaml', '.yml'}
    
    for path in paths:
        if path.is_file():
            if path.suffix in yaml_extensions:
                yaml_files.append(path)
        elif path.is_dir():
            for ext in yaml_extensions:
                yaml_files.extend(path.rglob(f'*{ext}'))
                
    return sorted(set(yaml_files))


def main():
    """Main entry point for the YAML validation script."""
    parser = argparse.ArgumentParser(
        description='Validate YAML files with support for multiple documents',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s file.yaml              # Validate a single file
  %(prog)s src/assets/            # Validate all YAML files in a directory
  %(prog)s file1.yaml dir/        # Validate multiple paths
        """
    )
    parser.add_argument(
        'paths',
        nargs='+',
        type=Path,
        help='YAML file(s) or directory(ies) to validate'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed validation results'
    )
    
    args = parser.parse_args()
    
    # Find all YAML files
    yaml_files = find_yaml_files(args.paths)
    
    if not yaml_files:
        print("No YAML files found to validate.")
        return 0
    
    # Validate each file
    total_files = len(yaml_files)
    failed_files = []
    
    print(f"Validating {total_files} YAML file(s)...\n")
    
    for yaml_file in yaml_files:
        success, errors = validate_yaml_file(yaml_file)
        
        if success:
            if args.verbose:
                print(f"✓ {yaml_file}")
        else:
            print(f"✗ {yaml_file}")
            for error in errors:
                print(f"  {error}")
            failed_files.append(yaml_file)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Validation complete: {total_files - len(failed_files)}/{total_files} files passed")
    
    if failed_files:
        print(f"\nFailed files ({len(failed_files)}):")
        for failed_file in failed_files:
            print(f"  - {failed_file}")
        return 1
    else:
        print("\n✓ All YAML files are valid!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
