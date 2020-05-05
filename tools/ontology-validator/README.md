# json-ld-validator

---
***IMPORTANT:***
All the commands must be executed in the tool's root folder.

---

**Install prerequisite modules**
* Install Python 3
* Execute the following: 
  ```
  pip install pipenv
  pipenv shell
  pipenv install
  ```
**How to run the app**

* Execute `python jsonld_validator.py --help` to print the help message:
```
usage: jsonld_validator.py [-h] -s SOURCE -v VERSION [-r RESOURCES]
                           [--spellcheck SPELLCHECK] [-t] [--verbose]

Tool for validating JSON-LD Ontology structure and files

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        Path to a folder that contains version folders
  -v VERSION, --version VERSION
                        Version number
  -r RESOURCES, --resources RESOURCES
                        The path to the resources.json file which must be used
                        for this version. Default value: resources.json
  --spellcheck SPELLCHECK
                        Specifies if the spell check for the english labels,
                        descriptions, comments and titles will be made. Value
                        type: boolean (true(t)/false(f), 1/0, yes(y)/no(n)).
                        Default value: true
  -t, --translation     If given as argument, validates that finnish language
                        must be present as translation of english labels,
                        descriptions, comments and titles
  --verbose, --verbose  Print debug info
  ```
* To run the validation for master version you must follow the steps:
  1) Clone / Download the ontology folder from [github](https://github.com/PlatformOfTrust/standards)
  2) Execute the following: `python jsonld_validator.py -s <path_to_folder> -v 1` (You can add optional arguments, or edit _resources.json_ file)

---
***NOTE:***
`<path_to_folder>` is the folder that contains v1 folder.

---

* To run the validation for ontotest version you must follow the steps:
  1) Clone / Download the ontology folder from [github](https://github.com/PlatformOfTrust/standards/tree/ontotest)
  2) Rename v1 folder to v2
  3) Execute the following: `python jsonld_validator.py -s <path_to_folder> -v 2 -r resources_v2.json ` (You can add optional arguments, or edit resources_v2.json file)
 
---
***NOTE:***
Because the ontotest version has a different structure (some missing files and some extra files) you should name the folder of that version _v2_ so that the proper structure validator will be chosen. 
Use _resources_v2.json_ as configuration file, it was made for this version. You can edit the fields so that you may have the expected validation.

---

**Run unit tests and check coding style**

* To run unit tests execute the following: `pytest tests`
* To run coding style checker execute the following: `pylint_runner.exe`

**Configuration (all "settings" are present in the _resources.json_ file)**

* fieldsWithTypeList - this stores the attributes which accept an array as value (for example domain)
* requiredAttributes - this stores all of the required attributes which should be present for all objects defined the list of attributes of that type (ex: for all supportedAttributes or Properties)
* acceptedWordsSpellCheck - these are words (excluding abbreviations) that are not validated by the spell checking library, nor by the spell checking API, but which are accepted within PoT standards
* URL: this is the URL the ontologies to be pushed are going to be accessible after the pull request is approved. This url is removed from referenced file paths to validate the local version. Ex: If the URL has the value: "https://standards.oftrust.net/v1/", then "https://standards.oftrust.net/v1/ClassDefinitions/Building" will be searched at the path "ClassDefinitions/Building" relative to the version file. 
* ontology: this is the ontology name. It is used to get the ontology file name in "Ontology/" folder
* prefix: specifies the prefix for supportedClass, supportedAttribute, required (on the master version prefix is 'dli' and on the ontotest version is 'pot')

**Description**

Please see below the steps this tool performs:
1) Search for a validator for the given version structure. If a validator for this version is not implemented, use the last version validator.
2) Validate the folder structure.
3) Validate the files starting from Context. For every class defined in Context, validate the associated ClassDefinitions and Vocabulary files. After that validate derived classes (subclasses) recursively.
4) Validate ontology file.