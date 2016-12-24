#! /usr/bin/python

import io
import sys
import struct

myData = {
        "ACCL": [],
        "GYRO": [],
        "GPS": [],
        }

class MyFile(object):
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.f = io.open(self.filename, 'rb')
        return self

    def __exit__(self, type, value, traceback):
        self.f.close()

    def read(self, count):
        return self.f.read(count)

    def tell(self):
        return self.f.tell()

    def has_code(self, code="DEVC"):
        return (self.f.peek(4)[:4] == code)

    def align(self):
        if (self.f.tell()%4 != 0):
            self.f.seek(self.f.tell() + (4 - self.f.tell()%4))

class DataPoint(object):
    def __cmp__(self, other):
        try:
            return self.timestamp - other.timestamp
        except AttributeError:
            raise Exception

class AccelerometerPoint(DataPoint):
    def __init__(self, timestamp, data):
        self.timestamp = data['timestamp']

        self.x = 0
        self.y = 0
        self.z = 0

class GyroPoint(DataPoint):
    def __init__(self, timestamp, data):
        self.timestamp = data['timestamp']

        self.wx = 0
        self.wy = 0
        self.wz = 0

class GpsPoint(DataPoint):
    def __init__(self, timestamp, data):
        self.timestamp = data['timestamp']

        self.r_lat = 0
        self.r_lon = 0
        self.elevation = 0
        self.v_lat = 0
        self.v_lon = 0

class DataStream(object):
    def __init__(self):
        self.code = code
        self.data_type = data_type
        self.count = count
        self.data = data

    def mutate(self):
        if (self.code == "ACCL"):
            pass
        elif (self.code == "GYRO"):
            pass
        elif (self.code == "GPS5"):
            pass

    def add(self, generic_stream):
        if (self.base_type not in generic_stream.keys()):
            return False

        time = generic_stream['TSMP']*self.time_scale
        for item in generic_stream['data']:
            self.data.append(AccelerometerPoint(time, item))
            time += self.time_increment

        return True

class AccelerometerStream(DataStream):
    base_type = "ACCL"
    time_increment = 5000
    time_scale = 1000

    def __init__(self, generic_stream):
        self.data = []

    def base_time():
        time = generic_stream['TSMP']*self.time_scale
        pass

class GyroStream(DataStream):
    base_type = "ACCL"
    time_increment = 2500
    time_scale = 1000

    def __init__(self, generic_stream):
        self.data = []

    def base_time():
        time = generic_stream['TSMP']*self.time_scale
        pass

class GpsStream(DataStream):
    base_type = "GPS5"
    time_increment = 55000
    time_scale = 1000

    def __init__(self, generic_stream):
        self.data = []

    def base_time():
        # You need to parse the GPSU stamp
        time = generic_stream['GPSU']*self.time_scale

have_subtypes = set([00])
def get_stream(f, size, count):
    stream = {}
    limit = f.tell() + (size*count)
    while f.tell() < limit:
        data = get_stream_element(f)
        stream[data["code"]] = data["data"]

    return stream

def get_stream_element(f):
    code = f.read(4)
    data_type, size, count = struct.unpack(">BBH", f.read(4))

    data = None
    if (code == "ACCL"):
        data = get_data(f, data_type, size, count)
    elif (code == "GYRO"):
        data = get_data(f, data_type, size, count)
    elif (code == "GPS5"):
        data = get_data(f, data_type, size, count)
    else:
        data = f.read(size*count)

    f.align()
    return {
        "code": code,
        "type": data_type,
        "size": size,
        "count": count,
        "data": data,
        }

def get_data(f, data_type, size, count):
    data_array = []
    limit = f.tell() + (size*count)

    while f.tell() < limit:
        data_array.append(f.read(size))

    return data_array

def read_devc(f):
    code = f.read(4)
    data_type, size, count = struct.unpack(">BBH", f.read(4))

    limit = f.tell() + (size*count)
    while (f.tell() < limit):
        data = get_devc_element(f, size, count)

    f.align()

    return {
        "code": code,
        "type": data_type,
        "size": size,
        "count": count,
        "data": data,
        }

def get_devc_element(f, size, count):
    code = f.read(4)
    data_type, size, count = struct.unpack(">BBH", f.read(4))

    if code == "STRM":
        read_stream(f, size, count)
    else:
        data = f.read(size*count)

    f.align()

def read_stream(f, size, count):
    stream = get_stream(f, size, count)
    if("ACCL" in stream.keys()):
        scale = struct.unpack(">H", stream["SCAL"])[0]
        data = list(map(lambda x: parse_accl_item(x, scale), stream["ACCL"]))
        myData["ACCL"] += data
    elif("GYRO" in stream.keys()):
        myData["GYRO"] += stream["GYRO"]
    elif("GPS5" in stream.keys()):
        myData["GPS"] += stream["GPS5"]

    return stream

def parse_accl_item(item, scale):
    data = struct.unpack(">3h", item)
    return list(map(lambda x: float(x)/scale, data))

def main(args):
    with MyFile(args[0]) as my_file:
        while my_file.has_code():
            read_devc(my_file)

    for item in myData["ACCL"]:
        print(item)

if __name__ == "__main__":
    main(sys.argv[1:])
