## Structure and definitions

The Standard is split into 3 sections, each having their own directory in the repository:

There are 3 types of JSON-LD files:
- **Context file** - file describing JSON object structure and referencing Vocabulary and Class definition files for details
- **Vocabulary file** - contains standard definition of attributes, class and its subclasses in RDF standard
- **Class definition file** - DLI extention required to specify attributes additional properties like mandatory, supported values e.t.c. It was named Vocabulary before and created confusion with JSON-LD term vocab, but was not vocab actually. This created some resolution problems

## Contexts

Contexts are laid out in a versioned tree structure. Each specific definition is in a `.jsonld` -file. For every directory under the `contexts` folder, the PARENT folder is expected to have `<folder>.jsonld` that defines the base class for that directory's contents. E.g. if `Context/Thing/FlowerPot.jsonld` exists, then `Context/Thing.jsonld` must exist as well.

Contexts need to be further divided into subtypes:

 - Data Products (identified by being located in the `DataProduct` -directory)
 - Identities (identified by being located in the `Identity` -directory)
 - Links (identified by being located in the `Link` -directory)

(The exact location of the `Data-Product`, `Identity` and `Link` directories is TBD)

Naming standard is:

 - URL friendly (no characters that require % signs in the URL or similar)
 - Human readable
 - U.S. English
 - Pascal case

## URL structure

Context file is available at URL containing base URL + `version` + `/Context/` + class name:
https://standards.oftrust.net/v1/Context/DataProduct/
https://standards.oftrust.net/v1/Context/Thing/Device/Sensor/TemperatureSensor/

Vocabulary files URLs have same structure as Context files, but Vocabulary folder should be used instead:
https://standards.oftrust.net/v1/Vocabulary/DataProduct/
https://standards.oftrust.net/v1/Vocabulary/Thing/Device/Sensor/TemperatureSensor/

Class descriptions files URLs have same structure as Context files, but ClassDefinition folder should be used instead
https://standards.oftrust.net/v1/ClassDefinitions/DataProduct/
https://standards.oftrust.net/v1/ClassDefinitions/Thing/Device/Sensor/TemperatureSensor/

Current WIP is hosted at https://verbose.terrikon.co/v1/Vocabulary/ etc.

## Versioning

Versioning should use semantic versions for names, except truncated to significant bits. The patch version does not need to be used for minor changes of e.g. titles and descriptions. Any backwards incompatible change (removal/rename of fields, restructuring) must be done in a new major version (e.g. `v2`), and adding fields should result in a new minor version (e.g. `v1.1`) as adding new required fields could break something. 

## Viewer

The raw JSON-LD will be hosted by default, however once the standards viewer has been implemented the server shall be configured so that instead of the raw JSON-LD the server will return a React application if the `Accept` header contains `text/html`. The React application will be built so it understands the same URL structure and will be able to visualize the standards.

## Hosting

Data Standards should be hosted at

 - https://standards.oftrust.net/ - Stable, ready for production use
 - https://standards-lab.oftrust.net/ - Work in progress, trying out new ideas, things that are not agreed on as useful and stable standards yet.

## Support for 3rd party developers

Suggested workflow for 3rd party developers:

 - "Fork this repository"
 - Enable Travis-CI integration
 - Point your Data Product to a stable context from https://standards.oftrust.net as well as your non-standard context
 - Make changes as needed
 - Send a PR to https://github.com/PlatformOfTrust/standards if you think your changes are ready for a stable release
   - Community feedback is requested for the PR
   - If PR is deemed useful and of good quality, it is merged to stable standards
 - Alternatively you can just use your own extension as an additional context to your data product

## How to navigate

To navigate through the context tree you should get root context file first. For example:
https://standards.oftrust.net/v1/Vocabulary/

In that file you'll have JSON-LD classes like
```json
{
    "@id": "pot:DataProduct"
}
```

Take `@id` of the Class and append it to URL. Use next URLs:
https://standards.oftrust.net/v1/Context/DataProduct/ - to get Context file (or React app)
https://standards.oftrust.net/v1/ClassDefinitions/DataProduct/ - to get class definition
https://standards.oftrust.net/v1/Vocabulary/DataProduct/ - to get Vocabulary file

In each Context file there is a list of subclasses so it is possible to navigate further

# Data examples

Next data examples work correctly based on [JSON-LD Playground](https://json-ld.org/playground/) testing

## Context

```json
{
  "@context" : "https://standards.oftrust.net/v1/Context/Thing/Device/Sensor/TemperatureSensor/",
  "name" : "Test sensor",
  "data" : {
    "physicalPower" : "40 W",
    "physicalWeight" : "100 gr",
    "physicalColorName" : "white"
  }
}
```

## Sample data product

**TODO: UPDATE TO MATCH REALITY**

```json
{
  "@context" : "https://standards.oftrust.net/v1/Context/DataProduct/",
  "name" : "ERP API",
  "version": "10.1",
  "authorization": "oauth2",
  "product_code": "DynamicsFO",
  "limit": "100000"
}
```