# Platform Of Trust Standards repository

This repository contains everything we need to standardize the Platform Of Trust
APIs.

The Platform Of Trust core ontology can be found as a JSON-LD
ontology file under [ontologies/pot.jsonld](ontologies/pot.jsonld).

The HTML version of the ontology documentation is hosted at our 
[Github Pages](https://standards.oftrust.net/)

_Please note that this repository is under active development, and the IRIs
and URIs in the ontology files are subject to change at any time._

# Using the standards

The ontology describes the real world entities as seen in Platform Of Trust.
The contexts that describes the different identities are found under the 
[contexts](contexts) folder. 

Each identity type has their own context which
describes the attributes the identity has. The context file name gives a notion
of whether the context is for an `identity` or a `link`. 

The identity describes the real world identities, such as apartments, 
buildings, rooms etc. The links are the relations between identities. 
As an example, the `Tenant`-link can be applied between
a user identity and an apartment identity, meaning that the user is a tenant
in the apartment.

If only a link between identities is needed, without any kind
of role, the generic `link-link.jsonld` can be used 
[contexts/link-link.jsonld](contexts/link-link.jsonld).

All identities MUST have a name, e.g. for an apartment it could be `A 18`.
The keys for the identities are defined under the `data`-object. The contexts
therefore defines the following:

    "@context": {
        "@version": 1.1,
        "@vocab": "https://standards.oftrust.net/vocabularies/app.jsonld#",
        "pot": {
          "@id": "https://standards.oftrust.net/ontologies/pot.jsonld#",
          "@prefix": true
        },
        "dli": {
          "@id": "https://digitalliving.github.io/standards/ontologies/dli.jsonld#",
          "@prefix": true
        },
        "data": "dli:data",
        "name": "pot:name",
        "description": {
          "@id": "pot:description",
          "@nest": "pot:data"
        },
        "completionYear": {
          "@id": "pot:year",
          "@nest": "pot:data"
        },
        "inaugurationYear": {
          "@id": "pot:year",
          "@nest": "pot:data"
        },
        "height": {
          "@id": "pot:meter",
          "@nest": "pot:data"
        },
        "usageType": {
          "@id": "pot:main",
          "@nest": "pot:data"
        }
        ...

From the context we can see, that the description, completionYear, 
inaugurationYear, height and usageType should be nested under the 
`data`-object, e.g.

    {
        "@context": "https://standards.oftrust.net/contexts/identity-apartment.jsonld",
        "@id": "<identity id>",
        "@type": "Apartment",
        "name": "A 18",
        "data": {
            "description": "The apartment A 18 has 3 rooms, sauna and kitchen",
            "completionYear": 2005,
            "inaugurationYear": 2006,
            "height": 3,
            "usageType": "Apartment"
        }
    }

By defining the prefixes with `"@prefix": true` a developer can programmatically
skip the ontology prefix definitions, which only defines what `pot:` should be
expanded to when processing the JSON-LD.

To know which attributes are required, what type of values are supported and
other information about the identity, we define `vocabularies` for each of the
contexts. The vocabularies can be found under the [vocabularies](vocabularies)
folder.

The context defines 
`@vocab: https://standards.oftrust.net/vocabularies/apartment.jsonld#`
from where the information can be found.

The `supportedClass` is a list of supported types for the identity in question.
Usually there's only one supportedClass per identity. 

The type also defines a list of `supportedAttribute` which
defines each of the attributes the identity can have. All attribute objects
MUST have `@type: pot:SupportedAttribute`.

Below you can see an example of the apartment attributes defined in the 
apartment vocabulary.

    ...
    {
      "@type": "pot:SupportedAttribute",
      "dli:attribute": "pot:name",
      "dli:title": "Name",
      "dli:description": "The name of the apartment.",
      "dli:required": true
    },
    {
      "@type": "pot:SupportedAttribute",
      "dli:attribute": "dli:data",
      "dli:title": "Data",
      "dli:description": "Additional key-value data to be saved for the apartment.",
      "dli:required": true,
      "dli:valueType": "xsd:object"
    },
    {
      "@type": "pot:SupportedAttribute",
      "dli:attribute": "pot:description",
      "dli:title": "Description",
      "dli:description": "Description of the apartment.",
      "dli:required": false
    },
    {
      "@type": "pot:SupportedAttribute",
      "dli:attribute": "pot:completionYear",
      "dli:title": "Completion year",
      "dli:description": "The year when the apartment was completed",
      "dli:required": false
    },
    {
      "@type": "pot:SupportedAttribute",
      "dli:attribute": "pot:inaugurationYear",
      "dli:title": "Inauguration year",
      "dli:description": "The year when the apartment was inaugurated",
      "dli:required": false
    },
    {
      "@type": "pot:SupportedAttribute",
      "dli:attribute": "pot:height",
      "dli:title": "Height",
      "dli:description": "The height of the apartment",
      "dli:required": false
    },
    {
      "@type": "pot:SupportedAttribute",
      "dli:attribute": "pot:usageType",
      "dli:title": "Usage type",
      "dli:description": "What is the apartment used for",
      "dli:required": false
    },
    ...

As can be seen from the example, we define the attribute, the title for the
attribute, description and if the attribute is required or not. We can also
define the value type of the attribute, e.g. `"dli:valueType": "xsd:object"`.
If no `valueType` is defined, the default should always be `xsd:string`.
We can also define default values for the attributes with 
`"dli:defaultValue": "Placeholder"`,
as well as different supported values with 
`"dli:supportedValue": ["Yes", "No", "None"]`.

With the vocabulary a developer can programmatically build the attributes in 
the front-end application, define if they are required or not, default values 
and even validate the types of the values given in the form.

Good examples are found for [contexts/identity-app.jsonld](contexts/identity-app.jsonld)
and its corresponding vocabulary [vocabularies/app.jsonld](vocabularies/app.jsonld)