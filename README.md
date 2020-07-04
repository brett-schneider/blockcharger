# Group Shilling: A Blockchain-Based System for Peer-to-Peer Energy Trading

## Development

### Prerequisites

- [Vagrant](https://www.vagrantup.com/)

### Quick start

Start the virtual machine:

```console
you@host$ vagrant up
```

Log into the VM:

```console
you@host$ vagrant ssh
```

#### Geth and Raiden nodes

It might be necessary to start a Raiden node a little bit later than Geth. In that case run the following in two separate terminals:

```console
vagrant@vm:/vagrant$ docker-compose up geth
```

```console
vagrant@vm:/vagrant$ docker-compose up raiden1
```

#### demo.py

Install the virtual environment and dependencies:

```console
vagrant@vm:/vagrant$ make venv
```

Run demo.py:

```console
vagrant@vm:/vagrant$ make demo
```

### Caveats

It might be worth to start the Geth container first to let it synchronize the blockchain before starting Raiden nodes.

### Troubleshooting

> raiden1_1  | requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.github.com', port=443): Max retries exceeded with url: /repos/raiden-network/raiden/releases/latest (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x7f5333328550>: Failed to establish a new connection: [Errno -5] No address associated with hostname'))  

A fix for this issue is to let Geth run for a while. Afterwards, try launching a Raiden node again.
