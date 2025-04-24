import requests
import os
import re
import yaml
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

organization = os.environ["AZURE_ORG"]
project = os.environ["AZURE_PROJECT"]
pat = os.environ["AZURE_PAT"]


def extract_ticket_ids_from_markdown(filepath: str) -> list[int]:
    ticket_ids = set()

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"- \[AB#(\d+)\]\(.*?\)", line)
            if match:
                ticket_id = int(match.group(1))
                ticket_ids.add(ticket_id)

    return sorted(ticket_ids)


def fetch_work_item(work_item_id: str):
    # TODO: skip if there is not work item ID
    url = f"https://dev.azure.com/{organization}/_apis/wit/workitems/{work_item_id}?api-version=7.0"
    response = requests.get(url, auth=HTTPBasicAuth('', pat))

    if response.status_code != 200:
        print(f"Error fetching work item: {response.status_code}")
        print(response.text)
        exit(1)

    data = response.json()
    title = data['fields'].get('System.Title')
    raw_description = data['fields'].get('System.Description')
    soup = BeautifulSoup(raw_description or "", 'html.parser')
    clean_description = soup.get_text(separator="\n").strip()

    return {
        "id": work_item_id,
        "title": title,
        "description": clean_description
    }


def fetch_work_item_list(work_item_ids: list[str]):
    print(f"=== {work_item_ids}")

    all_tickets = []

    for work_item_id in work_item_ids:
        print(f"Fetching work item {work_item_id}...")

        ticket = fetch_work_item(str(work_item_id))
        all_tickets.append(ticket)

    return all_tickets


if __name__ == "__main__":
    output_filename = "tickets.yml"
    work_item_ids = extract_ticket_ids_from_markdown("output.md")
    all_tickets = fetch_work_item_list(work_item_ids)
    
    with open(output_filename, "w", encoding="utf-8") as f:
        yaml.dump(all_tickets, f, sort_keys=False, allow_unicode=True)

    print(f"{len(all_tickets)} items written to {output_filename}")

