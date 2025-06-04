# PyALint

PyALint is a Python-based GitHub Actions workflow linting tool that combines `yamllint` and `actionlint` to provide comprehensive validation of your GitHub Actions workflow files.

## Features

- YAML syntax validation using `yamllint`
- GitHub Actions specific validation using `actionlint`
- Configurable linting rules
- Support for single file or directory scanning
- JSON output option for integration with other tools
- Verbose and debug output options

## Prerequisites

Before installing PyALint, you need to have the following installed on your macOS system:

- Python 3.6 or higher
- `yamllint`
- `actionlint`

### Installing Prerequisites on macOS

```bash
# Install Homebrew if you haven't already
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install yamllint and actionlint
brew install yamllint
brew install actionlint
```

## Installation

### Option 1: Using a Virtual Environment (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/pyalint.git
cd pyalint

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (if you add any Python dependencies in the future)
# pip install -r requirements.txt

# Make the script executable
chmod +x pyalint.py

# Create a symlink (optional)
ln -s "$(pwd)/pyalint.py" /usr/local/bin/pyalint
```

### Option 2: Direct Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pyalint.git
cd pyalint

# Make the script executable
chmod +x pyalint.py

# Create a symlink (optional)
ln -s "$(pwd)/pyalint.py" /usr/local/bin/pyalint
```

## Usage

PyALint can be used in several ways:

### Basic Usage

```bash
# Check all workflow files in .github/workflows
./pyalint.py

# Check a specific workflow file
./pyalint.py -f path/to/workflow.yml
```

### Advanced Options

```bash
# Enable verbose output
./pyalint.py -v

# Enable debug output
./pyalint.py -d

# Output actionlint results in JSON format
./pyalint.py -j

# Use a custom configuration file
./pyalint.py -c path/to/config.yml
```

### Configuration

You can customize the linting rules by creating a configuration file. Here's an example `config.yml`:

```yaml
yamllint:
  rules:
    line-length: disable
    trailing-spaces: enable
    
actionlint:
  flags:
    - "-ignore=SC2016"
    - "-shell=bash"
```

## Exit Codes

- `0`: All checks passed successfully
- `1`: One or more checks failed
- `1`: Missing dependencies or invalid configuration

## Development

To contribute to PyALint:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

[Add your chosen license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
