"""
License:
This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import fsspec
import os
import json
from hub.store.metastore import MetaStorage


def test_meta_storage():
    os.makedirs("./data/test/test_meta_storage/internal_tensor", exist_ok=True)
    fs: fsspec.AbstractFileSystem = fsspec.filesystem("file")
    meta_map = fs.get_mapper("./data/test/test_meta_storage")
    meta_map["meta.json"] = bytes(json.dumps(dict()), "utf-8")
    fs_map = fs.get_mapper("./data/test/test_meta_storage/internal_tensor")
    MetaStorage("internal_tensor", fs_map, meta_map)
