VENV_DIR=	./venv
PIP=		$(VENV_DIR)/bin/pip
PYTHON=		$(VENV_DIR)/bin/python

# Initialize the virtual environment for Python and install required
# dependencies.
.PHONY: venv
venv:
	rm -rf -- "$(VENV_DIR)"
	virtualenv --python=python3.8 "$(VENV_DIR)"
	$(PIP) install -r requirements.txt

# Run demo.
.PHONY: demo
demo:
	$(PYTHON) dev/demo.py

# Open a shell in the container running Raiden node.
.PHONY: raiden1_shell
raiden1_shell:
	sudo docker exec -it vagrant_raiden1_1 /bin/bash

# Open a shell in the container running Raiden node.
.PHONY: raiden1_shell
raiden_run:
	sudo docker run --entrypoint /bin/bash -it raidennetwork/raiden:v1.1.0

# Open a shell in the container running Geth.
# Then it is possible to interact with Geth with commands like:
# - geth attach
.PHONY: geth_shell
geth_shell:
	sudo docker exec -it vagrant_geth_1 /bin/sh

.PHONY: geth
geth:
	sudo docker-compose up geth

.PHONY: raiden1
raiden1:
	sudo docker-compose up raiden1

.PHONY: raiden2
raiden2:
	sudo docker-compose up raiden2

.PHONY: raidens
raidens:
	sudo docker-compose up raiden1 raiden2 raiden3

# Show the current size of the Geth blockchain stored locally:
.PHONY: get_size_of_geth_blockchain
get_size_of_geth_blockchain:
	@du -sh volumes/geth_persistent_blockchain/
