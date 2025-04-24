"""
Test fixtures for release notes parser tests.

This module contains pytest fixtures used across multiple test modules.
"""

import pytest

@pytest.fixture
def sample_azure_ticket_entry():
    return "- [AB#1234](https://dev.azure.com/...) - Fix login issue @user (#5678)"

@pytest.fixture
def sample_dependency_entry():
    return "- Update all non-major dependencies @[renovate[bot]](...) (#5678)"

@pytest.fixture
def sample_custom_entry():
    return "- dependencies/upgrade-0417 @user (#5678)" 