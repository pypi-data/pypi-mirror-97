"""
The below is COMING SOON
"""


from arc.middleware import Middleware
from starlette.requests import Request
import secrets


class SessionHandler:
    def __init__(self, app, secret_key=None):
        self.app = app
        self.lifetime = self.app.to_seconds(1, "hour")

        self.secret_key = secrets.token_urlsafe()

        self.initialized = False

    def init_session(self, request, response):
        if not request.cookies.get("secret_key"):
            key = secrets.token_urlsafe(50)
            response.set_cookie("secret_key", key+self.secret_key,
                                httponly=True, max_age=self.lifetime)
            
            self._dict = {}

            self._dict[key] = {}

            self.initialized = True

        self.initialized = True

    def __call__(self):
        assert self.initialized, "Session Not Initialized"
        return self._dict


# class SessionMiddleware(Middleware):
#     def process_request(self, req):
#         self.app.scope["current_secret"] = req.cookies.get("secret_key")

#     def process_response(self, req, res):
#         pass
