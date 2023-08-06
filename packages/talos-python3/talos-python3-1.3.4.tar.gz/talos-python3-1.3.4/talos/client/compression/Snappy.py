# -*- coding:utf-8 -*-
#
# Copyright 2020, Xiaomi.
# All rights reserved.
# Author: huyumei@xiaomi.com
#

from io import BytesIO
import struct
import six
import snappy
import platform

_XERIAL_V1_HEADER = (-126, b'S', b'N', b'A', b'P', b'P', b'Y', 0, 1, 1)
_XERIAL_V1_FORMAT = 'bccccccBii'

PYPY = bool(platform.python_implementation() == 'PyPy')

class Snappy:
    def encode(self, payload, xerial_compatible=True, xerial_blocksize=32 * 1024):
        """Encodes the given data with snappy compression.

        If xerial_compatible is set then the stream is encoded in a fashion
        compatible with the xerial snappy library.

        The block size (xerial_blocksize) controls how frequent the blocking occurs
        32k is the default in the xerial library.

        The format winds up being:


            +-------------+------------+--------------+------------+--------------+
            |   Header    | Block1 len | Block1 data  | Blockn len | Blockn data  |
            +-------------+------------+--------------+------------+--------------+
            |  16 bytes   |  BE int32  | snappy bytes |  BE int32  | snappy bytes |
            +-------------+------------+--------------+------------+--------------+


        It is important to note that the blocksize is the amount of uncompressed
        data presented to snappy at each block, whereas the blocklen is the number
        of bytes that will be present in the stream; so the length will always be
        <= blocksize.

        """

        if not xerial_compatible:
            return snappy.compress(payload)

        out = BytesIO()
        for fmt, dat in zip(_XERIAL_V1_FORMAT, _XERIAL_V1_HEADER):
            out.write(struct.pack('!' + fmt, dat))

        # Chunk through buffers to avoid creating intermediate slice copies
        if PYPY:
            # on pypy, snappy.compress() on a sliced buffer consumes the entire
            # buffer... likely a python-snappy bug, so just use a slice copy
            chunker = lambda payload, i, size: payload[i:size + i]

        elif six.PY2:
            # Sliced buffer avoids additional copies
            # pylint: disable-msg=undefined-variable
            chunker = lambda payload, i, size: buffer(payload, i, size)
        else:
            # snappy.compress does not like raw memoryviews, so we have to convert
            # tobytes, which is a copy... oh well. it's the thought that counts.
            # pylint: disable-msg=undefined-variable
            chunker = lambda payload, i, size: memoryview(payload)[i:size + i].tobytes()

        for chunk in (chunker(payload, i, xerial_blocksize)
                      for i in range(0, len(payload), xerial_blocksize)):
            block = snappy.compress(chunk)
            block_size = len(block)
            out.write(struct.pack('!i', block_size))
            out.write(block)

        return out.getvalue()

    def _detect_xerial_stream(self, payload):
        """Detects if the data given might have been encoded with the blocking mode
            of the xerial snappy library.

            This mode writes a magic header of the format:
                +--------+--------------+------------+---------+--------+
                | Marker | Magic String | Null / Pad | Version | Compat |
                +--------+--------------+------------+---------+--------+
                |  byte  |   c-string   |    byte    |  int32  | int32  |
                +--------+--------------+------------+---------+--------+
                |  -126  |   'SNAPPY'   |     \0     |         |        |
                +--------+--------------+------------+---------+--------+

            The pad appears to be to ensure that SNAPPY is a valid cstring
            The version is the version of this format as written by xerial,
            in the wild this is currently 1 as such we only support v1.

            Compat is there to claim the miniumum supported version that
            can read a xerial block stream, presently in the wild this is
            1.
        """

        if len(payload) > 16:
            header = struct.unpack('!' + _XERIAL_V1_FORMAT, bytes(payload)[:16])
            return header == _XERIAL_V1_HEADER
        return False

    def decode(self, payload):

        if self._detect_xerial_stream(payload):
            # TODO ? Should become a fileobj ?
            out = BytesIO()
            byt = payload[16:]
            length = len(byt)
            cursor = 0

            while cursor < length:
                block_size = struct.unpack_from('!i', byt[cursor:])[0]
                # Skip the block size
                cursor += 4
                end = cursor + block_size
                out.write(snappy.decompress(byt[cursor:end]))
                cursor = end

            out.seek(0)
            return out.read()
        else:
            return snappy.decompress(payload)
