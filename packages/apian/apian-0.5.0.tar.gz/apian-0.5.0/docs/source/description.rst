Description
============

Introduction
------------

Apian is an opinionated library for setting up a Python-based service with a
minimum of boilerplate. It is a thin wrapper around `flask-restplus
<https://pypi.org/project/flask-restplus/>`_ and provides:

* Documentation using OpenAPI.
* Info and health resources.
* JWT-based authentication.
* Configuration injection using `miniscule
  <https://pypi.org/project/miniscule/>`_.

Example
-------

Add a configuration file :code:`config.yaml` in the root of the project, with the
following contents:

.. code-block:: yaml

  environment: production
  debug: False
  authentication:
    enabled: True
    secret: secret

To create a Flask application and run it on :code:`localhost:5000`:

.. code-block:: python

  from apian import read_config, create_api, create_app, authenticated
  from flask_restplus import Namespace, Resource

  ns = Namespace("user")

  @ns.route("")
  class UserItem(Resource):

      @authenticated
      def get(self, user_id):
          return user_id

  config = read_config()
  api = create_app("my-app", config)
  api.add_namespace(ns)
  app = create_app(api, config)
  app.run()

The application has endpoints at the paths:

* :code:`GET /my-app/api/info` - Return information about the service.
* :code:`GET /my-app/api/health` - Return the health status of the service.
* :code:`GET /my-app/api/user` - Return the user ID set in the Bearer token.

To access the user resource, ensure that the `requests
<https://pypi.org/project/requests/>`_ package is installed and execute the
following snippet:

.. code-block:: python

  import jwt
  import requests

  def auth_token():
    user_id = 10
    claims = {"iat": dt.datetime.utcnow(), "sub": user_id}
    key = "secret"
    return jwt.encode(claims, key, "HS256")

  headers = {"Authorization": "Bearer {}".format(
  requests.get("http://localhost:5000/my-app/api/user", headers=headers)
