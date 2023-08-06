# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['openapi_to_fastapi',
 'openapi_to_fastapi.tests',
 'openapi_to_fastapi.tests.snapshots',
 'openapi_to_fastapi.validator']

package_data = \
{'': ['*'], 'openapi_to_fastapi.tests': ['data/ihan/*', 'data/pet_store/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'coloredlogs>=14.0,<15.0',
 'datamodel-code-generator>=0.5.24,<0.6.0',
 'fastapi>=0.47.1,<0.48.0',
 'genson==1.2.1']

entry_points = \
{'console_scripts': ['openapi-validator = '
                     'openapi_to_fastapi.cli:cli_validate_specs']}

setup_kwargs = {
    'name': 'openapi-to-fastapi',
    'version': '0.1.2',
    'description': 'Create FastAPI routes from OpenAPI spec',
    'long_description': '## Reasoning\n\n[FastAPI](https://github.com/tiangolo/fastapi) is an awesome framework that\nsimplifies the process of creating APIs. One of the most exciting features is\nthat it can generate OpenAPI specs out of the box. But what if.. you have an\nOpenAPI spec and you need to create an API from it?\n\nOne day we faced that problem — we had to create an API from multiple OpenAPI\nspecs, and make sure that the incoming requests and the outgoing responses were\naligned with the models defined the specs.\n\n> ⚠️ This library was created to cover only our own needs first. So for now it\'s\n> not suitable for everyone and has a lot of technical restrictions. Please\n> consider it as experimental stuff\n\n## Installation\n\nThe package is available on PyPi:\n\n```bash\npip install openapi-to-fastapi\n```\n\n## Generating FastAPI routes\n\nThe main purpose of this library is to generate FastAPI routes from OpenAPI\nspecs. This is done by:\n\n```python\nfrom pathlib import Path\nfrom openapi_to_fastapi.routes import SpecRouter\n\nspecs = Path("./specs")\n\nrouter = SpecRouter(specs).to_fastapi_router()\n```\n\nThe code above will create a FastAPI router that can be either included into the\nmain router, or used as the default one.\n\nImagine you have a following spec (some parts are cut off for brevity):\n\n```json\n{\n  "openapi": "3.0.2",\n  "paths": {\n    "/Company/BasicInfo": {\n      "post": {\n        "requestBody": {\n          "required": true,\n          "content": {\n            "application/json": {\n              "schema": {\n                "$ref": "#/components/schemas/BasicCompanyInfoRequest",\n                "responses": {\n                  "200": {\n                    "content": {\n                      "application/json": {\n                        "schema": {\n                          "$ref": "#/components/schemas/BasicCompanyInfoResponse"\n                        }\n                      }\n                    }\n                  }\n                }\n              }\n            }\n          }\n        }\n      },\n      "components": {\n        "schemas": {\n          "BasicCompanyInfoRequest": {\n            "title": "BasicCompanyInfoRequest",\n            "required": ["companyId"],\n            "type": "object",\n            "properties": {\n              "companyId": {\n                "title": "Company Id",\n                "type": "string",\n                "example": "2464491-9"\n              }\n            }\n          },\n          "BasicCompanyInfoResponse": {\n            "title": "BasicCompanyInfoResponse",\n            "required": ["name", "companyId", "companyForm"],\n            "type": "object",\n            "properties": {\n              "name": {\n                "title": "Name of the company",\n                "type": "string"\n              },\n              "companyId": {\n                "title": "ID of the company",\n                "type": "string"\n              },\n              "companyForm": {\n                "title": "The company form of the company",\n                "type": "string"\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}\n```\n\nThe FastAPI route equivalent could look like this:\n\n```python\nclass BasicCompanyInfoRequest(pydantic.BaseModel):\n    companyId: str\n\nclass BasicCompanyInfoResponse(pydantic.BaseModel):\n    name: str\n    companyId: str\n    companyForm: str\n\n\n@router.post("/Company/BasicInfo", response_model=BasicCompanyInfoResponse)\ndef _route(request: BasicCompanyInfoRequest):\n    return {}\n\n```\n\nAnd `openapi-to-fastapi` can create it automagically.\n\n### Custom routes\n\nIn most cases it makes no sense to create an API without any business logic.\n\nHere\'s how to define it:\n\n```python\nfrom fastapi import Header, HTTPException\nfrom openapi_to_fastapi.routes import SpecRouter\n\nspec_router = SpecRouter("./specs")\n\n# Default handler for all POST endpoints found in the spec\n@spec_router.post()\ndef hello_world(params, x_my_token: str = Header(...)):\n    if x_my_token != "my_token":\n        raise HTTPException(status_code=403, detail="Sorry")\n    return {"Hello": "World"}\n\n# Specific endpoint for a "/pet" route\n@spec_router.post("/pet")\ndef create_pet(params):\n        pet = db.make_pet(name=params.name)\n        return pet.to_dict()\n\nrouter = spec_router.to_fastapi_router()\n```\n\n### API Documentation\n\nNow after you have a lot of routes, you might want to leverage another great\nfeature of FastAPI — auto documentation.\n\nRequest and response models are already handled. But to display documentation\nnicely, FastAPI needs to assign a name for each endpoint. Here is how you can\nprovide such name:\n\n```python\nfrom openapi_to_fastapi.routes import SpecRouter\n\nspec_router = SpecRouter("./specs")\n\n@spec_router.post(\n    "/pet",\n    name="Create a pet",\n    description="Create a pet",\n    response_description="A Pet",\n    tags=["pets"],\n)\ndef create_pet(params):\n    return {}\n\n# Or you can set the dynamic name based on API path\ndef name_factory(path: str, **kwargs):\n    return path.replace("/", " ")\n\n@spec_router.post(name_factory=name_factory)\ndef create_pet(params):\n    return {}\n\n```\n\n## OpenAPI validation\n\nThis package also provides a CLI entrypoint to validate OpenAPI specs. It\'s\nespecially useful when you need to define you own set of rules for validation.\n\nImagine your API specs are stored in a separate repository and maintained by\nanother team. You also expect that all OpenAPI specs have only one endpoint\ndefined (some internal agreement).\n\nNow you can set up a CI check and validate them on every push.\n\nFirstly create a file with a custom validator:\n\n```python\n# my_validator.py\n\nfrom openapi_to_fastapi.validator import BaseValidator, OpenApiValidationError\n\nclass CustomError(OpenApiValidationError):\n    pass\n\n# important: must be inherited from BaseValidator\nclass MyValidator(BaseValidator):\n\n    # implement this single method\n    def validate_spec(self, spec: dict):\n        if len(spec["paths"]) != 1:\n            raise CustomError("Only one endpoint allowed")\n```\n\nThen run the tool:\n\n```\nopenapi-validator --path ./standards -m my_validator.py -v MyValidator\n\n===============================================================================\nOpenAPI specs root path: ./standards\nValidators: DefaultValidator, MyValidator\n===============================================================================\nFile: ./standards/Current.json\n[PASSED]\n-------------------------------------------------------------------------------\nFile: ./standards/Metric.json\n[PASSED]\n-------------------------------------------------------------------------------\nFile: ./standards/BasicInfo.json\n[PASSED]\n-------------------------------------------------------------------------------\n===============================================================================\nSummary:\nTotal : 3\nPassed: 3\nFailed: 0\n===============================================================================\n```\n\nThis validator can also be reused when generating routes:\n\n```python\nrouter = SpecRouter(specs, validators=[MyValidator])\n```\n\n## License\n\nThis code is released under the BSD 3-Clause license. Details in the\n[LICENSE](./LICENSE) file.\n',
    'author': 'Digital Living International Ltd',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/digitalliving/openapi-to-fastapi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
