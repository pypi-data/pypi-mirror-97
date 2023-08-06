import functools
import os
import re
import requests
import time
from urllib.parse import urlencode
from random import randint
from requests import Session
from requests.exceptions import HTTPError
from requests.packages import urllib3

from wxkit.utils.logger import get_logger


RETRY_TIMES = 3
BACKOFF_FACTOR = 1
STATUS_TO_RETRY = (429, 500, 502, 504)
DEFAULT_TIMEOUT = (30, 120)
COMPOSE_PATH_PATTERN = re.compile("([^/]).*")


class HTTP_METHOD:
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class RetryException(Exception):
    """Specified exception to retry request."""

    def __init__(self, message):
        super().__init__(message)


def is_ssl_verification():
    return False if os.environ.get("CURL_CA_BUNDLE") == "" else True


def retry(*exceptions):
    """Decorate an async function to execute it a few times before giving up.
    Hopes that problem is resolved by another side shortly.
    Args:
        exceptions (tuple): The exceptions expected during function execution
    """

    logger = get_logger()

    def accumulate_cooldown(retry_times, backoff_factor=None):
        backoff_factor = backoff_factor or BACKOFF_FACTOR
        return backoff_factor * (2 ** retry_times) + (randint(1, 999)) * 0.001

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _count = 0
            _errors = None
            while _count < RETRY_TIMES:
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    _errors = err
                    if getattr(_errors, "response", None) is not None:
                        if err.response.status_code not in STATUS_TO_RETRY:
                            break

                    _count += 1
                    time.sleep(
                        accumulate_cooldown(_count, kwargs.get("backoff_factor"))
                    )

            logger.error(f"Retry exhausted error: {str(_errors)}")
            if _errors:
                raise _errors

        return wrapper

    return decorator


@retry(RetryException, HTTPError)
def retry_request(
    method,
    url,
    headers=None,
    files=None,
    data=None,
    json=None,
    params=None,
    auth=None,
    cookies=None,
    hooks=None,
    timeout=DEFAULT_TIMEOUT,
    verify=None,
    session=None,
    proxies=None,
    backoff_factor=BACKOFF_FACTOR,
    jsonify=True,
    object_hook=None,
    **kwargs,
):
    """
    Args:
        method: HTTP request method.
        url: HTTP request url.
        session: The session is used to send HTTP request.
        proxies: The proxy configs are applied to session.
        timeout: The specified timeout for HTTP response.
        jsonify: By default it is True, return response content as dictionary.
            If False, return HTTP response object.
        backoff_factor (float): The factor is used to calculate cooldown for retry.
        object_hook: The hook is used for json.loads if jsonify is True.
        error_handler: The function is used to handle raised exception and accept
            the exception object(maybe None) as first args of function.
    """

    logger = get_logger()
    session = session or Session()
    if isinstance(proxies, dict):
        session.proxies.update(proxies)

    req = requests.Request(
        method=method,
        url=url,
        headers=headers,
        files=files,
        data=data,
        json=json,
        params=params,
        auth=auth,
        cookies=cookies,
        hooks=hooks,
    ).prepare()
    _msg = f"[{method}] {url}?{urlencode(params)}" if params else f"[{method}] {url}"
    logger.info(f"Prepare to request. {_msg}")
    resp_data = None
    verify = verify if isinstance(verify, bool) else is_ssl_verification()
    if verify is False:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    _st = time.time()
    resp = session.send(req, timeout=timeout, verify=verify, **kwargs)
    resp.raise_for_status()
    resp_data = resp.json(object_hook=object_hook) if jsonify else resp
    _et = time.time() - _st
    logger.info(f"Request has finished and costs {_et:f} (s). {_msg}",)

    return resp_data


def compose_url_path(*args):
    # Make sure to trim leading slash if the path args start with.
    _args = [str(a) for a in args]
    _args = (
        _match.group() for _match in map(COMPOSE_PATH_PATTERN.search, _args) if _match
    )
    url_path = os.path.join(*_args)
    return url_path
