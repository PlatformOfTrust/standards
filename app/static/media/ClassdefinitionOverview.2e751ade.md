# Class definition file

Class definition file describes class and associated properties detailed information.

# Class definition

Class definition contains basic class properties, ex:
```json
"pot:supportedClass":{
      "@id":"pot:Thing/BuiltEnvironment/Room",
      "@type":"pot:Class",
      "subClassOf":"dli:Thing/BuiltEnvironment",
      "rdfs:label":[
         {
            "@language":"en",
            "@value":"Room"
         }
      ],
      "rdfs:comment":[
         {
            "@language":"en",
            "@value":"Room\u00a0is any space enclosed within four walls\u00a0to which entry is possible only by a\u00a0door\u00a0that connects it either to a\u00a0passageway to another room, or to the outdoors, that is large enough for several persons to move about, and whose size, fixtures, furnishings, and sometimes placement within the building support the activity to be conducted in it."
         }
      ],
      "owl:versionInfo":"DRAFT",
      "vs:term_status":"unstable",
	  ...
}
```

# Properties definition

Properties section is defined by property `supportedAttribute` and gives more details about class properties, ex:
```json
{
   ...
   "@id":"http://verbose.terrikon.co/v1/Vocabulary/Thing/BuiltEnvironment/Room",
   "pot:supportedClass":{
      "@id":"pot:Thing/BuiltEnvironment/Room",
      "@type":"pot:Class",
	  ...
      "pot:supportedAttribute":{
	     ...
         "physicalTemperature":{
            "@id":"pot:physicalTemperature",
            "@type":"pot:SupportedAttribute",
            "dli:title":"Temperature",
            "dli:required":false,
            "xs:restriction":{
               "xs:base":"xs:decimal",
               "xs:minInclusive":-273,
               "xs:maxInclusive":1000,
               "xs:fractionDigits":2
            },
            "dli:range":{
               "@type":"obo:UO_0000027",
               "dli:description":"degree Celsius"
            },
            "dli:description":[
               {
                  "@language":"en",
                  "@value":"Temperature of the room"
               }
            ]
         }
      }
   }
}
```

# XML Schema Datatypes

For defining restrictions on properties and datatypes XML Schema Datatypes are used. For more details on those please refer https://www.w3.org/TR/swbp-xsch-datatypes/.
However we do not define separate datatypes over simple types to apply restriction, but use XSD terms to define restrictions directly in property definition, ex:
```json
"xsd:restriction":{
    "xsd:base":"xsd:decimal",
    "xsd:minInclusive":-273,
    "xsd:maxInclusive":1000,
    "xsd:fractionDigits":2
}
```

Please use this reference for list of simple datatypes:
https://www.w3.org/2001/XMLSchema-datatypes

To get additional properties of simple datatypes to apply restrictions please browse https://www.w3.org/2001/XMLSchema.xsd document and search for section describing specific datatype, for example:
```xml
<xs:simpleType name="decimal" id="decimal">
	<xs:annotation>
		<xs:appinfo>
			<hfp:hasFacet name="totalDigits"/>
			<hfp:hasFacet name="fractionDigits"/>
			<hfp:hasFacet name="pattern"/>
			<hfp:hasFacet name="whiteSpace"/>
			<hfp:hasFacet name="enumeration"/>
			<hfp:hasFacet name="maxInclusive"/>
			<hfp:hasFacet name="maxExclusive"/>
			<hfp:hasFacet name="minInclusive"/>
			<hfp:hasFacet name="minExclusive"/>
			<hfp:hasProperty name="ordered" value="total"/>
			<hfp:hasProperty name="bounded" value="false"/>
			<hfp:hasProperty name="cardinality" value="countably infinite"/>
			<hfp:hasProperty name="numeric" value="true"/>
		</xs:appinfo>
		<xs:documentation source="http://www.w3.org/TR/xmlschema-2/#decimal"/>
	</xs:annotation>
	<xs:restriction base="xs:anySimpleType">
		<xs:whiteSpace value="collapse" fixed="true" id="decimal.whiteSpace"/>
	</xs:restriction>
</xs:simpleType>
```

Please refer https://www.w3schools.com/xml/schema_facets.asp for description of applicable facets

# External unit of measures ontology

Unit of measures are defined by `range` property of `SupportedAttribute` class. Currently we use http://www.ontobee.org/ontology/UO ontology to reference physical measurement units.
Specification of unit applied to specific property looks like following:
```json
"dli:range":{
    "@type":"obo:UO_0000096",
    "dli:description":"cubic meter"
}
```

Where type is resolved to http://purl.obolibrary.org/obo/UO_0000096 - link to term in ontology. Also we specify additional description to make it clear what is the unit, because referenced ontology do not have self-explanatory IRIs.

# Define and support several unit of measures
Let's say we need to define that our property supports several unit of measures. In this case we might need to put different limitations based on unit of measure. In example below we define area as both square meter and acre (Not best example to measure room square in acres until you are Salman of Saudi Arabia, but just an example of technical aspects).

