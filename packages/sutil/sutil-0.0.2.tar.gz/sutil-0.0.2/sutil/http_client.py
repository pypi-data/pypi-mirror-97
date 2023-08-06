import requests
from requests.exceptions import Timeout
import logging
import json
import sutil.consts
from sutil.http_common import convert_file_args


class HttpClient:

    def __init__(self):
        self.logger = logging.getLogger(sutil.consts.LOGGER_NAME)

    def get(self, url, headers=None, timeout=5, timeout_retry=3,
            decode_json=True, return_binary=False, **kwargs):
        return self.request("get", url, None, headers, None,
                            timeout, timeout_retry, decode_json,
                            return_binary, **kwargs)

    def post(self, url, data, headers=None,
             timeout=5, timeout_retry=3, decode_json=True,
             return_binary=False, **kwargs):
        return self.request("post", url, data, headers, None,
                            timeout, timeout_retry, decode_json,
                            return_binary, **kwargs)

    def post_form(self, url, data, files, headers=None,
                        timeout=5, timeout_retry=3, decode_json=True,
                        return_binary=False, **kwargs):
        return self.request("post", url, data, headers, files,
                            timeout, timeout_retry, decode_json,
                            return_binary, **kwargs)

    def request(self, method, url, data, headers=None, files=None,
                timeout=5, timeout_retry=3, decode_json=True,
                return_binary=False, **kwargs):
        for _ in range(timeout_retry):
            fileobjs = []
            try:
                post_data = data
                if isinstance(post_data, dict) or isinstance(post_data, list):
                    post_data = json.dumps(data, ensure_ascii=False).encode("utf8")
                file_args, fileobjs = convert_file_args(files)
                resp = requests.request(method, url, data=post_data,
                                        headers=headers, files=file_args,
                                        timeout=timeout, **kwargs)
                if resp.status_code != 200:
                    self.logger.error(
                        "[%s] url[%s], data[%s] headers[%s] kwargs[%s] failed,"\
                        " code[%d], response[%s]",
                        method, url, data, headers, kwargs, resp.status_code, resp.text)
                    return None
                if return_binary:
                    result = resp.content
                else:
                    result = resp.content.decode("utf8")
                    if decode_json:
                        result = json.loads(result)
                return result
            except Timeout as e:
                self.logger.warning(
                    "[%s] url[%s], data[%s] headers[%s] kwargs[%s] timeout",
                    method, url, data, headers, kwargs)
            finally:
                for fileobj in fileobjs:
                    fileobj.close()
        else:
            self.logger.error("[%s] url[%s], timeout after retry [%d] times",
                              method, url, timeout_retry)
