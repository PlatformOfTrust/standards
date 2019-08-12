#!/bin/sh

set -eo pipefail

readonly CNAME_ADDRESS="standards.oftrust.net"
readonly WORKDIR="/src/v1"
readonly ONT_FILE="${WORKDIR}/ontology/pot.jsonld"
readonly OUT_FOLDER="/tmp/html"
readonly ARTIFACTS="/artifacts"
readonly THEME="darkly"

cd "${WORKDIR}"

mkdir "${OUT_FOLDER}"

ontospy gendocs "${ONT_FILE}" -o "${OUT_FOLDER}" -title "Platform Of Trust" --theme="${THEME}" --type 2

# Copy the HTML to the artifacts folder.
cp -R "${OUT_FOLDER}"/* "${ARTIFACTS}"/

# Copy over the ontologies and contexts to GH pages
cp -R "${WORKDIR}/context" "${ARTIFACTS}"/
cp -R "${WORKDIR}/vocabulary" "${ARTIFACTS}"/
cp -R "${WORKDIR}/classdefinitions" "${ARTIFACTS}"/
echo "${CNAME_ADDRESS}" > "${ARTIFACTS}"/CNAME