#! /usr/bin/python

import io
import sys
import struct

have_subtypes = set([00])
code_types = {
        'DEVC': 0x00,
        'DVID': 0x4c,
        'DVNM': 0x63,
        'TSMP': 0x4c,
        'SIUN': 0x63,
        'SCAL': 0x73,
        'TMPC': 0x66,
        'ACCL': 0x73,
        'STRM': 0x00,
        'GYRO': 0x73,
        'GPSF': 0x4c,
        'GPSU': 0x63,
        'GPSP': 0x53,
        'GPS5': 0x6c,
        'UNIT': 0x63,
        }

def get_chunk(f):
    i = 0
    code = f.read(4)
    i += 4

    data_type, size, count = struct.unpack(">BBH", f.read(4))
    i += 4

    jump = size * count
    jump_tail = jump % 4
    if jump_tail != 0:
        jump = jump + (4-jump_tail)

    data = None
    if (data_type in have_subtypes):
        data = get_chunks(f, jump)
    else:
        data = f.read(jump)

    i += jump

    if (code == "GPS5" and jump >= 20):
        pass
        #print(struct.unpack(">5I", data[0:20])[2]/1000)
    elif (code == "TMPC"):
        pass
        #print(struct.unpack(">f", data)[0])
    elif (code not in code_types.keys() or code_types.get(code) != data_type):
        pass
        #print(code + ' - ' + hex(data_type))

    return {
        "code": code,
        "type": data_type,
        "total_size": i,
        "size": size,
        "count": count,
        "data": data,
        }

def get_all(f):
    chunks = []
    while f.peek(4) != '':
        chunks.append(get_chunk(f))

    return chunks

def get_chunks(f, limit):
    i = 0

    chunks = []
    while i < limit:
        chunks.append(get_chunk(f))
        i += chunks[len(chunks)-1].get('total_size')

    return chunks

def main(args):
    pack = []

    for key in code_types:
        value = code_types.get(key)
        hexval = "0x{:02x}".format(value)
        binval = "0b{:08b}".format(value)
        #print(key + ' ' + hex(value) + ' ' + bin(value))
        print(key + ' ' + hexval + ' ' + binval)

    with io.open(args[0], 'rb') as f:
        pack = get_all(f)
        print(len(pack))

if __name__ == "__main__":
    main(sys.argv[1:])
