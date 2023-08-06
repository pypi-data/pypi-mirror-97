# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['routerling']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'routerling',
    'version': '0.1.5',
    'description': 'Extremely Stupid Simple, Blazing Fast, Get Out of your way immediately Microframework for building Python Web Applications.',
    'long_description': '**********\n# Routerling\n\nA new born baby router on it\'s way to being a web development platform. Routerling is a router\nmultiplexer built with 1 goal in mind.\n\n- Make it stupid simple to build high performance web applications\n\n\n## How?\nFollowing the unix philosophy of be the master of one thing and one thing only - Routerling has only **ONE** API you need to learn - `Router`. The API is also deliberately made\nconsistent across the 3 different supported languages [Golang, Python, Typescript/JavaScript].\n[See Similarities](#similarities)\n\n&nbsp;\n\n## Python\n\n```py\nfrom routerling import Context, HttpRequest, ResponseWriter, Router\nfrom logging import log\n\ndef get_customer_orders(r: HttpRequest, w: ReponseWriter, s: State):\n    w.headers = "go-go-gadget", ""\n    w.body = \'{customer: {customer_id}, orders: []}\'.format(r.params.get(\'id\'))\n\ndef change_headers(r: HttpRequest, w: ResponseWriter, s: State):\n    w.headers = "go-go-gadget", "i was changed after..."\n\ndef create_customer(r: HttpRequest, w: ResponseWriter, s: State):\n    print(r.body)\n    w.status = 201\n    w.body = \'{id: 13}\'\n\n\n# register functions to routes\nrouter.BEFORE(\'/*\', lambda req, res, state: print(\'will run before all routes are handled\'))\nrouter.AFTER(\'/v1/customers/*\', change_headers)\nrouter.GET(\'/v1/customers/:id/orders\', get_customer_orders)\nrouter.GET(\'/v1/customers/:id\', lambda req, res, state: log(2, state.abcxyz_variable))\nrouter.POST(\'/v1/customers\', create_customer)\n```\n\n### Serve your application\n```sh\nuvicorn app:router\n```\n\n\n&nbsp;\n\n\n## Request Object\n\n- **request.body**\n    > Body/payload of request if it exists. You can use any `XML, JSON, CSV etc.` library you prefer\n    > to parse `r.body` as you like.\n    ```py\n    # r.body: str\n    body: str = r.body\n    ```\n\n- **request.headers** `header = r.headers.get(\'header-name\')`\n    > All headers sent with the request.\n    ```py\n    # r.headers: dict\n    header = r.headers.get(\'content-type\')\n    ```\n\n- **request.params** `param = r.params.get(\'param-name\')`\n    > Dictionary containing parts of the url that matched your route parameters i.e. `/customers/:id/orders` will\n    > return `{\'id\': 45}` for url `/customers/45/orders`.\n    ```py\n    body: str = r.body\n    ```\n\n&nbsp;\n\n## Response Object\n\n- **response.abort**\n    > Signals to routerling that you want to abort a request and ignore all `GET`, `POST`, `PUT etc.` handlers including all\n    > `AFTER` or `BEFORE` hooks from executing. The payload given to abort is used as the response body.\n    > Only calling `w.abort() will not end function execution.` You have to explicitly return from the request handler after using w.abort().\n\n    ```py\n    w.abort(\'This is the body/payload i want to abort with\')\n    return\n    ```\n\n- **response.body**\n    > Used to set payload/body to be sent back to the client. Returning data from a handler function does not do\n    > anything and is not used by routerling. `To send something back to the client use w.body`.\n\n    ```py\n    w.body = b\'my body\'\n    ```\n\n- **response.headers**\n    > Used to set headers to be sent back to the client.\n\n    ```py\n    w.headers = "Content-Type", "application/json"\n    w.headers = ["Authorization", "Bearer myToken"]\n    ```\n\n&nbsp;\n\n## Context Object\n\n> Documentation coming soon\n\n\n&nbsp;\n\n&nbsp;\n\n# Socket Connections\n\n> Documentation coming soon\n',
    'author': 'Raymond Ortserga',
    'author_email': 'ortserga@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
