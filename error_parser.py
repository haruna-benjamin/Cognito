import re
from typing import Dict, Any
from datetime import datetime

class ErrorParser:
    def __init__(self):
        self.patterns = {
            'apt_repository': [
                r"E: The repository '.+' does not have a Release file",
                r"E: .*repository.*not found",
                r"E: .*failed to fetch",
                r"W: Failed to fetch .* 404 Not Found",
                r"E: .*release file",
                r"repository.*not available",
                r"failed to fetch.*repository"
            ],
            'permission_denied': [
                r"Permission denied",
                r"E: Could not open lock file",
                r"Operation not permitted",
                r"Access denied",
                r"Unable to acquire the dpkg frontend lock",
                r"permission.*denied",
                r"not allowed",
                r"access.*denied",
                r"cannot open.*permission"
            ],
            'command_not_found': [
                r"command not found",
                r"Command '.+' not found",
                r"bash: .*: command not found",
                r"zsh: command not found:",
                r"command.*not found",
                r"not found.*command",
                r"no such.*command"
            ],
            'file_not_found': [
                r"No such file or directory",
                r"File not found",
                r"cannot access .*: No such file or directory",
                r"ls: cannot access .*: No such file or directory",
                r"file.*not found",
                r"no such file",
                r"cannot find.*file",
                r"missing.*file",
                r"file.*missing",
                r"cannot open.*file",
                r"open.*file.*failed"
            ],
            'syntax_error': [
                r"SyntaxError:",
                r"E: Invalid operation",
                r"Invalid command",
                r"bash: syntax error",
                r"unexpected token",
                r"syntax error",
                r"invalid syntax"
            ],
            'dependency_error': [
                r"dependency problems",
                r"unmet dependencies",
                r"broken packages",
                r"you have held broken packages",
                r"depends on .* but it is not going to be installed",
                r"dependency.*error",
                r"broken.*dependency"
            ],
            'network_error': [
                r"Temporary failure resolving",
                r"Failed to connect to",
                r"Connection timed out",
                r"Network is unreachable",
                r"connection.*failed",
                r"network.*error",
                r"cannot connect",
                r"timeout"
            ]
        }
        
        # Natural language patterns for common phrases
        self.natural_patterns = {
            'file_not_found': [
                r"can'?t open file",
                r"cannot open file",
                r"file (is )?missing",
                r"missing file",
                r"file not found",
                r"no such file",
                r"couldn'?t find file",
                r"unable to open file"
            ],
            'permission_denied': [
                r"permission denied",
                r"not allowed",
                r"access denied",
                r"don'?t have permission",
                r"cannot access"
            ],
            'command_not_found': [
                r"command not found",
                r"can'?t find command",
                r"no such command",
                r"command.*missing"
            ]
        }
    
    def parse_error(self, error_message: str) -> Dict[str, Any]:
        """Parse error message and extract structured information"""
        error_type = self.classify_error(error_message)
        
        return {
            'original_message': error_message,
            'error_type': error_type,
            'components': self.extract_components(error_message, error_type),
            'confidence': self.calculate_confidence(error_message, error_type),
            'timestamp': datetime.now().isoformat()
        }
    
    def classify_error(self, error_message: str) -> str:
        """Classify the error type based on patterns"""
        error_lower = error_message.lower()
        
      
        for error_type, patterns in self.natural_patterns.items():
            for pattern in patterns:
                if re.search(pattern, error_lower, re.IGNORECASE):
                    return error_type
        
       
        for error_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, error_message, re.IGNORECASE):
                    return error_type
        
        return 'unknown'
    
    def extract_components(self, error_message: str, error_type: str) -> Dict[str, str]:
        """Extract specific components from the error message"""
        components = {}
        
        if error_type == 'apt_repository':
            repo_match = re.search(r"'([^']+)'", error_message)
            if repo_match:
                components['repository'] = repo_match.group(1)
            
            distro_match = re.search(r'(\w+)\s+Release', error_message)
            if distro_match:
                components['distribution'] = distro_match.group(1)
        
        elif error_type == 'command_not_found':
            cmd_match = re.search(r"Command '([^']+)'", error_message)
            if not cmd_match:
                cmd_match = re.search(r"(?:bash|zsh): ([^:]+): command not found", error_message)
            if not cmd_match:
                
                cmd_match = re.search(r"(?:can'?t find|command not found).*?([a-zA-Z0-9_-]+)", error_message.lower())
            if cmd_match:
                components['command'] = cmd_match.group(1)
        
        elif error_type == 'file_not_found':
            file_match = re.search(r"'(.*?)'", error_message)
            if not file_match:
                file_match = re.search(r"cannot access (.+?):", error_message)
            if not file_match:
               
                file_match = re.search(r"(?:file|open).*?([a-zA-Z0-9_./-]+)", error_message.lower())
            if file_match:
                components['filename'] = file_match.group(1)
        
        elif error_type == 'permission_denied':
            
            access_match = re.search(r"(?:access|open|execute).*?([a-zA-Z0-9_./-]+)", error_message.lower())
            if access_match:
                components['resource'] = access_match.group(1)
        
        return components
    
    def calculate_confidence(self, error_message: str, error_type: str) -> float:
        """Calculate confidence score for the classification"""
        if error_type == 'unknown':
            return 0.3
        
        error_lower = error_message.lower()
        
        
        technical_matches = 0
        if error_type in self.patterns:
            for pattern in self.patterns[error_type]:
                if re.search(pattern, error_message, re.IGNORECASE):
                    technical_matches += 1
        
        
        natural_matches = 0
        if error_type in self.natural_patterns:
            for pattern in self.natural_patterns[error_type]:
                if re.search(pattern, error_lower, re.IGNORECASE):
                    natural_matches += 1
        
        if technical_matches > 0:
            return min(0.3 + (technical_matches * 0.2) + (natural_matches * 0.1), 0.95)
        elif natural_matches > 0:
            return min(0.5 + (natural_matches * 0.15), 0.9)
        
        return 0.7
