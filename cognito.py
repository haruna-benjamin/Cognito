#!/usr/bin/env python3
import argparse
import sys
import os
from datetime import datetime

from error_parser import ErrorParser
from explanation_generator import ExplanationGenerator
from knowledge_base import KnowledgeBase
from banner import get_ascii_logo

class Cognito:
    def __init__(self):
        self.parser = ErrorParser()
        self.generator = ExplanationGenerator()
        self.knowledge = KnowledgeBase()
        self.version = "2.0"
        self.interaction_count = 0
        
    def display_banner(self):
        print(get_ascii_logo())
        print("-" * 50)
        
    def run_interactive(self):
        self.display_banner()
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\nCognito > ").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    print("\nGoodbye!")
                    break
                elif user_input.lower() in ['help', '?']:
                    self.show_help()
                    continue
                elif not user_input:
                    continue
                    
                self.process_error(user_input)
                self.interaction_count += 1
                
            except (EOFError, KeyboardInterrupt):
                print("\nSee you next time!")
                break
    
    def process_error(self, error_message):
        try:
            print("Analyzing error...")
            
            parsed_error = self.parser.parse_error(error_message)
            explanation = self.generator.generate_explanation(parsed_error)
            
            self.display_explanation(explanation)
            
        except Exception as e:
            print(f"Error: {e}")
    
    def display_explanation(self, explanation):
        print("\n" + "="*50)
        print("COGNITO ANALYSIS")
        print("="*50)
        print(f"Type: {explanation['error_type'].replace('_', ' ').title()}")
        print(f"Severity: {explanation['severity'].upper()}")
        print(f"Summary: {explanation['summary']}")
        print(f"Cause: {explanation['likely_cause']}")
        
        print("\nSolutions:")
        for i, solution in enumerate(explanation['solutions'], 1):
            print(f"   {i}. {solution}")
        
        if explanation['prevention_tips']:
            print("\nPrevention:")
            for tip in explanation['prevention_tips']:
                print(f"   - {tip}")
        
        print(f"\nConfidence: {explanation['confidence']:.0%}")
        print("="*50)
    
    def show_help(self):
        help_text = """
Cognito Help:
  <error>   - Analyze error message
  help, ?   - Show this help
  exit      - Quit

Examples:
  "E: The repository ... does not have a Release file"
  "bash: npm: command not found"
  "Permission denied"
        """
        print(help_text)

def main():
    cognito = Cognito()
    
    parser = argparse.ArgumentParser(description='Cognito - CLI Error Assistant')
    parser.add_argument('error', nargs='?', help='Error message to analyze')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    if args.interactive:
        cognito.run_interactive()
    elif args.error:
        cognito.process_error(args.error)
    else:
        cognito.run_interactive()

if __name__ == "__main__":
    main()