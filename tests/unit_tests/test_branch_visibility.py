"""
Unit tests for the check_branch_local.py script.
"""
import subprocess
import sys
import os
import pytest

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../scripts'))


def test_check_branch_local_script_exists():
    """Test that the check_branch_local.py script exists and is executable."""
    script_path = os.path.join(os.path.dirname(__file__), '../../scripts/check_branch_local.py')
    assert os.path.exists(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"


def test_check_branch_local_help():
    """Test that the script can be executed and provides help."""
    script_path = os.path.join(os.path.dirname(__file__), '../../scripts/check_branch_local.py')
    
    # Run script with --help should not fail
    # Note: The script doesn't have --help, but we can test if it runs
    result = subprocess.run(
        [sys.executable, script_path, 'main'],
        capture_output=True,
        text=True
    )
    
    # Should execute without crashing
    assert result.returncode in [0, 1], "Script should exit with 0 (found) or 1 (not found)"
    assert "Checking branch:" in result.stdout, "Script should print 'Checking branch:'"


def test_check_branch_local_with_valid_branch():
    """Test checking a branch that likely exists (main or development)."""
    script_path = os.path.join(os.path.dirname(__file__), '../../scripts/check_branch_local.py')
    
    # Try to find main or master branch
    for branch in ['main', 'master', 'development']:
        result = subprocess.run(
            [sys.executable, script_path, branch],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # Found a valid branch
            assert "SUMMARY:" in result.stdout
            assert "accessible on the remote repository" in result.stdout
            break
    else:
        pytest.skip("No common branches found (main, master, or development)")


def test_check_branch_local_with_invalid_branch():
    """Test checking a branch that doesn't exist."""
    script_path = os.path.join(os.path.dirname(__file__), '../../scripts/check_branch_local.py')
    
    # Use a branch name that definitely doesn't exist
    result = subprocess.run(
        [sys.executable, script_path, 'this-branch-definitely-does-not-exist-12345'],
        capture_output=True,
        text=True
    )
    
    # Should exit with code 1 (not found)
    assert result.returncode == 1, "Script should exit with code 1 for non-existent branch"
    assert "does not exist on the remote repository" in result.stdout


def test_check_branch_visibility_script_exists():
    """Test that the check_branch_visibility.py script exists."""
    script_path = os.path.join(os.path.dirname(__file__), '../../scripts/check_branch_visibility.py')
    assert os.path.exists(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"


def test_check_branch_visibility_shell_script_exists():
    """Test that the shell script wrapper exists."""
    script_path = os.path.join(os.path.dirname(__file__), '../../scripts/check_branch_visibility.sh')
    assert os.path.exists(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"


def test_documentation_exists():
    """Test that the documentation file exists."""
    doc_path = os.path.join(os.path.dirname(__file__), '../../scripts/CHECK_BRANCH_VISIBILITY.md')
    assert os.path.exists(doc_path), f"Documentation not found at {doc_path}"
    
    # Check that it contains essential sections
    with open(doc_path, 'r') as f:
        content = f.read()
        assert "# Check Branch Visibility" in content
        assert "check_branch_local.py" in content
        assert "check_branch_visibility.py" in content
        assert "Usage" in content
