import numpy as np
import os
import scipy.io as spio
from roiextractors.extraction_tools import check_keys, todict
from os.path import abspath, relpath
from roiextractors import SbxImagingExtractor


def giocomo_sbxread(self, k=0, N=None):
    """
    Input: self.file_name should be full path excluding .sbx, starting index, batch size
    By default Loads whole file at once, make sure you have enough ram available to do this
    """
    # Check if contains .sbx and if so just truncate

    # Load info
    info = self.giocomo_loadmat()
    # print info.keys()

    # Paramters
    # k = 0; #First frame
    max_idx = info["max_idx"]
    if N is None:
        N = max_idx  # Last frame
    else:
        N = min([N, max_idx - k])

    nSamples = (
        info["sz"][1]
        * info["recordsPerBuffer"]
        / info["fov_repeats"]
        * 2
        * info["nChan"]
    )
    # print(nSamples, N)

    # Open File
    fo = open(self.file_name)

    # print(int(k) * int(nSamples))
    fo.seek(int(k) * int(nSamples), 0)
    x = np.fromfile(fo, dtype="uint16", count=int(nSamples / 2 * N))
    x = np.int16((np.int32(65535) - x).astype(np.int32) / np.int32(2))
    x = x.reshape(
        (
            info["nChan"],
            info["sz"][1],
            int(info["recordsPerBuffer"] / info["fov_repeats"]),
            int(N),
        ),
        order="F",
    )

    return x


# SIMA: get info:
def scanbox_imaging_parameters(filepath):
    """Parse imaging parameters from Scanbox.
    Based off of the implementation of SIMA
    https://github.com/losonczylab/sima/blob/master/sima/imaging_parameters.py
    """
    assert filepath.endswith(".mat")
    data_path = os.path.splitext(filepath)[0] + ".sbx"
    data = spio.loadmat(filepath)["info"]
    info = check_keys(data)
    # Fix for old scanbox versions
    if "sz" not in info:
        info["sz"] = np.array([512, 796])

    if "scanmode" not in info:
        info["scanmode"] = 1  # unidirectional
    elif info["scanmode"] == 0:
        info["recordsPerBuffer"] *= 2  # bidirectional

    if info["channels"] == 1:
        # both PMT 0 and 1
        info["nchannels"] = 2
        # factor = 1
    elif info["channels"] == 2 or info["channels"] == 3:
        # PMT 0 or 1
        info["nchannels"] = 1
        # factor = 2

    # Bytes per frame (X * Y * C * bytes_per_pixel)
    info["nsamples"] = info["sz"][1] * info["recordsPerBuffer"] * info["nchannels"] * 2

    # Divide 'max_idx' by the number of plane to get the number of time steps
    if info.get("scanbox_version", -1) >= 2:
        # last_idx = total_bytes / (Y * X * 4 / factor) - 1
        # info['max_idx'] = os.path.getsize(data_path) // \
        #     info['recordsPerBuffer'] // info['sz'][1] * factor // 4 - 1
        info["max_idx"] = os.path.getsize(data_path) // info["nsamples"] - 1
    else:
        if info["nchannels"] == 1:
            factor = 2
        elif info["nchannels"] == 2:
            factor = 1
        info["max_idx"] = (
            os.path.getsize(data_path) // info["bytesPerBuffer"] * factor - 1
        )

    # Check optotune planes
    if ("volscan" in info and info["volscan"] > 0) or (
        "volscan" not in info and len(info.get("otwave", []))
    ):
        info["nplanes"] = len(info["otwave"])
    else:
        info["nplanes"] = 1

    # SIMA sbx read:

    nrows = info["recordsPerBuffer"]
    ncols = info["sz"][1]
    nchannels = info["nchannels"]
    nplanes = info["nplanes"]
    nframes = (info["max_idx"] + 1) // nplanes
    shape = (nchannels, ncols, nrows, nplanes, nframes)

    seq = _Sequence_memmap(
        path=data_path, shape=shape, dim_order="cxyzt", dtype="uint16", order="F"
    )

    # max_uint16_seq = sima.Sequence.create(
    #     'constant', value=np.iinfo('uint16').max, shape=seq.shape)

    return seq


class _Sequence_memmap:
    """
    Reading raw data as memory map. Used in sbx datasets.
    Based off of the implementation:
    https://github.com/losonczylab/sima/blob/0b16818d9ba47fe4aae6d4aad1a9735d16da00dc/sima/sequence.py
    """

    def __init__(self, path, shape, dim_order, dtype="float32", order="C"):
        self._path = abspath(path)
        self._shape = shape
        self._dtype = dtype
        self._order = order
        self._dataset = np.memmap(
            path, dtype=dtype, mode="r", shape=tuple(shape), order=order
        )
        if len(dim_order) != len(shape):
            raise ValueError(
                "dim_order must have same length as the number of "
                + "dimensions in the memmap dataset."
            )
        self._T_DIM = dim_order.find("t")
        self._Z_DIM = dim_order.find("z")
        self._Y_DIM = dim_order.find("y")
        self._X_DIM = dim_order.find("x")
        self._C_DIM = dim_order.find("c")
        self._dim_order = dim_order

    def __del__(self):
        del self._dataset

    def __len__(self):
        return self._shape[self._T_DIM]

    def _get_frame(self, t):
        """Get the frame at time t, but not clipped."""
        slices = tuple(slice(None) for _ in range(self._T_DIM)) + (t,)
        frame = self._dataset[slices]

        swapper = [None for _ in range(frame.ndim)]
        for i, v in [
            (self._Z_DIM, 0),
            (self._Y_DIM, 1),
            (self._X_DIM, 2),
            (self._C_DIM, 3),
        ]:
            if i >= 0:
                j = i if self._T_DIM > i else i - 1
                swapper[j] = v
            else:
                swapper.append(v)
                frame = np.expand_dims(frame, -1)
        assert not any(s is None for s in swapper)
        for i in range(frame.ndim):
            idx = swapper.index(i)
            if idx != i:
                swapper[i], swapper[idx] = swapper[idx], swapper[i]
                frame = frame.swapaxes(i, idx)
        assert swapper == [0, 1, 2, 3]
        assert frame.ndim == 4
        return frame.astype(float)

    def _todict(self, savedir=None):
        d = {
            "__class__": self.__class__,
            "dim_order": self._dim_order,
            "dtype": self._dtype,
            "shape": self._shape,
            "order": self._order,
        }
        if savedir is None:
            d.update({"path": abspath(self._path)})
        else:
            d.update(
                {
                    "_abspath": abspath(self._path),
                    "_relpath": relpath(self._path, savedir),
                }
            )
        return d


if __name__ == "__main__":
    filepath = r"C:\Users\Saksham\Documents\NWB\roiextractors\testdatasets\GiocomoData\10_02_2019\TwoTOwer_foraging"
    sbx = SbxImagingExtractor(filepath)
    info = sbx._info
    nrows = info["recordsPerBuffer"]
    ncols = info["sz"][1]
    nchannels = info["nChan"]
    nplanes = info["nplanes"]
    nframes = (info["max_idx"] + 1) // nplanes
    shape = (nchannels, ncols, nrows, nplanes, nframes)

    seq = _Sequence_memmap(
        path=sbx.sbx_file_path,
        shape=shape,
        dim_order="cxyzt",
        dtype="uint16",
        order="F",
    )
    # check sima vs roiext:
    fr1 = sbx.get_frames([0]).squeeze()
    fr2 = np.iinfo("uint16").max - seq._get_frame(t=0).squeeze()
    assert np.all(fr1 == fr2)
