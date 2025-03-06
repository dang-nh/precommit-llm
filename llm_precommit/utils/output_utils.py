"""
Utilities for formatting and displaying output from the LLM to the user.
"""
import json
from typing import Dict, Any, List
import os
from colorama import Fore, Style, init

# Initialize colorama
init()


class OutputFormatter:
    """
    Format and display the analysis results from the LLM.
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the formatter.
        
        Args:
            verbose: Whether to display verbose output.
        """
        self.verbose = verbose
    
    def format_analysis_result(self, result: Dict[str, Any], file_path: str) -> str:
        """
        Format the analysis result from the LLM.
        
        Args:
            result: The analysis result from the LLM.
            file_path: The path to the analyzed file.
            
        Returns:
            Formatted string for display.
        """
        if "parsing_error" in result:
            return self._format_parsing_error(result, file_path)
        
        output = []
        
        # File header
        output.append(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
        output.append(f"{Fore.CYAN}File: {file_path}{Style.RESET_ALL}")
        output.append(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
        
        # Issues
        if "issues" in result and result["issues"]:
            output.append(f"{Fore.YELLOW}Issues:{Style.RESET_ALL}")
            for issue in result["issues"]:
                severity = issue.get("severity", "unknown")
                severity_color = self._get_severity_color(severity)
                
                output.append(f"  {severity_color}[{severity.upper()}]{Style.RESET_ALL} " + 
                             f"{issue.get('description', 'No description provided')}")
                
                if "line_number" in issue and issue["line_number"]:
                    output.append(f"    {Fore.BLUE}Line: {issue['line_number']}{Style.RESET_ALL}")
                
                if "suggestion" in issue and issue["suggestion"]:
                    output.append(f"    {Fore.GREEN}Suggestion: {issue['suggestion']}{Style.RESET_ALL}")
                
                output.append("")  # Empty line
        
        # Coding convention issues
        if "coding_convention_issues" in result and result["coding_convention_issues"]:
            output.append(f"{Fore.MAGENTA}Coding Convention Issues:{Style.RESET_ALL}")
            for issue in result["coding_convention_issues"]:
                output.append(f"  {Fore.MAGENTA}•{Style.RESET_ALL} {issue.get('description', 'No description provided')}")
                
                if "line_number" in issue and issue["line_number"]:
                    output.append(f"    {Fore.BLUE}Line: {issue['line_number']}{Style.RESET_ALL}")
                
                if "suggestion" in issue and issue["suggestion"]:
                    output.append(f"    {Fore.GREEN}Suggestion: {issue['suggestion']}{Style.RESET_ALL}")
                
                output.append("")  # Empty line
        
        # Security concerns
        if "security_concerns" in result and result["security_concerns"]:
            output.append(f"{Fore.RED}Security Concerns:{Style.RESET_ALL}")
            for concern in result["security_concerns"]:
                severity = concern.get("severity", "unknown")
                severity_color = self._get_severity_color(severity)
                
                output.append(f"  {severity_color}[{severity.upper()}]{Style.RESET_ALL} " + 
                             f"{concern.get('description', 'No description provided')}")
                
                if "suggestion" in concern and concern["suggestion"]:
                    output.append(f"    {Fore.GREEN}Suggestion: {concern['suggestion']}{Style.RESET_ALL}")
                
                output.append("")  # Empty line
        
        # General feedback
        if "general_feedback" in result and result["general_feedback"]:
            output.append(f"{Fore.WHITE}General Feedback:{Style.RESET_ALL}")
            output.append(f"  {result['general_feedback']}\n")
        
        # File type
        if "file_type" in result and result["file_type"]:
            output.append(f"{Fore.CYAN}File Type: {result['file_type']}{Style.RESET_ALL}\n")
        
        # Add a separator at the end
        output.append(f"{Fore.CYAN}{'-' * 80}{Style.RESET_ALL}\n")
        
        return "\n".join(output)
    
    def _format_parsing_error(self, result: Dict[str, Any], file_path: str) -> str:
        """
        Format a parsing error result.
        
        Args:
            result: The result with parsing error.
            file_path: The path to the analyzed file.
            
        Returns:
            Formatted string for display.
        """
        output = []
        
        # File header
        output.append(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
        output.append(f"{Fore.CYAN}File: {file_path}{Style.RESET_ALL}")
        output.append(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
        
        # Error message
        output.append(f"{Fore.RED}Error: {result['parsing_error']}{Style.RESET_ALL}\n")
        
        # Raw response if verbose
        if self.verbose and "raw_response" in result:
            output.append(f"{Fore.YELLOW}Raw Response:{Style.RESET_ALL}")
            output.append(result["raw_response"])
            output.append("")
        
        # Add a separator at the end
        output.append(f"{Fore.CYAN}{'-' * 80}{Style.RESET_ALL}\n")
        
        return "\n".join(output)
    
    def _get_severity_color(self, severity: str) -> str:
        """
        Get the color for a severity level.
        
        Args:
            severity: The severity level.
            
        Returns:
            ANSI color code for the severity level.
        """
        severity = severity.lower()
        if severity == "critical":
            return Fore.RED + Style.BRIGHT
        elif severity == "high":
            return Fore.RED
        elif severity == "medium":
            return Fore.YELLOW
        elif severity == "low":
            return Fore.YELLOW + Style.DIM
        elif severity == "info":
            return Fore.BLUE
        else:
            return Fore.WHITE


def print_summary(results: Dict[str, Dict[str, Any]]) -> None:
    """
    Print a summary of all file analyses.
    
    Args:
        results: Dictionary mapping file paths to analysis results.
    """
    total_files = len(results)
    files_with_issues = sum(1 for r in results.values() 
                          if "issues" in r and r["issues"])
    files_with_convention_issues = sum(1 for r in results.values() 
                                     if "coding_convention_issues" in r and r["coding_convention_issues"])
    files_with_security_concerns = sum(1 for r in results.values() 
                                     if "security_concerns" in r and r["security_concerns"])
    
    print(f"\n{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}SUMMARY{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}")
    print(f"Total files analyzed: {total_files}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Files with convention issues: {files_with_convention_issues}")
    print(f"Files with security concerns: {files_with_security_concerns}")
    print(f"{Fore.CYAN}{'=' * 40}{Style.RESET_ALL}\n")
    
    if files_with_issues > 0 or files_with_convention_issues > 0 or files_with_security_concerns > 0:
        print(f"{Fore.YELLOW}Please review the issues above before committing.{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}No issues found! Your code looks good.{Style.RESET_ALL}")
    
    print("")  # Empty line 