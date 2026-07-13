"""
Lightweight request validation helpers.

`require_json_fields` is a decorator you can put on any route that expects
a JSON body with certain required keys. Keeps routes.py files free of
repetitive `if not data.get(...)` checks.
"""
from functools import wraps
from flask import request
from middleware.error_handler import AppError


def require_json_fields(*fields):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True)
            if data is None:
                raise AppError("Request body must be valid JSON", 400)
            missing = [f for f in fields if not data.get(f)]
            if missing:
                raise AppError(f"Missing required field(s): {', '.join(missing)}", 400)
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def require_file(field_name="file"):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if field_name not in request.files or request.files[field_name].filename == "":
                raise AppError(f"Missing uploaded file field: {field_name}", 400)
            return fn(*args, **kwargs)
        return wrapper
    return decorator
