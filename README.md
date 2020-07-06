# Group Shilling: A Blockchain-Based System for Peer-to-Peer Energy Trading

## Development

### Prerequisites

- [Vagrant](https://www.vagrantup.com/)

### Quick start

Start the virtual machine:

```sh
vagrant up
```

Log into the VM:

```sh
vagrant ssh
```

The project directory is located at `/vagrant` inside the VM. Run the following command to change the current working directory after sshing into the VM:

```sh
cd /vagrant
```

Afterwards, you may call any of the commands below:

#### Geth and Raiden nodes

It might be necessary to start a Raiden node a little bit later than Geth. In that case run the following in two separate terminals:

```sh
docker-compose up geth
```

```sh
docker-compose up raiden1
```

We support 4 Raiden nodes currently: `raiden1`, `raiden2`, `raiden3`, and `raiden4`.

Also, it is possible to start a service with `make`, e.g.: `make geth` or `make raiden1`. See the `Makefile` file for the list of all targets like that.

#### Python

Install the virtual environment and dependencies:

```sh
make venv
```

Activate the Python environment:

```sh
source ./venv/bin/activate
```

Now you are able to run the Python scripts from the `dev` directory by invoking them like this:

```sh
python ./dev/w3.py
```

### Caveats

It might be worth to start the Geth container first to let it synchronize the blockchain before starting Raiden nodes.

### Troubleshooting

> raiden1_1  | requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.github.com', port=443): Max retries exceeded with url: /repos/raiden-network/raiden/releases/latest (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x7f5333328550>: Failed to establish a new connection: [Errno -5] No address associated with hostname'))  

A fix for this issue is to let Geth run for a while. Afterwards, try launching a Raiden node again.
