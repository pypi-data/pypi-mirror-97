from pythonit_toolkit.starlette_backend.pastaporto_backend import PastaportoAuthBackend, on_auth_error
from starlette.middleware import Middleware

from starlette.middleware.authentication import AuthenticationMiddleware

pastaporto_auth_middleware = Middleware(
    AuthenticationMiddleware,
    backend=PastaportoAuthBackend(),
    on_error=on_auth_error,
)
