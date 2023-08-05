from pyheapfile.heap import to_bytes, from_bytes

from pydllfile.dllist import LINK_SIZE

KEY_DATA_MAX = 2 ** (3 * 4)  # 4096, can be stored in 12 bits == 3 nibbles

F_LEAF = 1 << 0
F_KEY = 1 << 1
F_DATA = 1 << 2
F_LEFT = 1 << 3
F_RIGHT = 1 << 4

F_BPLUS_TREE_INNER_VAR = F_KEY | F_LEFT
F_BPLUS_TREE_INNER_RIGHTMOST_VAR = F_KEY | F_LEFT | F_RIGHT
F_BPLUS_TREE_LEAF_VAR = F_LEAF | F_KEY | F_DATA


class Node(object):
    def __init__(
        self,
        flags=F_BPLUS_TREE_INNER_RIGHTMOST_VAR,
        leaf=False,
        key=None,
        data=None,
        left=0,
        right=0,
        link_size=LINK_SIZE,
    ):
        self.link_size = link_size
        self.flags = 0
        self.set_flags(0, flags)
        if leaf:
            self.set_flags(F_LEAF, F_LEAF)
        self.set_key(key)
        self.set_data(data)
        self.set_left(left)
        self.set_right(right)

    def __repr__(self):
        return (
            self.__class__.__name__
            + "("
            + " flags:"
            + hex(self.flags)
            + " leaf:"
            + str(self.leaf)
            + ", key:"
            + str(self.key)
            + ", data:"
            + str(self.data)
            + ", left:"
            + hex(self.left)
            + ", right:"
            + hex(self.right)
            + " )"
        )

    def __lt__(self, other):
        return self.key < other.key

    def __eq__(self, other):
        return (
            self.flags == other.flags
            and self.leaf == other.leaf
            and self.key == other.key
            and self.data == other.data
            and self.left == other.left
            and self.right == other.right
        )

    def set_flags(self, mask, flags):
        self.flags &= 0xFF ^ mask
        self.flags |= flags
        self.leaf = self.flags & F_LEAF > 0
        return self.flags

    def set_key(self, key):
        self.key_len = len(key) if key != None else 0
        self.set_flags(F_KEY, F_KEY if self.key_len > 0 else 0)
        if self.key_len > KEY_DATA_MAX:
            raise Exception("key len exceeded")
        self.key = key

    def set_data(self, data, patch_leaf=True):
        if patch_leaf:
            self.set_flags(F_LEAF, data != None and len(data) > 0)
        self.data_len = len(data) if data != None else 0
        self.set_flags(F_DATA, F_DATA if self.data_len > 0 else 0)
        if self.data_len > KEY_DATA_MAX:
            raise Exception("data len exceeded")
        self.data = data

    def set_left(self, left):
        self.set_flags(F_LEFT, F_LEFT if left > 0 else 0)
        self.left = left

    def set_right(self, right):
        self.set_flags(F_RIGHT, F_RIGHT if right > 0 else 0)
        self.right = right

    def to_bytes(self, encode_key=True, encode_data=True):
        buf = []
        buf.extend(to_bytes(self.flags, 1))

        if (self.flags & (F_KEY | F_DATA)) > 0:

            key_low = self.key_len & 0xFF
            data_low = self.data_len & 0xFF

            key_high = self.key_len >> 8 & 0xF
            data_high = self.data_len >> 8 & 0xF

            high = (key_high << 4) | data_high

            buf.extend(to_bytes(high, 1))

            if self.flags & F_KEY > 0:
                buf.extend(to_bytes(key_low, 1))
            if self.flags & F_DATA > 0:
                buf.extend(to_bytes(data_low, 1))

        if self.flags & F_KEY > 0:
            if self.key == None or len(self.key) == 0:
                raise Exception("no key set")
            buf.extend(self.key.encode() if encode_key else self.key)

        if self.flags & F_DATA > 0:
            if self.data == None or len(self.data) == 0:
                raise Exception("no data set")
            buf.extend(self.data.encode() if encode_data else self.data)

        if self.flags & F_LEFT > 0:
            buf.extend(to_bytes(self.left, self.link_size))
        if self.flags & F_RIGHT > 0:
            buf.extend(to_bytes(self.right, self.link_size))

        return buf

    @staticmethod
    def _split(buf, blen):
        return buf[:blen], buf[blen:]

    def from_bytes(self, buf, pos=0, decode_key=True, decode_data=True):
        self.pos = pos
        b, buf = self._split(buf, 1)
        flags = from_bytes(b)
        self.set_flags(0, flags)

        if self.flags & (F_KEY | F_DATA) > 0:
            b, buf = self._split(buf, 1)
            high = from_bytes(b)
            key_high = high >> 4 & 0xF
            data_high = high & 0xF

            key_low = 0
            if self.flags & F_KEY > 0:
                b, buf = self._split(buf, 1)
                key_low = from_bytes(b)

            data_low = 0
            if self.flags & F_DATA > 0:
                b, buf = self._split(buf, 1)
                data_low = from_bytes(b)

            self.key_len = key_high << 8 | key_low
            self.data_len = data_high << 8 | data_low

            if self.flags & F_KEY > 0:
                b, buf = self._split(buf, self.key_len)
                self.key = bytes(b).decode() if decode_key else b
            else:
                self.key = None

            if self.flags & F_DATA > 0:
                b, buf = self._split(buf, self.data_len)
                self.data = bytes(b).decode() if decode_data else b
            else:
                self.data = None

        if self.flags & F_LEFT > 0:
            b, buf = self._split(buf, self.link_size)
            self.left = from_bytes(b)
        else:
            self.left = 0

        if self.flags & F_RIGHT > 0:
            b, buf = self._split(buf, self.link_size)
            self.right = from_bytes(b)
        else:
            self.right = 0

        if len(buf) > 0:
            return self, buf
        return self
