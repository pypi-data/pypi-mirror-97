from collections import deque
from inspect import iscoroutinefunction

from typing import Callable, Generic, TypeVar

from .constants import (
    CONNECT,
    DELETE,
    GET,
    HEAD,
    MESSAGE_NOT_FOUND,
    METHOD_CONNECT,
    METHOD_DELETE,
    METHOD_GET,
    STATUS_NOT_FOUND,
    OPTIONS,
    PATCH,
    POST,
    PUT,
    TRACE
)

from .request import HttpRequest
from .response import ResponseWriter
from .context import Context


methods = ['get', 'post', 'put', 'delete', 'connect', 'head', 'options', 'patch']


Handler = Callable[[HttpRequest, ResponseWriter], object]


MARK_PRESENT = 'yes father... (RIP Rev. Angus Fraser...)'
SEPARATOR = INDEX = "/"


def isparamx(r: str):
    return (':', r[1:],) if r.startswith(':') else (r, None,)


def isvariable(r: str):
    newr = ':' if r.startswith(':') else r
    return newr, newr != r or r == '*'


class Route(object):
    def __init__(self, route: str, handler: Callable, name: str) -> None:
        self.parameterized = False
        self.route = route
        self.name = name
        self.handler = handler
        self.children = {}
    
    def add(self, pathstring: deque, handler):
        # We can do this with confidence because we use cache to ensure url mask not used twice
        node = self
        while pathstring:
            route = pathstring.popleft()
            url, parameterized = isparamx(route)
            current_node = node.children.get(route)
            if not current_node:
                url, func, name = None, None, None
                current_node = Route(url, func, name)
                node.children[route] = current_node
            node = current_node
            node.parameterized = parameterized
        node.handler = handler

    def match(self, routes: deque, r: HttpRequest):
        matched = None
        node = self
        mylist = list(routes)
        while routes:
            route = routes.popleft()
            current_node = node.children.get(route)
            if not current_node:
                # is there a parameterized child?
                current_node = node.children.get(':')
                if current_node:
                    # what to do here
                    r.params = current_node.parameterized, route
                    node = current_node
                    continue

                # is there a wild card child? the minute a wildcard is seen all bets are off and children make no sense after it
                wildcard = node.children.get('*')
                if wildcard:
                    return wild_card.route, wild_card.handler

                return matched, self.not_found
            node = current_node
        return node.route, node.handler
    
    def not_found(self, r: HttpRequest, w: ResponseWriter, c: Context):
        w.status = 404
        w.body = b'Not found'
    
    def retrieve(self, match: str):
        pass


class Routes(object):
    def __init__(self):
        self.afters = {}
        self.befores = {}

        self.cache = {CONNECT: {}, DELETE: {}, GET: {}, HEAD: {}, OPTIONS: {}, PATCH: {}, POST: {}, PUT: {}, TRACE: {}}
        self.routes = {}

    def add(self, method: str, route: str, handler: Callable, name: str = None):
        # ensure the method and route combo has not been already registered
        assert self.cache.get(method, {}).get(route) is None
        self.cache[method][route] = MARK_PRESENT

        # here we check and set the root to be a route node i.e. / with no handler
        # if necessary so we can traverse freely
        route_node: Route = self.routes.get(method)
        if not route_node:
            route_node = Route(None, None, None)
            self.routes[method] = route_node

        if route == SEPARATOR:
            route_node.route = route
            route_node.handler = handler
            route_node.name = name
            return

        # Otherwise strip and split the routes into stops or stoppable stumps i.e. /customers /:id /orders
        routes = route.strip(SEPARATOR).split(SEPARATOR)

        # get the length of the routes so we can use for validation checks in a loop later
        stop_at = len(routes) - 1

        for index, routerling in enumerate(routes):
            routerling, parameterized = isparamx(routerling)
            new_route_node = route_node.children.get(routerling)
            if not new_route_node:
                new_route_node = Route(None, None, None)
                route_node.children[routerling] = new_route_node
            
            route_node = new_route_node
            route_node.parameterized = parameterized

            if index == stop_at:
                assert route_node.handler is None, f'Handler already registered for route: ${routerling}'
                route_node.route = route
                route_node.name = name
                route_node.handler = handler
    
    @property
    def before(self):
        raise KeyError('Not readable')

    @before.setter
    def before(self, values):
        route, handler = values
        routes = self.befores.get(route)
        if routes:
            route.append(handler)
        else:
            self.befores[route] = [handler]
    
    def get_handler(self, routes):
        for route in routes:...
        return None, None

    async def handle(self, scope, receive, send):
        """
        Traverse internal route tree and use appropriate method
        """
        body = await receive()

        r = HttpRequest(scope, body, receive)
        w = ResponseWriter(scope)
        c = Context()

        method = scope.get('method')
        matched = None
        handler = None

        # if the cache has nothing under its GET, POST etc it means nothing's been registered and we can leave early
        roots = self.cache.get(method, {})
        if not roots:
            return w

        # if no route node then no methods have been registered
        route_node = self.routes.get(method)
        if not route_node:
            return w

        route = scope.get('path')
        if route == SEPARATOR:
            matched = route_node.route # same as = SEPARATOR
            handler = route_node.handler
        else:
            routes = route.strip(SEPARATOR).split('/')
            matched, handler = route_node.match(deque(routes), r)

        if not matched:
            return w

        # call all pre handle request hooks but first reset response_writer from not found to found
        w.status = 200; w.body = b''
        await self.xhooks(self.befores, matched, r, w, c)

        # call request handler
        if iscoroutinefunction(handler): await handler(r, w, context)
        else: handler(r, w, c)

        # call all post handle request hooks
        await self.xhooks(self.afters, matched, r, w, c)

        # too many hooks is not good for the pan ;-)
        # i.e. hook lookup is constant but running many hooks will
        # increase the time it takes before the response is released to the network
        return w

    async def xhooks(self, hooks, matched, r: HttpRequest, w: ResponseWriter, c: Context):
        # traverse the before tree - changed to tree to match routes tree
        # for every * add it to list of hooks to call
        # if match also add functions there to list of hooks to call
        pass


class Router(object):
    def __init__(self) -> None:
        self.rtx = Routes()
    
    async def __call__(self, scope, receive, send):
        response = await self.rtx.handle(scope, receive, send)
        await send({
            'type': 'http.response.start',
            'headers': response.headers,
            'status': response.status
        })
        await send({
            'type': 'http.response.body',
            'body': response.body
        }) 

    def abettor(self, method: str, route: str, handler: Handler, name: str = None):
        self.rtx.add(method, route, handler, name)

    def AFTER(self, route: str, handler: Callable, name: str):
        pass

    def BEFORE(self, route: str, handler: Callable, name: str = None):
        self.rtx.before = route, handler

    def CONNECT(self, route: str, handler: Callable[[HttpRequest, ResponseWriter], object], name: str):
        self.abettor(METHOD_CONNECT, route, handler, name)

    def DELETE(self, route: str, handler: Callable, name: str = None):
        self.abettor(METHOD_DELETE, route, handler, name)
    
    def GET(self, route: str, handler: Callable, name: str = None):
        self.abettor(METHOD_GET, route, handler, name)
    
    def POST(self, route: str, handler: Callable, name: str = None):
        self.abettor(POST, route, handler, name)

    def listen(self, host='localhost', port='8701', debug=False):
        pass
