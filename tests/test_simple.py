from pytest import raises

from python_openapi3 import OASContactObject, OASLicenseObject, OASInfoObject
from python_openapi3.openapi_specification.oas_response import OASExampleObject, OASEncodingObject, OASSecuritySchemeObject
from python_openapi3.openapi_specification.oas_server import OASExternalDocumentationObject, OASServerVariableObject, \
    OASServerObject
from python_openapi3.openapi_specification.root import OAS3Specification
from python_openapi3.openapi_specification.oas_parameters import OASParameterObject, OASSchemaObject, OASReferenceObject


class TestParameter:
    def setup(self):
        pass
    def teardown(self):
        pass
    def test_refobj(self):
        p = OASReferenceObject("#/components/schemas/PetFood")
        assert p.to_dict() == {"$ref":"#/components/schemas/PetFood"}
    def test_refobj_from_kwargs(self):
        p = OASReferenceObject(**{"$ref":"#/components/schemas/PetFood"})
        assert p.to_dict() == {"$ref":"#/components/schemas/PetFood"}
    def test_refobj_from_kwargs_alt(self):
        p = OASReferenceObject(**{"ref":"#/components/schemas/PetFood"})
        assert p.to_dict() == {"$ref":"#/components/schemas/PetFood"}
    def test_schema_simple_string(self):
        p = OASSchemaObject("string",description="a serial number")
        assert p.to_dict() == {"type":"string","description":"a serial number","example":"a string"}
        return p
    def test_object_missing_properties(self):
        p = OASSchemaObject("object")
        assert p.to_dict() == {"type":"object","example":{},"properties":{}}
    def test_schema_simple_number(self):
        p = OASSchemaObject("number")
        assert p.to_dict() == {"type": "number","example":0.0}
        return p
    def test_schema_simple_object(self):
        p = OASSchemaObject("object",properties={"A":{"type":"number"},
                                                 "B":{"type":"string"}})
        data = p.to_dict()
        assert data == {'type': 'object',
                        'properties': {'A': {'type': 'number', 'example': 0.0},
                                       'B': {'type': 'string', 'example': 'a string'}},
                        'example': {'A': 0.0, 'B': 'a string'}}
        return p
    def test_schema_simple_array(self):
        p = OASSchemaObject("array",items=[{"type":"integer"},])
        data = p.to_dict()
        expected = {'items': [{'type': 'integer', 'example': 0}], 'type': 'array', 'example': [0]}
        assert data == expected
    def test_schema_array_error(self):
        assert raises(TypeError,lambda:OASSchemaObject("array"))
    def test_parameter_1(self):
        p = OASParameterObject("pet_id","path","string",description="The Pet ID", deprecated=False,required=False)
        p_data = p.to_dict()
        assert p_data == {'description': 'The Pet ID',
                          'deprecated': False, 'required': False, 'in': 'path',
                          'schema': {'type': 'string', "example":"a string"}, 'name': 'pet_id'}
        return p
    def test_parameter_2(self):
        kwargs = dict(schema = {"type": "object", "properties": {
            "A": {"type": "string"}}}, description = "The Pet ID", deprecated = True)
        p = OASParameterObject("pet_id", "query", **kwargs)
        p_data = p.to_dict()
        expected = {'description': 'The Pet ID', 'deprecated': True, 'required': True,
                          'in': 'query',
                          'schema': {
                              'type': 'object', 'properties': {'A': {'type': 'string',"example":"a string"}},
                              "example":{"A":"a string"}
                          },
                          'name': 'pet_id'
                          }
        assert p_data == expected
    def test_parameter_upgrade_to_schema(self):
        kwargs = {"type": "object", "properties": {
            "A": {"type": "string"}}, "description":"The Pet ID", "deprecated":True}
        p = OASParameterObject("pet_id", "query", **kwargs)
        expected = {'description': 'The Pet ID', 'deprecated': True, 'required': True,
         'in': 'query',
         'schema': {
             'type': 'object', 'properties': {'A': {'type': 'string', "example": "a string"}},
             "example": {"A": "a string"}
         },
         'name': 'pet_id'
         }
    def test_parameter_style_violation(self):
        assert raises(TypeError,lambda:OASParameterObject(
        "tag_name","path","string",style="asd"))

