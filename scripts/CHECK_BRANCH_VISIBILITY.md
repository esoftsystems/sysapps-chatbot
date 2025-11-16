# Check Branch Visibility

This directory contains scripts to check if a GitHub repository is public or private, and verify if specific branches exist and are accessible.

## Available Scripts

### 1. check_branch_visibility.py
Uses GitHub API to check repository visibility and branch existence. Requires internet access and may need authentication for private repositories.

### 2. check_branch_local.py
Uses local git commands to check branch existence. Works offline if the repository is already cloned and doesn't require GitHub API access.

## Quick Start

### Method 1: Using Local Git Commands (Recommended for Quick Checks)

This method works without GitHub API access and doesn't require authentication:

```bash
# Check if 'development' branch exists
python3 scripts/check_branch_local.py development

# Check if another branch exists
python3 scripts/check_branch_local.py main
```

### Method 2: Using GitHub API (For Full Repository Details)

This method provides more details about repository visibility but requires GitHub API access:

```bash
# Check repository and branch (may require GITHUB_TOKEN)
python3 scripts/check_branch_visibility.py esoftsystems/sysapps-chatbot development
```

## Overview

In GitHub, repositories are either public or private - individual branches inherit the repository's visibility. These tools help you:

1. Check if a repository is public or private
2. Verify if a specific branch exists in the repository
3. Check branch protection status (API method only)

## Usage

### Using check_branch_local.py (Git-based method)

This script uses local git commands and doesn't require GitHub API access:

```bash
# From repository root
cd /path/to/repository
python3 scripts/check_branch_local.py development
```

**Advantages:**
- No GitHub API token required
- Works with any git repository (GitHub, GitLab, etc.)
- No rate limits
- Works offline if repository is already cloned

**Limitations:**
- Doesn't show repository visibility (public/private)
- Doesn't show branch protection status
- Requires the repository to be cloned locally

### Using check_branch_visibility.py (API-based method)

#### Basic Usage

Check the 'development' branch of the current repository:
```bash
cd /path/to/repository
python3 scripts/check_branch_visibility.py
```

### Specify Repository and Branch

```bash
python3 scripts/check_branch_visibility.py esoftsystems/sysapps-chatbot development
```

### Using the Shell Script Wrapper

```bash
./scripts/check_branch_visibility.sh esoftsystems/sysapps-chatbot development
```

## Authentication

For private repositories or to avoid API rate limits, you can provide a GitHub Personal Access Token:

### Generate a GitHub Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name (e.g., "Branch Visibility Checker")
4. Select scopes: `repo` (for private repositories) or `public_repo` (for public repositories only)
5. Click "Generate token" and copy the token

### Use the Token

#### Linux/macOS:
```bash
export GITHUB_TOKEN="your_token_here"
python3 scripts/check_branch_visibility.py esoftsystems/sysapps-chatbot development
```

#### Windows (PowerShell):
```powershell
$env:GITHUB_TOKEN="your_token_here"
python scripts/check_branch_visibility.py esoftsystems/sysapps-chatbot development
```

#### Windows (Command Prompt):
```cmd
set GITHUB_TOKEN=your_token_here
python scripts/check_branch_visibility.py esoftsystems/sysapps-chatbot development
```

## Output

The script provides detailed output including:

- Repository visibility (PUBLIC or PRIVATE)
- Repository full name
- Default branch name
- Branch existence status
- Branch protection status
- Summary of findings

### Example Output

```
Checking repository: esoftsystems/sysapps-chatbot
Checking branch: development
Using GitHub token for authentication ✓
------------------------------------------------------------

🔒 Repository Visibility: PRIVATE
   Full Name: esoftsystems/sysapps-chatbot
   Default Branch: main
   Access: Authenticated

Checking if branch 'development' exists...
✅ Branch 'development' exists
   Protection Status: Not Protected

============================================================
SUMMARY:
  Repository 'esoftsystems/sysapps-chatbot' is PRIVATE
  Branch 'development' exists and is accessible
  Note: This is a private repository
============================================================
```

## Requirements

- Python 3.6 or higher
- Internet connection
- (Optional) GitHub Personal Access Token for private repositories

## Troubleshooting

### Error: "Access forbidden. API rate limit exceeded or requires authentication"

**Solution:** Set the `GITHUB_TOKEN` environment variable with a valid GitHub personal access token.

### Error: "Repository not found or is private and requires authentication"

**Solution:** The repository might be private. Set the `GITHUB_TOKEN` environment variable with a token that has access to the repository.

### Error: "Branch not found"

**Solution:** The specified branch doesn't exist in the repository. Check the branch name or list available branches with:
```bash
git ls-remote --heads origin
```

## Notes

- GitHub's API has rate limits for unauthenticated requests (60 requests per hour)
- Authenticated requests have higher limits (5,000 requests per hour)
- Repository visibility (public/private) is a repository-level setting, not a branch-level setting
- All branches in a repository share the same visibility as the repository itself
