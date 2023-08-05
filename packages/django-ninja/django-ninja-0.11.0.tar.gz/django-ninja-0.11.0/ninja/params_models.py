from pydantic import BaseModel
from django.conf import settings
from ninja.compatibility import get_headers
from ninja.errors import HttpError


class ParamModel(BaseModel):
    @classmethod
    def resolve(cls, request, api, path_params):
        data = cls.get_request_data(request, api, path_params)
        if data is None:
            return cls()

        varname = getattr(cls, "_single_attr", None)
        if varname:
            data = {varname: data}
        # TODO: I guess if data is not dict - raise an HttpBadRequest
        return cls(**data)


class QueryModel(ParamModel):
    @classmethod
    def get_request_data(cls, request, api, path_params):
        list_fields = getattr(cls, "_collection_fields", [])
        return api.parser.parse_querydict(request.GET, list_fields, request)


class PathModel(ParamModel):
    @classmethod
    def get_request_data(cls, request, api, path_params):
        return path_params


class HeaderModel(ParamModel):
    @classmethod
    def get_request_data(cls, request, api, path_params):
        data = {}
        headers = get_headers(request)
        for name, field in cls.__fields__.items():
            if name in headers:
                data[name] = headers[name]
            elif field.alias in headers:
                data[field.alias] = headers[field.alias]
        return data


class CookieModel(ParamModel):
    @classmethod
    def get_request_data(cls, request, api, path_params):
        return request.COOKIES


class BodyModel(ParamModel):
    @classmethod
    def get_request_data(cls, request, api, path_params):
        if request.body:
            try:
                return api.parser.parse_body(request)
            except Exception as e:
                msg = "Cannot parse request body"
                if settings.DEBUG:
                    msg += f" ({e})"
                raise HttpError(400, msg)


class FormModel(ParamModel):
    @classmethod
    def get_request_data(cls, request, api, path_params):
        list_fields = getattr(cls, "_collection_fields", [])
        return api.parser.parse_querydict(request.POST, list_fields, request)


class FileModel(ParamModel):
    @classmethod
    def get_request_data(cls, request, api, path_params):
        list_fields = getattr(cls, "_collection_fields", [])
        return api.parser.parse_querydict(request.FILES, list_fields, request)
