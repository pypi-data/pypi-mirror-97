import datetime
import time
import functools
import logging
from enum import IntEnum

DEFAULT_POLL_PERIOD = 1


class UnexpectedErrorException(Exception):
    pass


class TimeoutException(Exception):
    pass


class CancelledException(Exception):
    pass


class PollWaitStatus(IntEnum):
    SUCC = 0
    FAIL = 1
    TIMEOUT = 2
    CANCEL = 3


def poll_wait_until(
    check_end,
    cleanup,
    timeout: int = None,
    poll_period: int = DEFAULT_POLL_PERIOD,
    allowed_exceptions=(Exception),
) -> PollWaitStatus:
    start = datetime.datetime.now()
    expect_end = None

    if timeout > 0:
        expect_end = start + datetime.timedelta(seconds=timeout)
    fail = False
    exec_info = None
    ret = False

    while (expect_end is None) or (expect_end >= datetime.datetime.now()):
        try:
            try:
                ret = check_end()
            except UnexpectedErrorException as e:
                logging.exception("unexpected error happens")
                fail = True
                exec_info = e
            except allowed_exceptions as e:
                fail = True
                logging.exception("critial exception happens")
                exec_info = RuntimeError("unexpect exception happens: %s" % e)

            if fail:
                cleanup(ret, exec_info)
                return PollWaitStatus.FAIL
            elif ret:
                cleanup(ret, exec_info)
                return PollWaitStatus.SUCC
            else:
                time.sleep(poll_period)
        except KeyboardInterrupt:
            logging.info("user cancelled")
            cleanup(False, CancelledException())
            return PollWaitStatus.CANCEL

    cleanup(ret, TimeoutException("timeouted %s" % timeout))
    return PollWaitStatus.TIMEOUT


def retry(retry_count=5, delay=5, allowed_exceptions=()):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            result = None
            last_exception = None
            for _ in range(retry_count):
                try:
                    result = f(*args, **kwargs)
                    last_exception = None
                    break
                except allowed_exceptions as e:
                    logging.exception("execution %s" % f.__qualname__)
                    last_exception = e
                logging.debug(
                    "Waiting for %s seconds before retrying again" % delay
                )
                time.sleep(delay)

            if last_exception is not None:
                raise type(last_exception) from last_exception

            return result

        return wrapper

    return decorator
