# Release Notes Formatter

Transforms the generated release notes output from [release-drafter](https://github.com/release-drafter/release-drafter).

This utlity will take a markdown file that looks like this:

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

## Usage

In order to use this utility, you must first clone this repository. Then: 

1. Copy the release notes you wish to format into the `input.md` doc
1. Rrom a terminal, run `python3 main.py`
1. Observe the formatted results in `output.md`

## Using the pull_commits_for_release.py script

This script is used to pull commits for a release. It takes a release number as an argument and outputs a list of commits associated with that release.

### Instructions for use:
1. From a terminal, run `python3 pull_commits_for_release.py <release_number>` where `<release_number>` is the number of the release you want to pull commits for.
2. The script will output a list of commits associated with the specified release.
3. Before running the script, ensure you have Python 3 installed and are in the root directory of the repository.

## Tests

This project includes unit tests found in `test_main.py`. Any changes, additions, or removals in `main.py` must be accounted for in the tests. 

Tests can be run using the following command: `python -m unittest test_main.py`

## Licesnse

[MIT](LICENSE)