# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # The vbguest plugin is used to synchronize VirtualBox Guest Additions
  # version of the guest with the VirtualBox version on the host.
  config.vagrant.plugins = [ "vagrant-vbguest" ]

  config.vm.box = "ubuntu/bionic64"
  config.vm.hostname = "vm"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  config.vm.network "forwarded_port", guest: 5001, host: 5001, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 5002, host: 5002, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 5003, host: 5003, host_ip: "127.0.0.1"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = true

    vb.memory = 1024 * 4
    vb.cpus = 2
  end

  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND="noninteractive"
    apt-get update
    apt-get upgrade -y

    # Install Docker-related bits.
    apt-get install -y docker.io docker-compose

    # Install Python tooling.
    apt-get install -y python3.8 python3.8-dev virtualenv

    # Set an appropriate timezone.
    timedatectl set-timezone Europe/Berlin

    # Add user vagrant to the docker group so that it is possible to operate
    # the docker command without sudo.
    usermod -aG docker vagrant
  SHELL
end
