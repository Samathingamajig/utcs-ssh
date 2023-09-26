# UTCS SSH

A better way to SSH into the CS Lab machines at UT Austin.

`USERNAME` is the username of your UTCS account. If you don't provide a username, it will first check the
`UTCS_SSH_USERNAME` environment variable, otherwise use your current username.

```
Usage: utcs-ssh [OPTIONS] [USERNAME]

Options:
  --comname   Print the computer's name instead of running the ssh command
  --hostname  Print the hostname instead of running the ssh command
  --command   Print the ssh command instead of running it
  --help      Show this message and exit.
```

## Installation

```bash
pip install utcs-ssh
```
