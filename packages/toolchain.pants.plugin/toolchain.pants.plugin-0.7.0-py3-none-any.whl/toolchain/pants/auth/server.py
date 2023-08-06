# Copyright © 2019 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.

import http
import time
from contextlib import suppress
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer  # type: ignore
from threading import Thread
from typing import Optional, Tuple
from urllib.parse import parse_qsl, urlparse

import pkg_resources


class AuthFlowHttpServer(ThreadingHTTPServer):
    class ServerHandler(BaseHTTPRequestHandler):
        CALLBACK_PATH = "/token-callback/"

        def _serve_favicon(self):
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            self.wfile.write(self.server.fav_icon)

        def _render_html_messages(self, *messages):
            self.wfile.write(b"<html><head><title>Toolchain Auth</title></head><body>")
            for msg in messages:
                self.wfile.write(f"<p>{msg}</p>".encode())
            self.wfile.write(b"</body></html>")

        def _unexpected_path(self, path: str):
            self.send_response(http.HTTPStatus.NOT_FOUND)
            self.end_headers()
            self._render_html_messages(f"Invalid path: {path}")

        def _accept_code(self, parsed_url):
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            query = dict(parse_qsl(parsed_url.query))
            auth_error = query.get("error")
            if auth_error:
                self._render_html_messages(f"The authentication flow has failed: {auth_error}")
                return
            code = query.get("code")
            state = query.get("state")
            success, error_message = self.server.set_access_token_code(code, state)
            if not success:
                self._render_html_messages(f"The authentication flow has failed: {error_message}.")
                return
            self._render_html_messages("The authentication flow has completed.", "You can close this browser window.")

        def do_GET(self):
            parsed_url = urlparse(self.path)
            if parsed_url.path == "/favicon.ico":
                return self._serve_favicon()
            if parsed_url.path == self.CALLBACK_PATH:
                return self._accept_code(parsed_url)
            return self._unexpected_path(parsed_url.path)

    @classmethod
    def create_server(cls, *, port: Optional[int], expected_state: str):
        if port:
            return cls(port, expected_state)
        for curr_port in range(8000, 8100):
            with suppress(OSError):
                return cls(curr_port, expected_state)
        # TODO: Pants exception (TaskError)
        raise Exception("Failed to create web server")

    def __init__(self, port, expected_state):
        super().__init__(("localhost", port), self.ServerHandler)
        with pkg_resources.resource_stream(__name__, "favicon.png") as fl:
            self.fav_icon = fl.read()
        self._thread = Thread(target=self._server_thread, daemon=True)
        self._server_url = f"http://localhost:{port}{self.ServerHandler.CALLBACK_PATH}"
        self._code = None
        self._expected_state = expected_state

    def _server_thread(self):
        self.serve_forever(poll_interval=0.2)

    def start_thread(self):
        self._thread.start()

    @property
    def server_url(self):
        return self._server_url

    def set_access_token_code(self, code: str, state: str) -> Tuple[bool, str]:
        if not code:
            return False, "Missing token exchange code"
        if self._expected_state != state:
            return False, f"Unexpected state value: {state} (expected {self._expected_state})"
        self._code = code
        return True, ""

    def wait_for_code(self, timeout_sec: int = 300) -> Optional[str]:
        # TODO: Failure scenarios
        timeout_time = time.time() + timeout_sec
        while not self._code and time.time() < timeout_time:
            time.sleep(0.1)
        self.shutdown()
        return self._code
