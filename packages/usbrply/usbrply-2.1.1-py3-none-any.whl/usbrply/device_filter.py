from .usb import req2s
import binascii
import struct
from .util import hexdump

# FIXME: this is super hacky right now


def default_arg(argsj, k, default):
    val = argsj.get(k)
    if val is None:
        return default
    else:
        return val


class DeviceFilter(object):
    def __init__(self, argsj, verbose=False):
        self.verbose = verbose
        self.entries = 0
        self.drops = 0

        self.arg_device = default_arg(argsj, "device", None)

    def should_filter(self, data):
        device = data.get('device')
        # Filter:
        # Devices not matching target
        # When device filtering not used
        return device is not None and device == self.keep_device

    def gen_data(self, datas):
        for data in datas:
            self.entries += 1
            if self.should_filter(data):
                if self.verbose:
                    print("DeviceFilter drop %s (%s %s %s)" %
                          (data['type'],
                           req2s(data["bRequestType"], data["bRequest"]),
                           data["bRequestType"], data["bRequest"]))
                self.drops += 1
                continue
            yield data
        yield {
            "type":
            "comment",
            "v":
            "DeviceFilter: dropped %s / %s entries" %
            (self.drops, self.entries)
        }

    def run(self, jgen):
        for k, v in jgen:
            if k == "data":
                yield k, self.gen_data(v)
            else:
                yield k, v
