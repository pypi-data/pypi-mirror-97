import re
import math


# https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#meaning-of-memory
class StorageUnit:
    # we only support g m k, E/P/T is useless, and we do not support 123e321
    # format
    M = re.compile(r"^(\d+)(G|M|K|)(i|)$")

    power = {
        "G": 3,
        "M": 2,
        "K": 1,
    }

    def __init__(self, unit):
        if not isinstance(unit, str):
            raise TypeError(
                "we only accept unit to str, not %s(%s)" % (unit, type(unit))
            )

        m = self.M.match(unit)
        if not m:
            raise ValueError(
                "%s not a storage unit, we only support G,M,K or Gi,Ki,Mi now"
            )
        numeric = m.group(1)
        unit = m.group(2)
        power_2 = m.group(3)
        if power_2:
            base = 1024
        else:
            base = 1000

        self._raw = int(numeric) * math.pow(base, self.power[unit])

    def __iadd__(self, other):
        self._raw = self._raw + other._raw
        return self

    def __add__(self, other):
        self._raw = self._raw + other._raw
        return self

    def to_mega_i(self):
        return int(self._raw / (1024 * 1024))

    def to_mega(self):
        return int(self._raw / (1000 * 1000))

    def to_mega_i_str(self):
        return "%sMi" % self.to_mega_i()

    def to_mega_str(self):
        return "%sM" % self.to_mega()

    def __str__(self):
        return "StorageUnit: %sMi" % self.to_mega_i()
