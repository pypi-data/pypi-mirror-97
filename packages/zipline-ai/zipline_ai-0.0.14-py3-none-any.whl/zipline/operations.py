import zipline.schema.thrift.ttypes \
    as zthrift

MIN = zthrift.Operation.MIN
MAX = zthrift.Operation.MAX
FIRST = zthrift.Operation.FIRST
LAST = zthrift.Operation.LAST
TOP = zthrift.Operation.TOP
BOTTOM = zthrift.Operation.BOTTOM

COUNT = zthrift.Operation.COUNT
SUM = zthrift.Operation.SUM
AVG = zthrift.Operation.MEAN


# TODO Online Moments
# VARIANCE = zthrift.Operation.VARIANCE
# SKEW = zthrift.Operation.SKEW
# KURTOSIS = zthrift.Operation.KURTOSIS
# TODO Tdigest for percentiles
# APPROX_PERCENTILE = zthrift.Operation.APPROX_PERCENTILE
# TODO HyperLoglog implementation for unique counts
# APPROX_UNIQUE = zthrift.Operation.APPROX_UNIQUE
