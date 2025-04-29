.PHONY: help release_notes release_notes_ui test test_coverage format_notes setup release_notes_be

setup: # Install package in development mode with test dependencies
	pip install -e ".[test]"

count_tags: # Counts the number of tags created within the last number of days
	python3 count_tags.py

release_notes: # fetches most recent release, wraps AB-* issues with hyperlinks
	python3 pull_prerelease.py && python3 pull_and_format_github_release_notes.py 

release_notes_ui: release_notes # fetches most recent release, wraps AB-* issues with hyperlinks for UI repo
	pbcopy < ./raw_release_notes/parallax-ui/output.md

release_notes_be: release_notes # fetches most recent release, wraps AB-* issues with hyperlinks for BE repo
	pbcopy < ./raw_release_notes/parallax-server/output.md

test: setup # Run all tests
	python -m pytest -v

test_coverage: setup # Run tests with coverage report
	python -m pytest -v --cov=release_notes --cov-report=term-missing

format_notes: # Format release notes from a file 
	python3 pull_prerelease.py && python3 pull_and_format_github_release_notes.py && \
	python3 fetch_azure_ticket_details.py
