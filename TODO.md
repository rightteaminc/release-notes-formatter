## Aggregate and Process Release Notes from All Output Files

- [x] **Read All Files in `raw_release_notes/`**

  - [x] List and open all output files in the `raw_release_notes` directory.
  - [x] Parse each file to extract all relevant entries (e.g., work items/ticket IDs).
  - [x] Combine all extracted ticket IDs into a single list, ensuring no duplicates.

- [x] **Update Ticket Fetching Workflow**

  - [x] Modify `fetch_azure_ticket_details.py` to accept a list of ticket IDs as input (from all files, not just one).
  - [x] Optionally, allow passing a directory path to automatically aggregate ticket IDs from all files within.
  - [x] Fetch details for all unique ticket IDs.

- [x] **CLI/Script Integration**

  - [x] Create or update an orchestrator script to:
    - Read all files in `raw_release_notes/`
    - Aggregate ticket IDs
    - Call `fetch_azure_ticket_details.py` with the full list
  - [x] Ensure the workflow is easy to run from the command line.

- [ ] **Testing**

  - [x] Test that all files in `raw_release_notes/` are read and parsed.
  - [x] Test that ticket IDs are correctly aggregated and deduplicated.
  - [x] Test that `fetch_azure_ticket_details.py` fetches details for all tickets.

- [ ] **Documentation**

  - [ ] Update README/Docs to document the new workflow and how to run the updated process.