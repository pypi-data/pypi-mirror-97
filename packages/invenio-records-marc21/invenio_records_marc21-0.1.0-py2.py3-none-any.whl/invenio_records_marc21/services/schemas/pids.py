# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Marc21 record schemas."""

from marshmallow import INCLUDE, Schema, fields, validate


#
# PIDs
#
class PIDSchema(Schema):
    """PIDs schema."""

    identifier = fields.Str(required=True)
    provider = fields.Str(required=True)
    client = fields.Str()