class TestServer:
    def test_externaldoc(self):
        p = OASExternalDocumentationObject("http://...",description="hello")
        assert p.to_dict() == {'url':"http://...","description":"hello"}
    def test_externaldoc_validation_fail(self):
        p = OASExternalDocumentationObject("http://...", description="hello")
        assert not p.validate()
    def test_externaldoc_validation_fail2(self):
        p = OASExternalDocumentationObject("http://asd.ccas123casd1213.com", description="hello")
        assert not p.validate()
    def test_externaldoc_validation_fail3(self):
        p = OASExternalDocumentationObject("http://google.com/asdfwefqewfdqav", description="hello")
        assert not p.validate()
    def test_externaldoc_validation_pass(self):
        p = OASExternalDocumentationObject("https://google.com", description="hello")
        assert p.validate()
    def test_servervariable(self):
        p = OASServerVariableObject("default_value","a description",["1","2"])
        data = p.to_dict()
        expect = {"default":"default_value","description":"a description","enum":["1","2"]}
        assert data == expect
    def test_serverobject(self):
        p = OASServerObject("http://...","a server",{"Variable":"Mapping"})
        data = p.to_dict()
        expect = {"url":"http://...","description":"a server",
                  "variables":
                      {"Variable":{"default":"Mapping"}}}
        assert expect == data

class TestInfo:
    def test_contactinfo(self):
        p = OASContactObject("test name","test@test.com","http://...")
        data = p.to_dict()
        expect = {"name":"test name","email":"test@test.com","url":"http://..."}
        assert expect == data
    def test_minimum_contactinfo(self):
        p = OASContactObject("test name")
        data = p.to_dict()
        expect = {"name":"test name"}
        assert expect == data
    def test_licenseinfo(self):
        p = OASLicenseObject("GPL")
        data = p.to_dict()
        assert data == {"name":"GPL"}
    def test_licenseinfo_with_url(self):
        p = OASLicenseObject("GPL","http://...")
        data = p.to_dict()
        assert data == {"name":"GPL","url":"http://..."}
    def test_infoobject_minimum(self):
        p = OASInfoObject("Simple App","0.1")
        assert p.to_dict() == {"title":"Simple App","version":"0.1"}

class TestResponses:
    def test_exampleobject_invalid(self):
        assert raises(TypeError,lambda:OASExampleObject({}))
    def test_exampleobject_min_literal(self):
        p = OASExampleObject("a simple example...")
        data = p.to_dict()
        expect = {"value":"a simple example..."}
        assert data == expect
    def test_exampleobject_min_external(self):
        p = OASExampleObject("http://...")
        data = p.to_dict()
        expect = {"externalValue":"http://..."}
        assert data == expect
    def test_exampleobject_min_kwargs_corrected_value(self):
        p = OASExampleObject(**{"value":"http://..."})
        data = p.to_dict()
        expect = {"value":"http://..."}
        assert data == expect
    def test_exampleobject_min_kwargs_corrected_externalValue(self):
        p = OASExampleObject(**{"externalValue":"http://..."})
        data = p.to_dict()
        expect = {"externalValue":"http://..."}
        assert data == expect
    def test_externalobject_typeErrors(self):
        RaisesTypeError1=lambda:OASExampleObject('a',**{"externalValue":"http://..."})
        assert raises(TypeError,RaisesTypeError1)
        RaisesTypeError2 = lambda: OASExampleObject('a', **{"value": "http://..."})
        assert raises(TypeError, RaisesTypeError2)
        RaisesTypeError3 = lambda: OASExampleObject(**{"value":"a","externalValue": "http://..."})
        assert raises(TypeError, RaisesTypeError3)

    def test_encoding_noargs(self):
        p = OASEncodingObject()
        assert p.to_dict() == {}
    def test_encoding_style(self):
        p = OASEncodingObject("text/ascii",style="form")
        expected = {'contentType':'text/ascii','style':'form'}
        assert p.to_dict() == expected
    def test_encoding_badstyle(self):
        assert raises(TypeError, lambda:OASEncodingObject("text/ascii",style="aform"))
    def test_encoding_headers(self):
        p = OASEncodingObject(headers={"Bearer":"ASD"})
        expected = {"headers":{"Bearer":{"description":"ASD","required":True}}}
        assert p.to_dict() == expected
    def test_securityscheme(self):
        p = OASSecuritySchemeObject("api-key","query","apiKey")
        data = p.to_dict()
        assert data == {'in': 'query', 'type': 'apiKey', 'name': 'api-key'}
    def test_securityscheme_alt(self):
        p = OASSecuritySchemeObject("api-key",**{"in":"query","type":"apiKey"})
        data = p.to_dict()
        assert data == {'in': 'query', 'type': 'apiKey', 'name': 'api-key'}
# class TestSpecConstructor:
#     def setup(self):
#         pass
#     def teardown(self):
#         pass
#     def test_spec_min(self):
#         info={
#             "appName":"Test0",
#             "appVersion":"1.0.-1",
#             "appDescription":"Test0 Description",
#         }
#         result=OAS3Spec(**info)
#         print(result['info']['license'])
#     def test_spec_errors(self):
#         result=OAS3Spec().to_dict()

