#!/bin/sh

readonly WORKDIR="/src"
readonly ONT_FILE="/src/ontologies/pot.jsonld"
readonly OUT_FOLDER="/artifacts/"
readonly THEME="darkly"

cd "${WORKDIR}"

# Need to choose type of export, 2 = Multi-site HTML.
echo 2 | ontodocs "${ONT_FILE}" -o "${OUT_FOLDER}" -t "Platform Of Trust" --theme="${THEME}"