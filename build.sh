#!/bin/sh

set -eo pipefail

readonly VERSION = "v1"
readonly CNAME_ADDRESS="standards.oftrust.net"
readonly WORKDIR="/src/${VERSION}"
readonly ONT_FILE="${WORKDIR}/Ontology/pot.jsonld"
readonly OUT_FOLDER="/tmp/html"
readonly ARTIFACTS_ROOT="/artifacts"
readonly ARTIFACTS="${ARTIFACTS_ROOT}/${VERSION}"
readonly THEME="darkly"

cd "${WORKDIR}"

mkdir "${OUT_FOLDER}"

ontospy gendocs "${ONT_FILE}" -o "${OUT_FOLDER}" --title "Platform Of Trust" --theme="${THEME}" --type 2

# Copy the HTML to the artifacts folder.
cp -R "${OUT_FOLDER}"/* "${ARTIFACTS}"/

# Copy over the ontologies and contexts to GH pages
cp -R "${WORKDIR}/Context" "${ARTIFACTS}"/
cp -R "${WORKDIR}/Vocabulary" "${ARTIFACTS}"/
cp -R "${WORKDIR}/ClassDefinitions" "${ARTIFACTS}"/
echo "${CNAME_ADDRESS}" > "${ARTIFACTS_ROOT}"/CNAME