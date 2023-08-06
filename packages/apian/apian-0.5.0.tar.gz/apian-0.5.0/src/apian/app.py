import logging
import os

from flask import Blueprint, Flask, url_for
from flask_restplus import Resource, apidoc, Namespace
from werkzeug.middleware.proxy_fix import ProxyFix

from apian.api import CustomAPI
from apian.auth import AUTH_CONFIG_KEY, authentication_enabled
from apian.config import init_logging
from apian.meta import read_version

log = logging.getLogger(__name__)


def create_api(name, config, *, title=None, **extra):
    # pylint: disable=unused-variable
    """Create an API with info and health endpoints.

    :param name: The name of the application; used in the generated frontend,
        and the URL prefix.
    :param config: The application configuration.

    :returns: An instance of :class:`~apian.api.CustomAPI`.
    """
    if "prefix" in extra:
        prefix = extra.pop("prefix")
    else:
        prefix = "/{}/api".format(name)
    title = _title_from_name(name) if title is None else title
    blueprint = Blueprint(prefix, __name__)
    if authentication_enabled(config.get(AUTH_CONFIG_KEY)):
        extra["security"] = "Bearer Auth"

        extra["authorizations"] = {
            "Bearer Auth": {"type": "apiKey", "in": "header", "name": "Authorization"}
        }

    api = CustomAPI(blueprint, title=title, prefix=prefix, doc=prefix + "/", **extra)
    ns = Namespace(name="Generic", path="/")

    @ns.route("/info")
    class Info(Resource):
        def get(self):
            # pylint: disable=no-self-use
            """Show information about the service"""
            return {"name": name, "version": read_version(), "config": config["__path"]}

    @ns.route("/health")
    class Health(Resource):
        def get(self):
            # pylint: disable=no-self-use
            """Check the health of the service"""
            return {"status": "ok"}

    api.add_namespace(ns)
    return api


def create_app(api, config):
    """Create a WSGI app.

    :param api: The API to serve, should be an instance of :class:`~CustomAPI`.
    :param config: Configuration for the app.  The following keys have an
        effect: 'debug', 'environment', '__path', 'log_config'.

    :returns: A WSGI app.
    """

    init_logging(config.get("log_config"))
    app = Flask(__name__)
    app.config.update(config)

    app.config["DEBUG"] = config.get("debug", False)
    app.config["ENV"] = config.get("environment", "production")

    swagger = _create_swagger()
    app.register_blueprint(api.blueprint)
    app.register_blueprint(swagger, url_prefix=api.prefix)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app


def _create_swagger():
    swagger = apidoc.Apidoc(
        "restplus_custom_doc",
        __name__,
        template_folder="templates",
        static_folder=os.path.dirname(apidoc.__file__) + "/static",
        static_url_path="/swagger",
    )

    @swagger.add_app_template_global
    def swagger_static(filename):
        # pylint: disable=unused-variable
        return url_for("restplus_custom_doc.static", filename=filename)

    return swagger


def _is_authenticated(config):
    if "authentication" not in config:
        return False
    return config["authentication"].get("enabled", True)


def _title_from_name(name):
    return " ".join(name.split("-")).title()
