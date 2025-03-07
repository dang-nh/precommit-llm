# LLM Pre-commit Hook

A pre-commit hook using LLM models to check code quality and coding conventions before committing. Currently supports Google Gemini with plans to expand to other LLM providers.

## Features

- Automatically analyzes staged files before committing
- Detects bugs, code quality issues, and coding convention problems
- Warns about potential security concerns
- Suggests specific, actionable fixes for issues
- Analyzes code in context with detailed feedback
- Supports multiple file types (Python, JavaScript, TypeScript, Java, Go, etc.)
- Highly customizable via configuration file
- Language-specific guidelines and conventions

## Requirements

- Python 3.7+
- Git
- API key for Gemini (https://aistudio.google.com/apikey)

## Installation

### From PyPI

```bash
pip install llm-precommit
```

### From Source

```bash
git clone https://github.com/dang-nh/llm-precommit.git
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

# LLM Model Configuration
llm_type: gemini
model_name: gemini-2.0-flash-exp

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

### Advanced Configuration

For more advanced configurations, see the [examples/advanced_config.yml](examples/advanced_config.yml) file, which includes:

- Language-specific analysis settings
- Custom analysis focus areas
- Performance tuning options
- Specialized prompt templates
- Severity-based failure conditions

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
    Category: bug
    Suggestion: Initialize 'result' with a default value before the try-except block
    Explanation: If an exception occurs before 'result' is assigned, using it later will raise NameError

Coding Convention Issues:
  • Function 'calculate_total' is too long (30 lines)
    Line: 25-55
    Convention: PEP 8 - Function Length
    Suggestion: Consider breaking it down into smaller functions

  • Variable names 'a', 'b', 'c' are not descriptive
    Line: 27-29
    Convention: PEP 8 - Naming Conventions
    Suggestion: Use more descriptive variable names like 'amount', 'base_price', 'count'

Security Concerns:
  [HIGH] Use of 'eval' function is a security risk
    Line: 42
    Vulnerability Type: code-injection
    Potential Impact: Remote code execution by attackers
    Suggestion: Replace eval() with safer alternatives like ast.literal_eval() or json.loads()
    CWE ID: CWE-95

Positive Aspects:
  • Good use of error handling with try/except blocks
  • Consistent code formatting
  • Helpful docstrings on public functions

General Feedback:
  The code is well structured but could benefit from more input validation and 
  better error handling. Consider adding type hints for better maintainability.

Summary: The code has one medium severity bug and one high security risk that should 
be addressed. It generally follows good practices but needs some refactoring for better maintainability.

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

## Extending 

### Supporting Additional LLM Models

The tool uses a modular design that can be extended to support other LLM models:

1. Create a new client that implements the `BaseLLMClient` interface
2. Register it with the `LLMClientFactory`
3. Update your config to use the new LLM type

## Testing

Run the test suite with:

```bash
python -m unittest discover tests
```

## License

MIT License

## Contributing

Contributions and feedback are always welcome! Please create an issue or pull request on GitHub. 