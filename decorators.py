from functools import wraps
from flask import redirect
from flask import session as login_session, url_for


def login_mandatory(fun):
    '''Checks to see whether a user is logged in'''
    @wraps(fun)
    def x(*args, **kwargs):
        if 'email' not in login_session:
            return redirect(url_for('login'))
        return fun(*args, **kwargs)
    return x