from __future__ import print_function, absolute_import, division, unicode_literals
###########

import os              # NOQA
import sys             # NOQA
import zipfile         # NOQA
from zipfile import *  # NOQA

if sys.version_info < (3, ):
    string_type = basestring
else:
    string_type = str


class InMemoryZipFile(object):
    # original idea from http://stackoverflow.com/a/19722365/1307905
    def __init__(self, file_name=None, compression=zipfile.ZIP_DEFLATED, debug=0):
        try:
            from cStringIO import StringIO
        except ImportError:
            from io import BytesIO as StringIO
        # Create the in-memory file-like object
        if hasattr(file_name, '_from_parts'):
            self._file_name = str(file_name)
        else:
            self._file_name = file_name
        self.in_memory_data = StringIO()
        # Create the in-memory zipfile
        self.in_memory_zip = zipfile.ZipFile(
            self.in_memory_data, "w", compression, False)
        self.in_memory_zip.debug = debug

    def append(self, filename_in_zip, file_contents):
        '''Appends a file with name filename_in_zip and contents of
        file_contents to the in-memory zip.'''
        self.in_memory_zip.writestr(filename_in_zip, file_contents)
        return self   # so you can daisy-chain

    def write_to_file(self, filename):
        '''Writes the in-memory zip to a file.'''
        # Mark the files as having been created on Windows so that
        # Unix permissions are not inferred as 0000
        for zfile in self.in_memory_zip.filelist:
            zfile.create_system = 0
        self.in_memory_zip.close()
        with open(filename, 'wb') as f:
            f.write(self.data)

    @property
    def data(self):
        return self.in_memory_data.getvalue()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._file_name is None:
            return
        self.write_to_file(self._file_name)

    def delete_from_zip_file(self, pattern=None, file_names=None, password=None): #Take extra parameter for password.
        """
        zip_file can be a string or a zipfile.ZipFile object, the latter will be closed
        any name in file_names is deleted, all file_names provided have to be in the ZIP
        archive or else an IOError is raised
        """
        if pattern and isinstance(pattern, string_type):
            import re
            pattern = re.compile(pattern)
        if file_names:
            if not isinstance(file_names, list):
                file_names = [str(file_names)]
            else:
                file_names = [str(f) for f in file_names]
        else:
            file_names = []
        with zipfile.ZipFile(self._file_name) as zf:
            zf.setpassword(password) #Set the password for the zip file.
            for l in zf.infolist():
                if l.filename in file_names:
                    file_names.remove(l.filename)
                    continue
                if pattern and pattern.match(l.filename):
                    continue
                self.append(l.filename, zf.read(l))
            if file_names:
                raise IOError('[Errno 2] No such file{}: {}'.format(
                    '' if len(file_names) == 1 else 's',
                    ', '.join([repr(f) for f in file_names])))


def delete_from_zip_file(file_name, pattern=None, file_names=None, password=None): #Take extra parameter for password (overloaded function).
    with InMemoryZipFile(file_name) as imz:
        imz.delete_from_zip_file(pattern, file_names, password) #Parse the extra parameter to the class' method.
