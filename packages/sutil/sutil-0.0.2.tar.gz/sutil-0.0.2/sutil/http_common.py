import logging
import sutil.consts
from io import BytesIO
from sutil.utils import clear_none_in_dict
import mimetypes


logger = logging.getLogger(sutil.consts.LOGGER_NAME)


def convert_file_args(files):
    def convert_fileobj(file_desc, fileobjs):
        fileobj = None
        if isinstance(file_desc, str):
            fileobj = open(file_desc, "rb")
            fileobjs.append(fileobj)
        elif isinstance(file_desc, bytes):
            fileobj = BytesIO(file_desc)
        else:
            raise Exception("unknown file_desc type[%s]", type(file_desc))
        return fileobj
    result = None
    fileobjs = []
    if files is not None:
        result = {}
        for k, v in files.items():
            if isinstance(v, list) or isinstance(v, tuple):
                result[k] = (v[0], convert_fileobj(v[1], fileobjs), v[2])
            else:
                result[k] = (None, convert_fileobj(v, fileobjs), None)
    return result, fileobjs

def extract_result(response, clear_none):
    if response["response"]["err_no"] != 0:
        return None
    result = response["response"]["results"]
    if clear_none and isinstance(result, dict):
        result = clear_none_in_dict(result)
    return result

