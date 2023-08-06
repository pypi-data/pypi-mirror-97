import socket
import time
import logging
import sutil.consts


logger = logging.getLogger(sutil.consts.LOGGER_NAME)


def clear_none_in_dict(d, recursive=True):
    clear_keys = []
    for k, v in d.items():
        if v is None:
            clear_keys.append(k)
        if isinstance(v, dict) and recursive:
            clear_none_in_dict(v, True)
    for k in clear_keys:
        del d[k]
    return d


def bound(val, min_val, max_val):
    return min(max(val, min_val), max_val)


def log_exec_time(func):
    def inner_func(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info("function [%s], args[%s], kwargs[%s] cost[%.2f] seconds",
                    func.__name__, args, kwargs, end - start)
        return result
    return inner_func


def get_host_ip():
    ip = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def chunk(data, size):
    assert size  > 0
    idx = 0
    while idx < len(data):
        yield data[idx: idx+size]
        idx += size
