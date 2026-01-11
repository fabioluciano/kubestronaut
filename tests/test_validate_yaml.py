#!/usr/bin/env python3
"""
Unit tests for YAML validation script.

Tests cover:
- Single-document YAML files
- Multiple-document YAML files
- Empty documents and files
- Malformed YAML
- Edge cases
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add scripts directory to path to import validate_yaml
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from validate_yaml import validate_yaml_file, find_yaml_files


class TestYAMLValidation(unittest.TestCase):
    """Test cases for YAML validation functionality."""
    
    def setUp(self):
        """Create a temporary directory for test files."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)
    
    def create_test_file(self, filename: str, content: str) -> Path:
        """Helper to create a test file."""
        file_path = self.test_path / filename
        file_path.write_text(content)
        return file_path
    
    def test_single_document_valid(self):
        """Test validation of a single valid YAML document."""
        content = """
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
  - name: nginx
    image: nginx:latest
"""
        file_path = self.create_test_file("single.yaml", content)
        success, errors = validate_yaml_file(file_path)
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_multiple_documents_valid(self):
        """Test validation of multiple valid YAML documents."""
        content = """
apiVersion: v1
kind: Pod
metadata:
  name: pod1
---
apiVersion: v1
kind: Service
metadata:
  name: service1
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: config1
data:
  key: value
"""
        file_path = self.create_test_file("multiple.yaml", content)
        success, errors = validate_yaml_file(file_path)
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_empty_file(self):
        """Test validation of an empty file."""
        file_path = self.create_test_file("empty.yaml", "")
        success, errors = validate_yaml_file(file_path)
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_empty_document(self):
        """Test validation of a file with empty documents."""
        content = """---
---
apiVersion: v1
kind: Pod
metadata:
  name: test
---
"""
        file_path = self.create_test_file("empty_doc.yaml", content)
        success, errors = validate_yaml_file(file_path)
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_whitespace_only(self):
        """Test validation of a file with only whitespace."""
        content = "   \n\n  \t  \n"
        file_path = self.create_test_file("whitespace.yaml", content)
        success, errors = validate_yaml_file(file_path)
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_malformed_yaml_syntax_error(self):
        """Test validation of YAML with syntax errors."""
        content = """
apiVersion: v1
kind: Pod
metadata:
  name: test
  labels:
    app: test
  bad indentation
spec:
  containers: []
"""
        file_path = self.create_test_file("malformed.yaml", content)
        success, errors = validate_yaml_file(file_path)
        self.assertFalse(success)
        self.assertGreater(len(errors), 0)
    
    def test_malformed_yaml_invalid_character(self):
        """Test validation of YAML with invalid characters."""
        content = """
apiVersion: v1
kind: Pod
metadata:
  name: test
  \ttabs: are bad
"""
        file_path = self.create_test_file("invalid_char.yaml", content)
        success, errors = validate_yaml_file(file_path)
        self.assertFalse(success)
        self.assertGreater(len(errors), 0)
    
    def test_multiple_documents_one_invalid(self):
        """Test validation when one document in a multi-doc file is invalid."""
        content = """
apiVersion: v1
kind: Pod
metadata:
  name: valid-pod
---
apiVersion: v1
kind: Service
metadata:
  name: invalid-service
  bad syntax here
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: valid-config
"""
        file_path = self.create_test_file("mixed.yaml", content)
        success, errors = validate_yaml_file(file_path)
        self.assertFalse(success)
        self.assertGreater(len(errors), 0)
    
    def test_yaml_with_list_document(self):
        """Test validation of YAML document that is a list."""
        content = """
- item1
- item2
- item3
"""
        file_path = self.create_test_file("list.yaml", content)
        success, errors = validate_yaml_file(file_path)
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)
    
    def test_yaml_with_scalar_document(self):
        """Test validation of YAML document that is a scalar (should fail)."""
        content = "just a string"
        file_path = self.create_test_file("scalar.yaml", content)
        success, errors = validate_yaml_file(file_path)
        self.assertFalse(success)
        self.assertGreater(len(errors), 0)
        self.assertIn("Invalid YAML structure", errors[0])
    
    def test_complex_kubernetes_manifest(self):
        """Test validation of a complex Kubernetes manifest."""
        content = """
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  storageClassName: standard
  accessModes:
    - ReadWriteOnce
  capacity:
    storage: 1Gi
  hostPath:
    path: /data
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  storageClassName: standard
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Mi
"""
        file_path = self.create_test_file("k8s.yaml", content)
        success, errors = validate_yaml_file(file_path)
        self.assertTrue(success)
        self.assertEqual(len(errors), 0)


