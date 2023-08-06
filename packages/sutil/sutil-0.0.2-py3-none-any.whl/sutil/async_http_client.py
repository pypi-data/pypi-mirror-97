import json
import logging
import asyncio
import aiohttp
import sutil.consts
from aiohttp.formdata import FormData
from aiohttp.client import ClientTimeout
from sutil.http_common import convert_file_args
from aiohttp import TCPConnector


class AsyncHttpClient():
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(sutil.consts.LOGGER_NAME)
        self.session = aiohttp.ClientSession(**kwargs)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.logger.exception("exception [%s] occurred when use"\
                                   " async_http_client by with syntax", exc)
        await self.destroy()

    async def destroy(self):
        if self.session is not None:
            await self.session.close()
            self.session = None

    async def get(self, url, headers=None, timeout=5, timeout_retry=3,
                  decode_json=True, return_binary=False, **kwargs):
        return await self.request("get", url, None, headers, None,
                                  timeout, timeout_retry, decode_json,
                                  return_binary, **kwargs)

    async def post(self, url, data, headers=None,
                   timeout=5, timeout_retry=3, decode_json=True,
                   return_binary=False, **kwargs):
        return await self.request("post", url, data, headers, None,
                                  timeout, timeout_retry, decode_json,
                                  return_binary, **kwargs)

    async def post_form(self, url, data, files, headers=None,
                        timeout=5, timeout_retry=3, decode_json=True,
                        return_binary=False,**kwargs):
        return await self.request("post", url, data, headers, files,
                                  timeout, timeout_retry, decode_json,
                                  return_binary, **kwargs)

    async def request(self, method, url, data=None, headers=None, files=None,
                      timeout=5, timeout_retry=3, decode_json=True,
                      return_binary=False, **kwargs):
        for _ in range(timeout_retry):
            try:
                post_data = data
                if files is None:
                    if isinstance(data, dict) or isinstance(data, list):
                        post_data = json.dumps(data, ensure_ascii=False)
                else:
                    post_data = FormData()
                    if data:
                        for k, v in data.items():
                            post_data.add_field(k, v)
                    file_args, fileobs = convert_file_args(files)
                    for name, (filename, fileobj, mimetype) in file_args.items():
                        post_data.add_field(name, fileobj,
                                            content_type=mimetype, filename=filename)
                func = getattr(self.session, method)
                async with func(url, data=post_data, headers=headers,
                                timeout=ClientTimeout(timeout), **kwargs) as resp:
                    if resp.status != 200:
                        self.logger.error(
                            "[%s] url[%s], data[%s] headers[%s] kwargs[%s] failed,"\
                            " code[%d], resp[%s]",
                            method, url, post_data, headers, kwargs, resp.status, resp)
                        return None
                    if return_binary:
                        result = await resp.content.read()
                    else:
                        result = await resp.text(encoding='UTF-8')
                        if decode_json:
                            result = json.loads(result)
                    return result
            except asyncio.TimeoutError:
                self.logger.warning(
                    "[%s] url[%s], data[%s] headers[%s] kwargs[%s] timeout",
                    method, url, data, headers, kwargs)
        else:
            self.logger.error("[%s] url[%s], timeout after retry [%d] times",
                              method, url, timeout_retry)

