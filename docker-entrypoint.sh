#!/bin/sh
set -exuo pipefail

KEYS_DIR="/var/public/keys"

mkdir -p "${KEYS_DIR}"
#echo "${JWT_PUBLIC_KEY}" > "${KEYS_DIR}/jwt.pub"
#echo "${BROKER_PUBLIC_KEY}" > "${KEYS_DIR}/translator.pub"

nginx
