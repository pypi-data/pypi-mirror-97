#
#  Bcon
#  Python Binary Compressed Object Notation module.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from io import BytesIO
from typing import Any
from .pack import pack, unpack
from .compress import compress, decompress


def dumps(obj: Any):
    return compress(pack(obj))


def loads(data: bytes):
    return unpack(decompress(data))


def dump(obj: Any, file: BytesIO):
    file.write(dumps(obj))


def load(file: BytesIO):
    return loads(file.read())
