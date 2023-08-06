import sysconfig
from pathlib import Path
import time

import pkg_resources
import yaml
from flask import Flask, escape, render_template, send_from_directory
# from flask_threaded_sockets import Sockets

try:
    __version__ = pkg_resources.get_distribution("brython-dev").version
except pkg_resources.DistributionNotFound:
    __version__ = "unknown"


def create_app(config: dict = {}) -> Flask:
    app = Flask(__name__, static_folder=str(Path.cwd()), static_url_path="/")

    config_file = Path("brython.yml").resolve()
    if config_file.exists():
        parse = yaml.safe_load(config_file.read_text()) or {}

        app.config["NAME"] = parse.get("name") or "Unnamed"
        app.config["STYLESHEETS"] = parse.get("stylesheets") or []
        app.config["EXTENSIONS"] = parse.get("extensions") or {}
        app.config["USE_BRYTHON"] = app.config["EXTENSIONS"].get("brython", True)
        app.config["USE_BRYTHON_STDLIB"] = app.config["EXTENSIONS"].get(
            "brython_stdlib"
        )
        app.config["SCRIPTS"] = parse.get("scripts") or []
        brython_options = parse.get("brython_options") or {"debug": 1}
        app.config["BRYTHON_OPTIONS"] = escape(
            "{" + ", ".join(f"{k}: {v}" for k, v in brython_options.items()) + "}"
        )
        app.config["APP"] = parse.get("app") or "app.py"
        app.config["TEMPLATE"] = parse.get("template") or "app.html"
        app.config["TEMPLATE_TEXT"] = Path(app.config["TEMPLATE"]).read_text() if Path(app.config["TEMPLATE"]).exists() else ""

    app.config.from_mapping(config)

    @app.route("/")
    def index():
        return render_template(
            "index.html",
            name=app.config["NAME"],
            stylesheets=app.config["STYLESHEETS"],
            use_brython=app.config["USE_BRYTHON"],
            use_brython_stdlib=app.config["USE_BRYTHON_STDLIB"],
            scripts=app.config["SCRIPTS"],
            brython_options=app.config["BRYTHON_OPTIONS"],
            app=app.config["APP"],
            template=app.config["TEMPLATE_TEXT"],
        )

    @app.route("/brython.js")
    def brythonjs():
        return send_from_directory(
            sysconfig.get_path("purelib"), "brython/data/brython.js"
        )

    @app.route("/brython_stdlib.js")
    def brythonstdlibjs():
        return send_from_directory(
            sysconfig.get_path("purelib"), "brython/data/brython_stdlib.js"
        )

    @app.route("/Lib/site-packages/<path:filename>")
    def site_packages(filename: str):
        return send_from_directory(sysconfig.get_path("purelib"), filename)

    # sockets = Sockets(app)
    # @sockets.route('/ws/console')
    # def echo_socket(ws):
        # print(dir(ws))
        # print(ws.raw_read())
        # while True:
            # message=""
            # if not ws.closed:
                # message = ws.receive()
                # print("recibido: "+str(message))
                # if message and not ws.closed:
                    # ws.send(message)
                    # print("enviado")
            # time.sleep(0.5)

    return app
