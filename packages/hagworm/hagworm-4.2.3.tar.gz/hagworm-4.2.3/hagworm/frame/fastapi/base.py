# -*- coding: utf-8 -*-

import os
import fastapi

from fastapi import __version__ as fastapi_version

from hagworm import hagworm_label, hagworm_slogan
from hagworm import __version__ as hagworm_version
from hagworm.extend.struct import Result
from hagworm.extend.asyncio.base import Utils
from hagworm.extend.logging import DEFAULT_LOG_FILE_ROTATOR, init_logger


DEFAULT_HEADERS = [(r'Server', hagworm_label)]


def create_fastapi(
        log_level=r'info', log_handler=None, log_file_path=None,
        log_file_rotation=DEFAULT_LOG_FILE_ROTATOR, log_file_retention=0xff,
        debug=False,
        routes=None,
        **setting
):

    init_logger(
        log_level.upper(),
        log_handler,
        log_file_path,
        log_file_rotation,
        log_file_retention,
        debug
    )

    environment = Utils.environment()

    Utils.log.info(
        f'{hagworm_slogan}'
        f'hagworm {hagworm_version}\n'
        f'fastapi {fastapi_version}\n'
        f'python {environment["python"]}\n'
        f'system {" ".join(environment["system"])}'
    )

    setting.setdefault(r'title', r'Hagworm')
    setting.setdefault(r'version', hagworm_version)

    return fastapi.FastAPI(debug=debug, routes=routes, **setting)


class Request(fastapi.Request):

    @property
    def referer(self):

        return self.headers.get(r'Referer')

    @property
    def client_ip(self):

        return self.headers.get(r'X-Read-IP', self.client.host)

    @property
    def x_forwarded_for(self):

        return Utils.split_str(self.headers.get(r'X-Forwarded-For', r''), r',')

    @property
    def content_type(self):

        return self.headers.get(r'Content-Type')

    @property
    def content_length(self):

        result = self.headers.get(r'Content-Length', r'')

        return int(result) if result.isdigit() else 0

    def get_header(self, name, default=None):

        return self.headers.get(name, default)


class Response(fastapi.responses.UJSONResponse):

    def render(self, content):
        return super().render(Result(data=content))


class ErrorResponse(Exception, fastapi.responses.UJSONResponse):

    def __init__(self, error_code, content=None, status_code=200, **kwargs):

        self.error_code = error_code

        Exception.__init__(self)
        fastapi.responses.UJSONResponse.__init__(self, content, status_code, **kwargs)

    def render(self, content):
        return super().render(Result(code=self.error_code, data=content))


class APIRoute(fastapi.routing.APIRoute):

    def get_route_handler(self):

        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: fastapi.Request):

            try:
                return await original_route_handler(
                    Request(request.scope, request.receive)
                )
            except ErrorResponse as error:
                return error

        return custom_route_handler


class APIRouter(fastapi.APIRouter):
    """目录可选末尾的斜杠访问
    """

    def __init__(
            self,
            *,
            prefix=r'',
            default_response_class=Response,
            route_class=APIRoute,
            **kwargs
    ):

        super().__init__(
            prefix=prefix,
            default_response_class=default_response_class,
            route_class=route_class,
            **kwargs
        )

    def _get_path_alias(self, path):

        _path = path.rstrip(r'/')

        if not _path:
            return [path]

        _path_split = os.path.splitext(_path)

        if _path_split[1]:
            return [_path]

        return [_path, _path + r'/']

    def api_route(self, path, *args, **kwargs):

        def _decorator(func):

            for index, _path in enumerate(self._get_path_alias(path)):

                self.add_api_route(_path, func, *args, **kwargs)

                # 兼容的URL将不会出现在docs中
                if index == 0:
                    kwargs[r'include_in_schema'] = False

            return func

        return _decorator
