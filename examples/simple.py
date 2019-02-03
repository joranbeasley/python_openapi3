from py_oas3._util import TypedMapFactory, TypedListFactory
from py_oas3.oas_specification.oas_parameters import OASParameterObject
from py_oas3.oas_specification.oas_response import OASResponseObject, OASMediaTypeObject
from py_oas3.oas_specification.paths_sections import OASOperationObject, OASPathItemObject

# Responses are required
responses = TypedMapFactory(OASResponseObject)()
responses['200'] = OASResponseObject("Success",
                                     OASMediaTypeObject(example='{"status":"OK"}')
                                     )
print(responses.to_dict())
# Parameters are *probably* required
parameters = TypedListFactory(OASParameterObject)()
parameters.append(OASParameterObject("thing_id","query","the id of the thing"))
print(parameters.to_dict())
# Build the endpoint operation
endpoint = OASOperationObject(responses,
                              parameters=parameters,
                              summary="example endpoint summary",
                              tags=["Users"])
print(endpoint.to_dict())
endpoint_map = OASPathItemObject(get=endpoint)
print(endpoint_map.to_dict())
paths={"api/v0/get_item":endpoint_map}

