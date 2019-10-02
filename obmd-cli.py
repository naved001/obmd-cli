import click
import os
import requests
import json

OBMD_ENDPOINT = os.environ.get("OBMD_ENDPOINT") + "/node/"
OBMD_ADMIN_TOKEN = os.environ.get("OBMD_ADMIN_TOKEN")


@click.group()
def cli():
    pass


@cli.command(name="register")
@click.argument("node")
@click.argument("address")
@click.argument("user")
@click.argument("password")
def node_register(node, address, user, password):
    """Register a new ipmi node"""
    data = {"type": "ipmi",
            "info": {
                "addr": address,
                "user": user,
                "pass": password
            }}
    url = OBMD_ENDPOINT + node
    r = requests.put(url, json=data, auth=("admin", OBMD_ADMIN_TOKEN))
    print(r)


@cli.command(name="delete")
@click.argument("node")
def node_delete(node):
    """Delete a node"""
    url = OBMD_ENDPOINT + node
    r = requests.delete(url, auth=("admin", OBMD_ADMIN_TOKEN))


@cli.command(name="gettoken")
@click.argument("node")
def get_token(node):
    """Get a new token to do non-admin operations"""
    url = OBMD_ENDPOINT + node + "/token"
    r = requests.post(url, auth=("admin", OBMD_ADMIN_TOKEN))
    print(json.loads(r.content)["token"])


@cli.group(name="power")
def power():
    """Perform power operations"""


@power.command(name="status")
@click.argument("node")
@click.argument("token")
def node_power_status(node, token):
    url = url = OBMD_ENDPOINT + node + "/power_status?token=" + token
    print(url)
    r = requests.get(url)
    print(r.content)


if __name__ == "__main__":
    cli()

