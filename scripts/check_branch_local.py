#!/usr/bin/env python3
"""
Alternative script to check branch existence using local git commands.

This script uses git commands to check if a branch exists locally or remotely,
without requiring GitHub API access.

Usage:
    python check_branch_local.py [branch]
    
    branch: Branch name to check (default: 'development')

Example:
    python check_branch_local.py development
"""

import sys
import subprocess


def run_command(cmd):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip(), True
    except subprocess.CalledProcessError as e:
        return e.stderr.strip(), False


def get_remote_url():
    """Get the remote URL of the current repository."""
    url, success = run_command(['git', 'config', '--get', 'remote.origin.url'])
    if success:
        return url
    return None


def check_branch_local(branch):
    """Check if branch exists locally."""
    output, success = run_command(['git', 'branch', '--list', branch])
    return bool(output.strip())


def check_branch_remote(branch):
    """Check if branch exists on remote."""
    output, success = run_command(['git', 'ls-remote', '--heads', 'origin', branch])
    return bool(output.strip())


def get_all_remote_branches():
    """Get list of all remote branches."""
    output, success = run_command(['git', 'ls-remote', '--heads', 'origin'])
    if success and output:
        branches = []
        for line in output.split('\n'):
            if line.strip():
                # Format: <hash> refs/heads/<branch>
                parts = line.split('refs/heads/')
                if len(parts) == 2:
                    branches.append(parts[1])
        return branches
    return []


def main():
    """Main function to check branch existence."""
    # Parse command line arguments
    if len(sys.argv) > 1:
        branch = sys.argv[1]
    else:
        branch = 'development'
    
    print(f"Checking branch: {branch}")
    print("=" * 60)
    
    # Get remote URL
    remote_url = get_remote_url()
    if remote_url:
        print(f"Repository: {remote_url}")
    else:
        print("Warning: Could not determine remote URL")
    
    print()
    
    # Check if branch exists locally
    exists_local = check_branch_local(branch)
    if exists_local:
        print(f"✅ Branch '{branch}' exists locally")
    else:
        print(f"❌ Branch '{branch}' does not exist locally")
    
    # Check if branch exists on remote
    print(f"\nChecking remote repository...")
    exists_remote = check_branch_remote(branch)
    if exists_remote:
        print(f"✅ Branch '{branch}' exists on remote")
    else:
        print(f"❌ Branch '{branch}' does not exist on remote")
        
        # List available remote branches
        print(f"\nAvailable remote branches:")
        remote_branches = get_all_remote_branches()
        if remote_branches:
            for rb in remote_branches[:10]:  # Show first 10
                print(f"  - {rb}")
            if len(remote_branches) > 10:
                print(f"  ... and {len(remote_branches) - 10} more")
        else:
            print("  (none found)")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    if exists_remote:
        print(f"  Branch '{branch}' is accessible on the remote repository")
        if exists_local:
            print(f"  Branch '{branch}' is also available locally")
        else:
            print(f"  Branch '{branch}' is not checked out locally")
            print(f"  You can check it out with: git checkout {branch}")
    else:
        print(f"  Branch '{branch}' does not exist on the remote repository")
    print("=" * 60)
    
    # Exit with appropriate code
    sys.exit(0 if exists_remote else 1)


if __name__ == "__main__":
    main()
