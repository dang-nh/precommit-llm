"""
Module for interacting with the Gemini API.
"""
import os
import json
import re
from typing import Dict, Any, List, Optional, Union

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from llm_precommit.utils.llm_client import BaseLLMClient, LLMClientFactory

class GeminiClient(BaseLLMClient):
    """
    Client for interacting with Google's Gemini API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: The API key for Gemini. If not provided, will attempt to read from
                environment variable GEMINI_API_KEY.
                
        Raises:
            ImportError: If google.generativeai package is not installed.
            ValueError: If API key is not provided.
        """
        super().__init__(api_key=api_key, api_key_env_var="GEMINI_API_KEY")
        
        if genai is None:
            raise ImportError(
                "The google.generativeai package is not installed. "
                "Please install it with: pip install google-generativeai"
            )
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        
        # Set the model
        self.model_name = "gemini-2.0-flash-exp"
        self.model = genai.GenerativeModel(self.model_name)
    
    def _call_llm(self, prompt: str) -> Dict[str, Any]:
        """
        Call the Gemini API with the given prompt.
        
        Args:
            prompt: The formatted prompt to send to Gemini.
            
        Returns:
            Dictionary containing the analysis results.
        """
        # Generate response from Gemini
        try:
            response = self.model.generate_content(prompt)
            return self._extract_json_from_response(response.text)
        except Exception as e:
            return {
                "error": str(e),
                "parsing_error": "Failed to call Gemini API"
            }
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extract JSON data from the response text.
        
        Args:
            response_text: The text response from Gemini
            
        Returns:
            Dictionary of parsed JSON data
        """
        try:
            # Try to extract JSON using a more robust approach
            # Look for content within ```json and ``` markers first
            json_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
            json_matches = re.findall(json_pattern, response_text)
            
            if json_matches:
                # Use the last match if there are multiple code blocks
                return json.loads(json_matches[-1])
            
            # If no JSON in code blocks, try to find JSON directly
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_content = response_text[json_start:json_end]
                return json.loads(json_content)
            
            # If no JSON format is found, wrap the entire response
            return {
                "raw_response": response_text,
                "parsing_error": "Could not extract JSON from response"
            }
        except json.JSONDecodeError as e:
            return {
                "raw_response": response_text,
                "parsing_error": f"Invalid JSON format in response: {str(e)}"
            }


# Register the GeminiClient with the factory
LLMClientFactory.register("gemini", GeminiClient) 