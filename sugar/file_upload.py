import os
from sugar.string.fernet import FernetHandler
from sugar.sugars import Sugars
from django.conf import settings
from django.core.files.storage import default_storage


def upload(file, path=None, hash_file_name=True):
    _file_name = file.name
    if hash_file_name:
        _, _ext = os.path.splitext(file.name)
        _file_name = "%s%s" % (Sugars.uuid(), _ext)
    return default_storage.save("/".join([path, _file_name]), file.file)


def upload_base64_data(file, path=None, file_name=None):
    return default_storage.save("/".join([path, file_name or file.name]), file.file)


def vendor_document_upload(file, path=None, hash_file_name=True):
    _file_name = file.name
    if hash_file_name:
        _, _ext = os.path.splitext(file.name)
        _file_name = "%s%s" % (Sugars.uuid(), _ext)

    fh = FernetHandler(settings.ENCRYPT_KEY_VENDOR_DOCUMENT)
    file_contents = file.read()
    enc_file_contents = fh.encrypt_to_bytes(file_contents)
    local_fname = "/tmp/" + _file_name
    fp = open(local_fname, "wb")
    fp.write(enc_file_contents)
    fp.close()
    fp = open(local_fname, "rb")
    return default_storage.save("/".join([path, _file_name]), fp)
