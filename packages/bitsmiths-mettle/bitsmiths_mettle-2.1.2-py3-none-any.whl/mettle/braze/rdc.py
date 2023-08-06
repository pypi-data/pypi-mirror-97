# **************************************************************************** #
#                           This file is part of:                              #
#                                   METTLE                                     #
#                           https://bitsmiths.co.za                            #
# **************************************************************************** #
#  Copyright (C) 2015 - 2021 Bitsmiths (Pty) Ltd.  All rights reserved.        #
#   * https://bitbucket.org/bitsmiths_za/mettle.git                            #
#                                                                              #
#  Permission is hereby granted, free of charge, to any person obtaining a     #
#  copy of this software and associated documentation files (the "Software"),  #
#  to deal in the Software without restriction, including without limitation   #
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
#  and/or sell copies of the Software, and to permit persons to whom the       #
#  Software is furnished to do so, subject to the following conditions:        #
#                                                                              #
#  The above copyright notice and this permission notice shall be included in  #
#  all copies or substantial portions of the Software.                         #
#                                                                              #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL     #
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  #
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
#  DEALINGS IN THE SOFTWARE.                                                   #
# **************************************************************************** #

from enum import IntEnum

from mettle.lib import xMettle


class Rdc:
    """
    Ross' Data Compression converted to a python class.
    """
    BEST_HASH = 4096

    class eDataState(IntEnum):
        """
        Enumeration for the data state.
        """
        NotApplicable  = 0
        Compressed     = 1
        Uncompressed   = 2


    def __init__(self):
        """
        Constructor.
        """
        self._state          = Rdc.eDataState.NotApplicable
        self._length         = 0
        self._compressed_len = 0
        self._blob           = None


    def data_state(self) -> eDataState:
        """
        Gets the current data state.

        :return: current data state of the rdc object.
        """
        return self._state


    def blob(self) -> bytearray:
        """
        Gets the current binary large object byte array

        :return: (bytearray) The current blob, this value could be None.
        """
        return self._blob


    def length(self) -> int:
        """
        Gets the the uncompresssed length of the blob.

        :return: The uncompressed size of the blob.
        """
        return self._length


    def compressed_length(self) -> int:
        """
        Gets the the compresssed length of the blob.

        :return: The compressed size of the blob.
        """
        return self._compressed_len


    def eat(self, data: bytes, length: int, compressed_len: int):
        """
        Eats a byte or bytearray, and assigns the uncompressed and compressed lengths.

        :param data: A bytes or bytearray object.
        :param length: The uncompressed length of the data.
        :param compressed_len: The compressed length of the data.
        """
        self._blob = None

        if not data:
            self._length         = 0
            self._compressed_len = 0
            self._state          = Rdc.eDataState.NotApplicable

            return

        if type(self._blob) is bytes:
            self._blob = bytearray(data)
        else:
            self._blob = data

        self._length         = length
        self._compressed_len = compressed_len

        if compressed_len != 0 and compressed_len != length:
            self._state = Rdc.eDataState.Compressed
        else:
            self._state = Rdc.eDataState.Uncompressed


    def compress(self):
        """
        Compresses the blob.
        """
        if self._state != Rdc.eDataState.Uncompressed:
            raise xMettle('RDC - Cannot compress, data state is not ready', src = Rdc.__name__)

        blobLen = len(self._blob)

        if blobLen <= 32:
            self._compressed_len = blobLen
            return

        new_blob     = bytearray(blobLen)
        hash_tbl     = {}
        rdc_buff     = 0
        anchor       = 0
        ctrl_cnt     = 0  # byte
        ctrl_idx     = 0
        ctrl_bits    = 0  # byte
        out_buf      = 1
        out_buf_end  = blobLen - 24
        cnt          = 0
        c            = 0
        hashkey      = 0
        pat_idx      = 0
        gap          = 0

        while rdc_buff < blobLen:
            # --make room for control bits-----------------------------------------
            if ctrl_cnt == 8:
                ctrl_cnt += 1

                # and check for output_buf overflow
                new_blob[ctrl_idx]  = ctrl_bits
                ctrl_cnt           = 1
                ctrl_idx           = out_buf
                out_buf           += 1

                if out_buf > out_buf_end:
                    return
            else:
                ctrl_cnt += 1

            # --Check for RLE------------------------------------------------------
            anchor    = rdc_buff
            c         = self._blob[rdc_buff]
            rdc_buff += 1

            while rdc_buff < blobLen and self._blob[rdc_buff] == c and (rdc_buff - anchor) < 4110:
                rdc_buff += 1

            # store compression code if character is repeated more than 2 times
            cnt = rdc_buff - anchor

            if cnt > 2:
                if cnt <= 18:                    # short RLE
                    new_blob[out_buf] = cnt - 3
                    out_buf += 1
                else:                            # long  RLE
                    cnt -= 19
                    new_blob[out_buf] = (16 + (cnt & int('0x0F', 16)))
                    out_buf += 1
                    new_blob[out_buf] = cnt >> 4
                    out_buf += 1

                new_blob[out_buf]  = c
                out_buf          += 1
                ctrl_bits         = ((ctrl_bits << 1) | 1) % 256

                continue


            # --look for pattern if 2 or more chars remain in the input buffer-----
            rdc_buff = anchor

            if blobLen - rdc_buff > 2:
                # locate offset of possible pattern in sliding dictionary
                hashkey = (((self._blob[rdc_buff] << 8) | self._blob[rdc_buff + 1]) ^ ((self._blob[rdc_buff] >> 4) | (self._blob[rdc_buff + 2] << 4))) % Rdc.BEST_HASH  # noqa

                if hashkey in hash_tbl.keys():
                    pat_idx = hash_tbl[hashkey]
                else:
                    pat_idx = 0

                hash_tbl[hashkey] = rdc_buff

                # compare chars id wer'e within 4090 bytes (set to 4090)
                gap = rdc_buff - pat_idx

                if pat_idx != 0 and gap <= 4090:

                    while rdc_buff               < blobLen              and\
                            pat_idx              < anchor               and\
                            self._blob[pat_idx] == self._blob[rdc_buff] and\
                            (rdc_buff - anchor)  < 271:

                        rdc_buff += 1
                        pat_idx  += 1

                    cnt = rdc_buff - anchor

                    if cnt > 2:  # store pattern if it is more
                        gap -= 3                         # than two chars

                        if cnt <= 15:                    # short pattern
                            new_blob[out_buf] = ((cnt << 4) + (gap & int('0x0F', 16)))
                            out_buf += 1
                            new_blob[out_buf] = (gap >> 4)
                            out_buf += 1
                        else:
                            new_blob[out_buf] = (32 + (gap & int('0x0F', 16)))
                            out_buf += 1
                            new_blob[out_buf] = (gap >> 4)
                            out_buf += 1
                            new_blob[out_buf] = (cnt - 16)
                            out_buf += 1

                        ctrl_bits = ((ctrl_bits << 1) | 1) % 256

                        continue


            # --cant compress this char so copy it to out buf----------------------
            new_blob[out_buf]  = c
            out_buf          += 1
            anchor           += 1
            rdc_buff          = anchor
            ctrl_bits         = (ctrl_bits << 1) % 256


        # save last load of bits
        ctrl_bits = (ctrl_bits << (8 - ctrl_cnt)) % 256

        new_blob[ctrl_idx] = ctrl_bits

        # finally set the output size
        self._compressed_len = out_buf
        self._state          = Rdc.eDataState.Compressed

        self._blob  = bytearray(new_blob[0:self._compressed_len])
        del new_blob


    def uncompress(self):
        """
        Decompresses the blob.
        """
        if self._state != Rdc.eDataState.Compressed:
            raise xMettle('RDC - Cannot uncompress, data state is not ready', src = Rdc.__name__)

        self._state = Rdc.eDataState.Uncompressed

        if self._compressed_len == 0 or self._compressed_len == self._length:
            return

        new_blob  = bytearray(self._length)
        rdc_buff  = 0
        out_buff  = 0
        ctrl_bits = 0  # byte
        ctrl_mask = 0  # byte
        cmd       = 0
        cnt       = 0
        offset    = 0

        while rdc_buff < self._compressed_len:
            # get new load of control bits if needed
            ctrl_mask >>= 1

            if ctrl_mask == 0:
                ctrl_bits  = self._blob[rdc_buff]
                rdc_buff  += 1
                ctrl_mask  = int('0x80', 16)


            # just copy this char if control bit is zero
            if (ctrl_bits & ctrl_mask) == 0:
                new_blob[out_buff] = self._blob[rdc_buff]
                out_buff += 1
                rdc_buff += 1
                continue

            # Undo the compression code
            cmd       = (self._blob[rdc_buff] >> 4) & int('0x0F', 16)
            cnt       = self._blob[rdc_buff] & int('0x0F', 16)
            rdc_buff += 1

            if cmd == 0:  # short rule
                cnt      += 3
                self._memfill(new_blob, self._blob[rdc_buff], out_buff, cnt)
                rdc_buff += 1
                out_buff += cnt
            elif cmd == 1:  # long rule
                cnt      += self._blob[rdc_buff] << 4
                rdc_buff += 1
                cnt      += 19
                self._memfill(new_blob, self._blob[rdc_buff], out_buff, cnt)
                rdc_buff += 1
                out_buff += cnt
            elif cmd == 2:  # long pattern
                offset    = cnt + 3
                offset   += self._blob[rdc_buff] << 4
                rdc_buff += 1
                cnt       = self._blob[rdc_buff]
                rdc_buff += 1
                cnt      += 16
                new_blob[out_buff:out_buff + cnt] = new_blob[out_buff - offset:out_buff - offset + cnt]
                out_buff += cnt
            else:  # short pattern
                offset    = cnt + 3
                offset   += self._blob[rdc_buff] << 4
                rdc_buff += 1
                new_blob[out_buff:out_buff + cmd] = new_blob[out_buff - offset:out_buff - offset + cmd]
                out_buff += cmd


        if out_buff != self._length:
            raise xMettle('RDC - Memory buffer is the incorrect size data corrupt! (got:%d/expected:%d)' % (
                out_buff, self._length), src = Rdc.__name__)

        del self._blob

        self._blob = new_blob


    def _memfill(self, dst, val, idx: int, dstlen: int):
        """
        A basic memcpy/array fill like method.

        :param dst: (bytearray) The destination byte array.
        :param val: (byte) The byte val to fill with.
        :param idx: The starting index to fill from.
        :param dstlen: The length to fill to.
        """
        dstlen += idx

        while idx < dstlen:
            dst[idx] = val
            idx += 1
