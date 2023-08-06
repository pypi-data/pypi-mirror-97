# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""

from __future__ import absolute_import, print_function

from invenio_indexer.api import RecordIndexer
from invenio_records_rest.utils import allow_all, check_elasticsearch
from invenio_search import RecordsSearch

RECORDS_REST_ENDPOINTS = {}
"""REST API for invenio-records-marc21."""

RECORDS_UI_ENDPOINTS = {
    "marcid": {
        "pid_type": "marcid",
        "route": "/marc21/<pid_value>",
        "template": "invenio_records_marc21/record.html",
    },
}
"""Records UI for invenio-records-marc21."""

SEARCH_UI_JSTEMPLATE_RESULTS = "templates/invenio_records_marc21/results.html"
"""Result list template."""

PIDSTORE_RECID_FIELD = "marcid"

INVENIO_RECORDS_MARC21_ENDPOINTS_ENABLED = True
"""Enable/disable automatic endpoint registration."""
