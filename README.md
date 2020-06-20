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

#### Caveats

On the first run, it might be wort to start the Geth container on its own to let it synchronize the blockchain.
