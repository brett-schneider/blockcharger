#! /bin/sh -

set -ue

node_name="$1"
passphrase="$2"
config="$3"
wallet="$4"

dir="./$node_name"
keystore="$dir/keystore"
passphrases="$dir/passphrases"

mkdir -p "$keystore"
mkdir -p "$passphrases"

mv "$config" "$dir"
(cd "$dir" && ln -fs "${config##*/}" config.toml)
mv "$wallet" "$keystore"
mv "$passphrase" "$passphrases"
