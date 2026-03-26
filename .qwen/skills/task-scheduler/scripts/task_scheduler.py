#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Task Scheduler - Windows Task Scheduler integration for AI Employee.

Silver Tier implementation for AI Employee Hackathon.

Usage:
    python task_scheduler.py create --name "GmailWatcher" --script "gmail_watcher.py"
    python task_scheduler.py install-all --vault "C:\path\to\vault"
    python task_scheduler.py list
    python task_scheduler.py remove --name "GmailWatcher"
"""

import os
import sys
import subprocess
import logging
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Task definitions for AI Employee
TASK_DEFINITIONS = {
    'GmailWatcher': {
        'script': 'gmail_watcher.py',
        'skill': 'gmail-watcher',
        'description': 'Monitor Gmail for new emails and create action files',
        'trigger': 'atlogon',
        'requires_credentials': True,
        'restart_on_failure': True,
        'execution_time_limit': 'PT24H'
    },
    'LinkedInWatcher': {
        'script': 'linkedin_watcher.py',
        'skill': 'linkedin-watcher',
        'description': 'Monitor LinkedIn for notifications and messages',
        'trigger': 'atlogon',
        'requires_credentials': False,
        'restart_on_failure': True,
        'execution_time_limit': 'PT24H'
    },
    'Orchestrator': {
        'script': 'orchestrator.py',
        'skill': None,  # Root scripts folder
        'description': 'Main orchestrator for AI Employee - processes pending items',
        'trigger': 'atlogon',
        'requires_credentials': False,
        'restart_on_failure': True,
        'execution_time_limit': 'PT24H'
    },
    'FileSystemWatcher': {
        'script': 'filesystem_watcher.py',
        'skill': None,
        'description': 'Monitor file system drop folder for new files',
        'trigger': 'atlogon',
        'requires_credentials': False,
        'restart_on_failure': True,
        'execution_time_limit': 'PT24H'
    },
    'DailyBriefing': {
        'script': 'daily_briefing.py',
        'skill': None,
        'description': 'Generate daily briefing report at 8 AM',
        'trigger': 'daily_8am',
        'requires_credentials': False,
        'restart_on_failure': True,
        'execution_time_limit': 'PT1H'
    }
}


class TaskScheduler:
    """
    Windows Task Scheduler integration for AI Employee.
    """

    def __init__(self, vault_path: str = None, credentials_path: str = None):
        """
        Initialize Task Scheduler.
        
        Args:
            vault_path: Path to Obsidian vault
            credentials_path: Path to Gmail credentials (if needed)
        """
        self.vault_path = Path(vault_path) if vault_path else None
        self.credentials_path = Path(credentials_path) if credentials_path else None
        self.logger = logging.getLogger('TaskScheduler')
        
        # Get Python executable path
        self.python_exe = sys.executable
        
        # Get project root
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.scripts_root = self.project_root / 'scripts'
        self.skills_root = self.project_root / '.qwen' / 'skills'

    def get_script_path(self, script_name: str, skill: str = None) -> Path:
        """Get full path to script."""
        if skill:
            return self.skills_root / skill / 'scripts' / script_name
        return self.scripts_root / script_name

    def build_command(self, task_name: str) -> List[str]:
        """Build command line for task."""
        task_def = TASK_DEFINITIONS.get(task_name)
        if not task_def:
            raise ValueError(f'Unknown task: {task_name}')
        
        script_path = self.get_script_path(task_def['script'], task_def['skill'])
        
        cmd = [self.python_exe, str(script_path)]
        
        # Add vault path
        if self.vault_path:
            cmd.append(str(self.vault_path))
        
        # Add credentials if required
        if task_def['requires_credentials'] and self.credentials_path:
            cmd.append(str(self.credentials_path))
        
        return cmd

    def create_task(self, task_name: str, trigger: str = 'atlogon',
                   run_as_user: bool = True) -> bool:
        """
        Create a scheduled task.
        
        Args:
            task_name: Name of the task (from TASK_DEFINITIONS)
            trigger: Trigger type (atlogon, atstartup, daily, etc.)
            run_as_user: Run as current user (vs SYSTEM)
            
        Returns:
            True if successful
        """
        task_def = TASK_DEFINITIONS.get(task_name)
        if not task_def:
            self.logger.error(f'Unknown task: {task_name}')
            return False
        
        # Build command
        cmd = self.build_command(task_name)
        cmd_str = ' '.join(f'"{c}"' for c in cmd)
        
        # Build schtasks command
        schtasks_cmd = ['schtasks', '/Create']
        schtasks_cmd.extend(['/TN', f'AI_Employee\\{task_name}'])
        schtasks_cmd.extend(['/TR', cmd_str])
        
        # Trigger
        if trigger == 'atlogon':
            schtasks_cmd.extend(['/SC', 'ONLOGON'])
        elif trigger == 'atstartup':
            schtasks_cmd.extend(['/SC', 'ONSTART'])
        elif trigger == 'daily':
            schtasks_cmd.extend(['/SC', 'DAILY', '/ST', '08:00'])
        elif trigger == 'daily_8am':
            schtasks_cmd.extend(['/SC', 'DAILY', '/ST', '08:00'])
        elif trigger == 'weekly':
            schtasks_cmd.extend(['/SC', 'WEEKLY', '/D', 'MON', '/ST', '09:00'])
        
        # Run as user
        if run_as_user:
            schtasks_cmd.extend(['/RL', 'HIGHEST'])
            schtasks_cmd.extend(['/RU', os.environ.get('USERNAME')])
        else:
            schtasks_cmd.extend(['/RU', 'SYSTEM'])
        
        # Additional settings
        schtasks_cmd.extend(['/F'])  # Force create
        
        # Execute
        try:
            self.logger.info(f'Creating task: {task_name}')
            self.logger.info(f'Command: {" ".join(schtasks_cmd)}')
            
            result = subprocess.run(
                schtasks_cmd,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info(f'Task created successfully: {task_name}')
                return True
            else:
                self.logger.error(f'Failed to create task: {result.stderr}')
                return False
                
        except Exception as e:
            self.logger.error(f'Error creating task: {e}')
            return False

    def remove_task(self, task_name: str) -> bool:
        """
        Remove a scheduled task.
        
        Args:
            task_name: Name of the task
            
        Returns:
            True if successful
        """
        try:
            self.logger.info(f'Removing task: {task_name}')
            
            result = subprocess.run(
                ['schtasks', '/Delete', '/TN', f'AI_Employee\\{task_name}', '/F'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info(f'Task removed successfully: {task_name}')
                return True
            else:
                self.logger.error(f'Failed to remove task: {result.stderr}')
                return False
                
        except Exception as e:
            self.logger.error(f'Error removing task: {e}')
            return False

    def list_tasks(self) -> List[Dict]:
        """
        List all AI Employee tasks.
        
        Returns:
            List of task information dictionaries
        """
        tasks = []
        
        try:
            # Query all tasks in AI_Employee folder
            result = subprocess.run(
                ['schtasks', '/Query', '/FO', 'CSV', '/V'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                
                # Skip header
                for line in lines[1:]:
                    if 'AI_Employee' in line:
                        parts = line.split(',')
                        if len(parts) >= 9:
                            tasks.append({
                                'name': parts[0].replace('AI_Employee\\', ''),
                                'status': parts[1],
                                'last_run': parts[7],
                                'next_run': parts[8]
                            })
            
        except Exception as e:
            self.logger.error(f'Error listing tasks: {e}')
        
        return tasks

    def get_task_status(self, task_name: str) -> Dict:
        """
        Get status of a specific task.
        
        Args:
            task_name: Name of the task
            
        Returns:
            Task status dictionary
        """
        try:
            result = subprocess.run(
                ['schtasks', '/Query', '/TN', f'AI_Employee\\{task_name}', '/FO', 'CSV', '/V'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    parts = lines[1].split(',')
                    return {
                        'name': task_name,
                        'status': parts[1] if len(parts) > 1 else 'Unknown',
                        'last_run': parts[7] if len(parts) > 7 else 'N/A',
                        'next_run': parts[8] if len(parts) > 8 else 'N/A',
                        'last_result': parts[9] if len(parts) > 9 else 'N/A'
                    }
            
            return {'name': task_name, 'status': 'Not Found'}
            
        except Exception as e:
            self.logger.error(f'Error getting task status: {e}')
            return {'name': task_name, 'status': 'Error'}

    def run_task(self, task_name: str) -> bool:
        """
        Manually run a task.
        
        Args:
            task_name: Name of the task
            
        Returns:
            True if successful
        """
        try:
            self.logger.info(f'Running task: {task_name}')
            
            result = subprocess.run(
                ['schtasks', '/Run', '/TN', f'AI_Employee\\{task_name}'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info(f'Task started: {task_name}')
                return True
            else:
                self.logger.error(f'Failed to run task: {result.stderr}')
                return False
                
        except Exception as e:
            self.logger.error(f'Error running task: {e}')
            return False

    def install_all(self) -> Dict:
        """
        Install all AI Employee tasks.
        
        Returns:
            Dictionary with installation results
        """
        results = {
            'success': [],
            'failed': [],
            'total': len(TASK_DEFINITIONS)
        }
        
        for task_name, task_def in TASK_DEFINITIONS.items():
            trigger = task_def.get('trigger', 'atlogon')
            
            # Override trigger for DailyBriefing
            if task_name == 'DailyBriefing':
                trigger = 'daily_8am'
            
            success = self.create_task(task_name, trigger)
            
            if success:
                results['success'].append(task_name)
            else:
                results['failed'].append(task_name)
        
        return results

    def remove_all(self) -> Dict:
        """
        Remove all AI Employee tasks.
        
        Returns:
            Dictionary with removal results
        """
        results = {
            'success': [],
            'failed': [],
            'total': 0
        }
        
        # Get existing tasks
        existing_tasks = self.list_tasks()
        results['total'] = len(existing_tasks)
        
        for task in existing_tasks:
            task_name = task['name']
            success = self.remove_task(task_name)
            
            if success:
                results['success'].append(task_name)
            else:
                results['failed'].append(task_name)
        
        return results

    def export_task(self, task_name: str, output_file: str) -> bool:
        """
        Export task to XML file.
        
        Args:
            task_name: Name of the task
            output_file: Output XML file path
            
        Returns:
            True if successful
        """
        try:
            self.logger.info(f'Exporting task: {task_name}')
            
            result = subprocess.run(
                ['schtasks', '/Query', '/TN', f'AI_Employee\\{task_name}', '/XML', output_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info(f'Task exported: {output_file}')
                return True
            else:
                self.logger.error(f'Failed to export task: {result.stderr}')
                return False
                
        except Exception as e:
            self.logger.error(f'Error exporting task: {e}')
            return False

    def import_task(self, xml_file: str) -> bool:
        """
        Import task from XML file.
        
        Args:
            xml_file: XML file path
            
        Returns:
            True if successful
        """
        try:
            self.logger.info(f'Importing task from: {xml_file}')
            
            result = subprocess.run(
                ['schtasks', '/Create', '/XML', xml_file, '/F'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.logger.info('Task imported successfully')
                return True
            else:
                self.logger.error(f'Failed to import task: {result.stderr}')
                return False
                
        except Exception as e:
            self.logger.error(f'Error importing task: {e}')
            return False


def main():
    parser = argparse.ArgumentParser(description='Task Scheduler - AI Employee Silver Tier')
    parser.add_argument('action',
                       choices=['create', 'remove', 'list', 'status', 'run',
                               'install-all', 'remove-all', 'export', 'import'],
                       help='Action to perform')
    parser.add_argument('--name', help='Task name')
    parser.add_argument('--script', help='Script name (for create)')
    parser.add_argument('--skill', help='Skill folder (for create)')
    parser.add_argument('--trigger', default='atlogon',
                       choices=['atlogon', 'atstartup', 'daily', 'daily_8am', 'weekly'],
                       help='Trigger type')
    parser.add_argument('--vault', help='Path to Obsidian vault')
    parser.add_argument('--credentials', help='Path to credentials file')
    parser.add_argument('--output', help='Output file (for export)')
    parser.add_argument('--file', help='Input XML file (for import)')
    
    args = parser.parse_args()
    
    scheduler = TaskScheduler(
        vault_path=args.vault,
        credentials_path=args.credentials
    )
    
    if args.action == 'create':
        if not args.name:
            parser.error("--name is required for create")
        
        # Add task to definitions if custom
        if args.script and args.name not in TASK_DEFINITIONS:
            TASK_DEFINITIONS[args.name] = {
                'script': args.script,
                'skill': args.skill,
                'description': f'Custom task: {args.name}',
                'trigger': args.trigger,
                'requires_credentials': False,
                'restart_on_failure': True,
                'execution_time_limit': 'PT24H'
            }
        
        success = scheduler.create_task(args.name, args.trigger)
        sys.exit(0 if success else 1)
    
    elif args.action == 'remove':
        if not args.name:
            parser.error("--name is required for remove")
        
        success = scheduler.remove_task(args.name)
        sys.exit(0 if success else 1)
    
    elif args.action == 'list':
        tasks = scheduler.list_tasks()
        
        print("=" * 60)
        print("AI Employee Scheduled Tasks")
        print("=" * 60)
        
        if not tasks:
            print("\nNo AI Employee tasks found.")
            print("\nTo install all tasks, run:")
            print("  python task_scheduler.py install-all --vault \"C:\\path\\to\\vault\"")
        else:
            print(f"\nFound {len(tasks)} task(s):\n")
            for task in tasks:
                status_icon = '✅' if task['status'] == 'Ready' else '⚠️'
                print(f"{status_icon} {task['name']}")
                print(f"   Status: {task['status']}")
                print(f"   Last Run: {task['last_run']}")
                print(f"   Next Run: {task['next_run']}")
                print()
    
    elif args.action == 'status':
        if not args.name:
            parser.error("--name is required for status")
        
        status = scheduler.get_task_status(args.name)
        
        print("=" * 60)
        print(f"Task Status: {status.get('name', 'Unknown')}")
        print("=" * 60)
        print(f"Status: {status.get('status', 'Unknown')}")
        print(f"Last Run: {status.get('last_run', 'N/A')}")
        print(f"Next Run: {status.get('next_run', 'N/A')}")
        print(f"Last Result: {status.get('last_result', 'N/A')}")
    
    elif args.action == 'run':
        if not args.name:
            parser.error("--name is required for run")
        
        success = scheduler.run_task(args.name)
        print(f"Task {'started' if success else 'failed to start'}: {args.name}")
        sys.exit(0 if success else 1)
    
    elif args.action == 'install-all':
        if not args.vault:
            parser.error("--vault is required for install-all")
        
        print("Installing all AI Employee tasks...")
        results = scheduler.install_all()
        
        print("\n" + "=" * 60)
        print("Installation Results")
        print("=" * 60)
        print(f"Total: {results['total']}")
        print(f"Success: {len(results['success'])}")
        print(f"Failed: {len(results['failed'])}")
        
        if results['success']:
            print("\n✅ Successful:")
            for task in results['success']:
                print(f"  - {task}")
        
        if results['failed']:
            print("\n❌ Failed:")
            for task in results['failed']:
                print(f"  - {task}")
    
    elif args.action == 'remove-all':
        print("Removing all AI Employee tasks...")
        results = scheduler.remove_all()
        
        print("\n" + "=" * 60)
        print("Removal Results")
        print("=" * 60)
        print(f"Total: {results['total']}")
        print(f"Success: {len(results['success'])}")
        print(f"Failed: {len(results['failed'])}")
    
    elif args.action == 'export':
        if not args.name or not args.output:
            parser.error("--name and --output are required for export")
        
        success = scheduler.export_task(args.name, args.output)
        print(f"Task {'exported' if success else 'failed to export'}: {args.output}")
        sys.exit(0 if success else 1)
    
    elif args.action == 'import':
        if not args.file:
            parser.error("--file is required for import")
        
        success = scheduler.import_task(args.file)
        print(f"Task {'imported' if success else 'failed to import'}")
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
