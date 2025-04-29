"""Tests for the GitHub release notes fetcher module."""

import os
import pytest
import responses
from pull_prerelease import get_draft_releases, write_draft_to_file, fetch_and_save_latest_draft


@pytest.fixture
def mock_github_response():
    """Mock response data for GitHub API."""
    return [
        {
            "id": 1,
            "draft": True,
            "body": "# Test Release Notes\n- Feature 1\n- Feature 2"
        },
        {
            "id": 2,
            "draft": False,
            "body": "Published release"
        }
    ]


@responses.activate
def test_get_draft_releases_success(mock_github_response):
    """Test successful fetching of draft releases."""
    repo = "test/repo"
    token = "fake-token"
    url = f"https://api.github.com/repos/{repo}/releases"
    
    responses.add(
        responses.GET,
        url,
        json=mock_github_response,
        status=200
    )
    
    drafts = get_draft_releases(repo, token)
    assert len(drafts) == 1
    assert drafts[0]["draft"] is True
    assert drafts[0]["body"] == "# Test Release Notes\n- Feature 1\n- Feature 2"


@responses.activate
def test_get_draft_releases_failure():
    """Test handling of failed API requests."""
    repo = "test/repo"
    token = "fake-token"
    url = f"https://api.github.com/repos/{repo}/releases"
    
    responses.add(
        responses.GET,
        url,
        json={"message": "Not Found"},
        status=404
    )
    
    drafts = get_draft_releases(repo, token)
    assert len(drafts) == 0


def test_write_draft_to_file(tmp_path):
    """Test writing draft content to a file."""
    test_file = tmp_path / "test_output.md"
    test_content = {
        "body": "# Test Content\n- Item 1\n- Item 2"
    }
    
    write_draft_to_file(test_content, str(test_file))
    
    assert test_file.exists()
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert content == test_content["body"]


@responses.activate
def test_fetch_and_save_latest_draft_success(tmp_path, mock_github_response):
    """Test the complete flow of fetching and saving a draft."""
    repo_obj = {"repo": "test/repo", "name": "test-repo"}
    token = "fake-token"
    url = f"https://api.github.com/repos/{repo_obj['repo']}/releases"

    responses.add(
        responses.GET,
        url,
        json=mock_github_response,
        status=200
    )

    repo_dir = tmp_path / "test-repo"
    repo_dir.mkdir()

    result = fetch_and_save_latest_draft(repo_obj, token, str(tmp_path))

    input_file = tmp_path / "test-repo" / "input.md"
    assert result is True
    assert input_file.exists()
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert content == mock_github_response[0]["body"]


@responses.activate
def test_fetch_and_save_latest_draft_no_drafts(tmp_path):
    """Test handling when no draft releases are found, but a non-draft release is present."""
    repo_obj = {"repo": "test/repo", "name": "test-repo"}
    token = "fake-token"
    url = f"https://api.github.com/repos/{repo_obj['repo']}/releases"

    responses.add(
        responses.GET,
        url,
        json=[{"draft": False, "body": "Published"}],
        status=200
    )

    repo_dir = tmp_path / "test-repo"
    repo_dir.mkdir()

    result = fetch_and_save_latest_draft(repo_obj, token, str(tmp_path))

    input_file = tmp_path / "test-repo" / "input.md"
    
    assert result is True
    assert input_file.exists()
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert content == "Published" 