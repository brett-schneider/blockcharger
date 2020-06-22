# Open a shell in the container running Geth.
# Then it is possible to interact with Geth with commands like:
# - geth attach
.PHONY: geth_shell
geth_shell:
	sudo docker exec -it vagrant_geth_1 /bin/sh

# Show the current size of the Geth blockchain stored locally:
.PHONY: get_size_of_geth_blockchain
get_size_of_geth_blockchain:
	@du -sh volumes/geth_persistent_blockchain/
