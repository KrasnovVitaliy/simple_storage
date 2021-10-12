from invoke import Collection
from . import openapi
from . import service

ns = Collection()
ns.add_collection(openapi)
ns.add_collection(service)

