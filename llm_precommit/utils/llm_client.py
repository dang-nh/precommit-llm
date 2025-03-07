"""
Abstract base classes for LLM clients.
"""
import os
import abc
import json
import logging
from typing import Dict, Any, Optional, List, Type, Protocol, runtime_checkable

from llm_precommit.constants import DEFAULT_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)

@runtime_checkable
class LLMClient(Protocol):
    """Protocol defining the interface for LLM clients."""
    
    def analyze_code_changes(
        self, 
        diff: str, 
        file_path: str,
        file_content: Optional[str] = None,
        prompt_template: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analyze code changes using the LLM.
        
        Args:
            diff: The git diff content to analyze
            file_path: Path to the file being analyzed
            file_content: Full content of the file (optional)
            prompt_template: Custom prompt template to use (optional)
            
        Returns:
            Dict containing the analysis results
        """
        ...


class BaseLLMClient(abc.ABC):
    """Abstract base class for LLM clients."""
    
    def __init__(self, api_key: Optional[str] = None, api_key_env_var: str = "API_KEY"):
        """
        Initialize the LLM client.
        
        Args:
            api_key: The API key for the LLM service. If not provided, will be read 
                from environment variable.
            api_key_env_var: Name of the environment variable containing the API key.
        
        Raises:
            ValueError: If API key is not provided and not found in environment.
        """
        self.api_key = api_key or os.environ.get(api_key_env_var)
        if not self.api_key:
            raise ValueError(
                f"API key not provided. Set the {api_key_env_var} environment variable or pass it directly."
            )
    
    def analyze_code_changes(
        self, 
        diff: str, 
        file_path: str,
        file_content: Optional[str] = None,
        prompt_template: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analyze code changes using the LLM.
        
        Args:
            diff: The git diff content to analyze
            file_path: Path to the file being analyzed
            file_content: Full content of the file (optional)
            prompt_template: Custom prompt template to use (optional)
            
        Returns:
            Dict containing the analysis results
        """
        # Create the prompt with the template
        template = prompt_template or DEFAULT_PROMPT_TEMPLATE
        
        # Add full content if provided
        full_content_section = ""
        if file_content:
            full_content_section = f"""
            Full file content:
            ```
            {file_content}
            ```
            """
        
        # Format the prompt
        formatted_prompt = template.format(
            file_path=file_path,
            diff=diff,
            full_content_section=full_content_section
        )
        
        # Call the LLM-specific implementation
        return self._call_llm(formatted_prompt)
    
    @abc.abstractmethod
    def _call_llm(self, prompt: str) -> Dict[str, Any]:
        """
        Call the LLM with the given prompt.
        
        Args:
            prompt: The formatted prompt to send to the LLM.
            
        Returns:
            Dictionary containing the analysis results.
        """
        pass


# Factory to create LLM clients
class LLMClientFactory:
    """Factory for creating LLM clients."""
    
    _clients: Dict[str, Type[BaseLLMClient]] = {}
    
    @classmethod
    def register(cls, name: str, client_class: Type[BaseLLMClient]) -> None:
        """
        Register an LLM client class.
        
        Args:
            name: Name to register the client under.
            client_class: The client class to register.
        """
        cls._clients[name] = client_class
    
    @classmethod
    def create(cls, name: str, **kwargs) -> BaseLLMClient:
        """
        Create an instance of an LLM client.
        
        Args:
            name: Name of the client to create.
            **kwargs: Arguments to pass to the client constructor.
            
        Returns:
            An instance of the requested LLM client.
            
        Raises:
            ValueError: If the requested client is not registered.
        """
        if name not in cls._clients:
            available = ", ".join(cls._clients.keys())
            raise ValueError(f"Unknown LLM client '{name}'. Available clients: {available}")
        
        return cls._clients[name](**kwargs) 