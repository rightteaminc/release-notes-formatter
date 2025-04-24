.PHONY: help release_notes test test_coverage format_notes

count_tags: # Counts the number of tags created within the last number of days
	python3 count_tags.py

release_notes: # fetches most recent release, wraps AB-* issues with hyperlinks
	python3 pull_prerelease.py && python3 main.py && pbcopy < ./output.md

test: # Run all tests
	python -m pytest -v

test_coverage: # Run tests with coverage report
	python -m pytest -v --cov=release_notes --cov-report=term-missing

format_notes: # Format release notes from a file 
	python3 pull_prerelease.py && python3 main.py && \
	python3 fetch_azure_ticket_details.py
