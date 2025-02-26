.PHONY: help release_notes

release_notes: # fetches most recent release, wraps AB-* issues with hyperlinks
	python3 pull_prerelease.py && python3 main.py && pbcopy < ./output.md
