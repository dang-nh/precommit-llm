"""
Module for interacting with the Gemini API.
"""
import os
import json
import google.generativeai as genai
from typing import Dict, Any, List, Optional, Union

class GeminiClient:
    """
    Client for interacting with Google's Gemini API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: The API key for Gemini. If not provided, will attempt to read from
                environment variable GEMINI_API_KEY.
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key not provided. Set the GEMINI_API_KEY environment variable or pass it directly."
            )
        
        # Configure the Gemini API
        genai.configure(api_key=self.api_key)
        
        # Set the model
        self.model_name = "gemini-2.0-flash-exp"
        self.model = genai.GenerativeModel(self.model_name)
    
    def analyze_code_changes(
        self, 
        diff: str, 
        file_path: str,
        file_content: Optional[str] = None,
        prompt_template: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analyze code changes using Gemini.
        
        Args:
            diff: The git diff content to analyze
            file_path: Path to the file being analyzed
            file_content: Full content of the file (optional)
            prompt_template: Custom prompt template to use (optional)
            
        Returns:
            Dict containing the analysis results
        """
        # Create a default prompt if none is provided
        if not prompt_template:
            prompt_template = """
            You are a code reviewer and your task is to analyze the following code changes.
            Please identify any issues, bugs, or improvements for code quality and convention.
            
            File path: {file_path}
            
            Git diff:
            ```
            {diff}
            ```
            
            {full_content_section}
            
            Provide your feedback in the following JSON format:
            {{
                "issues": [
                    {{
                        "severity": "critical|high|medium|low|info",
                        "description": "Clear description of the issue",
                        "line_number": "line number or range (if applicable)",
                        "suggestion": "Suggestion to fix the issue (if applicable)"
                    }}
                ],
                "coding_convention_issues": [
                    {{
                        "line_number": "line number or range",
                        "description": "Description of the convention issue",
                        "suggestion": "Suggestion to fix the issue"
                    }}
                ],
                "security_concerns": [
                    {{
                        "severity": "critical|high|medium|low",
                        "description": "Description of the security concern",
                        "suggestion": "Suggestion to address the security concern"
                    }}
                ],
                "general_feedback": "Overall thoughts and general feedback",
                "file_type": "The type of file (e.g., Python, JavaScript, HTML, etc.)"
            }}
            
            Ensure your response is strictly in this JSON format and correctly escaped.
            """
        
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
        formatted_prompt = prompt_template.format(
            file_path=file_path,
            diff=diff,
            full_content_section=full_content_section
        )
        
        # Generate response from Gemini
        response = self.model.generate_content(formatted_prompt)
        
        # Parse the response to extract JSON
        result = self._extract_json_from_response(response.text)
        
        return result
    
    def _extract_json_from_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extract JSON data from the response text.
        
        Args:
            response_text: The text response from Gemini
            
        Returns:
            Dictionary of parsed JSON data
        """
        try:
            # Try to find JSON content within the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_content = response_text[json_start:json_end]
                return json.loads(json_content)
            else:
                # If no JSON format is found, wrap the entire response
                return {
                    "raw_response": response_text,
                    "parsing_error": "Could not extract JSON from response"
                }
        except json.JSONDecodeError:
            return {
                "raw_response": response_text,
                "parsing_error": "Invalid JSON format in response"
            } 