```json
"physicalSizeAreaLivingAudited":{
    "@id":"pot:physicalSizeAreaLivingAudited",
    "@type":"pot:SupportedAttribute",
    "xsd:restriction":{
       "xsd:base":"xsd:decimal",
       "xsd:fractionDigits":2
    },
    "dli:title":"Audited living area size",
	"dli:range":[
	{
       "@type":"obo:UO_0000080",
       "dli:description":"square meter",
	   "xsd:restriction":{
			"xsd:minInclusive":0,
			"xsd:maxInclusive":4046.86
		}
    },
	{
       "@type":"obo:UO_0010025",
       "dli:description":"acre",
	   "xsd:restriction":{
			"xsd:minInclusive":0,
			"xsd:maxInclusive":1
		}
    }			
	],
    "dli:required":false,
    "dli:description":[
       {
          "@language":"en",
          "@value":"Audited area size suitable or used for living"
       }
    ]
}
``` 

In this example we define restrictions on 2 levels. First - is general property level and than additionaly per each supported unit of measure. 

Please find below example of actual instance. In the example we skip type definition for `physicalTemperature` and `physicalVolume` because they support only one unit, but we are forced to specify exact type for `physicalSizeAreaLivingAudited` because it supports several different units.
```json
{
  "@context": "http://verbose.terrikon.co/v1/Classes/Thing/BuiltEnvironment/Room",  
  "name" : "A1",
  "data" :
  {    
    "physicalTemperature" : 19,
    "physicalVolume" : 60,
    "physicalSizeAreaLivingAudited" :
    {
      "@type" : "obo:UO_0000080",
      "@value" : 108
    }
  }
}
```

#Extended example

```json
{
   "@context":{
      "@version":1.1,
      "rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
      "rdfs":"http://www.w3.org/2000/01/rdf-schema#",
      "dli":"https://digitalliving.github.io/standards/ontologies/dli.jsonld#",
      "pot":"http://verbose.terrikon.co/v1/Vocabulary/",
      "xsd":"http://www.w3.org/2001/XMLSchema#",
      "obo":"http://purl.obolibrary.org/obo/",
      "@vocab":"http://verbose.terrikon.co/v1/Vocabulary/Thing/BuiltEnvironment/Room"
   },
   "@id":"http://verbose.terrikon.co/v1/Vocabulary/Thing/BuiltEnvironment/Room",
   "pot:supportedClass":{
      "@id":"pot:Thing/BuiltEnvironment/Room",
      "@type":"pot:Class",
      "subClassOf":"dli:Thing/BuiltEnvironment",
      "rdfs:label":[
         {
            "@language":"en",
            "@value":"Room"
         }
      ],
      "rdfs:comment":[
         {
            "@language":"en",
            "@value":"Room\u00a0is any space enclosed within four walls\u00a0to which entry is possible only by a\u00a0door\u00a0that connects it either to a\u00a0passageway to another room, or to the outdoors, that is large enough for several persons to move about, and whose size, fixtures, furnishings, and sometimes placement within the building support the activity to be conducted in it."
         }
      ],
      "owl:versionInfo":"DRAFT",
      "vs:term_status":"unstable",
      "pot:supportedAttribute":{
         "physicalSizeAreaLivingAudited":{
            "@id":"pot:physicalSizeAreaLivingAudited",
            "@type":"pot:SupportedAttribute",
            "xsd:restriction":{
               "xsd:base":"xsd:decimal",
               "xsd:fractionDigits":2
            },
            "dli:title":"Audited living area size",
			"dli:range":[
			{
               "@type":"obo:UO_0000080",
               "dli:description":"square meter",
			   "xsd:restriction":{
					"xsd:minInclusive":0,
					"xsd:maxInclusive":4046.86
				}
            },
			{
               "@type":"obo:UO_0010025",
               "dli:description":"acre",
			   "xsd:restriction":{
					"xsd:minInclusive":0,
					"xsd:maxInclusive":1
				}
            }			
			],
            "dli:required":false,
            "dli:description":[
               {
                  "@language":"en",
                  "@value":"Audited area size suitable or used for living"
               }
            ]
         },
         "physicalTemperature":{
            "@id":"pot:physicalTemperature",
            "@type":"pot:SupportedAttribute",
            "dli:title":"Temperature",
            "dli:required":false,
            "xsd:restriction":{
               "xsd:base":"xsd:decimal",
               "xsd:minInclusive":-273,
               "xsd:maxInclusive":1000,
               "xsd:fractionDigits":2
            },
            "dli:range":{
               "@type":"obo:UO_0000027",
               "dli:description":"degree Celsius"
            },
            "dli:description":[
               {
                  "@language":"en",
                  "@value":"Temperature of the room"
               }
            ]
         },
         "physicalVolume":{
            "@id":"pot:physicalVolume",
            "@type":"pot:SupportedAttribute",
            "dli:title":"Volume",
            "dli:required":false,
            "xsd:restriction":{
               "xsd:base":"xs:decimal",
               "xsd:minInclusive":0,
               "xsd:maxInclusive":1000,
               "xsd:fractionDigits":3
            },
            "dli:range":{
               "@type":"obo:UO_0000096",
               "dli:description":"cubic meter"
            },
            "dli:description":[
               {
                  "@language":"en",
                  "@value":"Volume of the building"
               }
            ]
         }
      }
   }
}
```