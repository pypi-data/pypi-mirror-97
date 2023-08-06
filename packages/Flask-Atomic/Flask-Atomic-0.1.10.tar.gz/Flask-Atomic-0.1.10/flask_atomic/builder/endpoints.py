import json

from flask import request

from sqlalchemy_blender import QueryBuffer
from sqlalchemy_blender.helpers import tojson
from sqlalchemy_blender.helpers import get_model_from_relationship

from handyhttp.responses import HTTPSuccess
from handyhttp.responses import HTTPCreated
from handyhttp.responses import HTTPUpdated
from handyhttp.responses import HTTPDeleted
from handyhttp.exceptions import HTTPConflict
from handyhttp.exceptions import HTTPBadRequest
from handyhttp.exceptions import HTTPNotFound
from handyhttp.exceptions import HTTPNotProcessable

# from flask_atomic.helpers import session
from .cache import link


def route(rule, **options):
    """
    A decorator that is used to define custom routes for methods in
    FlaskView subclasses. The format is exactly the same as Flask's
    `@app.route` decorator.
    """

    def decorator(f):
        # Put the rule cache on the method itself instead of globally
        if not hasattr(f, '_rule_cache') or f._route_cache is None:
            f._route_cache = {f.__name__: [(rule, options)]}
        elif f.__name__ not in f._rule_cache:
            f._route_cache[f.__name__] = [(rule, options)]
        else:
            f._route_cache[f.__name__].append((rule, options))
        return f
    return decorator


