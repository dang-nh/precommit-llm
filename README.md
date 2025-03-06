# LLM Pre-commit Hook

A pre-commit hook using LLM models (specifically Google Gemini) to check code quality and coding conventions before committing.

## Features

- Automatically analyzes staged files before committing
- Detects bugs, code quality issues, and coding convention problems
- Warns about potential security concerns
- Suggests fixes for issues
- Supports multiple file types (Python, JavaScript, TypeScript, Java, Go, etc.)
- Customizable via configuration file

## Requirements

- Python 3.7+
- Git
- API key for Gemini (https://ai.google.dev/)

## Installation

### From PyPI

```bash
pip install llm-precommit
```

### From Source

```bash
git clone https://github.com/yourusername/llm-precommit.git
cd llm-precommit
pip install -e .
```

### Installing the pre-commit hook

After installing the package, you need to install the pre-commit hook in your repository:

```bash
cd /path/to/your/repository
llm-precommit install
```

This command will create a pre-commit hook file in the `.git/hooks` directory and a default configuration file `.llm-precommit.yml` in the root directory of your repository.

## Configuration

The `.llm-precommit.yml` configuration file contains options for the pre-commit hook:

```yaml
# API key is retrieved from environment variable
api_key_env_var: GEMINI_API_KEY

# File types to analyze
include_extensions:
  - .py
  - .js
  - .jsx
  - .ts
  - .tsx
  - .css
  - .html
  - .go
  - .java
  - .c
  - .cpp
  - .rs

# Patterns for files to exclude
exclude_patterns:
  - node_modules/
  - venv/
  - env/
  - __pycache__/
  - "*.min.js"
  - "*.min.css"
  - build/
  - dist/

# Maximum file size (KB)
max_file_size_kb: 100

# Show detailed information
verbose: false

# Check all files, not just staged files
check_all_files: false

# Custom prompt template for LLM
custom_prompt_template: null

# Fails the commit if issues are found
fail_on_issues: false
```

## Usage

### Automatic

After installing the pre-commit hook, each time you run `git commit`, the hook will automatically run and analyze the staged files.

### Manual

You can run the analysis manually without committing:

```bash
llm-precommit run
```

Or to analyze all files in the repository:

```bash
llm-precommit run --all
```

### Setting the API Key

You need to set the API key for Gemini in an environment variable:

```bash
export GEMINI_API_KEY=your_api_key_here
```

Or you can add this variable to your `.bashrc` or `.zshrc` file:

```bash
echo 'export GEMINI_API_KEY=your_api_key_here' >> ~/.bashrc
source ~/.bashrc
```

## CLI Commands

```
Usage: llm-precommit [command] [options]

Commands:
  install    Install pre-commit hook
  uninstall  Remove pre-commit hook
  config     Create default configuration file
  run        Run code analysis manually

Options for 'run' command:
  --config   Path to configuration file
  --all      Check all files, not just staged files
  --verbose  Display more detailed information

Options for 'config' command:
  --output, -o  Output path for configuration file
  --force, -f   Overwrite existing configuration file
```

## Example output

```
================================================================================
File: src/utils.py
================================================================================

Issues:
  [MEDIUM] Potential bug: variable 'result' may be used before assignment
    Line: 45-50
    Suggestion: Initialize 'result' with a default value before the try-except block

Coding Convention Issues:
  • Function 'calculate_total' is too long (30 lines)
    Line: 25-55
    Suggestion: Consider breaking it down into smaller functions

  • Variable names 'a', 'b', 'c' are not descriptive
    Line: 27-29
    Suggestion: Use more descriptive variable names

Security Concerns:
  [HIGH] Use of 'eval' function is a security risk
    Line: 42
    Suggestion: Replace eval() with safer alternatives

General Feedback:
  The code could benefit from more comments and better error handling.

File Type: Python
--------------------------------------------------------------------------------

================================================================================
SUMMARY
================================================================================
Total files analyzed: 1
Files with issues: 1
Files with convention issues: 1
Files with security concerns: 1
================================================================================

Please review the issues above before committing.
```

## License

MIT License

## Contributing

Contributions and feedback are always welcome! Please create an issue or pull request on GitHub. 