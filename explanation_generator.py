from knowledge_base import KnowledgeBase

class ExplanationGenerator:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
    
    def generate_explanation(self, parsed_error: dict) -> dict:
        """Generate a comprehensive explanation for the parsed error"""
        error_type = parsed_error['error_type']
        components = parsed_error['components']
        knowledge = self.knowledge_base.get_knowledge(error_type)
        
        # Customize based on components
        customized_solutions = self.customize_solutions(
            knowledge['solutions'], 
            components
        )
        
        customized_cause = self.customize_cause(
            knowledge['common_causes'],
            components
        )
        
        return {
            'error_type': error_type,
            'severity': self.assess_severity(error_type),
            'summary': knowledge['summary'],
            'likely_cause': customized_cause,
            'solutions': customized_solutions,
            'prevention_tips': knowledge['prevention_tips'],
            'learn_more': knowledge['learn_more'],
            'confidence': parsed_error['confidence']
        }
    
    def assess_severity(self, error_type: str) -> str:
        """Assess the severity of the error"""
        severity_map = {
            'apt_repository': 'medium',
            'permission_denied': 'low',
            'command_not_found': 'low', 
            'file_not_found': 'low',
            'syntax_error': 'low',
            'dependency_error': 'high',
            'network_error': 'medium',
            'unknown': 'unknown'
        }
        return severity_map.get(error_type, 'unknown')
    
    def customize_cause(self, common_causes: list, components: dict) -> str:
        """Choose and customize the most likely cause based on error context"""
        if not common_causes:
            return "Unknown cause - requires further investigation"
        
        # Default to first cause
        cause = common_causes[0]
        
        # Customize based on components
        if 'repository' in components:
            cause = f"Repository '{components['repository']}' is not available for your system version"
        elif 'command' in components:
            cause = f"Command '{components['command']}' is not installed or not in PATH"
        elif 'filename' in components:
            cause = f"File or directory '{components['filename']}' does not exist or cannot be accessed"
        elif 'resource' in components:
            cause = f"You don't have permission to access '{components['resource']}'"
        
        return cause
    
    def customize_solutions(self, base_solutions: list, components: dict) -> list:
        """Customize solutions based on specific error components"""
        solutions = base_solutions.copy()
        
        if 'repository' in components:
            repo_solution = f"Remove this specific repository: sudo add-apt-repository --remove '{components['repository']}'"
            if repo_solution not in solutions:
                solutions.insert(1, repo_solution)
        
        elif 'command' in components:
            cmd_solution = f"Install package containing '{components['command']}': sudo apt install {components['command']}"
            solutions.insert(0, cmd_solution)
        
        elif 'filename' in components:
            file_solution = f"Check if file exists: ls -la '{components['filename']}'"
            solutions.insert(0, file_solution)
            
            # Add file creation solution for missing files
            create_solution = f"Create the file if it should exist: touch '{components['filename']}'"
            if create_solution not in solutions:
                solutions.insert(1, create_solution)
        
        elif 'resource' in components:
            perm_solution = f"Check permissions on '{components['resource']}': ls -la '{components['resource']}'"
            solutions.insert(0, perm_solution)
        
        return solutions