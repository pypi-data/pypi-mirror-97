# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 Record Resource."""


from invenio_drafts_resources.resources import DraftResource, RecordResource

from . import config


#
# Records
#
class Marc21RecordResource(RecordResource):
    """Bibliographic record resource."""

    config_name = "MARC21_RECORDS_RECORD_CONFIG"
    default_config = config.Marc21RecordResourceConfig


#
# Drafts
#
class Marc21DraftResource(DraftResource):
    """Bibliographic record draft resource."""

    config_name = "MARC21_RECORDS_DRAFT_CONFIG"
    default_config = config.Marc21DraftResourceConfig
