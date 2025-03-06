#!/usr/bin/env python3
"""
Main pre-commit hook for code review using LLM.
"""
import os
import sys
import argparse
from typing import Dict, Any, List, Optional

# Add parent directory to path to enable imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_precommit.utils.gemini_client import GeminiClient
from llm_precommit.utils.git_utils import (
    get_staged_files, 
    get_file_diff, 
    get_file_content, 
    filter_files_by_extension,
)
from llm_precommit.utils.config import load_config, should_analyze_file
from llm_precommit.utils.output_utils import OutputFormatter, print_summary


def get_api_key(config: Dict[str, Any]) -> Optional[str]:
    """
    Get the API key from the environment variable specified in the config.
    
    Args:
        config: The configuration dictionary.
        
    Returns:
        The API key or None if not found.
    """
    env_var_name = config.get("api_key_env_var", "GEMINI_API_KEY")
    return os.environ.get(env_var_name)


def analyze_files(files: List[str], config: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Analyze a list of files using the LLM.
    
    Args:
        files: List of file paths to analyze.
        config: Configuration dictionary.
        
    Returns:
        Dictionary mapping file paths to analysis results.
    """
    api_key = get_api_key(config)
    if not api_key:
        print(f"Error: API key not found in environment variable {config.get('api_key_env_var', 'GEMINI_API_KEY')}")
        print("Please set the API key in your environment or config file.")
        return {}
    
    # Initialize clients
    gemini_client = GeminiClient(api_key=api_key)
    formatter = OutputFormatter(verbose=config.get("verbose", False))
    
    # Custom prompt template if provided
    custom_prompt = config.get("custom_prompt_template")
    
    # Process each file
    results = {}
    for file_path in files:
        if not should_analyze_file(file_path, config):
            continue
        
        # Get file diff and content
        diff = get_file_diff(file_path)
        if not diff:
            print(f"Skipping {file_path}: No changes detected")
            continue
        
        # Get the full file content if available
        file_content = get_file_content(file_path)
        
        # Analyze with LLM
        try:
            print(f"Analyzing {file_path}...")
            result = gemini_client.analyze_code_changes(
                diff=diff,
                file_path=file_path,
                file_content=file_content,
                prompt_template=custom_prompt,
            )
            
            # Display the formatted result
            print(formatter.format_analysis_result(result, file_path))
            
            # Store the result
            results[file_path] = result
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            results[file_path] = {
                "error": str(e),
                "parsing_error": "Failed to analyze file"
            }
    
    return results


def main() -> int:
    """
    Main entry point for the pre-commit hook.
    
    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    parser = argparse.ArgumentParser(description="LLM-powered code review pre-commit hook")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--all", action="store_true", help="Check all files in repo, not just staged files")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override config with command line args
    if args.all:
        config["check_all_files"] = True
    if args.verbose:
        config["verbose"] = True
    
    # Get files to analyze
    files = get_staged_files()
    if not files:
        print("No staged files found.")
        return 0
    
    # Analyze files
    results = analyze_files(files, config)
    
    # Print summary
    if results:
        print_summary(results)
    
    # Determine exit code
    has_issues = any(
        ("issues" in result and result["issues"]) or 
        ("security_concerns" in result and result["security_concerns"])
        for result in results.values()
    )
    
    # If configured to fail on issues, return non-zero exit code
    if config.get("fail_on_issues", False) and has_issues:
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 