import asyncio
import functools
import inspect
import typing

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from starlette.websockets import WebSocket
from starlette.authentication import has_required_scope


def token_url(func):
    if not hasattr(func, 'auth_dict'):
        setattr(func, "auth_dict", {})
    func.auth_dict['token_url'] = True

    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def decorator(*args, **kwargs):
            return await func(*args, **kwargs)

        return decorator
    else:
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            return func(*args, **kwargs)

        return decorator


def requires(
        scopes: typing.Union[str, typing.Sequence[str]],
        status_code: int = 403,
        redirect: str = None,
) -> typing.Callable:
    scopes_list = [scopes] if isinstance(scopes, str) else list(scopes)

    def decorator(func: typing.Callable) -> typing.Callable:
        setattr(func, "auth_dict", {})
        func.auth_dict['auth_require'] = scopes
        func.auth_dict['auth_type'] = 'oauth2'
        func.auth_dict['name'] = "OAuth2PasswordBearer"

        # copy from starlette.authentication.requires below
        sig = inspect.signature(func)
        for idx, parameter in enumerate(sig.parameters.values()):
            if parameter.name == "request" or parameter.name == "websocket":
                type = parameter.name
                break
        else:
            raise Exception(
                f'No "request" or "websocket" argument on function "{func}"'
            )

        if type == "websocket":
            # Handle websocket functions. (Always async)
            @functools.wraps(func)
            async def websocket_wrapper(
                    *args: typing.Any, **kwargs: typing.Any
            ) -> None:
                websocket = kwargs.get("websocket", args[idx] if args else None)
                assert isinstance(websocket, WebSocket)

                if not has_required_scope(websocket, scopes_list):
                    await websocket.close()
                else:
                    await func(*args, **kwargs)

            return websocket_wrapper

        elif asyncio.iscoroutinefunction(func):
            # Handle async request/response functions.
            @functools.wraps(func)
            async def async_wrapper(
                    *args: typing.Any, **kwargs: typing.Any
            ) -> Response:
                request = kwargs.get("request", args[idx] if args else None)
                assert isinstance(request, Request)

                if not has_required_scope(request, scopes_list):
                    if redirect is not None:
                        return RedirectResponse(
                            url=request.url_for(redirect), status_code=303
                        )
                    raise HTTPException(status_code=status_code)
                return await func(*args, **kwargs)

            return async_wrapper

        else:
            # Handle sync request/response functions.
            @functools.wraps(func)
            def sync_wrapper(*args: typing.Any, **kwargs: typing.Any) -> Response:
                request = kwargs.get("request", args[idx] if args else None)
                assert isinstance(request, Request)

                if not has_required_scope(request, scopes_list):
                    if redirect is not None:
                        return RedirectResponse(
                            url=request.url_for(redirect), status_code=303
                        )
                    raise HTTPException(status_code=status_code)
                return func(*args, **kwargs)

            return sync_wrapper

    return decorator
