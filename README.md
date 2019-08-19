## Structure and definitions

The Standard is split into 3 sections, each having their own directory in the repository.

There are 3 types of JSON-LD files:
- **Context file** - file describing JSON object structure and referencing Vocabulary and Class definition files for details
- **Vocabulary file** - contains standard definition of properties, class and its subclasses in RDF standard
- **Class definition file** - extention required to specify fields additional properties like mandatory, types, supported values e.t.c. 

## Contexts

Contexts are laid out in a versioned tree structure. Each specific definition is in a `.jsonld` -file. For every directory under the `contexts` folder, the PARENT folder is expected to have `<folder>.jsonld` that defines the base class for that directory's contents. E.g. if `Context/Identity/Thing/FlowerPot.jsonld` exists, then `Context/Identity/Thing.jsonld` must exist as well.

Naming standard is:

 - URL friendly (no characters that require % signs in the URL or similar)
 - Human readable
 - U.S. English
 - Pascal case

## URL structure

Context file is available at URL containing base URL + `version` + `/Context/` + class name:
https://standards.oftrust.net/v1/Context/Identity/Digital/Data/DataProduct/
https://standards.oftrust.net/v1/Context/Identity/Thing/Device/Sensor/TemperatureSensor/

Vocabulary files URLs have same structure as Context files, but Vocabulary folder should be used instead:
https://standards.oftrust.net/v1/Vocabulary/Identity/Digital/Data/DataProduct
https://standards.oftrust.net/v1/Vocabulary/Identity/Thing/Device/Sensor/TemperatureSensor

Class descriptions files URLs have same structure as Context files, but ClassDefinition folder should be used instead
https://standards.oftrust.net/v1/ClassDefinitions/Identity/Digital/Data/DataProduct
https://standards.oftrust.net/v1/ClassDefinitions/Identity/Thing/Device/Sensor/TemperatureSensor

Web server is configured to return `JSON-LD` files by appending `.jsonld` to requests. In case of context file it will also remove trailing slash before appending `.jsonld` extention. In repository respective files can be found in folders following URL logic

## Versioning

Versioning use semantic versions for names, except truncated to significant bits. The patch version is not used for minor changes of e.g. titles and descriptions. Any backwards incompatible change (removal/rename of fields, restructuring) is done in a new major version (e.g. `v2`), and adding fields result in a new minor version (e.g. `v1.1`) as adding new required fields could break something. 

## Viewer

The raw JSON-LD will be hosted by default, however once the standards viewer has been implemented the server shall be configured so that instead of the raw JSON-LD the server will return a React application if the `Accept` header contains `text/html`. The React application will be built so it understands the same URL structure and will be able to visualize the standards.

## Hosting

Data Standards should be hosted at
- https://standards.oftrust.net/ - Stable, ready for production use
- https://standards-lab.oftrust.net/ - Work in progress, trying out new ideas, things that are not agreed on as useful and stable standards yet.

## How to navigate

To navigate through the context tree you should get root context file first. For example:
https://standards.oftrust.net/v1/Vocabulary/

In that file you'll have JSON-LD classes like
```json
{
    "@id": "dli:Identity"
}
```

Take `@id` of the Class and append it to URL. Use next URLs:
https://standards.oftrust.net/v1/Context/Identity/ - to get Context file (or React app)
https://standards.oftrust.net/v1/ClassDefinitions/Identity - to get class definition
https://standards.oftrust.net/v1/Vocabulary/Identity - to get Vocabulary file

In each Context file there is a list of subclasses so it is possible to navigate further

# Data examples

Next data examples work correctly based on [JSON-LD Playground](https://json-ld.org/playground/) testing

## Context

```json
{
  "@context" : "https://standards.oftrust.net/v1/Context/Identity/Thing/Device/Sensor/TemperatureSensor/",
  "@id" : "123e4567-e89b-12d3-a456-426655440000",
  "name" : "Test sensor",
  "data" : {
    "physicalPower" : "40 W",
    "physicalWeight" : "100 gr",
    "physicalColorName" : "white"
  }
}
```