from functools import wraps
from flask import session, render_template, request, current_app


def login_required(func):
    @wraps(func)
    def wrapper(*argc, **kwargs):
        if 'id_user' in session:
            return func(*argc, **kwargs)
        return render_template('no_access.html')

    return wrapper


def group_validation(config: dict):
    endpoint_app = request.endpoint.split('.')[0]
    handler = request.endpoint.split('.')[-1]
    print(request.endpoint)
    if 'group_user' in session:
        group = session['group_user']
        if group in config and endpoint_app in config[group] and handler in config[group]:
            return 1
    return 0


def group_required(func):
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if group_validation(config):
            return func(*args, **kwargs)
        return render_template('no_access.html')

    return wrapper
