.PHONY: help release_notes

count_tags: # Counts the number of tags created within the last number of days
	python3 count_tags.py

release_notes: # fetches most recent release, wraps AB-* issues with hyperlinks
	python3 pull_prerelease.py && python3 main.py && pbcopy < ./output.md
