# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Graz University of Technology.
#
# Invenio-Records-Marc21 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Resources configuration."""

from flask_resources.serializers import JSONSerializer
from invenio_drafts_resources.resources import DraftResourceConfig, RecordResourceConfig
from invenio_records_resources.resources import RecordResponse
from invenio_records_resources.resources.records.schemas_links import (
    ItemLink,
    LinksSchema,
    SearchLinksSchema,
)

from ..serializers.ui import UIJSONSerializer

#
# Links
#
RecordLinks = LinksSchema.create(
    links={
        "self": ItemLink(template="/api/marc21/{pid_value}"),
        "self_html": ItemLink(template="/marc21/{pid_value}"),
    }
)


DraftLinks = LinksSchema.create(
    links={
        "self": ItemLink(template="/api/marc21/{pid_value}/draft"),
        "self_html": ItemLink(template="/marc21/uploads/{pid_value}"),
        "publish": ItemLink(
            template="/api/marc21/{pid_value}/draft/actions/publish",
            permission="publish",
        ),
    }
)


SearchLinks = SearchLinksSchema.create(template="/api/marc21{?params*}")

#
# Response handlers
#
record_serializers = {
    "application/json": RecordResponse(UIJSONSerializer()),
    "application/vnd.inveniomarc21.v1+json": RecordResponse(UIJSONSerializer()),
}


#
# marc21
#
class Marc21RecordResourceConfig(RecordResourceConfig):
    """Record resource configuration."""

    list_route = "/marc21"

    item_route = "/marc21/<pid_value>"

    links_config = {
        "marc21": RecordLinks,
        "search": SearchLinks,
    }

    draft_links_config = {
        "marc21": DraftLinks,
    }

    response_handlers = record_serializers


#
# Drafts and draft actions
#
class Marc21DraftResourceConfig(DraftResourceConfig):
    """Draft resource configuration."""

    list_route = "/marc21/<pid_value>/draft"

    item_route = "/marc21/<pid_value>"  # None

    links_config = {"marc21": DraftLinks}
