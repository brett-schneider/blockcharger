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
vagrant@vm:/vagrant$ sudo docker-compose up geth raiden
```

#### Caveats

On the first run, it might be wort to start the Geth container on its own to let it synchronize the blockchain.
