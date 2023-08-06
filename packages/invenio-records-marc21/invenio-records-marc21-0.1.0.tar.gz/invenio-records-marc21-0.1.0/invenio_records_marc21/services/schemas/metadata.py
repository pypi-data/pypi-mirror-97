# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 record schemas."""

from dojson.contrib.marc21 import marc21
from dojson.contrib.marc21.utils import create_record
from marshmallow import INCLUDE, Schema, fields, post_load


class MetadataSchema(Schema):
    """Schema for the record metadata."""

    field_load_permissions = {
        # TODO: define "can_admin" action
    }

    field_dump_permissions = {
        # TODO: define "can_admin" action
    }

    xml = fields.Str(required=False)
    json = fields.Dict(required=False)

    class Meta:
        """Meta class to accept unknwon fields."""

        unknown = INCLUDE

    @post_load
    def convert_xml(self, data, **kwargs):
        """Convert marc21 xml into json."""
        if "xml" in data:
            data["json"] = marc21.do(create_record(data["xml"]))
            del data["xml"]
        return data
