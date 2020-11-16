#!/bin/sh
set -exuo pipefail

KEYS_DIR="/var/public/keys"

mkdir -p "${KEYS_DIR}"
echo "${JWT_PUBLIC_KEY}" > "${KEYS_DIR}/jwt.pub"
echo "${BROKER_PUBLIC_KEY}" > "${KEYS_DIR}/translator.pub"


sed -i "s|/v1|/${standards_version}|" /etc/nginx/nginx.conf

nginx
