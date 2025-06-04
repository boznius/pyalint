#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
import json
import shutil
from pathlib import Path
from typing import List, Optional, Dict
import yaml

DEFAULT_CONFIG = {
    'yamllint': {
        'rules': {
            'line-length': 'disable'
        }
    },
    'actionlint': {
        'flags': []
    }
}

def load_config(config_path: Optional[str] = None) -> Dict:
    """Load configuration from file or return defaults.
    
    Args:
        config_path: Optional path to config file
        
    Returns:
        Dict containing configuration
    """
    if config_path:
        try:
            with open(config_path, 'r') as f:
                return {**DEFAULT_CONFIG, **yaml.safe_load(f)}
        except Exception as e:
            print(f"⚠️ Error loading config file: {e}")
            print("Using default configuration.")
    return DEFAULT_CONFIG

def check_dependencies() -> None:
    """Check if required command line tools are available."""
    missing = []
    for tool in ['yamllint', 'actionlint']:
        if not shutil.which(tool):
            missing.append(tool)
    if missing:
        print(f"❌ Missing tools: {', '.join(missing)}. Please install them before running the script.")
        sys.exit(1)

def find_workflow_files(directory: str | Path) -> List[Path]:
    """Find all YAML workflow files in the given directory."""
    return list(Path(directory).rglob("*.yml")) + list(Path(directory).rglob("*.yaml"))

def run_command(command, verbose=False) -> str:
    """Run a shell command and return its output.
    
    Args:
        command (List[str]): Command to run as a list of strings
        verbose (bool): Whether to print the command being run
        
    Returns:
        str: Command output (stdout + stderr if error occurs)
        
    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit code
    """
    try:
        if verbose:
            print(f"🔧 Running: {' '.join(command)}")
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Command failed with exit code {e.returncode}")
        return e.stdout + e.stderr
    except Exception as e:
        print(f"❌ Unexpected error running command: {str(e)}")
        return f"Error: {str(e)}"

def lint_yaml(file_path: str | Path, config: Dict, verbose: bool = False) -> str:
    """Run yamllint on the specified file."""
    rules = config.get('yamllint', {}).get('rules', {})
    rules_str = ','.join(f'{k}: {v}' for k, v in rules.items())
    yamllint_cmd = [
        'yamllint',
        '-d',
        f'{{extends: default, rules: {{{rules_str}}}}}',
        str(file_path)
    ]
    return run_command(yamllint_cmd, verbose)

def lint_action(file_path: str | Path, config: Dict, verbose: bool = False, json_output: bool = False) -> str:
    """Run actionlint on the specified file."""
    cmd = ['actionlint']
    if json_output:
        cmd += ['-format=json']
    elif verbose:
        cmd += ['-verbose']
    
    # Add any custom flags from config
    cmd.extend(config.get('actionlint', {}).get('flags', []))
    cmd.append(str(file_path))
    return run_command(cmd, verbose)

def main() -> int:
    """Run the main linting process.
    
    Returns:
        int: Exit code (0 for success, 1 for errors)
    """
    parser = argparse.ArgumentParser(description="Lint GitHub Actions YAML files.")
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('-j', '--json', action='store_true', help='Output JSON from actionlint')
    parser.add_argument('-f', '--file', type=str, help='Specify a single workflow file to check')
    parser.add_argument('-c', '--config', type=str, help='Path to configuration file')
    args = parser.parse_args()

    config = load_config(args.config)
    if args.debug:
        print("Configuration:", json.dumps(config, indent=2))

    files_to_check = []
    has_errors = False

    if args.file:
        target = Path(args.file)
        if not target.exists() or not target.is_file():
            print(f"❌ Specified file does not exist: {target}")
            return 1
        files_to_check.append(target)
    else:
        workflows_dir = Path(".github/workflows")
        if not workflows_dir.exists():
            print("⚠️ .github/workflows directory not found.")
            return 0
        files_to_check = find_workflow_files(workflows_dir)

    if not files_to_check:
        print("⚠️ No workflow files found.")
        return 0

    for file in files_to_check:
        print(f"\n📄 Checking: {file}")

        print("  • yamllint:")
        yamllint_output = lint_yaml(file, config, verbose=args.verbose or args.debug)
        print(yamllint_output)
        if "error" in yamllint_output.lower():
            has_errors = True

        print("  • actionlint:")
        actionlint_output = lint_action(file, config, verbose=args.verbose or args.debug, json_output=args.json)
        if args.json:
            try:
                parsed = json.loads(actionlint_output)
                if parsed:  # If there are any issues
                    has_errors = True
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print("⚠️ Failed to parse JSON output.")
                print(actionlint_output)
                has_errors = True
        else:
            print(actionlint_output)
            if actionlint_output.strip():  # If there's any output, it's usually an error
                has_errors = True

    if has_errors:
        print("\n❌ Checks completed with errors.")
        return 1
    else:
        print("\n✅ All checks completed successfully.")
        return 0

if __name__ == "__main__":
    check_dependencies()
    sys.exit(main())
