#!/usr/bin/env python3
"""
Script to check if a repository and its branches are public or private.

This script uses the GitHub API to check the visibility status of a repository
and verify if a specific branch exists and is accessible.

Usage:
    python check_branch_visibility.py [repository] [branch]
    
    repository: GitHub repository in format 'owner/repo' (default: current git repo)
    branch: Branch name to check (default: 'development')

Environment Variables:
    GITHUB_TOKEN: Optional GitHub personal access token for accessing private repositories

Example:
    python check_branch_visibility.py esoftsystems/sysapps-chatbot development
    GITHUB_TOKEN=your_token python check_branch_visibility.py esoftsystems/sysapps-chatbot development
"""

import sys
import subprocess
import json
import urllib.request
import urllib.error
import os


def get_current_repo():
    """Get the current repository from git remote."""
    try:
        result = subprocess.run(
            ['git', 'config', '--get', 'remote.origin.url'],
            capture_output=True,
            text=True,
            check=True
        )
        remote_url = result.stdout.strip()
        
        # Parse GitHub URL to get owner/repo
        # Handle both HTTPS and SSH URLs
        # Only accept URLs that properly start with GitHub patterns
        if remote_url.startswith('https://github.com/') or remote_url.startswith('http://github.com/'):
            # HTTPS: https://github.com/owner/repo
            # Remove .git suffix if present
            remote_url = remote_url.rstrip('.git')
            parts = remote_url.split('github.com/')
            if len(parts) == 2:
                return parts[1]
        elif remote_url.startswith('git@github.com:'):
            # SSH: git@github.com:owner/repo
            # Remove .git suffix if present
            remote_url = remote_url.rstrip('.git')
            parts = remote_url.split('github.com:')
            if len(parts) == 2:
                return parts[1]
        
        return None
    except subprocess.CalledProcessError:
        return None


def check_repository_visibility(repo):
    """
    Check if a GitHub repository is public or private.
    
    Args:
        repo: Repository in format 'owner/repo'
        
    Returns:
        dict: Dictionary containing visibility status and repository info
    """
    api_url = f"https://api.github.com/repos/{repo}"
    
    try:
        req = urllib.request.Request(api_url)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        req.add_header('User-Agent', 'Branch-Visibility-Checker')
        
        # Add authentication token if available
        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token:
            req.add_header('Authorization', f'token {github_token}')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            return {
                'success': True,
                'private': data.get('private', False),
                'visibility': 'private' if data.get('private', False) else 'public',
                'full_name': data.get('full_name', repo),
                'default_branch': data.get('default_branch', 'main'),
                'authenticated': bool(github_token)
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {
                'success': False,
                'error': 'Repository not found or is private and requires authentication',
                'hint': 'If this is a private repository, set GITHUB_TOKEN environment variable',
                'code': 404
            }
        elif e.code == 403:
            return {
                'success': False,
                'error': 'Access forbidden. API rate limit exceeded or requires authentication',
                'hint': 'Set GITHUB_TOKEN environment variable for authenticated requests',
                'code': 403
            }
        else:
            return {
                'success': False,
                'error': f'HTTP Error {e.code}: {e.reason}',
                'code': e.code
            }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error: {str(e)}'
        }


def check_branch_exists(repo, branch):
    """
    Check if a specific branch exists in the repository.
    
    Args:
        repo: Repository in format 'owner/repo'
        branch: Branch name to check
        
    Returns:
        dict: Dictionary containing branch existence status
    """
    api_url = f"https://api.github.com/repos/{repo}/branches/{branch}"
    
    try:
        req = urllib.request.Request(api_url)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        req.add_header('User-Agent', 'Branch-Visibility-Checker')
        
        # Add authentication token if available
        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token:
            req.add_header('Authorization', f'token {github_token}')
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
            return {
                'success': True,
                'exists': True,
                'name': data.get('name', branch),
                'protected': data.get('protected', False)
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {
                'success': True,
                'exists': False,
                'error': 'Branch not found'
            }
        else:
            return {
                'success': False,
                'error': f'HTTP Error {e.code}: {e.reason}',
                'code': e.code
            }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error: {str(e)}'
        }


def main():
    """Main function to check repository and branch visibility."""
    # Parse command line arguments
    if len(sys.argv) > 1:
        repo = sys.argv[1]
    else:
        repo = get_current_repo()
        if not repo:
            print("Error: Could not determine repository from git remote.")
            print("Please provide repository as: owner/repo")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        branch = sys.argv[2]
    else:
        branch = 'development'
    
    print(f"Checking repository: {repo}")
    print(f"Checking branch: {branch}")
    
    # Check if authenticated
    if os.environ.get('GITHUB_TOKEN'):
        print("Using GitHub token for authentication ✓")
    else:
        print("No GitHub token provided (unauthenticated request)")
        print("Tip: Set GITHUB_TOKEN environment variable for private repositories")
    
    print("-" * 60)
    
    # Check repository visibility
    repo_info = check_repository_visibility(repo)
    
    if not repo_info['success']:
        print(f"❌ Failed to check repository: {repo_info['error']}")
        if 'hint' in repo_info:
            print(f"💡 Hint: {repo_info['hint']}")
        sys.exit(1)
    
    # Print repository visibility
    visibility = repo_info['visibility'].upper()
    icon = "🔒" if repo_info['private'] else "🌐"
    print(f"\n{icon} Repository Visibility: {visibility}")
    print(f"   Full Name: {repo_info['full_name']}")
    print(f"   Default Branch: {repo_info['default_branch']}")
    if repo_info.get('authenticated'):
        print(f"   Access: Authenticated")
    
    # Check branch existence
    print(f"\nChecking if branch '{branch}' exists...")
    branch_info = check_branch_exists(repo, branch)
    
    if not branch_info['success']:
        print(f"❌ Failed to check branch: {branch_info['error']}")
        sys.exit(1)
    
    if branch_info['exists']:
        protected_status = "Protected" if branch_info.get('protected', False) else "Not Protected"
        print(f"✅ Branch '{branch}' exists")
        print(f"   Protection Status: {protected_status}")
    else:
        print(f"❌ Branch '{branch}' does not exist")
        sys.exit(1)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  Repository '{repo}' is {visibility}")
    print(f"  Branch '{branch}' exists and is accessible")
    if repo_info['private']:
        print(f"  Note: This is a private repository")
    print("=" * 60)


if __name__ == "__main__":
    main()
