"""
Custom Channels middleware to authenticate WebSocket connections via JWT query token.
This middleware extracts the JWT token from the query string of the WebSocket connection,
validates it, and attaches the corresponding user to the connection scope for use in chat consumers.
"""

from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


@database_sync_to_async
def _get_user_from_token(token: str):
    """
    Validate the JWT token and return the associated user.
    If the token is invalid or expired, return an AnonymousUser.
    """

    jwt_auth = JWTAuthentication()
    try:
        validated_token = jwt_auth.get_validated_token(token)
        return jwt_auth.get_user(validated_token)
    except (InvalidToken, TokenError, Exception):
        return AnonymousUser()


class JwtAuthMiddleware:
    """
    Custom middleware for JWT authentication in Channels.
    Extracts the token from the query string, validates it, and attaches the user to the scope.
    If the token is invalid or missing, the user will be set to AnonymousUser.
    """ 
    
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        """
        Authenticate the user based on the JWT token in the query string and attach it to the scope.
        """
        
        scope["user"] = AnonymousUser()

        query_string = scope.get("query_string", b"").decode("utf-8")
        params = parse_qs(query_string)
        token = params.get("token", [None])[0]

        if token:
            scope["user"] = await _get_user_from_token(token)

        return await self.app(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    """
    Helper function to apply the JWT authentication middleware to the Channels application stack.
    """

    return JwtAuthMiddleware(inner)