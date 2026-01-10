# YAML Validation Script

This directory contains a Python script for validating YAML files with support for multiple documents per file.

## Features

- **Multiple Document Support**: Handles YAML files containing multiple documents separated by `---`
- **Independent Validation**: Each document is validated separately
- **Clear Error Messages**: Provides detailed error messages with line and column numbers
- **Edge Case Handling**: Properly handles empty files, empty documents, and whitespace
- **Flexible Usage**: Can validate single files, multiple files, or entire directories
- **Recursive Search**: Automatically finds all `.yaml` and `.yml` files in subdirectories

## Requirements

- Python 3.6 or higher
- PyYAML library

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Validate a single YAML file:

```bash
python scripts/validate_yaml.py file.yaml
```

Validate multiple files:

```bash
python scripts/validate_yaml.py file1.yaml file2.yaml file3.yaml
```

Validate all YAML files in a directory:

```bash
python scripts/validate_yaml.py src/assets/
```

Validate with verbose output (shows all files, including successful ones):

```bash
python scripts/validate_yaml.py src/assets/ -v
```

### Command-Line Options

```
usage: validate_yaml.py [-h] [-v] paths [paths ...]

Validate YAML files with support for multiple documents

positional arguments:
  paths          YAML file(s) or directory(ies) to validate

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Show detailed validation results
```

## Examples

### Single Document YAML File

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: nginx
    image: nginx:latest
```

### Multiple Document YAML File

YAML files can contain multiple documents separated by `---`:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Mi
```

Each document is validated independently, so if one document has an error, the others can still be validated.

### Empty Documents

Empty documents (just `---` with no content) are considered valid:

```yaml
---
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
---
```

## Exit Codes

- `0`: All YAML files are valid
- `1`: One or more YAML files have validation errors

## Error Messages

The script provides detailed error messages:

- **Syntax Errors**: Shows the exact line and column where the error occurred
- **Structure Errors**: Indicates if a document has an unexpected structure
- **Multiple Errors**: Reports all errors found in a file

Example error output:

```
✗ src/assets/example.yaml
  YAML parsing error at line 15, column 3: could not find expected ':'
```

## Testing

Run the unit tests:

```bash
python -m unittest tests.test_validate_yaml -v
```

The test suite covers:
- Single-document YAML files
- Multiple-document YAML files
- Empty documents and files
- Malformed YAML syntax
- Edge cases (whitespace-only files, scalar documents, etc.)
- File discovery functionality

## Integration with CI/CD

The repository includes a GitHub Actions workflow (`.github/workflows/yaml-lint.yaml`) that automatically validates YAML files on pull requests.

The workflow:
1. Triggers on changes to `.yaml` or `.yml` files
2. Installs Python and dependencies
3. Runs the validation script
4. Fails the check if any YAML files are invalid

## How It Works

The script uses PyYAML's `safe_load_all()` function to parse multiple documents from a single YAML file:

1. **File Reading**: Reads the entire file content
2. **Document Parsing**: Uses `yaml.safe_load_all()` to iterate through all documents
3. **Validation**: Checks each document for valid structure (dict or list)
4. **Error Reporting**: Collects and reports any parsing or validation errors

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'yaml'`

**Solution**: Install PyYAML:
```bash
pip install PyYAML
```

**Issue**: Script reports "Invalid YAML structure" for a scalar value

**Solution**: YAML documents should typically be dictionaries or lists. If you have a file with just a scalar value (like `just a string`), consider wrapping it in a proper structure.

**Issue**: Empty file reported as error

**Solution**: Empty files are actually considered valid. If you're seeing an error, check for invisible characters or encoding issues.

## Contributing

When modifying the validation script:

1. Ensure all existing tests pass
2. Add new tests for any new functionality
3. Update this documentation to reflect changes
4. Test with the repository's existing YAML files

## License

This script is part of the Kubestronaut project and follows the same license.
