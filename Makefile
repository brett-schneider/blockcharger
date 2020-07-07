VENV_DIR=	./venv
PIP=		$(VENV_DIR)/bin/pip
PYTHON=		$(VENV_DIR)/bin/python
RNODE_2_ADDRESS=	0x37275F6314cAA14dE6A2D5332709f97d89ef162F
RNODE_2_PORT=		5002

# Initialize the virtual environment for Python and install required
# dependencies.
.PHONY: venv
venv:
	rm -rf -- "$(VENV_DIR)"
	virtualenv --python=python3.8 "$(VENV_DIR)"
	$(PIP) install -r requirements.txt

# Run the consumer.
.PHONY: consumer
consumer:
	$(PYTHON) dev/consumer.py --provider-address ${RNODE_2_ADDRESS}

# Run the producer.
.PHONY: provider
provider:
	$(PYTHON) dev/provider.py --node-port ${RNODE_2_PORT}

# Open a shell in the container running Raiden node.
.PHONY: raiden1_shell
raiden1_shell:
	docker exec -it vagrant_raiden1_1 /bin/bash

# Open a shell in the container running Raiden node.
.PHONY: raiden1_shell
raiden_run:
	docker run --entrypoint /bin/bash -it raidennetwork/raiden:v1.1.0

# Open a shell in the container running Geth.
# Then it is possible to interact with Geth with commands like:
# - geth attach
.PHONY: geth_shell
geth_shell:
	docker exec -it vagrant_geth_1 /bin/sh

.PHONY: geth
geth:
	docker-compose up geth

.PHONY: raiden1 raiden2 raiden3 raiden4
raiden1 raiden2 raiden3 raiden4:
	docker-compose up $@

.PHONY: raidens
raidens:
	docker-compose up raiden1 raiden2 raiden3

# Show the current size of the Geth blockchain stored locally:
.PHONY: get_size_of_geth_blockchain
get_size_of_geth_blockchain:
	@du -sh volumes/geth_persistent_blockchain/
