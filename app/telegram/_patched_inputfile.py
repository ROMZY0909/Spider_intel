# app/telegram/_patched_inputfile.py

import logging
import mimetypes
import os
from typing import IO, Optional, Tuple, Union
from uuid import uuid4

DEFAULT_MIME_TYPE = 'application/octet-stream'
logger = logging.getLogger(__name__)


class InputFile:
    __slots__ = ('filename', 'attach', 'input_file_content', 'mimetype', '__dict__')

    def __init__(self, obj: Union[IO, bytes], filename: str = None, attach: bool = None):
        self.filename = None
        if isinstance(obj, bytes):
            self.input_file_content = obj
        else:
            self.input_file_content = obj.read()
        self.attach = 'attached' + uuid4().hex if attach else None

        if filename:
            self.filename = filename
        elif hasattr(obj, 'name') and not isinstance(obj.name, int):
            self.filename = os.path.basename(obj.name)

        if self.filename:
            self.mimetype = mimetypes.guess_type(self.filename)[0] or DEFAULT_MIME_TYPE
        else:
            self.mimetype = DEFAULT_MIME_TYPE

        if not self.filename:
            self.filename = self.mimetype.replace('/', '.')

    @property
    def field_tuple(self) -> Tuple[str, bytes, str]:
        return self.filename, self.input_file_content, self.mimetype

    @staticmethod
    def is_file(obj: object) -> bool:
        return hasattr(obj, 'read')

    def to_dict(self) -> Optional[str]:
        if self.attach:
            return 'attach://' + self.attach
        return None
