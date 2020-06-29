#!/usr/local/opt/python@3.8/bin/python3

from raiden_api import rnode
import argparse

DEFAULT_PROVIDER_NODE_PORT = 5006


def parse_args():
    parser = argparse.ArgumentParser(description="Run provider simulation")
    parser.add_argument(
        "--node-port",
        action="store",
        default=DEFAULT_PROVIDER_NODE_PORT,
        help="set the port of the Raiden node to connect to (default: {})".format(
            DEFAULT_PROVIDER_NODE_PORT
        ),
    )
    return parser.parse_args()


# Parse commmand-line arguments.
args = parse_args()

node = rnode(args.node_port)

q = node.histpay()
print(q.text)
