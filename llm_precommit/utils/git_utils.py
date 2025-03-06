"""
Utilities for working with Git repositories and diffs.
"""
import os
import subprocess
from typing import List, Dict, Any, Tuple, Set


def get_staged_files() -> List[str]:
    """
    Get a list of staged files in the current git repository.
    
    Returns:
        List of staged file paths.
    """
    cmd = ["git", "diff", "--cached", "--name-only"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return [f for f in result.stdout.splitlines() if os.path.isfile(f)]
    except subprocess.CalledProcessError as e:
        print(f"Error getting staged files: {e}")
        print(f"Command output: {e.stderr}")
        return []


def get_file_diff(file_path: str) -> str:
    """
    Get the git diff for a staged file.
    
    Args:
        file_path: Path to the file.
    
    Returns:
        String containing the git diff.
    """
    cmd = ["git", "diff", "--cached", file_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error getting diff for {file_path}: {e}")
        print(f"Command output: {e.stderr}")
        return ""


def get_file_content(file_path: str) -> str:
    """
    Get the content of a file.
    
    Args:
        file_path: Path to the file.
    
    Returns:
        String containing the file content.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""


def is_python_file(file_path: str) -> bool:
    """
    Check if a file is a Python file.
    
    Args:
        file_path: Path to the file.
    
    Returns:
        True if the file is a Python file, False otherwise.
    """
    return file_path.endswith('.py')


def is_javascript_file(file_path: str) -> bool:
    """
    Check if a file is a JavaScript file.
    
    Args:
        file_path: Path to the file.
    
    Returns:
        True if the file is a JavaScript file, False otherwise.
    """
    return file_path.endswith(('.js', '.jsx', '.ts', '.tsx'))


def filter_files_by_extension(files: List[str], extensions: Set[str]) -> List[str]:
    """
    Filter files by their extensions.
    
    Args:
        files: List of file paths.
        extensions: Set of file extensions to include (with dot, e.g., '.py').
    
    Returns:
        Filtered list of file paths.
    """
    return [f for f in files if any(f.endswith(ext) for ext in extensions)]


def get_git_repo_root() -> str:
    """
    Get the root directory of the git repository.
    
    Returns:
        Path to the root directory of the git repository.
    """
    cmd = ["git", "rev-parse", "--show-toplevel"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting git repo root: {e}")
        print(f"Command output: {e.stderr}")
        return os.getcwd()  # Fallback to current directory 