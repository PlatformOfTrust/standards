
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
