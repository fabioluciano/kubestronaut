#!/usr/bin/env python3
"""
Script to inline PlantUML include statements in markdown files.
This replaces file paths or !include directives with the actual content of the .puml files.
"""

import os
import re
import sys

def inline_includes(md_file):
    """Process a markdown file and inline all plantuml includes."""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern 1: ```plantuml blocks containing just a .puml file path (no !include)
    # e.g., ```plantuml,format=png
    #       ../assets/diagrams/file.puml
    #       ```
    pattern1 = r'(```plantuml[^\n]*\n)([^\n`]+\.puml)\n(```)'
    
    # Pattern 2: ```plantuml blocks with !include directive
    pattern2 = r'(```plantuml[^\n]*\n)(!include\s+([^\n]+\.puml))\n(```)'
    
    md_dir = os.path.dirname(md_file)
    src_dir = os.path.dirname(md_dir)  # Usually 'src'
    
    def find_puml_file(puml_path, md_dir):
        """Try to find the puml file in various locations."""
        # Try 1: Relative to the markdown file
        full_path = os.path.normpath(os.path.join(md_dir, puml_path))
        if os.path.exists(full_path):
            return full_path
        
        # Try 2: If path goes outside src, redirect to src/assets
        if 'assets' in puml_path:
            # Extract the part after 'assets' and try in src/assets
            idx = puml_path.find('assets')
            if idx >= 0:
                alt_path = os.path.join(src_dir, puml_path[idx:])
                alt_path = os.path.normpath(alt_path)
                if os.path.exists(alt_path):
                    return alt_path
        
        # Try 3: Direct path from src directory
        direct_path = os.path.normpath(os.path.join(src_dir, puml_path.lstrip('../')))
        if os.path.exists(direct_path):
            return direct_path
        
        return None
    
    def replace_path(match):
        prefix = match.group(1)
        puml_path = match.group(2).strip()
        suffix = match.group(3)
        
        # Find the file
        full_path = find_puml_file(puml_path, md_dir)
        
        if full_path:
            with open(full_path, 'r', encoding='utf-8') as pf:
                puml_content = pf.read().rstrip()
            return prefix + puml_content + '\n' + suffix
        else:
            print(f'Warning: {puml_path} not found (from {md_file})', file=sys.stderr)
            return match.group(0)
    
    def replace_include(match):
        prefix = match.group(1)
        puml_path = match.group(3).strip()
        suffix = match.group(4)
        
        # Find the file
        full_path = find_puml_file(puml_path, md_dir)
        
        if full_path:
            with open(full_path, 'r', encoding='utf-8') as pf:
                puml_content = pf.read().rstrip()
            return prefix + puml_content + '\n' + suffix
        else:
            print(f'Warning: {puml_path} not found (from {md_file})', file=sys.stderr)
            return match.group(0)
    
    # Apply both patterns
    new_content = re.sub(pattern1, replace_path, content)
    new_content = re.sub(pattern2, replace_include, new_content)
    
    if new_content != content:
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    """Process all markdown files in src directory."""
    src_dir = 'src'
    if len(sys.argv) > 1:
        src_dir = sys.argv[1]
    
    count = 0
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f.endswith('.md'):
                filepath = os.path.join(root, f)
                if inline_includes(filepath):
                    count += 1
                    print(f'Processed: {filepath}')
    
    print(f'Total files modified: {count}')

if __name__ == '__main__':
    main()
