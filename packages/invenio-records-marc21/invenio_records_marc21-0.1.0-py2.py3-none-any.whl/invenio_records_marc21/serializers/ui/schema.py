# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Schema ui."""
from copy import deepcopy

from dojson.contrib.to_marc21 import to_marc21
from dojson.contrib.to_marc21.utils import dumps
from marshmallow import INCLUDE, Schema, missing, pre_dump
from marshmallow.fields import Dict, Method, Nested, Str

from invenio_records_marc21.vocabularies import Vocabularies


#
# Object schema
#
class AccessRightSchema(Schema):
    """Access right vocabulary."""


#
# Object schema
#
class MetadataSchema(Schema):
    """Access right vocabulary."""

    xml = Str(required=False)
    # json = Dict(required=False)

    @pre_dump
    def convert_xml(self, data, **kwargs):
        """Convert json into marc21 xml."""
        if "json" in data:
            data["xml"] = dumps(to_marc21.do(data["json"]))
        return data


class UIObjectSchema(Schema):
    """Schema for dumping extra information for the UI."""

    metadata = Nested(MetadataSchema, attribute="metadata")

    access_right = Nested(AccessRightSchema, attribute="access")


#
# List schema
class UIListSchema(Schema):
    """Schema for dumping extra information in the UI."""

    class Meta:
        """."""

        unknown = INCLUDE

    hits = Method("get_hits")
    aggregations = Method("get_aggs")

    def get_hits(self, obj_list):
        """Apply hits transformation."""
        for obj in obj_list["hits"]["hits"]:
            obj[self.context["object_key"]] = self.context["object_schema_cls"]().dump(
                obj
            )
        return obj_list["hits"]

    def get_aggs(self, obj_list):
        """Apply aggregations transformation."""
        aggs = obj_list.get("aggregations")
        if not aggs:
            return missing

        for name, agg in aggs.items():
            vocab = Vocabularies.get_vocabulary(name)
            if not vocab:
                continue

            buckets = agg.get("buckets")
            if buckets:
                apply_labels(vocab, buckets)

        return aggs


def apply_labels(vocab, buckets):
    """Inject labels in the aggregation buckets.

    :params agg: Current aggregation object.
    :params vocab: The vocabulary
    """
    for bucket in buckets:
        bucket["label"] = vocab.get_title_by_dict(bucket["key"])

        # Recursively apply to subbuckets
        for data in bucket.values():
            if isinstance(data, dict) and "buckets" in data:
                apply_labels(vocab, data["buckets"])
