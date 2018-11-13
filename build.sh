#!/bin/sh

set -eo pipefail

readonly WORKDIR="/src"
readonly ONT_FILE="/src/ontologies/pot.jsonld"
readonly ONT_URL="https://raw.githubusercontent.com/PlatformOfTrust/standards/master/ontologies/pot.jsonld"
readonly OUT_FOLDER="/tmp/html"
readonly ARTIFACTS="/artifacts"
readonly THEME="darkly"

cd "${WORKDIR}"

mkdir "${OUT_FOLDER}"

# Copy over the ontologies and contexts to GH pages
cp -R "${WORKDIR}/ontologies" "${ARTIFACTS}"/
cp -R "${WORKDIR}/contexts" "${ARTIFACTS}"/

# Need to choose type of export, 2 = Multi-site HTML.
echo 2 | ontodocs "${ONT_FILE}" -o "${OUT_FOLDER}" -t "Platform Of Trust" --theme="${THEME}"

cp -R "${OUT_FOLDER}"/* "${ARTIFACTS}"/