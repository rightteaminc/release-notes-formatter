# Release Notes Formatter

## Table of Contents
- [What It Does](#what-it-does)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Clone the Repository](#1-clone-the-repository)
  - [Set Up Virtual Environment](#2-set-up-virtual-environment)
  - [GitHub CLI Setup](#3-github-cli-setup)
- [Usage](#usage)
  - [Format Release Notes](#format-release-notes)
  - [Count Tags](#count-tags)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Tests](#tests)
- [License](#licesnse)

A Python tool to format release notes by automatically converting AB ticket numbers into clickable links for Azure DevOps.

## What It Does

This utility transforms the generated release notes output from [release-drafter](https://github.com/release-drafter/release-drafter).

For example, it will take a markdown file that looks like this:

```md
## 🐛 Bug Fixes

- AB-5284-People Assignments vs Search - End Date discrepancy @kcvikander (#4245)
- AB#5258 Fix Service Offering only uses rate card default bill rate @codeBelt (#4240)
- AB#5284 Use ISO date for requests to strip time @kcvikander (#4241)
- AB-5266-fix pdp dropdown order  @pstubbs-rt (#4236)
- AB-5272 Fix Sales pipeline listing page displays $0 for all Planned Revenue @codeBelt (#4235)
- AB#5240 - Employee search assignment dates @kcvikander (#4231)
- AB-5282 Fix Tab Submit @kcvikander (#4233)
```

and format everything to something consistent like this:

```md
## 🐛 Bug Fixes

- [AB#5284](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/5284) - People Assignments vs Search - End Date discrepancy @kcvikander (#4245)
- [AB#5258](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/5258) - Fix Service Offering only uses rate card default bill rate @codeBelt (#4240)
- [AB#5284](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/5284) - Use ISO date for requests to strip time @kcvikander (#4241)
- [AB#5266](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/5266) - fix pdp dropdown order  @pstubbs-rt (#4236)
- [AB#5272](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/5272) - Fix Sales pipeline listing page displays $0 for all Planned Revenue @codeBelt (#4235)
- [AB#5240](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/5240) - Employee search assignment dates @kcvikander (#4231)
- [AB#5282](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/5282) - Fix Tab Submit @kcvikander (#4233)
```

## Prerequisites

- Python 3.x
- GitHub CLI (`gh`)
- Access to the Parallax Azure DevOps project

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd release-notes-formatter
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. GitHub CLI Setup

1. Install GitHub CLI:
   - macOS: `brew install gh`
   - Linux: Follow [GitHub CLI installation instructions](https://cli.github.com/manual/installation)
   - Windows: `winget install GitHub.cli`

2. Authenticate with GitHub:
```bash
gh auth login
```
Follow the prompts to complete authentication.

## Usage

The tool provides several commands through the Makefile:

### Format Release Notes

```bash
make release_notes
```
This will:
1. Pull the most recent release draft from GitHub
2. Format the release notes by converting AB ticket numbers to clickable links
3. Copy the formatted content to your clipboard
4. Paste output into GitHub release notes

### Count Tags

```bash
make count_tags
```
This will count the number of tags created within a specified number of days.

## Testing

The project includes comprehensive test coverage. To run the tests:

```bash
# Run all tests
python3 -m unittest discover

# Run specific test file
python3 -m unittest test_main.py
python3 -m unittest test_pull_prerelease.py
```

The test suite includes:
- Unit tests for ticket number formatting
- Unit tests for release note building
- Integration tests for the complete workflow
- Tests for GitHub release draft functionality

## Project Structure

- `main.py`: Core functionality for formatting release notes
- `pull_prerelease.py`: Handles fetching release drafts from GitHub
- `count_tags.py`: Utility for counting repository tags
- `test_main.py`: Tests for the main formatting functionality
- `test_pull_prerelease.py`: Tests for GitHub release draft functionality
- `Makefile`: Contains common commands for the project


## Tests

This project includes unit tests found in `test_main.py`. Any changes, additions, or removals in `main.py` must be accounted for in the tests. 

Tests can be run using the following command: `python -m unittest test_main.py`

## Licesnse

[MIT](LICENSE)