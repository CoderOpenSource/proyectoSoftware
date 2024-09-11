def get_user_from_token(token):
    from rest_framework_simplejwt.tokens import UntypedToken
    from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
    from django.contrib.auth.models import AnonymousUser
    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        UntypedToken(token)
        user_id = UntypedToken(token)['user_id']
        return User.objects.get(id=user_id)
    except (InvalidToken, TokenError, User.DoesNotExist):
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)

class TokenAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.scope = dict(scope)
        self.middleware = middleware

    async def __call__(self, receive, send):
        from channels.db import database_sync_to_async

        @database_sync_to_async
        def get_user():
            query_string = self.scope['query_string'].decode()
            token = dict(item.split('=') for item in query_string.split('&')).get('token', None)
            return get_user_from_token(token)

        self.scope['user'] = await get_user()
        inner = self.middleware.inner(self.scope)
        return await inner(receive, send)

def TokenAuthMiddlewareStack(inner):
    from channels.auth import AuthMiddlewareStack
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))

