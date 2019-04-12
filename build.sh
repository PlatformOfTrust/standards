#!/bin/sh

set -eo pipefail

readonly CNAME_ADDRESS="standards.oftrust.net"
readonly WORKDIR="/src"
readonly ONT_FILE="/src/ontologies/pot.jsonld"
readonly OUT_FOLDER="/tmp/html"
readonly ARTIFACTS="/artifacts"
readonly THEME="darkly"

cd "${WORKDIR}"

mkdir "${OUT_FOLDER}"

# Need to choose type of export, 2 = Multi-site HTML.
echo 2 | ontodocs "${ONT_FILE}" -o "${OUT_FOLDER}" -t "Platform Of Trust" --theme="${THEME}"

# Copy the HTML to the artifacts folder.
cp -R "${OUT_FOLDER}"/* "${ARTIFACTS}"/

# Copy over the ontologies and contexts to GH pages
cp -R "${WORKDIR}/ontologies" "${ARTIFACTS}"/
cp -R "${WORKDIR}/contexts" "${ARTIFACTS}"/
cp -R "${WORKDIR}/vocabularies" "${ARTIFACTS}"/
echo "${CNAME_ADDRESS}" > "${ARTIFACTS}"/CNAME