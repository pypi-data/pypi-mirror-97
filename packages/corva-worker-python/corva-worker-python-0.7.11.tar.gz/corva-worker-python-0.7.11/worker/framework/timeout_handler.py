import functools
from wrapt_timeout_decorator import timeout


def timeout_track(before=2, default_timeout=30):
    """
    A decorator that can be applied to a lambda function handler
    to raise an exception just before a timeout occur
    :param before: the seconds before the timeout occurs; used with lambda function
    :param default_timeout: actual timeout in seconds with cases other than lambda function
    :return:
    """
    def wrapper(func):
        @functools.wraps(func)
        @timeout(
            dec_timeout=f"((args[1].get_remaining_time_in_millis() - 1000 * {before}) / 1000) if args[1] else {default_timeout}",
            dec_allow_eval=True
        )
        def decorated(*args, **kwargs):
            return func(*args, **kwargs)

        return decorated
    return wrapper
