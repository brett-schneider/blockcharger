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
