"""
License:
This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import os
from hub.store.store import get_fs_and_path
import numpy as np
import sys
from hub.exceptions import ModuleNotInstalledException, DirectoryNotEmptyException


def slice_split(slice_):
    """Splits a slice into subpath and list of slices"""
    path = ""
    list_slice = []
    for sl in slice_:
        if isinstance(sl, str):
            path += sl if sl.startswith("/") else "/" + sl
        elif isinstance(sl, (int, slice)):
            list_slice.append(sl)
        else:
            raise TypeError(
                "type {} isn't supported in dataset slicing".format(type(sl))
            )
    return path, list_slice


def slice_extract_info(slice_, num):
    """Extracts number of samples and offset from slice"""
    if isinstance(slice_, int):
        slice_ = slice_ + num if num and slice_ < 0 else slice_
        if num and (slice_ >= num or slice_ < 0):
            raise IndexError(
                "index out of bounds for dimension with length {}".format(num)
            )
        return (1, slice_)

    if slice_.step is not None and slice_.step < 0:  # negative step not supported
        raise ValueError("Negative step not supported in dataset slicing")
    offset = 0
    if slice_.start is not None:
        slice_ = (
            slice(slice_.start + num, slice_.stop) if slice_.start < 0 else slice_
        )  # make indices positive if possible
        if num and (slice_.start < 0 or slice_.start >= num):
            raise IndexError(
                "index out of bounds for dimension with length {}".format(num)
            )
        offset = slice_.start
    if slice_.stop is not None:
        slice_ = (
            slice(slice_.start, slice_.stop + num) if slice_.stop < 0 else slice_
        )  # make indices positive if possible
        if num and (slice_.stop < 0 or slice_.stop > num):
            raise IndexError(
                "index out of bounds for dimension with length {}".format(num)
            )
    if slice_.start is not None and slice_.stop is not None:
        if (
            slice_.start < 0
            and slice_.stop < 0
            or slice_.start >= 0
            and slice_.stop >= 0
        ):
            # If same signs, bound checking can be done
            if abs(slice_.start) > abs(slice_.stop):
                raise IndexError("start index is greater than stop index")
            num = abs(slice_.stop) - abs(slice_.start)
        else:
            num = 0
        # num = 0 if slice_.stop < slice_.start else slice_.stop - slice_.start
    elif slice_.start is None and slice_.stop is not None:
        num = slice_.stop
    elif slice_.start is not None and slice_.stop is None:
        num = num - slice_.start if num else 0
    return num, offset


def create_numpy_dict(dataset, index, label_name=False):
    """Creates a list of dictionaries with the values from the tensorview objects in the dataset schema.

    Parameters
    ----------
    dataset: hub.api.dataset.Dataset object
        The dataset whose TensorView objects are being used.
    index: int
        The index of the dataset record that is being used.
    label_name: bool, optional
        If the TensorView object is of the ClassLabel type, setting this to True would retrieve the label names
        instead of the label encoded integers, otherwise this parameter is ignored.
    """
    numpy_dict = {}
    for path in dataset._tensors.keys():
        d = numpy_dict
        split = path.split("/")
        for subpath in split[1:-1]:
            if subpath not in d:
                d[subpath] = {}
            d = d[subpath]
        d[split[-1]] = dataset[path, index].numpy(label_name=label_name)
    return numpy_dict


def get_value(value):
    if isinstance(value, np.ndarray) and value.shape == ():
        value = value.item()
    elif isinstance(value, list):
        for i in range(len(value)):
            if isinstance(value[i], np.ndarray) and value[i].shape == ():
                value[i] = value[i].item()
    return value


def str_to_int(assign_value, tokenizer):
    if isinstance(assign_value, bytes):
        try:
            assign_value = assign_value.decode("utf-8")
        except Exception:
            raise ValueError(
                "Bytes couldn't be decoded to string. Other encodings of bytes are currently not supported"
            )
    if (
        isinstance(assign_value, np.ndarray) and assign_value.dtype.type is np.bytes_
    ) or (isinstance(assign_value, list) and isinstance(assign_value[0], bytes)):
        assign_value = [item.decode("utf-8") for item in assign_value]
    if tokenizer is not None:
        if "transformers" not in sys.modules:
            raise ModuleNotInstalledException("transformers")
        import transformers

        global transformers
        tokenizer = transformers.AutoTokenizer.from_pretrained("bert-base-cased")
        assign_value = (
            np.array(tokenizer(assign_value, add_special_tokens=False)["input_ids"])
            if isinstance(assign_value, str)
            else assign_value
        )
        if (
            isinstance(assign_value, list)
            and assign_value
            and isinstance(assign_value[0], str)
        ):
            assign_value = [
                np.array(tokenizer(item, add_special_tokens=False)["input_ids"])
                for item in assign_value
            ]
    else:
        assign_value = (
            np.array([ord(ch) for ch in assign_value])
            if isinstance(assign_value, str)
            else assign_value
        )
        if (
            isinstance(assign_value, list)
            and assign_value
            and isinstance(assign_value[0], str)
        ):
            assign_value = [np.array([ord(ch) for ch in item]) for item in assign_value]
    return assign_value


def _copy_helper(
    dst_url: str, token=None, fs=None, public=True, src_url=None, src_fs=None
):
    """Helper function for Dataset.copy"""
    src_url = src_fs.expand_path(src_url)[0]
    dst_url = dst_url[:-1] if dst_url.endswith("/") else dst_url
    dst_fs, dst_url = (
        (fs, dst_url) if fs else get_fs_and_path(dst_url, token=token, public=public)
    )
    if dst_fs.exists(dst_url) and dst_fs.ls(dst_url):
        raise DirectoryNotEmptyException(dst_url)
    for path in src_fs.ls(src_url, refresh=True):
        dst_full_path = dst_url + path[len(src_url) :]
        dst_folder_path, dst_file = os.path.split(dst_full_path)
        if src_fs.isfile(path):
            if not dst_fs.exists(dst_folder_path):
                dst_fs.mkdir(dst_folder_path)
            content = src_fs.cat_file(path)
            dst_fs.pipe_file(dst_full_path, content)
        else:
            _copy_helper(
                dst_full_path,
                token=token,
                fs=dst_fs,
                public=public,
                src_url=path,
                src_fs=src_fs,
            )
    return dst_url
