#!/usr/bin/env bash

JAVA=$(which java)
WORKDIR=/src

cd "${WORKDIR}"

"${JAVA}" -jar widoco.jar -ontFile /src/ontologies/pot.rdf \
-outFolder /artifacts/ -getOntologyMetadata -rewriteAll -lang en-fi \
-includeImportedOntologies -webVowl -ignoreIndividuals \
-includeAnnotationProperties