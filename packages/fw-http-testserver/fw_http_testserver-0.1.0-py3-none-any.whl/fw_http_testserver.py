"""HTTP test server to make testing easy with external APIs."""
import threading
from unittest.mock import patch

import flask
import pytest
import requests
from fw_utils import AttrDict


class HttpTestServer(threading.Thread):
    """HTTP server with on-the-fly handler configuration for unit testing."""

    def __init__(self, port=5000):
        super().__init__()
        self.host = "localhost"
        self.port = port
        self.addr = f"{self.host}:{self.port}"
        self.url = f"http://{self.addr}"
        self.app = flask.Flask(self.__class__.__name__)
        self.app.before_request(self._track_request)
        self.reset()

    def __getattr__(self, name: str):
        """Proxy attributes of flask for simple access."""
        return getattr(flask, name)

    def __repr__(self) -> str:
        """Return string representation of the test server."""
        return f"{type(self).__name__}(port={self.port})"

    def run(self):
        """Thread entrypoint called upon start()."""
        with patch("flask.cli.show_server_banner"):
            self.app.run(port=self.port)

    def _track_request(self):
        """Track each incoming request for test assertions later."""
        request = flask.request
        body = request.get_data()  # read/store before accessing .files
        self.requests_log.append(f"{request.method} {request.path}")
        self.requests.append(
            AttrDict(
                method=request.method,
                url=request.path,
                params=AttrDict(request.args),
                headers=AttrDict(request.headers),
                form=AttrDict(request.form),
                body=body,
                json=request.get_json(silent=True),
                files={k: v.getvalue() for k, v in request.files.items()},
            )
        )

    # pylint: disable=too-many-arguments
    def add_response(self, url, body="", method="GET", status=200, headers=None):
        """Add handler that responds with given body, status and headers."""

        def callback():
            data = flask.jsonify(body) if isinstance(body, list) else body
            return data, status, headers or {}

        self.add_callback(url, callback, methods=[method])

    def add_callback(self, url, callback, methods=("GET",)):
        """Add a custom callback as a handler."""
        callback.__name__ = "_".join([url, *sorted(methods)])
        # allow overriding view function
        self.app.view_functions.pop(callback.__name__, None)
        self.app.add_url_rule(url, methods=methods, view_func=callback)

    def reset(self):
        """Restore initial state."""
        self.requests = []
        self.requests_log = []
        self.app.url_map = self.app.url_map_class()
        self.app.view_functions = {"static": self.app.view_functions["static"]}
        self.app.add_url_rule("/shutdown", view_func=self._shutdown)

    def shutdown(self):
        """Trigger shutdown by sending GET /shutdown."""
        requests.get(f"{self.url}/shutdown")
        self.join()

    def _shutdown(self):
        """Shutdown server upon receiving GET /shutdown."""
        if "werkzeug.server.shutdown" not in flask.request.environ:
            raise RuntimeError("Not running the development server")  # pragma: no cover
        flask.request.environ["werkzeug.server.shutdown"]()
        return f"Shutting down {self}"


@pytest.fixture(scope="session")
def _server():
    """Session scoped HTTP server fixture that shuts down upon exit."""
    http_server = HttpTestServer()
    http_server.start()
    yield http_server
    http_server.shutdown()


@pytest.fixture(scope="function")
def server(_server):
    """Function scoped HTTP server fixture that cleans state after each test."""
    yield _server
    _server.reset()
