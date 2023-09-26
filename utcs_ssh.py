from bs4 import BeautifulSoup, PageElement
import requests
import click
from dataclasses import dataclass
import random
import getpass

LAB_STATUS_URL = "https://apps.cs.utexas.edu/unixlabstatus/"
HOST_TEMPLATE = "{}.cs.utexas.edu"
SSH_COMMAND_TEMPLATE = "ssh {}@{}"


@dataclass
class Machine:
    host: str
    active: bool
    num_users: int
    high_avg_load: bool

    def __init__(self, raw_row_data: PageElement):
        cols = raw_row_data.find_all_next('td')
        self.host = cols[0].text
        self.active = cols[1].text == "up"
        self.num_users = int(cols[3].text) if self.active else 0
        self.high_avg_load = "yellow" in cols[1]["style"]


def get_all_machines() -> list[Machine]:
    html_doc = requests.get(LAB_STATUS_URL).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.find('table')
    machines_raw = table.find_all('tr')[3:]
    machines = [Machine(machine_raw) for machine_raw in machines_raw]
    return machines


def main():
    machines = get_all_machines()
    online_machines = [machine for machine in machines if machine.active]
    lowest_user_count = min(machine.num_users for machine in online_machines)
    lowest_user_count_machines = [machine for machine in online_machines if machine.num_users == lowest_user_count]
    valid_machines = lowest_user_count_machines
    if any(not machine.high_avg_load for machine in lowest_user_count_machines):
        valid_machines = [machine for machine in lowest_user_count_machines if not machine.high_avg_load]
    machine = random.choice(valid_machines)
    print(machine.host)


if __name__ == "__main__":
    main()
