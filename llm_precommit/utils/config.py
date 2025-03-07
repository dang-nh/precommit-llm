"""
Configuration utilities for LLM pre-commit hooks.
"""
import os
import yaml
from typing import Dict, Any, Optional, Set, List

from llm_precommit.constants import (
    DEFAULT_CONFIG_PATHS,
    DEFAULT_API_KEY_ENV_VAR,
    DEFAULT_LLM_TYPE,
    DEFAULT_MODEL_NAME,
    DEFAULT_INCLUDE_EXTENSIONS,
    DEFAULT_EXCLUDE_PATTERNS,
    DEFAULT_MAX_FILE_SIZE_KB,
    DEFAULT_PROMPT_TEMPLATE,
)


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file. If None, looks for default locations.
        
    Returns:
        Dictionary containing the configuration.
    """
    # Default config
    default_config = {
        "api_key_env_var": DEFAULT_API_KEY_ENV_VAR,
        "llm_type": DEFAULT_LLM_TYPE,
        "model_name": DEFAULT_MODEL_NAME,
        "include_extensions": DEFAULT_INCLUDE_EXTENSIONS,
        "exclude_patterns": DEFAULT_EXCLUDE_PATTERNS,
        "max_file_size_kb": DEFAULT_MAX_FILE_SIZE_KB,
        "verbose": False,
        "check_all_files": False,  # If True, check all files in the repo, not just staged files
        "custom_prompt_template": None,
        "fail_on_issues": False,  # If True, the hook will fail if issues are found
    }
    
    # Look for config file in default locations
    if not config_path:
        for path in DEFAULT_CONFIG_PATHS:
            if os.path.isfile(path):
                config_path = path
                break
    
    # Load config from file if exists
    if config_path and os.path.isfile(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    # Merge user config with default config
                    default_config.update(user_config)
        except Exception as e:
            print(f"Error loading config from {config_path}: {e}")
            print("Using default configuration.")
    
    return default_config


def should_analyze_file(file_path: str, config: Dict[str, Any]) -> bool:
    """
    Determine if a file should be analyzed based on configuration.
    
    Args:
        file_path: Path to the file.
        config: Configuration dictionary.
        
    Returns:
        True if the file should be analyzed, False otherwise.
    """
    # Check file extension
    include_extensions = set(config.get("include_extensions", DEFAULT_INCLUDE_EXTENSIONS))
    if not any(file_path.endswith(ext) for ext in include_extensions):
        return False
    
    # Check exclude patterns
    exclude_patterns = config.get("exclude_patterns", DEFAULT_EXCLUDE_PATTERNS)
    if any(pattern in file_path for pattern in exclude_patterns):
        return False
    
    # Check file exists
    if not os.path.isfile(file_path):
        print(f"Skipping {file_path}: File does not exist")
        return False
    
    # Check file size
    max_file_size_kb = config.get("max_file_size_kb", DEFAULT_MAX_FILE_SIZE_KB)
    try:
        file_size_kb = os.path.getsize(file_path) / 1024
        if file_size_kb > max_file_size_kb:
            print(f"Skipping {file_path}: File size ({file_size_kb:.2f} KB) exceeds limit ({max_file_size_kb} KB)")
            return False
    except Exception as e:
        print(f"Error checking file size for {file_path}: {e}")
        return False
    
    return True


def create_default_config_file(config_path: str = ".llm-precommit.yml") -> bool:
    """
    Create a default configuration file.
    
    Args:
        config_path: Path where the configuration file should be created.
        
    Returns:
        True if the file was created successfully, False otherwise.
    """
    default_config = {
        "api_key_env_var": DEFAULT_API_KEY_ENV_VAR,
        "llm_type": DEFAULT_LLM_TYPE,
        "model_name": DEFAULT_MODEL_NAME,
        "include_extensions": DEFAULT_INCLUDE_EXTENSIONS,
        "exclude_patterns": DEFAULT_EXCLUDE_PATTERNS,
        "max_file_size_kb": DEFAULT_MAX_FILE_SIZE_KB,
        "verbose": False,
        "check_all_files": False,
        "custom_prompt_template": None,
        "fail_on_issues": False,
    }
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f, default_flow_style=False, sort_keys=False)
        print(f"Created default configuration file at {config_path}")
        return True
    except Exception as e:
        print(f"Error creating default configuration file: {e}")
        return False 