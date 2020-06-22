# Group Shilling: A Blockchain-Based System for Peer-to-Peer Energy Trading

## Development

#### Prerequisites

- [Vagrant](https://www.vagrantup.com/)

#### Quick start

Start the virtual machine:

```console
you@host$ vagrant up
```

Log into the VM:

```console
you@host$ vagrant ssh
```

Start Geth and Raiden nodes:

```console
vagrant@vm:~$ cd /vagrant
vagrant@vm:/vagrant$ sudo docker-compose up geth raiden1
```

It might be necessary to start a Raiden node a little bit later than Geth. In that case run the following in two separate terminals:

```console
vagrant@vm:/vagrant$ sudo docker-compose up geth
```

```console
vagrant@vm:/vagrant$ sudo docker-compose up raiden1
```

#### Caveats

On the first run, it might be wort to start the Geth container on its own to let it synchronize the blockchain.

#### Troubleshooting

> raiden1_1  | requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.github.com', port=443): Max retries exceeded with url: /repos/raiden-network/raiden/releases/latest (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x7f5333328550>: Failed to establish a new connection: [Errno -5] No address associated with hostname'))  

A fix for this issue is to let Geth run for a while. Afterwards, try launching a Raiden node again.
