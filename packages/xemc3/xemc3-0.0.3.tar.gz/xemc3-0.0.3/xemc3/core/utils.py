import itertools
import time
import numpy as np
import xarray as xr


class rrange2(object):
    def __init__(self, args, *, update=100):
        self.args = [int(a) for a in args]
        self.total = 1
        self.t0 = time.time()
        self.update = int(update)
        for a in self.args:
            self.total *= a
        self._has_returned = 0
        return None

    def __iter__(self):
        self.state = [0 for a in self.args]
        if len(self.state) > 0:
            self.state[0] = -1
        self.tstate = -1
        self.tnext = 0
        return self

    def __next__(self):
        self.tstate += 1
        if self.tstate == self.tnext:
            self.tnext += ((self.total - 1) // self.update) + 1
            print(
                f"{self.tstate * 100 / self.total:6.2f} % ... {time.time() - self.t0:.0f} s",
                end="\r",
            )
        try:
            self.state[0] += 1
        except IndexError:
            if self.tstate == 0:
                return tuple()
            raise StopIteration
        for i in range(len(self.args)):
            if self.state[i] < self.args[i]:
                return tuple(self.state)
            else:
                self.state[i] = 0
                try:
                    self.state[i + 1] += 1
                except IndexError:
                    raise StopIteration


def rrange(args):
    ranges = [range(a) for a in args]
    return itertools.product(*ranges)


def prod(args):
    ret = 1
    for arg in args:
        ret *= arg
    return ret


def to_interval(dims, data=None):
    """Transforms a N-D i_1+1 x ... x i_N+1 mesh to an
    i_1 x ... x i_N x 2 x ... x 2 mesh of quads
    """
    if isinstance(dims, tuple) and data is None:
        dims, data = dims

    if data is None:
        data = dims
        in_dims = data.dims
        attrs = data.attrs
        data = data.data
    else:
        in_dims = dims
        attrs = {}
    dims = len(data.shape)
    if not dims == len(in_dims):
        raise ValueError(
            f"Data mismatch - {in_dims} as dimensions given, but data is shape {data.shape} (len{len(data.shape)})"
        )
    out_dims = [d for d in in_dims] + ["delta_" + d for d in in_dims]
    ret = np.empty([i - 1 for i in data.shape] + [2] * dims, dtype=data.dtype)
    for ijk in itertools.product(*[range(a - 1) for a in data.shape]):
        tmp = np.array(data[tuple([slice(i, i + 2) for i in ijk])])
        ret[ijk] = tmp
    return xr.DataArray(data=ret, dims=out_dims, attrs=attrs)


def from_interval(data, check=True):
    dims = len(data.shape) // 2
    out_dims = data.dims[:dims]
    attrs = data.attrs
    data = data.data
    ret = np.empty([i + 1 for i in data.shape[:dims]])
    # if dims == 1:
    #     ret[:-1] = data[:, 0]
    #     ret[-1] = data[-1, 1]
    # elif dims == 2:
    #     ret[:-1, :-1] = data[:, :, 0, 0]
    #     ret[-1, :-1] = data[-1, :, 1, 0]
    #     ret[:-1, -1] = data[:, -1, 0, 1]
    #     ret[-1, -1] = data[-1, -1, 1, 1]
    for ijk in itertools.product(*[[0, 1]] * dims):
        first = tuple([[slice(None, -1), -1][i] for i in ijk])
        second = tuple([[slice(None), -1][i] for i in ijk] + [i for i in ijk])
        ret[first] = data[second]
    if check:
        for ijk in itertools.product(*[[0, 1]] * dims):
            first = tuple([[slice(None, -1), slice(1, None)][i] for i in ijk])
            second = tuple([slice(None)] * dims + [i for i in ijk])
            assert (ret[first] == data[second]).all()
    return xr.DataArray(data=ret, dims=out_dims, attrs=attrs)


class timeit:
    def __init__(self, info="%f"):
        self.info = info

    def __enter__(self):
        self.t0 = time.time()

    def __exit__(self, *args):
        print(self.info % (time.time() - self.t0))


T0 = time.time()
last = time.time()


class timeit2:
    def __init__(self, info="%f to %f - %f vs %f"):
        self.info = info

    def __enter__(self):
        self.t0 = time.time()

    def __exit__(self, *args):
        t0 = self.t0
        t1 = time.time()
        global T0, last
        print(self.info % (t0 - T0, t1 - T0, t1 - t0, t0 - last))
        last = t1


def _fft(data):
    from scipy.fftpack import fft

    fr = fft(data)
    import matplotlib.pyplot as plt

    plt.plot(np.abs(fr))
    # print(abs(fr.)
    plt.show()
    exit(1)
