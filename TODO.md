- [ ] **Focus Only on "Work Items"**

  - [ ] Only parse and process the "Work Items" section from the release notes (see `sample_be_release_notes.md` for examples).
  - [ ] Ignore all other sections (e.g., "Pull Requests").

- [ ] **Extract Only Required Fields**

  - [ ] For each work item line (e.g., `- [9176](...) - Create new Pagination Model...`), extract:
    - The work item ID (e.g., `9176`)
    - The title/description (e.g., `Create new Pagination Model...`)
  - [ ] Do not use the URL in the markdown link.

- [ ] **Use Differentiators for Format Selection**

  - [ ] In `format_prs_for_release.py`, add a CLI flag or parameter to specify the format/source (e.g., `--type BE` or `--type UI`).
  - [ ] Use this flag to select the correct parsing logic.

- [ ] **Leverage and Extend Existing Parser Infrastructure**

  - [ ] In `release_notes/models.py`, add a new `EntryType` (e.g., `WORK_ITEM`).
  - [ ] In `release_notes/parser.py`, add a new parsing pattern for work item lines.
  - [ ] Ensure the parser can be invoked to only process the "Work Items" section.

- [ ] **Consider a Factory/Strategy Pattern for Parser Selection**

  - [ ] Implement a factory or strategy pattern (could be a function or class in `release_notes/parser.py` or a new file) to select the appropriate parser based on the format.

- [ ] **Integrate with `format_prs_for_release.py`**

  - [ ] Update the script to accept the new parameter/flag.
  - [ ] Use the parser to extract work items from BE release notes.
  - [ ] Output the extracted work items in the desired format.

- [ ] **Testing**

  - [ ] Add or update tests in `tests/` to ensure:
    - Only "Work Items" are parsed.
    - Both the work item ID and title/description are correctly extracted.
    - The correct parser is selected based on the differentiator.
