# Test Suite

This directory contains unit tests for the Kubestronaut project.

## Running Tests

Run all tests:

```bash
python -m unittest discover tests -v
```

Run a specific test file:

```bash
python -m unittest tests.test_validate_yaml -v
```

## Test Coverage

### YAML Validation Tests (`test_validate_yaml.py`)

Tests the YAML validation script with comprehensive coverage:

#### Single Document Tests
- `test_single_document_valid`: Valid single-document YAML
- `test_yaml_with_list_document`: Document that is a list

#### Multiple Document Tests
- `test_multiple_documents_valid`: Multiple valid documents
- `test_multiple_documents_one_invalid`: Mix of valid and invalid documents
- `test_complex_kubernetes_manifest`: Real Kubernetes manifests with multiple resources

#### Edge Cases
- `test_empty_file`: Completely empty file
- `test_empty_document`: Files with empty documents (`---` with no content)
- `test_whitespace_only`: Files containing only whitespace

#### Error Handling
- `test_malformed_yaml_syntax_error`: YAML with indentation errors
- `test_malformed_yaml_invalid_character`: YAML with invalid characters
- `test_yaml_with_scalar_document`: Invalid scalar document (should be dict/list)

#### File Discovery Tests
- `test_find_single_file`: Finding a specific file
- `test_find_in_directory`: Recursive directory search
- `test_find_in_subdirectory`: Subdirectory search
- `test_find_multiple_paths`: Multiple paths at once
- `test_ignore_non_yaml_files`: Filtering non-YAML files
- `test_find_both_extensions`: Finding both `.yaml` and `.yml` files

## Test Structure

Each test class follows Python's `unittest` framework:

- `setUp()`: Creates temporary test files and directories
- `tearDown()`: Cleans up temporary resources
- `test_*()`: Individual test cases

## Adding New Tests

When adding new tests:

1. Follow the existing naming convention: `test_<feature>_<scenario>`
2. Add descriptive docstrings
3. Use `setUp()` and `tearDown()` for resource management
4. Test both positive and negative cases
5. Update this README with new test descriptions

## Dependencies

Tests use only Python standard library modules:
- `unittest`: Test framework
- `tempfile`: Temporary file creation
- `pathlib`: Path manipulation

No additional test dependencies are required.
