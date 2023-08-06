# 0.01 = 2021-03-06 = Initial version
import os
import base64

from Crypto.Cipher import AES
import Crypto.Util.Padding
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from pbkdf2 import PBKDF2
# ##################################################################################################
from n0struct import *
# __DEBUG__ = True
# ##################################################################################################
class n0Vault(dict):
    _encrypted = False
    # Not crypted file format: ordinary json
    _encrypted = True  # Comment current line for not-crypted file format
    __vault_file_is_encrypted = None
    __password = None   # Used in case of _encrypted == True
    # Encrypted file format:
    #>> __sign   8 bytes: constant
    __sign = "n0Vault1"
    #>> flags    4 bytes: variable
    # File:     zzzz_zzzz_yyyy_yyyy_xxxx_xxxx_wwww_wwww
    # -> 'little endian' according to x86 architecture ->
    #     Native byte order is big-endian or little-endian, depending on the host system.
    #     For example, Intel x86 and AMD64 (x86-64) are little-endian;
    #     Motorola 68000 and PowerPC G5 are big-endian;
    #     ARM and Intel Itanium feature switchable endianness (bi-endian).
    #     Use sys.byteorder to check the endianness of your system.
    __flags = 0b0000_0000_0000_0000_0000_0000_0000_0000
    # Memory:   wwww_wwww_xxxx_xxxx_yyyy_yyyy_zzzz_zzzz
    #           ││││ ││││ ││││ ││││ ││││ ││││ ││││ ││││
    #           └┴┴┴─┴┴┴┴─┴┴┴┴─┴┴┴┴─┴┴┴┴─┴┴┴┴─┴┴┴┴─┴┤└┤
    #                                               │ │
    #                                               │ └─── 00 = AES encryption without password:
    #                                               │               static 256-bit Key (self.__key)
    #                                               │               + variable 128-bit Initialization Vector
    #                                               │      01 = AES encryption WITH password:
    #                                               │               static 256-bit Key (self.__key)
    #                                               │               + variable 128-bit Initialization Vector
    #                                               └───── reserved for future usage
    #>> iv      16 bytes unique 16 bytes, generated every time during saving
    #>> sha256  32 bytes control sum of iv+buffer before encryption
    #   __vault .. bytes encrypted with AES
    _vault = None  # n0dict()
    # **********************************************************************************************
    # 32 bytes / 256-bit Key: key is used for encryption or like salt in case of encryption with password
    __key = 0xf1d0f3b89f3cf706af3303fb549e18ce22e1bc744d8994da859e4d4e7700ae7b.to_bytes(32, 'big')  # 'little endian' or 'big endian' is no different in this case
    vault_file_name = None
    # **********************************************************************************************
    def __init__(
        self,
        vault_file_name: str = None,
        encrypted = True,
        password: str = None,
        key = None
    ):
        if not vault_file_name:
            vault_file_name = os.path.splitext(os.path.split(__file__)[1])[0] + ".vault"
        self._encrypted = encrypted
        self.__password = password
        if key:
            self.__key = base64.b64decode(key)[:32]  # 256-bit Key encrypted with base64
        self.load(vault_file_name)
    # **********************************************************************************************
    def __setitem__(self, xpath: str, new_value):
        self._vault[xpath] = new_value
        return new_value
    # **********************************************************************************************
    def update(self, xpath: typing.Union[dict, str], new_value: str = None) -> dict:
        return self._vault.update(xpath, new_value)
    # **********************************************************************************************
    def delete(self, xpath) -> dict:
        return self._vault.delete(xpath)
    # **********************************************************************************************
    def pop(self, xpath) -> dict:
        return self._vault.pop(xpath)
    # **********************************************************************************************
    def show(self) -> dict:
        return json.dumps(self._vault, indent = 4)
    # **********************************************************************************************
    def set_bits(
        self,
        flag: int,
        bit_offset: int = 0,
        binary_mask: int = 0b1,
        bit_value: int = 0b1,
    ) -> bool:
        return flag & binary_mask << bit_offset | bit_value
    # **********************************************************************************************
    def is_bit_set(
        self,
        flag: int,
        bit_offset: int = 0,
        binary_mask: int = 0b1,
    ) -> bool:
        return flag & binary_mask << bit_offset != 0
    # **********************************************************************************************
    def load(self, vault_file_name: str):
        def read_buffer(len_to_read = None, name = None):
            buffer = in_file.read(len_to_read)
            if globals().get("__DEBUG__"):
                n0debug("len_to_read")
                n0debug_calc(buffer, name)
                n0print(len(buffer))
            return buffer

        self.vault_file_name = vault_file_name
        if os.path.exists(self.vault_file_name):
            with open(self.vault_file_name, "rb") as in_file:
                sign = read_buffer(1)
                if sign == b'{':
                    # Not-crypted storage
                    self.__vault_file_is_encrypted = False
                    self._vault = n0dict((sign + read_buffer()).decode("utf-8"))
                else:
                    # Encrypted storage
                    self.__vault_file_is_encrypted = True
                    sign += read_buffer(7, "sign")
                    if sign.decode("utf-8") != self.__sign:
                        raise Exception(f"File '{vault_file_name}' is not n0Vault storage")
                    # 4 bytes/32-bits flag
                    self.__flags = int.from_bytes(read_buffer(4, "flags"), 'little')
                    cipher_iv = read_buffer(16, "cipher_iv")
                    control_sum = read_buffer(32, "control_sum")
                    # ******************************************************************************
                    # ******************************************************************************
                    if self.is_bit_set(self.__flags, 0, 0b11) == 0b00:
                        cipher = AES.new(self.__key, AES.MODE_CBC, cipher_iv)
                    elif self.is_bit_set(self.__flags, 0, 0b11) == 0b01:
                        if not self.__password:
                            raise Exception(f"Password for loading is required")
                        cipher = AES.new(
                            temp:=PBKDF2(self.__password, self.__key[:16]).read(32),    # 256-bit key
                            AES.MODE_CBC,
                            cipher_iv
                        )
                    else:
                        raise Exception(f"Unknown format of encryption for n0Vault storage")
                    # ******************************************************************************
                    try:
                        buffer = Crypto.Util.Padding.unpad(
                                    cipher.decrypt(
                                            read_buffer(None, "encrypted buffer")
                                        ),
                                    AES.block_size
                        )
                    except:
                        raise Exception(f"Incorrect password for n0Vault storage")
                    # ******************************************************************************
                    # ******************************************************************************
                    calculated_control_sum = SHA256.new(data=cipher_iv + buffer).digest()
                    if control_sum != calculated_control_sum:
                        raise Exception(f"Incorrect control sum of n0Vault storage")
                    # self._vault = json.loads(buffer)
                    self._vault = n0dict(buffer.decode("utf-8"))

                if self._vault.get("__sign") != self.__sign:
                    raise Exception(f"Incorrect format of n0Vault storage")
        else:
            self._vault = n0dict({"__sign": self.__sign})
        return self._vault
    # **********************************************************************************************
    def save(self, new_vault_file_name: str = None):
        # ******************************************************************************************
        def write_buffer(buffer, name):
            if isinstance(buffer, str):
                buffer = buffer.encode("utf-8")             # str -> bytes
            if isinstance(buffer, int):
                buffer = buffer.to_bytes(4, 'little')       # int32 -> bytes
            if globals().get("__DEBUG__"):
                n0debug_calc(buffer, name)
                n0print(len(buffer))
            out_file.write(buffer)
        # ******************************************************************************************
        with open(new_vault_file_name or self.vault_file_name, "wb") as out_file:
            if self._encrypted is None:
                self._encrypted = self.__vault_file_is_encrypted
            if self._encrypted:
                if self.__password:
                    self.__flags = self.set_bits(self.__flags, 0, 0b11, 0b01)
                    cipher = AES.new(
                        PBKDF2(self.__password, self.__key[:16]).read(32),          # Generate 256-bit key
                        AES.MODE_CBC
                    )
                else:
                    cipher = AES.new(self.__key, AES.MODE_CBC)
                write_buffer(self.__sign,   "sign")
                write_buffer(self.__flags,  "flags")
                write_buffer(cipher.iv,     "cipher.iv")
                # buffer = json.dumps(self._vault).encode("utf-8")                   # str -> bytes
                buffer = n0pretty(self._vault, show_type=False, __indent_size = 0).encode("utf-8") # str -> bytes
                write_buffer(SHA256.new(data=cipher.iv + buffer).digest(), "control_sum")
                write_buffer(
                            cipher.encrypt(
                                    Crypto.Util.Padding.pad(
                                        buffer,
                                        AES.block_size
                                    )
                            ),
                            "encrypted buffer"
                )
            else:
                buffer = self.show().replace('\n', "\r\n").encode("utf-8")  # str -> bytes
                write_buffer(buffer, "notcrypted buffer")
    # **********************************************************************************************
    def __getitem__(self, xpath):
        """
        Public function []:
        return _vault[where1/where2/.../whereN]
            AKA
        return _vault[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, exception IndexError will be raised
        """
        return self._vault._get(xpath, raise_exception = True)
    def get(self, xpath: str, if_not_found = None):
        """
        Public function:
        return _vault[where1/where2/.../whereN]
            AKA
        return _vault[where1][where2]...[whereN]

        If any of [where1][where2]...[whereN] are not found, if_not_found will be returned
        """
        return self._vault._get(xpath, raise_exception = False, if_not_found = if_not_found)
    # **********************************************************************************************
# ##################################################################################################
