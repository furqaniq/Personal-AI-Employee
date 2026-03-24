#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Bronze Tier AI Employee.

This script verifies that all components are working correctly.

Usage:
    python test_bronze_tier.py /path/to/vault
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger('TestBronzeTier')


def test_vault_structure(vault_path: Path) -> bool:
    """Test that vault has required structure."""
    logger.info("Testing vault structure...")
    
    required_folders = [
        'Inbox', 'Needs_Action', 'Done', 'Plans',
        'Pending_Approval', 'Approved', 'Rejected',
        'Logs', 'Briefings', 'Invoices', 'Accounting'
    ]
    
    required_files = ['Dashboard.md', 'Company_Handbook.md']
    
    all_ok = True
    
    for folder in required_folders:
        if (vault_path / folder).exists():
            logger.info(f"  ✓ {folder}/")
        else:
            logger.error(f"  ✗ {folder}/ - MISSING")
            all_ok = False
    
    for file in required_files:
        if (vault_path / file).exists():
            logger.info(f"  ✓ {file}")
        else:
            logger.error(f"  ✗ {file} - MISSING")
            all_ok = False
    
    return all_ok


def test_scripts() -> bool:
    """Test that required scripts exist."""
    logger.info("Testing scripts...")
    
    scripts_dir = Path(__file__).parent
    
    required_scripts = [
        'base_watcher.py',
        'filesystem_watcher.py',
        'orchestrator.py'
    ]
    
    all_ok = True
    
    for script in required_scripts:
        script_path = scripts_dir / script
        if script_path.exists():
            logger.info(f"  ✓ {script}")
        else:
            logger.error(f"  ✗ {script} - MISSING")
            all_ok = False
    
    return all_ok


def test_dependencies() -> bool:
    """Test that required Python packages are installed."""
    logger.info("Testing Python dependencies...")
    
    try:
        import watchdog
        logger.info(f"  ✓ watchdog (installed)")
        return True
    except ImportError:
        logger.error("  ✗ watchdog - NOT INSTALLED")
        logger.error("    Install with: pip install watchdog")
        return False


def test_claude_code() -> bool:
    """Test that Claude Code is available."""
    logger.info("Testing Claude Code...")
    
    import subprocess
    
    try:
        result = subprocess.run(
            ['claude', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            logger.info(f"  ✓ claude ({result.stdout.strip()})")
            return True
        else:
            logger.warning(f"  ! claude returned error code {result.returncode}")
            return False
    except FileNotFoundError:
        logger.warning("  ! claude - NOT FOUND in PATH")
        logger.warning("    Install with: npm install -g @anthropic/claude-code")
        logger.warning("    (Bronze tier can work in manual mode without Claude)")
        return False
    except subprocess.TimeoutExpired:
        logger.warning("  ! claude - TIMEOUT")
        return False


def test_sample_file(vault_path: Path) -> bool:
    """Create and test processing a sample file."""
    logger.info("Testing sample file creation...")
    
    inbox = vault_path / 'Inbox'
    inbox.mkdir(parents=True, exist_ok=True)
    
    # Create a sample test file
    sample_file = inbox / 'test_sample.txt'
    sample_content = """This is a test file for the AI Employee Bronze Tier.

Created: """ + datetime.now().isoformat() + """

Purpose: Verify that the file watcher detects new files and creates action files.

Action Required: Please process this file and move it to Done when complete.
"""
    sample_file.write_text(sample_content)
    logger.info(f"  ✓ Created sample file: {sample_file.name}")
    
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_bronze_tier.py <vault_path>")
        print("\nExample:")
        print('  python test_bronze_tier.py "C:\\Users\\...\\AI_Employee_Vault"')
        sys.exit(1)
    
    vault_path = Path(sys.argv[1])
    
    if not vault_path.exists():
        logger.error(f"Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("AI Employee - Bronze Tier Test")
    print("=" * 60)
    print()
    
    results = []
    
    results.append(("Vault Structure", test_vault_structure(vault_path)))
    print()
    
    results.append(("Scripts", test_scripts()))
    print()
    
    results.append(("Dependencies", test_dependencies()))
    print()
    
    results.append(("Claude Code", test_claude_code()))
    print()
    
    results.append(("Sample File", test_sample_file(vault_path)))
    print()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"  {status}: {name}")
    
    print()
    logger.info(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print()
        logger.info("All tests passed! Bronze Tier is ready to use.")
        print()
        print("Next steps:")
        print("  1. Start the watcher:")
        print("     python filesystem_watcher.py <vault_path>")
        print()
        print("  2. Start the orchestrator (in new terminal):")
        print("     python orchestrator.py <vault_path>")
        print()
        print("  3. Check AI_Employee_Vault/Inbox/test_sample.txt")
        print("     The watcher should detect it and create an action file.")
        print()
    else:
        print()
        logger.warning("Some tests failed. Please fix the issues above.")
        print()


if __name__ == '__main__':
    main()
