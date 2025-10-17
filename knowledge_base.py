class KnowledgeBase:
    def __init__(self):
        self.error_knowledge = {
            'apt_repository': {
                'summary': 'APT repository configuration error',
                'common_causes': [
                    'Repository does not support your Ubuntu version',
                    'Repository URL is incorrect or deprecated',
                    'Repository has been removed or is temporarily unavailable',
                    'Network connectivity issues preventing access',
                    'Distribution codename mismatch'
                ],
                'solutions': [
                    'Check if the repository supports your Ubuntu version',
                    'Remove the problematic repository: sudo add-apt-repository --remove <repository>',
                    'Update your package lists: sudo apt update',
                    'Check your internet connection and DNS settings',
                    'Verify the repository URL in /etc/apt/sources.list or /etc/apt/sources.list.d/',
                    'Try changing the distribution codename in the repository URL to match your system'
                ],
                'prevention_tips': [
                    'Always verify repository compatibility before adding',
                    'Use official Ubuntu repositories when possible',
                    'Regularly clean up unused repositories',
                    'Keep your system updated to supported versions'
                ],
                'learn_more': 'https://help.ubuntu.com/community/Repositories/CommandLine'
            },
            'permission_denied': {
                'summary': 'File or operation permission error',
                'common_causes': [
                    'Insufficient user privileges for the operation',
                    'File ownership issues',
                    'Running command without sudo when required',
                    'File system permissions are too restrictive',
                    'Another process is holding a lock'
                ],
                'solutions': [
                    'Try running the command with sudo: sudo <command>',
                    'Check file permissions: ls -l <filename>',
                    'Change file ownership: sudo chown $USER <filename>',
                    'Change file permissions: chmod +x <filename> for executables',
                    'Check if another package manager is running: ps aux | grep apt',
                    'Remove lock files: sudo rm /var/lib/dpkg/lock* /var/cache/apt/archives/lock'
                ],
                'prevention_tips': [
                    'Understand when sudo is required for system operations',
                    'Be careful when changing file permissions system-wide',
                    'Use groups for shared file access instead of world permissions',
                    'Always check what commands do before running with sudo'
                ],
                'learn_more': 'https://wiki.ubuntu.com/Security/Privileges'
            },
            'command_not_found': {
                'summary': 'Command not available in system PATH',
                'common_causes': [
                    'Required package is not installed',
                    'Command name is misspelled',
                    'Command is not in PATH environment variable',
                    'Package is installed but not properly linked',
                    'Shell needs to be restarted after installation'
                ],
                'solutions': [
                    'Install the required package: sudo apt install <package-name>',
                    'Check command spelling and try again',
                    'Find which package provides the command: apt search <command> or apt-file search <command>',
                    'Check if command is in PATH: which <command> or type <command>',
                    'Update your shell: exec bash or source ~/.bashrc',
                    'Install apt-file for searching: sudo apt install apt-file && sudo apt-file update'
                ],
                'prevention_tips': [
                    'Use tab completion to avoid spelling errors',
                    'Keep your system updated regularly',
                    'Document required packages for your projects',
                    'Verify installations with --dry-run first when possible'
                ],
                'learn_more': 'https://help.ubuntu.com/community/InstallingSoftware'
            },
            'file_not_found': {
                'summary': 'File or directory does not exist',
                'common_causes': [
                    'File was moved, renamed, or deleted',
                    'Path contains typos or incorrect case',
                    'Working directory is different than expected',
                    'Symbolic link is broken',
                    'Filesystem mount issue'
                ],
                'solutions': [
                    'Check if file exists: ls -la <path>',
                    'Verify the full path to the file',
                    'Check your current directory: pwd',
                    'Use absolute paths instead of relative paths',
                    'Check for case sensitivity in filenames',
                    'Verify symbolic links: ls -l <link-path>'
                ],
                'prevention_tips': [
                    'Use tab completion for paths to avoid typos',
                    'Double-check paths in scripts and commands',
                    'Use environment variables for common paths',
                    'Regularly backup important files'
                ],
                'learn_more': 'https://help.ubuntu.com/community/LinuxFilesystemTreeOverview'
            },
            'dependency_error': {
                'summary': 'Package dependency resolution failure',
                'common_causes': [
                    'Conflicting package requirements',
                    'Broken packages from previous installations',
                    'Third-party repositories causing conflicts',
                    'Partial upgrades or mixed release sources',
                    'Held packages preventing resolution'
                ],
                'solutions': [
                    'Fix broken packages: sudo apt --fix-broken install',
                    'Clean the package cache: sudo apt clean',
                    'Update package lists: sudo apt update',
                    'Try automatic repair: sudo apt autoremove && sudo apt autoclean',
                    'Use dpkg to repair: sudo dpkg --configure -a',
                    'Check for held packages: apt-mark showhold',
                    'Remove problematic repositories temporarily'
                ],
                'prevention_tips': [
                    'Avoid mixing repositories from different Ubuntu versions',
                    'Be cautious with third-party PPAs',
                    'Regularly run system updates',
                    'Read changelogs before major upgrades'
                ],
                'learn_more': 'https://help.ubuntu.com/community/AptGet/Howto'
            },
            'network_error': {
                'summary': 'Network connectivity issue',
                'common_causes': [
                    'Internet connection is down',
                    'DNS resolution failure',
                    'Firewall blocking connections',
                    'Repository server is down',
                    'Proxy configuration issues'
                ],
                'solutions': [
                    'Check internet connection: ping 8.8.8.8',
                    'Test DNS resolution: ping google.com',
                    'Check firewall settings: sudo ufw status',
                    'Try different network or wait if server is down',
                    'Check proxy settings: echo $http_proxy',
                    'Restart network services: sudo systemctl restart systemd-resolved'
                ],
                'prevention_tips': [
                    'Keep track of reliable repository mirrors',
                    'Configure backup DNS servers',
                    'Monitor network connectivity regularly',
                    'Use VPNs carefully with package management'
                ],
                'learn_more': 'https://help.ubuntu.com/community/InternetAndNetworking'
            },
            'syntax_error': {
                'summary': 'Command syntax or usage error',
                'common_causes': [
                    'Typographical errors in commands',
                    'Incorrect option flags',
                    'Missing or extra arguments',
                    'Wrong command order or structure',
                    'Shell interpretation issues'
                ],
                'solutions': [
                    'Check command spelling and syntax',
                    'Review command documentation: man <command>',
                    'Use --help flag: <command> --help',
                    'Check for proper quoting of arguments',
                    'Verify variable expansion in scripts',
                    'Test commands in a clean environment'
                ],
                'prevention_tips': [
                    'Always review commands before executing',
                    'Use shell syntax highlighting',
                    'Test complex commands in scripts first',
                    'Keep command documentation handy'
                ],
                'learn_more': None
            },
            'unknown': {
                'summary': 'Unrecognized error type',
                'common_causes': [
                    'New or uncommon error pattern',
                    'Multiple errors combined in one message',
                    'Application-specific error not in database',
                    'Custom or proprietary software error'
                ],
                'solutions': [
                    'Search the exact error message online',
                    'Check application-specific documentation',
                    'Look for similar issues in community forums',
                    'Try to isolate the specific component causing the error',
                    'Check system logs: dmesg | tail or journalctl -xe',
                    'Run commands with verbose output for more details'
                ],
                'prevention_tips': [
                    'Keep detailed logs of operations',
                    'Reproduce errors in isolated environments',
                    'Stay updated with software patches',
                    'Participate in community support forums'
                ],
                'learn_more': None
            }
        }
    
    def get_knowledge(self, error_type: str) -> dict:
        """Get knowledge for a specific error type"""
        return self.error_knowledge.get(error_type, self.error_knowledge['unknown'])
    
    def search_documentation(self, error_type: str, components: dict) -> list:
        """Search for relevant documentation based on error components"""
        base_urls = {
            'apt_repository': 'https://help.ubuntu.com/community/Repositories',
            'permission_denied': 'https://wiki.ubuntu.com/Security/Privileges',
            'command_not_found': 'https://help.ubuntu.com/community/InstallingSoftware',
            'file_not_found': 'https://help.ubuntu.com/community/LinuxFilesystemTreeOverview',
            'dependency_error': 'https://help.ubuntu.com/community/AptGet/Howto',
            'network_error': 'https://help.ubuntu.com/community/InternetAndNetworking'
        }
        
        urls = []
        if error_type in base_urls:
            urls.append(base_urls[error_type])
        
        return urls