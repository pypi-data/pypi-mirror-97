"""
License:
This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""

import os

curr_path = os.path.dirname(os.path.abspath(__file__))

TOKEN_FILE_PATH = os.path.expanduser("~/.activeloop/token")
STORE_CONFIG_PATH = os.path.expanduser("~/.activeloop/store")
CACHE_FILE_PATH = os.path.expanduser("~/.activeloop/tmp")
AWSCRED_PATH = os.path.expanduser("~/.aws/credentials")

HUB_REST_ENDPOINT = "https://app.activeloop.ai"
HUB_DEV_REST_ENDPOINT = "https://app.dev.activeloop.ai"
HUB_LOCAL_REST_ENDPOINT = "http://localhost:5000"

DEFAULT_TIMEOUT = 170

GET_TOKEN_REST_SUFFIX = "/api/user/token"
GET_CREDENTIALS_SUFFIX = "/api/credentials"
GET_REGISTER_SUFFIX = "/api/user/register"
GET_DATASET_SUFFIX = "/api/dataset/get"
GET_DATASET_PATH_SUFFIX = "/api/dataset/get/path"

CREATE_DATASET_SUFFIX = "/api/dataset/create"
UPDATE_STATE_SUFFIX = "/api/dataset/state"
DATASET_SUFFIX = "/api/dataset/"
DISTRIBUTED = True

# Reporting-related configuration
HUMBUG_TOKEN = "63423cd9-0951-4525-aeb3-257bbed6c6f5"
HUMBUG_KB_ID = "5e264dc7-72bf-44bb-9b0b-220b7381ad72"
REPORT_CONSENT_FILE_PATH = os.path.expanduser("~/.activeloop/reporting_config.json")