class Routes:
    def __init__(self, model, dao, key, throw=True, response=None):
        self.model = model
        self.dao = dao
        self.key = key
        self.throw = throw
        self.response = response
        self.errors = list()

    def views(self):
        return list([i for i in self.__class__.__dict__.values() if hasattr(i, '_route_cache')])

    def refresh(self):
        self.errors.clear()

    def payload(self):
        return json.loads(request.data)

    def bake(self, http, data=None, metadata=None, **kwargs):
        return http(data, **self.metadata(**kwargs, **dict(metadata=dict(count=len(data or [])))))

    def metadata(self, **kwargs):
        resp = dict()
        resp['links'] = {}
        resp['links']['self'] = request.url
        resp['links']['_self'] = request.base_url
        resp['metadata'] = dict(args=dict(request.args))
        resp['errors'] = self.errors

        if kwargs:
            resp['metadata'].update(kwargs)
        return resp

    def json(self, data, *args, **kwargs):
        resp = tojson(data, *args, **kwargs)
        return resp

    @link(url='', methods=['GET'])
    @route('', methods=['GET'])
    def get(self, *args, **kwargs):
        """
        The principal GET handler for the RouteBuilder. All GET requests that are
        structured like so:

        `HTTP GET http://localhost:5000/<prefix>/<route-model>`

        (Where your-blueprint represents a particular resource mapping).

        Will be routed to this function. This will use the RouteBuilder DAO
        and then fetch data for the assigned model. In this case, select all.

        :return: response object with application/json content-type preset.
        :rtype: HTTPSuccess
        """

        print(request.args.to_dict(flat=False))
        query = QueryBuffer(self.model).apply().all()
        self.errors.extend(query.errors)
        return self.bake(HTTPSuccess, self.json(query.data, **query.queryargs.__dict__))

    @link(url='/<resource>', methods=['HEAD'])
    @route('/<resource>', methods=['HEAD'])
    def head(self, resource):
        query = QueryBuffer(self.model)
        resp = query.one(self.key, resource)

        if not resp:
            raise HTTPNotFound()
        return self.bake(HTTPSuccess)

    @link(url='/<resource>', methods=['GET'])
    @route('/<resource>', methods=['GET'])
    def one(self, resource, *args, **kwargs):
        """
        The principal GET by ID handler for the RouteBuilder. All GET requests
        that are structured like so:

        `HTTP GET http://localhost:5000/<prefix>/<route-model>/<uuid>`

        (Where <your-blueprint> represents a particular resource mapping).

        (Where <uuid> represents an database instance ID).

        This will use the RouteBuilder DAO and then fetch data for the
        assigned model. In this case, selecting only one, by UUID.

        :return: response object with application/json content-type preset.
        :rtype: Type[JsonResponse]
        """

        if isinstance(resource, str) and resource.endswith('/'):
            resource = resource.split('/').pop(0)

        query = QueryBuffer(self.model)
        resp = query.one(self.key, resource)

        if not resp.data:
            raise HTTPNotFound(f'{self.model.__tablename__} not found')
        return self.bake(HTTPSuccess, self.json(query.data, **query.queryargs.__dict__))

    @link(url='/<resource>/<path:field>', methods=['GET'])
    @route('/<resource>/<path:field>', methods=['GET'])
    def one_child_resource(self, resource, field, *args, **kwargs):
        """
        This endpoint takes a parent tablename as argument and a resource path
        which can be n number of levels deep. If the path is > 1 levels deep
        it will loop over the nested relationships and pluck out the final
        element in the path.

        :param resource:
        :param field:
        :param args:
        :param kwargs:
        :return:
        """

        query = QueryBuffer(self.model, auto=False).one(self.key, resource)
        instance = query.one(self.key, resource).data
        path = field.split('/')
        prop = None

        if not instance:
            raise HTTPNotFound(f'{self.model.__tablename__} not found')

        if field not in self.model.__mapper__.relationships:
            return self.bake(HTTPSuccess, {field: getattr(instance, field)})

        session = query.session
        tree = False
        if request.args.get('tree', False):
            tree = [tojson(instance)]
            del request['tree']

        if len(path) > 1:
            child = None
            data = query.data
            endpoint = path.pop()
            for idx, item in enumerate(path):
                if isinstance(data, int) or isinstance(data, str):
                    raise HTTPBadRequest(msg='Cannot query this data type')
                if isinstance(data, list):
                    child = data[int(item)]
                else:
                    child = getattr(instance, item)
            data = getattr(child, endpoint)
            prop = endpoint
        else:
            # session.query(arti).join(arti, self.model.articles).filter(arti.active=='Y').order_by(arti.created).all()
            related = get_model_from_relationship(self.model, field)
            iquery = session.query(related).join(getattr(self.model, field))
            iquery = iquery.filter(getattr(self.model, self.key) == getattr(instance, self.key))

            # session.query(related).join(self.model.articles).filter(self.model.id==2).all()

            iquery = QueryBuffer(related).build(iquery, query.queryargs)
            data = iquery.all()

        resp = {
            self.model.__tablename__: self.json(instance, **query.queryargs.__dict__),
            field: self.json(data, **query.queryargs.__dict__)
        }
        return self.bake(
            HTTPSuccess,
            resp,
            **{
                'content': {
                    'model': prop,
                    'parent': tojson(instance)
                },
            }
        )

    @link(url='/', methods=['POST'])
    @route('/', methods=['POST'])
    def post(self, *args, **kwargs):
        payload = request.json
        if not payload:
            raise HTTPNotProcessable(msg='Invalid request payload.')
        instance = self.dao.create(payload, **kwargs)
        # self.dao.save(HTTPCreated)
        return self.bake(HTTPSuccess, self.json(instance))

    @link(url='/<resource>/<field>/', methods=['POST'])
    @route('/<resource>/<field>/', methods=['POST'])
    def post_child_resource(self, resource, field, *args, **kwargs):
        instance = QueryBuffer(self.model).one(self.key, resource).data
        child = getattr(self.model.__mapper__.relationships, field).entity.entity(**self.payload())
        getattr(instance, field).append(child)
        self.dao.save(instance)
        return self.bake(HTTPSuccess, self.json(instance))

    @link(url='/<resource>', methods=['DELETE'])
    @route('/<resource>', methods=['DELETE'])
    def delete(self, resource, *args, **kwargs):
        instance = QueryBuffer(self.model).one(self.key, resource)
        if not instance.data:
            raise HTTPNotFound()

        if self.dao:
            self.dao.delete(instance.data)
        return self.bake(HTTPDeleted)

    @link(url='/<resource>', methods=['PUT'])
    @route('/<resource>', methods=['PUT'])
    def put(self, resource, *args, **kwargs):
        query = QueryBuffer(self.model).one(self.key, resource)
        instance = query.data
        payload = self.payload()
        self.dao.update(instance, payload)
        return self.bake(HTTPUpdated, self.json(instance))