class TestFindYAMLFiles(unittest.TestCase):
    """Test cases for finding YAML files."""
    
    def setUp(self):
        """Create a temporary directory structure."""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        
        # Create test directory structure
        (self.test_path / "subdir1").mkdir()
        (self.test_path / "subdir2").mkdir()
        
        # Create test files
        (self.test_path / "file1.yaml").write_text("test: 1")
        (self.test_path / "file2.yml").write_text("test: 2")
        (self.test_path / "file3.txt").write_text("not yaml")
        (self.test_path / "subdir1" / "nested.yaml").write_text("test: 3")
        (self.test_path / "subdir2" / "another.yml").write_text("test: 4")
    
    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)
    
    def test_find_single_file(self):
        """Test finding a single YAML file."""
        file_path = self.test_path / "file1.yaml"
        found = find_yaml_files([file_path])
        self.assertEqual(len(found), 1)
        self.assertIn(file_path, found)
    
    def test_find_in_directory(self):
        """Test finding all YAML files in a directory."""
        found = find_yaml_files([self.test_path])
        self.assertEqual(len(found), 4)  # file1.yaml, file2.yml, nested.yaml, another.yml
    
    def test_find_in_subdirectory(self):
        """Test finding YAML files in a subdirectory."""
        found = find_yaml_files([self.test_path / "subdir1"])
        self.assertEqual(len(found), 1)
        self.assertIn(self.test_path / "subdir1" / "nested.yaml", found)
    
    def test_find_multiple_paths(self):
        """Test finding YAML files from multiple paths."""
        paths = [
            self.test_path / "file1.yaml",
            self.test_path / "subdir2"
        ]
        found = find_yaml_files(paths)
        self.assertEqual(len(found), 2)
    
    def test_ignore_non_yaml_files(self):
        """Test that non-YAML files are ignored."""
        found = find_yaml_files([self.test_path])
        txt_files = [f for f in found if f.suffix == '.txt']
        self.assertEqual(len(txt_files), 0)
    
    def test_find_both_extensions(self):
        """Test finding both .yaml and .yml files."""
        found = find_yaml_files([self.test_path])
        yaml_files = [f for f in found if f.suffix == '.yaml']
        yml_files = [f for f in found if f.suffix == '.yml']
        self.assertGreater(len(yaml_files), 0)
        self.assertGreater(len(yml_files), 0)
    
    def test_exclude_pattern(self):
        """Test excluding files with a glob pattern."""
        # Create some template files
        (self.test_path / "template.yaml").write_text("test: template")
        (self.test_path / "subdir1" / "template-file.yaml").write_text("test: template")
        
        # Find without exclusion
        found_all = find_yaml_files([self.test_path])
        self.assertGreater(len(found_all), 4)
        
        # Find with exclusion
        found_filtered = find_yaml_files([self.test_path], ["**/template*.yaml"])
        self.assertLess(len(found_filtered), len(found_all))
        self.assertEqual(len(found_all) - len(found_filtered), 2)
    
    def test_exclude_multiple_patterns(self):
        """Test excluding files with multiple glob patterns."""
        # Create some files
        (self.test_path / "example-1.yaml").write_text("test: 1")
        (self.test_path / "example-2.yaml").write_text("test: 2")
        (self.test_path / "helm-template.yaml").write_text("test: helm")
        
        found_filtered = find_yaml_files(
            [self.test_path], 
            ["**/*example*.yaml", "**/helm-*.yaml"]
        )
        
        # Should exclude example-1, example-2, and helm-template
        found_all = find_yaml_files([self.test_path])
        self.assertEqual(len(found_all) - len(found_filtered), 3)


if __name__ == '__main__':
    unittest.main()
