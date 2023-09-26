from bs4 import BeautifulSoup, PageElement
import requests
import click
from dataclasses import dataclass
import random
import getpass
import os

UTCS_SSH_USERNAME_ENV_KEY = "UTCS_SSH_USERNAME"
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


def filter_machines(machines: list[Machine]) -> list[Machine]:
    online_machines = [machine for machine in machines if machine.active]

    lowest_user_count = min(machine.num_users for machine in online_machines)
    lowest_user_count_machines = [machine for machine in online_machines if machine.num_users == lowest_user_count]

    valid_machines = lowest_user_count_machines
    if any(not machine.high_avg_load for machine in lowest_user_count_machines):
        valid_machines = [machine for machine in lowest_user_count_machines if not machine.high_avg_load]

    return valid_machines


@click.command()
@click.argument("username", required=False)
@click.option("--comname", is_flag=True, help="Print the computer's name instead of running the ssh command",
              default=False)
@click.option("--hostname", is_flag=True, help="Print the hostname instead of running the ssh command", default=False)
@click.option("--command", is_flag=True, help="Print the ssh command instead of running it", default=False)
def cli(username: str, comname: bool, hostname: bool, command: bool):
    if (comname + hostname + command) > 1:
        raise click.ClickException("Cannot specify more than one --comname, --hostname, --command")

    if not username:
        if UTCS_SSH_USERNAME_ENV_KEY in os.environ:
            username = os.environ[UTCS_SSH_USERNAME_ENV_KEY]
        else:
            username = getpass.getuser()

    machines = get_all_machines()
    valid_machines = filter_machines(machines)

    if not valid_machines:
        raise click.ClickException("No valid machines found")

    machine = random.choice(valid_machines)

    if comname:
        click.echo(machine.host)
        return

    if hostname:
        click.echo(HOST_TEMPLATE.format(machine.host))
        return

    if command:
        click.echo(SSH_COMMAND_TEMPLATE.format(username, HOST_TEMPLATE.format(machine.host)))
        return

    os.system(SSH_COMMAND_TEMPLATE.format(username, HOST_TEMPLATE.format(machine.host)))


if __name__ == "__main__":
    cli()
